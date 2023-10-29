from os.path import dirname, join

from prosper_api.config import Config

TEST_CONFIG = """
[testSection]
testString="stringValue"
testNumber=123
"""


class TestConfig:
    def test_get(self):
        config = Config(config_string=TEST_CONFIG, validate=False)

        assert config.get("testSection.testString") == "stringValue"
        assert config.get("testSection.testNumber") == 123

    def test_get_invalid_key(self):
        config = Config(config_string=TEST_CONFIG, validate=False)

        assert config.get("invalidSection.testString") is None
        assert config.get("testSection.invalidKey") is None

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
        assert config.get("auth.token-cache").endswith("/.prosper-api/token-cache")

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
