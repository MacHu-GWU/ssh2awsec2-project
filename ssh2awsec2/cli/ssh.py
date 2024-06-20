# -*- coding: utf-8 -*-

import typing as T
import subprocess
from pathlib import Path

from simple_aws_ec2.api import (
    CannotDetectOSTypeError,
    Ec2Instance,
    Image,
)

from ..cache import cache
from ..logger import logger
from ..config import Config
from ..boto_ses import get_boto_ses
from ..recent import ListChoices
from ..pem_file import PemFileStore
from ..better_boto import get_account_id, get_account_alias


def _filter_ec2(
    ec2_client,
    name: T.Optional[str] = None,
    id: T.Optional[str] = None,
    kv: T.Optional[str] = None,
    exact: bool = False,
    strip: bool = True,
) -> T.Tuple[T.List[Ec2Instance], T.List[dict]]:
    """
    Filter EC2 instances by name tag, instance id, or arbitrary key-value tag.

    :param ec2_client:
    :param name: filter by name tag, if there's a space in the name, and
        exact = False, then the name will be split by facets. valid examples:
        "foo", "foo-bar", "foo bar"
    :param id: filter by instance id, if there's a space in the id, and
        exact = False, then the id will be split by facets. valid examples:
        "i-1234567890abcdef0", "1a2b", "1a2b 8x9y0z"
    :param kv: arbitrary key-value tag, valid example: "foo=bar", "foo=bar&baz=qux"
    :param exact: if True, then exact match; otherwise, sub string match
    """
    # filter the EC2
    filters = [
        dict(
            Name="instance-state-name",
            Values=[
                "running",
            ],
        )
    ]

    if name is not None:
        name = str(name)
        if strip:
            name = name.strip()
        if exact:
            filters.append(dict(Name="tag:Name", Values=[name]))
        else:
            if " " in name:  # split to facets
                values = [word.strip() for word in name.split("") if word.strip()]
            else:
                values = [name]
            for v in values:
                filters.append(dict(Name="tag:Name", Values=[f"*{v}*"]))

    if id is not None:
        id = str(id)
        if strip:
            name = name.strip()
        # ec2 instance id is 17 chars long, e.g. "i-1234567890abcdef0"
        # if the input is not full instance id or the alphanumeric part of it
        # exact match is not possible
        if len(id) not in [15, 17]:
            exact = False  # force to use substring match
        if exact:
            filters.append(dict(Name=f"instance-id", Values=[name]))
        else:
            if " " in id:  # split to facets
                values = [word.strip() for word in id.split("") if word.strip()]
            else:
                values = [id]
            for v in values:
                filters.append(dict(Name="instance-id", Values=[f"*{v}*"]))

    if kv is not None:
        pairs = [pair.split("=", 1) for pair in kv.split("&")]
        for k, v in pairs:
            if exact:
                filters.append(dict(Name=f"tag:{k}", Values=[v]))
            else:
                filters.append(dict(Name=f"tag:{k}", Values=[f"*{v}*"]))

    ec2_inst_list = Ec2Instance.query(ec2_client=ec2_client, filters=filters).all()
    return ec2_inst_list, filters


def get_ec2_inst_choice(ec2_inst: Ec2Instance) -> str:
    """
    Create the choice string for an EC2 instance.
    """
    inst_id = ec2_inst.id
    name = ec2_inst.tags.get("Name", "no name")
    pub_ip = ec2_inst.public_ip
    return f"id = {inst_id}, name = {name!r}, public ip = {pub_ip}"


def get_ssh_cmd(
    path_pem_file: Path,
    username: str,
    public_ip: str,
) -> T.List[str]:
    """
    Construct the ssh to ec2 command.
    """
    args = ["ssh", "-i", f"{path_pem_file}", f"{username}@{public_ip}"]
    return args


@logger.start_and_end(
    msg="SSH to EC2 instance",
)
def ssh(
    name: T.Optional[str] = None,
    id: T.Optional[str] = None,
    kv: T.Optional[str] = None,
    exact: bool = False,
    strip: bool = True,
):
    """
    SSH to an EC2 instance.

    :param name:
    :param id:
    :param kv:
    :param exact:
    :param strip:
    :return:
    """
    # prepare AWS client
    config = Config.read()
    boto_ses = get_boto_ses(config)
    aws_account_id = get_account_id(boto_ses.client("sts"))
    aws_region = boto_ses.region_name
    ec2_client = boto_ses.client("ec2")

    # filter EC2 instances
    ec2_inst_list, filters = _filter_ec2(
        ec2_client=ec2_client,
        name=name,
        id=id,
        kv=kv,
        exact=exact,
        strip=strip,
    )

    if len(ec2_inst_list) == 0:
        logger.info(f"🔴 No EC2 instance match filter: {filters}")
        return

    # ask user to select an EC2 instance
    ec2_inst_mapper = {ec2_inst.id: ec2_inst for ec2_inst in ec2_inst_list}
    choices = dict()
    for ec2_inst in ec2_inst_list:
        choices[ec2_inst.id] = get_ec2_inst_choice(ec2_inst)

    list_choices = ListChoices(
        key=f"SSH-{aws_account_id}-{aws_region}",
        expire=config.recent_cache_expire,
    )
    logger.info("Which EC2 you want to SSH to?")
    logger.info("⬆ ⬇ Move your cursor up and down and press Enter to select.")
    inst_id, choice = list_choices.ask(
        message="Current selection",
        choices=choices,
        merge_selected=False,
    )
    logger.info(f"✅ selected: {choice}")
    ec2_inst: Ec2Instance = ec2_inst_mapper[inst_id]  # get selected ec2 instance

    # try to get the successful ssh command from cache
    cache_key = ec2_inst.id
    if cache_key in cache:
        ssh_cmd = cache[cache_key]
        # check if ip address changed
        if ec2_inst.public_ip in ssh_cmd:
            logger.info(f"try to use cached ssh command: {ssh_cmd}")
            try:
                subprocess.run(ssh_cmd, shell=True)
                # if cached ssh command works, update cache
                cache.set(cache_key, ssh_cmd, expire=config.ssh_cmd_cache_expire)
                return
            except Exception as e:
                # if cached ssh command doesn't work, delete cache and continue
                cache.delete(cache_key)
        # if ip address changed, delete cache and continue
        else:
            cache.delete(cache_key)

    # locate pem file
    logger.info("try to locate pem file ...")
    aws_account_alias = get_account_alias(boto_ses.client("iam"))
    pem_file_store = PemFileStore()
    path_pem_file = pem_file_store.locate_pem_file(
        region=aws_region,
        key_name=ec2_inst.key_name,
        account_id=aws_account_id,
        account_alias=aws_account_alias,
    )
    logger.info(f"✅ found pem file at: {path_pem_file}")

    # find OS username
    def prompt_to_select_users() -> T.List[str]:
        list_choices = ListChoices(
            key=f"OS-USERNAME-{ec2_inst.id}",
            expire=config.recent_cache_expire,
        )
        _choices = [
            "ec2-user",
            "ubuntu",
            "fedora",
            "centos",
            "admin",
            "bitnami",
            "root",
        ]
        choices = {v: v for v in _choices}
        logger.info(
            "Choose OS username of your EC2, if you don't know, see this document: "
            "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connection-prereqs.html#connection-prereqs-get-info-about-instance"
        )
        logger.info("⬆ ⬇ Move your cursor up and down and press Enter to select.")
        user_id, choice = list_choices.ask(
            message="Current selection",
            choices=choices,
            merge_selected=False,
        )
        users = [choice]
        return users

    image = Image.from_id(ec2_client, image_id=ec2_inst.image_id)
    if image is None:
        users = prompt_to_select_users()
    else:
        logger.info(
            f"Try to find OS username based on the "
            f"AMI id = {image.id}, name = {image.name}"
        )
        try:
            os_type = image.os_type
            users = os_type.users
            logger.info(
                f"✅ found os type {os_type.value} and potential usernames: {users}"
            )
        except CannotDetectOSTypeError:
            logger.info(f"cannot automatically detect OS username")
            users = prompt_to_select_users()

    # run ssh command
    for user in users:
        ssh_args = get_ssh_cmd(
            path_pem_file=path_pem_file,
            username=user,
            public_ip=ec2_inst.public_ip,
        )
        ssh_cmd = " ".join(ssh_args)
        logger.info(f"Run ssh command: {ssh_cmd}")
        logger.info("Precess Ctrl + D to exit SSH session")
        cache.set(cache_key, ssh_cmd, expire=config.ssh_cmd_cache_expire)
        try:
            subprocess.run(ssh_cmd, shell=True)
        except Exception as e:
            cache.delete(cache_key)
