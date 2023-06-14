# -*- coding: utf-8 -*-

"""
- Default user name for AMI: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connection-prereqs.html#connection-prereqs-get-info-about-instance
"""

import typing as T
import enum
from pathlib import Path


class AmiTypeEnum(str, enum.Enum):
    AmazonLinux = "ec2-user"
    CentOS = "ec2-user"
    Debian = "admin"
    Fedora = "ec2-user"
    RHEL = "ec2-user"
    SUSE = "ec2-user"
    Ubuntu = "ubuntu"
    Oracle = "ec2-user"
    Bitnami = "bitnami"


def get_ssh_cmd(
    path_pem_file: Path,
    username: str,
    public_ip: str,
) -> str:
    return "ssh -i {ec2_pem} {username}@{public_ip}".format(
        ec2_pem=path_pem_file,
        username=username,
        public_ip=public_ip,
    )
