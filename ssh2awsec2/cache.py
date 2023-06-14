# -*- coding: utf-8 -*-

import diskcache

from .paths import dir_cache

cache = diskcache.Cache(f"{dir_cache}")
