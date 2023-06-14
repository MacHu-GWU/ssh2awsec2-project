# -*- coding: utf-8 -*-

import typing as T
import subprocess

import fire

from simple_aws_ec2.api import (
    CannotDetectOSTypeError,
    Ec2Instance,
    Image,
)

from . import api
from .cache import cache
from .paths import dir_home
from .logger import logger


class Config:
    def show(self):
        config = api.Config.read()
        print(config.to_json())

    def set_profile(self, profile: str):
        config = api.Config.read()
        config.aws_profile = profile
        config.write()

    def set_region(self, region: str):
        config = api.Config.read()
        config.aws_region = region
        config.write()


class Command:
    def __init__(self):
        self.config = Config()

    @logger.start_and_end(
        msg="SSH to EC2 instance",
    )
    def ssh(
        self,
        name: T.Optional[str] = None,
        id: T.Optional[str] = None,
        kv: T.Optional[str] = None,
        exact: bool = False,
    ):
        # prepare AWS client
        config = api.Config.read()
        boto_ses = api.get_boto_ses(config)
        aws_account_id = api.get_account_id(boto_ses.client("sts"))
        aws_region = boto_ses.region_name
        ec2_client = boto_ses.client("ec2")

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
            if exact:
                filters.append(dict(Name=f"tag:Name", Values=[name]))
            else:
                if " " in name:
                    values = [word.strip() for word in name.split("") if word.strip()]
                else:
                    values = [name]
                for v in values:
                    filters.append(dict(Name=f"tag:Name", Values=[f"*{v}*"]))

        if id is not None:
            id = str(id)
            if len(id) <= 15:
                exact = False
            if exact:
                filters.append(dict(Name=f"instance-id", Values=[name]))
            else:
                if " " in id:
                    values = [word.strip() for word in id.split("") if word.strip()]
                else:
                    values = [id]
                for v in values:
                    filters.append(dict(Name=f"instance-id", Values=[f"*{v}*"]))

        if kv is not None:
            k, v = kv.split("=", 1)
            if exact:
                filters.append(dict(Name=f"tag:{k}", Values=[v]))
            else:
                filters.append(dict(Name=f"tag:{k}", Values=[f"*{v}*"]))

        ec2_inst_list = Ec2Instance.query(
            ec2_client=ec2_client,
            filters=filters,
        ).all()

        if len(ec2_inst_list) == 0:
            logger.info(f"🔴 No EC2 instance match: {filters}")
            return

        ec2_inst_mapper = {ec2_inst.id: ec2_inst for ec2_inst in ec2_inst_list}
        choices = dict()
        for ec2_inst in ec2_inst_list:
            inst_id = ec2_inst.id
            name = ec2_inst.tags.get("Name", "no name")
            pub_ip = ec2_inst.public_ip
            choice = f"id = {inst_id}, name = {name!r}, public ip = {pub_ip}"
            choices[inst_id] = choice

        # ask user to select an EC2 instance
        list_choices = api.ListChoices(key=f"SSH-{aws_account_id}-{aws_region}")
        logger.info("What EC2 you want to SSh to?")
        logger.info("⬆ ⬇ Move your cursor up and down and press Enter to select.")
        inst_id, choice = list_choices.ask(
            message="Current selection",
            choices=choices,
            merge_selected=False,
        )
        logger.info(f"✅ selected: {choice}")
        ec2_inst: Ec2Instance = ec2_inst_mapper[inst_id]

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
                    cache.set(cache_key)
                    return
                except Exception as e:
                    # if cached ssh command doesn't work, delete cache and continue
                    cache.delete(cache_key)
            # ip address changed, delete cache and continue
            else:
                cache.delete(cache_key)

        # locate pem file
        logger.info("try to locate pem file ...")

        aws_account_alias = api.get_account_alias(boto_ses.client("iam"))
        pem_file_store = api.PemFileStore()
        path_pem_file = pem_file_store.locate_pem_file(
            region=aws_region,
            key_name=ec2_inst.key_name,
            account_id=aws_account_id,
            account_alias=aws_account_alias,
        )
        logger.info(f"✅ found pem file at: {path_pem_file}")

        # find OS username
        image = Image.from_id(ec2_client, image_id=ec2_inst.image_id)
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
            list_choices = api.ListChoices(key=f"OS-USERNAME-{ec2_inst.id}")
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

            logger.info(f"cannot automatically detect OS username")
            logger.info(
                "Choose OS username of your EC2, if you don't know, see this document: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connection-prereqs.html#connection-prereqs-get-info-about-instance"
            )
            logger.info("⬆ ⬇ Move your cursor up and down and press Enter to select.")
            user_id, choice = list_choices.ask(
                message="Current selection",
                choices=choices,
                merge_selected=False,
            )
            users = [choice]

        # run ssh command
        for user in users:
            ssh_args = api.get_ssh_cmd(
                path_pem_file=path_pem_file,
                username=user,
                public_ip=ec2_inst.public_ip,
            )
            ssh_cmd = " ".join(ssh_args)
            logger.info(f"Run ssh command: {ssh_cmd}")
            logger.info("Precess Ctrl + D to exit SSH session")
            cache.set(cache_key, ssh_cmd)
            try:
                res = subprocess.run(ssh_cmd, shell=True)
            except Exception as e:
                cache.delete(cache_key)


def main():
    fire.Fire(Command)
