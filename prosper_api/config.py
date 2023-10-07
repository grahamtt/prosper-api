from os.path import expanduser

import dpath
from schema import Schema, Regex
from toml import load, loads


class Config:
    DEFAULT_CONFIG_PATH = expanduser("~/.prosperlib/config.toml")
    SCHEMA = Schema(
        {
            "credentials": {
                "client-id": Regex(r"^[a-f0-9]{32}$"),
                "client-secret": Regex(r"^[a-f0-9]{32}$"),
                "username": str,
                "password": str,
            }
        }
    )

    def __init__(
        self, config_path=DEFAULT_CONFIG_PATH, config_string=None, validate=True
    ):
        if config_string:
            self.config_dict = loads(config_string)

        elif config_path:
            with open(config_path) as config_file:
                self.config_dict = load(config_file)

        if validate:
            self.SCHEMA.validate(self.config_dict)

    def get(self, key):
        return dpath.get(self.config_dict, key, separator=".")
