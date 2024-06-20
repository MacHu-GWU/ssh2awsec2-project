# -*- coding: utf-8 -*-

from .vendor.vislog import VisLog

logger = VisLog(name="ssh2awsec2", log_format="%(message)s")
