# -*- coding: utf-8 -*-

import fire

from .config import SubCommandConfig, info
from .ssh import ssh


class Command:
    def __init__(self):
        self.config = SubCommandConfig()
        self.info = info
        self.ssh = ssh


def run():
    fire.Fire(Command)
