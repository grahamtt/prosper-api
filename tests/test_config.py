import sys
from decimal import Decimal
from os import getcwd
from os.path import join

import pytest
from platformdirs import user_config_dir
from schema import SchemaError, SchemaMissingKeyError

from prosper_api.config import Config

TEST_CONFIG = {
    "testSection": {
        "testString": "stringValue",
        "testNumber": 123,
        "testBoolTrue": True,
        "testBoolFalse": False,
        "testBoolStringTrue": "Y",
        "testBoolStringFalse": "N",
        "testBoolNumberTrue": 1,
        "testBoolNumberFalse": 0,
        "testBoolOther": {},
        "testDecimalString": "123.456",
        "testDecimalFloat": 123.456,
    }
}

TEST_SCHEMA = {
    "testSection": {
        "testString": "stringValue",
        "testNumber": 123,
        "testBoolTrue": True,
        "testBoolFalse": False,
        "testBoolStringTrue": "Y",
        "testBoolStringFalse": "N",
        "testBoolNumberTrue": 1,
        "testBoolNumberFalse": 0,
        "testBoolOther": {},
        "testDecimalString": "123.456",
        "testDecimalFloat": 123.456,
    }
}


class TestConfig:
    def test_get(self):
        config = Config(config_dict=TEST_CONFIG, schema=TEST_SCHEMA)

        assert config.get("testSection.testString") == "stringValue"
        assert config.get("testSection.testNumber") == 123

    def test_get_as_bool(self):
        config = Config(config_dict=TEST_CONFIG)

        assert config.get_as_bool("testSection.testBoolTrue") is True
        assert config.get_as_bool("testSection.testBoolFalse") is False
        assert config.get_as_bool("testSection.testBoolStringTrue") is True
        assert config.get_as_bool("testSection.testBoolStringFalse") is False
        assert config.get_as_bool("testSection.testBoolNumberTrue") is True
        assert config.get_as_bool("testSection.testBoolNumberFalse") is False
        assert config.get_as_bool("testSection.testBoolOther") is False
        assert config.get_as_bool("testSection.testBoolNotFound") is False
        assert config.get_as_bool("testSection.testBoolNotFound", True) is True

    def test_get_as_decimal(self):
        config = Config(config_dict=TEST_CONFIG)

        assert config.get_as_decimal("testSection.testDecimalString") == Decimal(
            "123.456"
        )
        assert config.get_as_decimal("testSection.testDecimalFloat") == pytest.approx(
            Decimal("123.456")
        )
        assert config.get_as_decimal("testSection.testDecimalNotFound") is None
        assert config.get_as_decimal(
            "testSection.testDecimalNotFound", Decimal("0")
        ) == Decimal("0")

    def test_get_invalid_key(self):
        config = Config(config_dict=TEST_CONFIG)

        assert config.get("invalidSection.testString") is None
        assert config.get("testSection.invalidKey") is None

    def test_init_with_config_dict(self):
        config = Config(
            config_dict={"section": {"key1": "value1", "key2": "value2"}},
        )

        assert config.get_as_str("section.key1") == "value1"
        assert config.get_as_str("section.key2") == "value2"

    def test_config_schema_validate_positive(self):
        Config(config_dict=TEST_CONFIG, schema=TEST_SCHEMA)

    def test_config_schema_validate_invalid_key(self):
        with pytest.raises(SchemaError):
            Config(
                config_dict={**TEST_CONFIG, "invalidKey": "value"},
                schema=TEST_SCHEMA,
            )

    def test_config_schema_validate_invalid_value(self):
        with pytest.raises(SchemaError):
            Config(
                config_dict={**TEST_CONFIG, "testString": 123},
                schema=TEST_SCHEMA,
            )

    def test_autoconfig(self, mocker):
        mocker.patch("sys.exit")
        json_config_mock = mocker.patch("prosper_api.config.JsonConfigurationSource")
        toml_config_mock = mocker.patch("prosper_api.config.TomlConfigurationSource")
        yaml_config_mock = mocker.patch("prosper_api.config.YamlConfigurationSource")
        env_config_mock = mocker.patch("prosper_api.config.EnvironmentVariableSource")

        Config.autoconfig(["app_name1", "app_name2"])

        json_config_mock.assert_has_calls(
            [
                mocker.call(join(user_config_dir("app_name1"), "config.json")),
                mocker.call(join(user_config_dir("app_name2"), "config.json")),
                mocker.call(join(getcwd(), ".app_name1.json")),
                mocker.call(join(getcwd(), ".app_name2.json")),
                mocker.call().read(),
                mocker.call().read(),
                mocker.call().read(),
                mocker.call().read(),
            ],
            any_order=False,
        )

        yaml_config_mock.assert_has_calls(
            [
                mocker.call(join(user_config_dir("app_name1"), "config.yml")),
                mocker.call(join(user_config_dir("app_name2"), "config.yml")),
                mocker.call(join(user_config_dir("app_name1"), "config.yaml")),
                mocker.call(join(user_config_dir("app_name2"), "config.yaml")),
                mocker.call(join(getcwd(), ".app_name1.yml")),
                mocker.call(join(getcwd(), ".app_name2.yml")),
                mocker.call(join(getcwd(), ".app_name1.yaml")),
                mocker.call(join(getcwd(), ".app_name2.yaml")),
                mocker.call().read(),
                mocker.call().read(),
                mocker.call().read(),
                mocker.call().read(),
                mocker.call().read(),
                mocker.call().read(),
                mocker.call().read(),
                mocker.call().read(),
            ],
            any_order=False,
        )

        toml_config_mock.assert_has_calls(
            [
                mocker.call(join(user_config_dir("app_name1"), "config.toml")),
                mocker.call(join(user_config_dir("app_name2"), "config.toml")),
                mocker.call(join(getcwd(), ".app_name1.toml")),
                mocker.call(join(getcwd(), ".app_name2.toml")),
                mocker.call(
                    join(getcwd(), ".pyproject.toml"),
                    "tools.app_name1",
                ),
                mocker.call(
                    join(getcwd(), ".pyproject.toml"),
                    "tools.app_name2",
                ),
                mocker.call().read(),
                mocker.call().read(),
                mocker.call().read(),
                mocker.call().read(),
                mocker.call().read(),
                mocker.call().read(),
            ],
            any_order=False,
        )

        env_config_mock.assert_has_calls(
            [
                mocker.call("APP_NAME1", separator="__"),
                mocker.call("APP_NAME2", separator="__"),
                mocker.call().read(),
                mocker.call().read(),
            ],
            any_order=False,
        )

    def test_integration_autoconfig_validation_error(self, mocker):
        mocker.patch.object(sys, "argv", ["prog-name"])

        with pytest.raises(SchemaMissingKeyError):
            Config.autoconfig("unknown-app", validate=True)
