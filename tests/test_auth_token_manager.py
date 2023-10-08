import json
from datetime import datetime
from os.path import join
from tempfile import TemporaryDirectory

import freezegun
import pytest

from prosper_api.auth_token_manager import (
    AuthTokenManager,
    EXPIRES_AT_KEY,
    ACCESS_TOKEN_KEY,
)
from prosper_api.config import Config


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
            config_string="""
            [credentials]
            client-id = "0123456789abcdef0123456789abcdef"
            client-secret = "fedcba0987654321fedcba0987654321"
            username = "test@test.test"
            password = "password_value"
            
            [auth]
            token-cache = "///NOT_A_VALID_PATH///"
        """
        )
        return config

    @pytest.fixture
    def request_mock(self, mocker):
        return mocker.patch("requests.request")

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

    @freezegun.freeze_time("2023-10-07 12:00:01")
    def test_cache_token(self, auth_token_manager):
        with TemporaryDirectory() as tempdir:
            auth_token_manager.token = self.DEFAULT_TOKEN
            auth_token_manager.token_cache_path = join(
                tempdir, "test_auth_token_cache.json"
            )

            auth_token_manager._cache_token()

            with open(auth_token_manager.token_cache_path) as token_cache_file:
                actual_saved_token = json.load(token_cache_file)

            assert actual_saved_token == auth_token_manager.token
            assert actual_saved_token[EXPIRES_AT_KEY] == 1696683590

    def test_get_token_when_no_token(
        self, auth_token_manager_for_get_token: AuthTokenManager
    ):
        def assign_token():
            auth_token_manager_for_get_token.token = self.DEFAULT_TOKEN

        auth_token_manager_for_get_token._initial_auth.side_effect = assign_token

        actual_token = auth_token_manager_for_get_token.get_token()

        auth_token_manager_for_get_token._initial_auth.assert_called_once()
        auth_token_manager_for_get_token._refresh_auth.assert_not_called()
        assert actual_token == self.DEFAULT_TOKEN[ACCESS_TOKEN_KEY]

    @freezegun.freeze_time("2023-10-07 12:00:01")
    def test_get_token_when_token_expired(
        self, auth_token_manager_for_get_token: AuthTokenManager
    ):
        auth_token_manager_for_get_token.token = {
            **self.DEFAULT_TOKEN,
            EXPIRES_AT_KEY: datetime(2023, 10, 7, 12, 0, 1).timestamp(),
        }

        def assign_token():
            auth_token_manager_for_get_token.token = self.DEFAULT_TOKEN

        auth_token_manager_for_get_token._refresh_auth.side_effect = assign_token

        actual_token = auth_token_manager_for_get_token.get_token()

        auth_token_manager_for_get_token._initial_auth.assert_not_called()
        auth_token_manager_for_get_token._refresh_auth.assert_called_once()
        assert actual_token == self.DEFAULT_TOKEN[ACCESS_TOKEN_KEY]

    @freezegun.freeze_time("2023-10-07 12:00:01")
    def test_get_token_when_token_expired_and_refresh_fails(
        self, auth_token_manager_for_get_token: AuthTokenManager
    ):
        auth_token_manager_for_get_token.token = {
            **self.DEFAULT_TOKEN,
            EXPIRES_AT_KEY: datetime(2023, 10, 7, 12, 0, 1).timestamp(),
        }

        def assign_token():
            auth_token_manager_for_get_token.token = self.DEFAULT_TOKEN

        auth_token_manager_for_get_token._refresh_auth.side_effect = Exception
        auth_token_manager_for_get_token._initial_auth.side_effect = assign_token

        actual_token = auth_token_manager_for_get_token.get_token()

        auth_token_manager_for_get_token._initial_auth.assert_called_once()
        auth_token_manager_for_get_token._refresh_auth.assert_called_once()
        assert actual_token == self.DEFAULT_TOKEN[ACCESS_TOKEN_KEY]

    @freezegun.freeze_time("2023-10-07 12:00:01")
    def test_get_token_when_token_expired_and_both_gens_fail(
        self, auth_token_manager_for_get_token: AuthTokenManager
    ):
        auth_token_manager_for_get_token.token = {
            **self.DEFAULT_TOKEN,
            EXPIRES_AT_KEY: datetime(2023, 10, 7, 12, 0, 1).timestamp(),
        }

        def assign_token():
            auth_token_manager_for_get_token.token = self.DEFAULT_TOKEN

        auth_token_manager_for_get_token._refresh_auth.side_effect = Exception
        auth_token_manager_for_get_token._initial_auth.side_effect = Exception

        actual_token = auth_token_manager_for_get_token.get_token()

        auth_token_manager_for_get_token._initial_auth.assert_called_once()
        auth_token_manager_for_get_token._refresh_auth.assert_called_once()
        assert actual_token is None