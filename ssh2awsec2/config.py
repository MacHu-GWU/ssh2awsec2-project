# -*- coding: utf-8 -*-

import typing as T
import json
import dataclasses


from .paths import path_config


RECENT_CACHE_EXPIRE = 24 * 60 * 60  # 1 day
SSH_CMD_CACHE_EXPIRE = 24 * 60 * 60  # 1 day


@dataclasses.dataclass
class Config:
    recent_cache_expire: int = dataclasses.field(default=RECENT_CACHE_EXPIRE)
    ssh_cmd_cache_expire: int = dataclasses.field(default=SSH_CMD_CACHE_EXPIRE)
    aws_profile: T.Optional[str] = dataclasses.field(default=None)
    aws_region: T.Optional[str] = dataclasses.field(default=None)

    @classmethod
    def read(cls) -> "Config":
        if path_config.exists():
            data = {
                k: v
                for k, v in json.loads(path_config.read_text()).items()
                if v is not None
            }
            return cls(**data)
        else:
            return cls()

    def write(self):
        path_config.write_text(json.dumps(dataclasses.asdict(self), indent=4))

    def to_dict(self) -> dict:
        return dataclasses.asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=4)
