# -*- coding: utf-8 -*-


from ..config import path_config
from ..paths import dir_pem_files
from ..cache import cache


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


def clear_cache():
    """
    Clear cache.
    """
    cache.clear()
    print("cache cleared")
