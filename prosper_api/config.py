import argparse
from copy import deepcopy
from decimal import Decimal
from importlib.util import find_spec
from numbers import Number
from os import getcwd
from os.path import join
from typing import List, Union

import dpath
from platformdirs import user_config_dir
from prosper_shared.omni_config import (
    ArgParseSource,
    ConfigurationSource,
    EnvironmentVariableSource,
    JsonConfigurationSource,
    SchemaType,
    TomlConfigurationSource,
    YamlConfigurationSource,
    arg_parse_from_schema,
    extract_defaults_from_schema,
    merge_config,
    realize_config_schemata,
    realize_input_schemata,
)
from schema import Schema


class Config:
    """Holds and allows access to prosper-api config values."""

    def __init__(
        self,
        config_dict: dict = None,
        schema: SchemaType = None,
    ):
        """Builds a config class instance.

        Args:
            config_dict (dict): A Python dict representing the config.
            schema (SchemaType): Validate the config against this schema. Unexpected or missing values will cause a validation error.
        """
        self._config_dict = deepcopy(config_dict)

        if schema:
            self._config_dict = Schema(schema, ignore_extra_keys=False).validate(
                self._config_dict
            )

    def get(self, key: str) -> object:
        """Get the specified config value.

        Args:
            key (str): The '.' separated path to the config value.

        Returns:
            object: The stored config value for the given key, or None if it doesn't
                exist.
        """
        return dpath.get(self._config_dict, key, separator=".", default=None)

    def get_as_str(self, key, default: Union[str, None] = None):
        """Get the specified value interpreted as a string."""
        value = self.get(key)
        if value is None:
            return default

        return str(value)

    def get_as_decimal(self, key, default: Union[Decimal, None] = None):
        """Get the specified value interpreted as a decimal."""
        value = self.get(key)
        if value is None:
            return default

        return Decimal(value)

    def get_as_bool(self, key: str, default: bool = False):
        """Get the specified value interpreted as a boolean.

        Specifically, the literal value `true`, string values 'true', 't', 'yes', and 'y' (case-insensitive), and any
        numeric value != 0 will return True, otherwise, False is returned.
        """
        value = self.get(key)
        if value is None:
            return default

        truthy_strings = {"true", "t", "yes", "y"}
        if isinstance(value, str) and value.lower() in truthy_strings:
            return True

        if isinstance(value, Number) and value != 0:
            return True

        return False

    @classmethod
    def autoconfig(
        cls,
        app_names: Union[str, List[str]],
        arg_parse: argparse.ArgumentParser = None,
        validate: bool = False,
    ) -> "Config":
        """Sets up a Config with default configuration sources.

        Gets config files from the following locations:
        1. The default config directory for the given app name.
        2. The working directory, including searching `pyproject.toml` for a `tools.{app_name}` section, if present.
        3. Environment variables prefixed by 'APP_NAME_' for each of the given app names.
        4. The given argparse instance.

        Config values found lower in the chain will override previous values for the same key.

        Args:
            app_names (Union[str, List[str]]): An ordered list of app names for which look for configs.
            arg_parse (argparse.ArgumentParser): A pre-configured argparse instance.
            validate (bool): Whether to validate the config prior to returning it.

        Returns:
            Config: A configured Config instance.
        """
        if isinstance(app_names, str):
            app_names = [app_names]

        config_schemata = realize_config_schemata()
        input_schemata = realize_input_schemata()
        schema = merge_config([*config_schemata, *input_schemata])

        conf_sources: List[ConfigurationSource] = [extract_defaults_from_schema(schema)]

        conf_sources += [
            JsonConfigurationSource(join(user_config_dir(app_name), "config.json"))
            for app_name in app_names
        ]
        if _has_yaml():
            conf_sources += [
                YamlConfigurationSource(join(user_config_dir(app_name), "config.yml"))
                for app_name in app_names
            ]
            conf_sources += [
                YamlConfigurationSource(join(user_config_dir(app_name), "config.yaml"))
                for app_name in app_names
            ]

        if _has_toml():
            conf_sources += [
                TomlConfigurationSource(join(user_config_dir(app_name), "config.toml"))
                for app_name in app_names
            ]

        conf_sources += [
            JsonConfigurationSource(join(getcwd(), f".{app_name}.json"))
            for app_name in app_names
        ]

        if _has_yaml():
            conf_sources += [
                YamlConfigurationSource(join(getcwd(), f".{app_name}.yml"))
                for app_name in app_names
            ]
            conf_sources += [
                YamlConfigurationSource(join(getcwd(), f".{app_name}.yaml"))
                for app_name in app_names
            ]

        if _has_toml():
            conf_sources += [
                TomlConfigurationSource(join(getcwd(), f".{app_name}.toml"))
                for app_name in app_names
            ]
            conf_sources += [
                TomlConfigurationSource(
                    join(getcwd(), ".pyproject.toml"), f"tools.{app_name}"
                )
                for app_name in app_names
            ]

        conf_sources += [
            EnvironmentVariableSource(
                _kebab_case_to_upper_train_case(app_name), separator="__"
            )
            for app_name in app_names
        ]
        conf_sources.append(
            ArgParseSource(arg_parse if arg_parse else arg_parse_from_schema(schema))
        )

        config_dict = merge_config(
            [(c.read() if not isinstance(c, dict) else c) for c in conf_sources]
        )

        config_dict = (
            Schema(schema, ignore_extra_keys=True).validate(config_dict)
            if validate
            else config_dict
        )

        return Config(config_dict=config_dict)


def _kebab_case_to_upper_train_case(name: str) -> str:
    return name.replace("-", "_").upper()


def _has_yaml():
    return find_spec("yaml")


def _has_toml():
    return find_spec("toml")
