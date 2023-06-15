# -*- coding: utf-8 -*-

import fire

from .config import SubCommandConfig
from .ssh import ssh
from .commands import info, clear_cache


class Command:
    def __init__(self):
        self.config = SubCommandConfig()
        self.info = info
        self.clear_cache = clear_cache
        self.ssh = ssh


def run():
    fire.Fire(Command)
