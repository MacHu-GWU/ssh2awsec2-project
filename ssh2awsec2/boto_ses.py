# -*- coding: utf-8 -*-

import boto3

from .config import Config


def get_boto_ses(config: Config):
    boto_ses = boto3.session.Session(
        profile_name=config.aws_profile,
        region_name=config.aws_region,
    )
    return boto_ses
