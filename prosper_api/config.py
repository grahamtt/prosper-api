from os.path import expanduser

import dpath
from schema import Schema, Regex, Optional
from toml import load, loads

CLIENT_ID = "credentials.client-id"
CLIENT_SECRET = "credentials.client-secret"
USERNAME = "credentials.username"
PASSWORD = "credentials.password"
TOKEN_CACHE = "auth.token-cache"


class Config:
    DEFAULT_CONFIG_PATH = expanduser("~/.prosper-client/config.toml")
    DEFAULT_TOKEN_CACHE_PATH = expanduser("~/.prosper-client/token-cache")

    SCHEMA = Schema(
        {
            "credentials": {
                "client-id": Regex(r"^[a-f0-9]{32}$"),
                "client-secret": Regex(r"^[a-f0-9]{32}$"),
                "username": str,
                "password": str,
            },
            Optional("auth", default={"token-cache": DEFAULT_TOKEN_CACHE_PATH}): {
                Optional("token-cache", default=DEFAULT_TOKEN_CACHE_PATH): str
            },
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
            self.config_dict = self.SCHEMA.validate(self.config_dict)

    def get(self, key) -> str:
        return dpath.get(self.config_dict, key, separator=".")
