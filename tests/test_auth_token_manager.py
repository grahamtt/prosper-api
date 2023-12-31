import json
from datetime import datetime
from os.path import join
from tempfile import TemporaryDirectory

import freezegun
import pytest
from prosper_shared.omni_config import Config

from prosper_api.auth_token_manager import (
    _ACCESS_TOKEN_KEY,
    _EXPIRES_AT_KEY,
    AuthTokenManager,
    _schema,
)


class TestAuthTokenManager:
    DEFAULT_TOKEN = {
        "access_token": "access_token_value",
        "token_type": "bearer",
        "refresh_token": "refresh_token_value",
        "expires_in": 3599,
    }

    @pytest.fixture
    def config(self):
        config = Config(
            config_dict={
                "prosper-api": {
                    "credentials": {
                        "client-id": "0123456789abcdef0123456789abcdef",
                        "client-secret": "fedcba0987654321fedcba0987654321",
                        "username": "test@test.test",
                        "password": "password_value",
                    },
                    "auth": {"token-cache": "///NOT_A_VALID_PATH///"},
                },
            },
            schema=_schema(),
        )
        return config

    @pytest.fixture
    def config_with_no_creds(self):
        config = Config(
            config_dict={
                "prosper-api": {
                    "credentials": {
                        "client-id": "0123456789abcdef0123456789abcdef",
                        "username": "test@test.test",
                    },
                    "auth": {"token-cache": "///NOT_A_VALID_PATH///"},
                },
            },
            schema=_schema(),
        )
        return config

    @pytest.fixture
    def temp_token_cache(self):
        with TemporaryDirectory() as temp_dir:
            temp_cache_path = join(temp_dir, "token-cache")
            with open(temp_cache_path, "w") as temp_cache_file:
                json.dump(self.DEFAULT_TOKEN, temp_cache_file)
            yield temp_cache_path

    @pytest.fixture
    def config_with_valid_token_cache(self, temp_token_cache):
        config = Config(
            config_dict={
                "prosper-api": {
                    "credentials": {
                        "client-id": "0123456789abcdef0123456789abcdef",
                        "username": "test@test.test",
                    },
                    "auth": {"token-cache": f"{temp_token_cache}"},
                },
            },
            schema=_schema(),
        )
        return config

    @pytest.fixture
    def request_mock(self, mocker):
        return mocker.patch("requests.request")

    @pytest.fixture
    def keyring_get_password_mock(self, mocker):
        return mocker.patch("keyring.get_password")

    @pytest.fixture
    def makedirs_mock(self, mocker):
        return mocker.patch("prosper_api.auth_token_manager.makedirs")

    @pytest.fixture
    def auth_token_manager(self, config):
        return AuthTokenManager(config)

    @pytest.fixture
    def auth_token_manager_for_get_token(self, mocker, auth_token_manager):
        mocker.patch.object(auth_token_manager, "_initial_auth", mocker.MagicMock())
        mocker.patch.object(auth_token_manager, "_refresh_auth", mocker.MagicMock())
        return auth_token_manager

    @pytest.fixture
    def auth_token_manager_for_gen_token(self, mocker, auth_token_manager):
        mocker.patch.object(auth_token_manager, "_cache_token", mocker.MagicMock())
        return auth_token_manager

    def test_init_when_creds_not_present(self, config_with_no_creds, caplog):
        AuthTokenManager(config_with_no_creds)

        assert len(caplog.messages) == 0

    def test_init_when_password_present(self, config_with_no_creds: Config, caplog):
        config_with_no_creds._config_dict["prosper-api"]["credentials"][
            "password"
        ] = "password_value"
        AuthTokenManager(config_with_no_creds)

        assert caplog.messages[-1].startswith("Providing secrets via config files")

    def test_init_when_client_secret_present(
        self, config_with_no_creds: Config, caplog
    ):
        config_with_no_creds._config_dict["prosper-api"]["credentials"][
            "client-secret"
        ] = "client_secret_value"
        AuthTokenManager(config_with_no_creds)

        assert caplog.messages[-1].startswith("Providing secrets via config files")

    def test_init_when_both_secrets_present(self, config_with_no_creds: Config, caplog):
        config_with_no_creds._config_dict["prosper-api"]["credentials"][
            "password"
        ] = "password_value"
        config_with_no_creds._config_dict["prosper-api"]["credentials"][
            "client-secret"
        ] = "client_secret_value"
        AuthTokenManager(config_with_no_creds)

        assert caplog.messages[-1].startswith("Providing secrets via config files")

    def test_initial_auth(
        self, auth_token_manager_for_gen_token: AuthTokenManager, request_mock
    ):
        request_mock.return_value.json.return_value = self.DEFAULT_TOKEN

        auth_token_manager_for_gen_token._initial_auth()

        request_mock.assert_called_once_with(
            "POST",
            "https://api.prosper.com/v1/security/oauth/token",
            data={
                "grant_type": "password",
                "client_id": "0123456789abcdef0123456789abcdef",
                "client_secret": "fedcba0987654321fedcba0987654321",
                "username": "test@test.test",
                "password": "password_value",
            },
            headers={"accept": "application/json"},
        )

        assert auth_token_manager_for_gen_token.token == self.DEFAULT_TOKEN
        auth_token_manager_for_gen_token._cache_token.assert_called_once()

    def test_initial_auth_when_no_client_id_present(
        self, mocker, config_with_no_creds, request_mock, keyring_get_password_mock
    ):
        auth_token_manager = AuthTokenManager(config_with_no_creds)
        mocker.patch.object(auth_token_manager, "_cache_token", mocker.MagicMock())

        fetch_secret_mock = mocker.MagicMock()
        mocker.patch.object(auth_token_manager, "_fetch_secret", fetch_secret_mock)

        def get_password_side_effect(username):
            if username == "0123456789abcdef0123456789abcdef":
                return "fedcba0987654321fedcba0987654321"
            if username == "test@test.test":
                return "password_value"

        fetch_secret_mock.side_effect = get_password_side_effect

        request_mock.return_value.json.return_value = self.DEFAULT_TOKEN

        auth_token_manager._initial_auth()

        request_mock.assert_called_once_with(
            "POST",
            "https://api.prosper.com/v1/security/oauth/token",
            data={
                "grant_type": "password",
                "client_id": "0123456789abcdef0123456789abcdef",
                "client_secret": "fedcba0987654321fedcba0987654321",
                "username": "test@test.test",
                "password": "password_value",
            },
            headers={"accept": "application/json"},
        )

        assert auth_token_manager.token == self.DEFAULT_TOKEN
        auth_token_manager._cache_token.assert_called_once()

    def test_refresh_auth(
        self, auth_token_manager_for_gen_token: AuthTokenManager, request_mock
    ):
        auth_token_manager_for_gen_token.token = {
            **self.DEFAULT_TOKEN,
            "refresh_token": "existing_refresh_token_value",
        }
        request_mock.return_value.json.return_value = self.DEFAULT_TOKEN

        auth_token_manager_for_gen_token._refresh_auth()

        request_mock.assert_called_once_with(
            "POST",
            "https://api.prosper.com/v1/security/oauth/token",
            data={
                "grant_type": "refresh_token",
                "client_id": "0123456789abcdef0123456789abcdef",
                "client_secret": "fedcba0987654321fedcba0987654321",
                "refresh_token": "existing_refresh_token_value",
            },
            headers={"accept": "application/json"},
        )

        assert auth_token_manager_for_gen_token.token == self.DEFAULT_TOKEN
        auth_token_manager_for_gen_token._cache_token.assert_called_once()

    @freezegun.freeze_time("2023-10-07 12:00:01")
    def test_cache_token(self, auth_token_manager, makedirs_mock):
        with TemporaryDirectory() as tempdir:
            auth_token_manager.token = self.DEFAULT_TOKEN
            auth_token_manager.token_cache_path = join(
                tempdir, "test_auth_token_cache.json"
            )

            auth_token_manager._cache_token()

            with open(auth_token_manager.token_cache_path) as token_cache_file:
                actual_saved_token = json.load(token_cache_file)

            assert actual_saved_token == auth_token_manager.token
            assert actual_saved_token[_EXPIRES_AT_KEY] == 1696683590
            makedirs_mock.assert_called_once_with(tempdir, exist_ok=True)

    def test_get_token_when_no_token(
        self, auth_token_manager_for_get_token: AuthTokenManager
    ):
        def assign_token():
            auth_token_manager_for_get_token.token = self.DEFAULT_TOKEN

        auth_token_manager_for_get_token._initial_auth.side_effect = assign_token

        actual_token = auth_token_manager_for_get_token.get_token()

        auth_token_manager_for_get_token._initial_auth.assert_called_once()
        auth_token_manager_for_get_token._refresh_auth.assert_not_called()
        assert actual_token == self.DEFAULT_TOKEN[_ACCESS_TOKEN_KEY]

    @freezegun.freeze_time("2023-10-07 12:00:01")
    def test_get_token_when_token_expired(
        self, auth_token_manager_for_get_token: AuthTokenManager
    ):
        auth_token_manager_for_get_token.token = {
            **self.DEFAULT_TOKEN,
            _EXPIRES_AT_KEY: datetime(2023, 10, 7, 12, 0, 1).timestamp(),
        }

        def assign_token():
            auth_token_manager_for_get_token.token = self.DEFAULT_TOKEN

        auth_token_manager_for_get_token._refresh_auth.side_effect = assign_token

        actual_token = auth_token_manager_for_get_token.get_token()

        auth_token_manager_for_get_token._initial_auth.assert_not_called()
        auth_token_manager_for_get_token._refresh_auth.assert_called_once()
        assert actual_token == self.DEFAULT_TOKEN[_ACCESS_TOKEN_KEY]

    @freezegun.freeze_time("2023-10-07 12:00:01")
    def test_get_token_when_token_expired_and_refresh_fails(
        self, auth_token_manager_for_get_token: AuthTokenManager
    ):
        auth_token_manager_for_get_token.token = {
            **self.DEFAULT_TOKEN,
            _EXPIRES_AT_KEY: datetime(2023, 10, 7, 12, 0, 1).timestamp(),
        }

        def assign_token():
            auth_token_manager_for_get_token.token = self.DEFAULT_TOKEN

        auth_token_manager_for_get_token._refresh_auth.side_effect = Exception
        auth_token_manager_for_get_token._initial_auth.side_effect = assign_token

        actual_token = auth_token_manager_for_get_token.get_token()

        auth_token_manager_for_get_token._initial_auth.assert_called_once()
        auth_token_manager_for_get_token._refresh_auth.assert_called_once()
        assert actual_token == self.DEFAULT_TOKEN[_ACCESS_TOKEN_KEY]

    @freezegun.freeze_time("2023-10-07 12:00:01")
    def test_get_token_when_token_expired_and_both_gens_fail(
        self, auth_token_manager_for_get_token: AuthTokenManager
    ):
        auth_token_manager_for_get_token.token = {
            **self.DEFAULT_TOKEN,
            _EXPIRES_AT_KEY: datetime(2023, 10, 7, 12, 0, 1).timestamp(),
        }

        def assign_token():
            auth_token_manager_for_get_token.token = self.DEFAULT_TOKEN

        auth_token_manager_for_get_token._refresh_auth.side_effect = Exception
        auth_token_manager_for_get_token._initial_auth.side_effect = Exception

        actual_token = auth_token_manager_for_get_token.get_token()

        auth_token_manager_for_get_token._initial_auth.assert_called_once()
        auth_token_manager_for_get_token._refresh_auth.assert_called_once()
        assert actual_token is None

    def test_get_cached_token(self, temp_token_cache, config_with_valid_token_cache):
        auth_token_manager = AuthTokenManager(config_with_valid_token_cache)

        assert auth_token_manager.token == self.DEFAULT_TOKEN
        assert "expires_at" in auth_token_manager.token

    def test_fetch_secret(self, keyring_get_password_mock, config_with_no_creds):
        auth_token_manager = AuthTokenManager(config_with_no_creds)

        auth_token_manager._fetch_secret("ID")

        keyring_get_password_mock.assert_called_once_with("prosper-api", "ID")
