from os.path import expanduser

import dpath
from schema import Optional, Regex, Schema
from toml import load, loads

_CLIENT_ID = "credentials.client-id"
_CLIENT_SECRET = "credentials.client-secret"
_USERNAME = "credentials.username"
_PASSWORD = "credentials.password"
_TOKEN_CACHE = "auth.token-cache"


class Config:
    """Holds and allows access to prosper-api config values."""

    _DEFAULT_CONFIG_PATH = expanduser("~/.prosper-api/config.toml")  # pragma: no mutate
    _DEFAULT_TOKEN_CACHE_PATH = expanduser("~/.prosper-api/token-cache")

    _SCHEMA = Schema(
        {
            "credentials": {
                "client-id": Regex(r"^[a-f0-9]{32}$"),
                Optional("client-secret"): Regex(r"^[a-f0-9]{32}$"),
                "username": str,
                Optional("password"): str,
            },
            Optional("auth", default={"token-cache": _DEFAULT_TOKEN_CACHE_PATH}): {
                Optional("token-cache", default=_DEFAULT_TOKEN_CACHE_PATH): str
            },
            Optional(str): {str: object},
        }
    )

    def __init__(
        self,
        config_path: str = _DEFAULT_CONFIG_PATH,
        config_string: str = None,
        validate: bool = True,
    ):
        """Builds a config class instance.

        Args:
            config_path (str): Path to the config file (defaults to
                `~/.prosper-api/config.toml`).
            config_string (str): A TOML string representing the config; this option is
                mainly used for unit tests.
            validate (bool): Specify whether the config file will be validated against
                the internal schema.
        """
        if config_string:
            self._config_dict = loads(config_string)

        elif config_path:
            with open(config_path) as config_file:
                self._config_dict = load(config_file)

        if validate:
            self._config_dict = self._SCHEMA.validate(self._config_dict)

    def get(self, key: str) -> str:
        """Get the specified config value as a string.

        Args:
            key (str): The '.' separated path to the config value.

        Returns:
            str: The stored config value for the given key, or None if it doesn't
                exist.
        """
        return dpath.get(self._config_dict, key, separator=".", default=None)
