# -*- coding: utf-8 -*-

from .vendor.nested_logger import NestedLogger

logger = NestedLogger(name="ssh2awsec2", log_format="%(message)s")
