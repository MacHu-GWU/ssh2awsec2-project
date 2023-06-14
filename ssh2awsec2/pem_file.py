# -*- coding: utf-8 -*-

"""
AWS recommend to use Pem file to SSH to EC2 instance.

This module follows some convention to locate the pem file.

Reference:

- Amazon EC2 key pairs and Linux instances: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html
"""

import dataclasses
from pathlib import Path


@dataclasses.dataclass
class PemFileStore:
    dir_root: Path

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
        return self.dir_root.joinpath(account_id_or_alias, region, filename)
