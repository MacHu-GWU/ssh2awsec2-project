# -*- coding: utf-8 -*-

import typing as T
import json
import dataclasses


from .paths import path_config


@dataclasses.dataclass
class Config:
    aws_profile: T.Optional[str] = dataclasses.field(default=None)

    @classmethod
    def read(cls) -> "Config":
        if path_config.exists():
            return cls(**json.loads(path_config.read_text()))
        else:
            return cls()

    def write(self):
        path_config.write_text(json.dumps(dataclasses.asdict(self), indent=4))

    def to_dict(self) -> dict:
        return dataclasses.asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=4)
