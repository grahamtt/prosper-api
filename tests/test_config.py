import tempfile
from os.path import dirname, join

import pytest

from prosper_api.config import Config

TEST_CONFIG = """
[testSection]
testString="stringValue"
testNumber=123
testBoolTrue=true
testBoolFalse=false
testBoolStringTrue="Y"
testBoolStringFalse="N"
testBoolNumberTrue=1
testBoolNumberFalse=0
testBoolOther={}
"""


class TestConfig:
    def test_get(self):
        config = Config(config_string=TEST_CONFIG, validate=False)

        assert config.get("testSection.testString") == "stringValue"
        assert config.get("testSection.testNumber") == 123

    def test_get_as_bool(self):
        config = Config(config_string=TEST_CONFIG, validate=False)

        assert config.get_as_bool("testSection.testBoolTrue") is True
        assert config.get_as_bool("testSection.testBoolFalse") is False
        assert config.get_as_bool("testSection.testBoolStringTrue") is True
        assert config.get_as_bool("testSection.testBoolStringFalse") is False
        assert config.get_as_bool("testSection.testBoolNumberTrue") is True
        assert config.get_as_bool("testSection.testBoolNumberFalse") is False
        assert config.get_as_bool("testSection.testBoolOther") is False
        assert config.get_as_bool("testSection.testBoolNotFound") is False
        assert config.get_as_bool("testSection.testBoolNotFound", True) is True

    def test_get_invalid_key(self):
        config = Config(config_string=TEST_CONFIG, validate=False)

        assert config.get("invalidSection.testString") is None
        assert config.get("testSection.invalidKey") is None

    def test_bad_path_throws(self):
        with pytest.raises(FileNotFoundError):
            Config("THIS_IS_A_BAD_CONFIG_PATH")

    def test_config_path_is_directory_throws(self):
        with tempfile.TemporaryDirectory() as tempdir:
            with pytest.raises(FileNotFoundError):
                Config(tempdir)

    def test_valid_config_with_defaults(self):
        config = Config(
            config_path=join(dirname(__file__), "data", "TEST_CONFIG_DEFAULTS.toml")
        )

        assert config.get("credentials.client-id") == "0123456789abcdef0123456789abcdef"
        assert (
            config.get("credentials.client-secret")
            == "fedcba0987654321fedcba0987654321"
        )
        assert config.get("credentials.username") == "test@test.test"
        assert config.get("credentials.password") == "password_value"
        assert config.get("auth.token-cache").endswith("/prosper-api/token-cache")

    def test_valid_config_no_defaults(self):
        config = Config(
            config_path=join(dirname(__file__), "data", "TEST_CONFIG_NO_DEFAULTS.toml")
        )

        assert config.get("credentials.client-id") == "0123456789abcdef0123456789abcdef"
        assert (
            config.get("credentials.client-secret")
            == "fedcba0987654321fedcba0987654321"
        )
        assert config.get("credentials.username") == "test@test.test"
        assert config.get("credentials.password") == "password_value"
        assert config.get("auth.token-cache") == "/token/cache/path"

    def test_valid_config_extra_section(self):
        config = Config(
            config_path=join(
                dirname(__file__), "data", "TEST_CONFIG_EXTRA_SECTION.toml"
            )
        )

        assert config.get("extra-section.extra-key") == "extra value"

    def test_init_with_config_dict(self):
        config = Config(
            config_dict={"section": {"key1": "value1", "key2": "value2"}},
            validate=False,
        )

        assert config.get_as_str("section.key1") == "value1"
        assert config.get_as_str("section.key2") == "value2"
