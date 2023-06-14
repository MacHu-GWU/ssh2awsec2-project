# -*- coding: utf-8 -*-

from ..config import Config, path_config
from ..paths import dir_pem_files


def info():
    """
    Show config related information.
    """
    path = dir_pem_files.joinpath(
        "${AWS_ACCOUNT_ID_OR_ALIAS}",
        "${AWS_REGION}",
        "${KEY_NAME}.pem",
    )

    print(f"edit config file at: {path_config}")
    print(f"store your ec2 key pem files at: {path}")


class SubCommandConfig:
    """
    ssh2awsec2 CLI configuration.
    """

    def show(self):
        """
        Show current config.
        """
        config = Config.read()
        print(config.to_json())

    def set_profile(self, profile: str):
        """
        Set AWS profile.
        """
        config = Config.read()
        config.aws_profile = profile
        config.write()

    def set_region(self, region: str):
        """
        Set AWS region.
        """
        config = Config.read()
        config.aws_region = region
        config.write()
