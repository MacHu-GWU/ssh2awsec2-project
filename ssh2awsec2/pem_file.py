# -*- coding: utf-8 -*-

"""
AWS recommend to use Pem file to SSH to EC2 instance.

This module follows some convention to locate the pem file.

Reference:

- Amazon EC2 key pairs and Linux instances: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html
"""

import typing as T
import dataclasses
from pathlib import Path
from .paths import dir_pem_files


@dataclasses.dataclass
class PemFileStore:
    dir_pem_files: Path = dataclasses.field(default=dir_pem_files)

    def get_pem_file_path(
        self,
        account_id_or_alias: str,
        region: str,
        key_name: str,
    ) -> Path:
        """
        The convention is to put the pem file at
        ``${dir_root}/${account_id_or_alias}/${region}/${key_name}.pem``.
        """
        region = region.replace("_", "-")
        if key_name.endswith(".pem"):
            filename = key_name
        else:
            filename = f"{key_name}.pem"
        return self.dir_pem_files.joinpath(account_id_or_alias, region, filename)

    def locate_pem_file(
        self,
        region: str,
        key_name: str,
        account_id: T.Optional[str],
        account_alias: T.Optional[str],
    ):
        """
        Try to locate the EC2 pem file at
        ${HOME}/${account_id_or_alias}/${region}/${key_name}.pem

        :param region:
        :param key_name:
        :param account_id:
        :param account_alias:
        """
        if account_id is None and account_alias is None:  # pragma: no cover
            raise ValueError("account_id and account_alias cannot be both None")

        if account_id is not None:
            path_pem_file = self.get_pem_file_path(account_id, region, key_name)
            if path_pem_file.exists():
                return path_pem_file

        if account_alias is not None:
            path_pem_file = self.get_pem_file_path(account_alias, region, key_name)
            if path_pem_file.exists():  # pragma: no cover
                return path_pem_file

        raise FileNotFoundError(
            f"Cannot find pem file at {path_pem_file}, "
            "please put your ec2 pem file at "
            "${HOME}/${account_id_or_alias}/${region}/${key_name}.pem"
        )
