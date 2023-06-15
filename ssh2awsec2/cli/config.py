# -*- coding: utf-8 -*-

from ..config import Config
from ..logger import logger


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
        if profile.lower() in ["default", "none", "null"]:
            config.aws_profile = None
            logger.info("set AWS profile to: default")
        else:
            config.aws_profile = profile
            logger.info(f"set AWS profile to: {profile}")

        config.write()

    @logger.start_and_end(
        msg="set AWS region for ssh2awsec2 CLI",
    )
    def set_region(self, region: str):
        """
        Set AWS region.
        """
        config = Config.read()
        config.aws_region = region
        logger.info(f"set AWS region to: {region}")
        config.write()

    @logger.start_and_end(
        msg="set cache expire",
    )
    def set_cache_expire(self, expire: int):
        """
        Set Cache expire time.
        """
        config = Config.read()
        config.recent_cache_expire = expire
        config.ssh_cmd_cache_expire = expire
        logger.info(f"set cache expire: {expire} seconds")
        config.write()
