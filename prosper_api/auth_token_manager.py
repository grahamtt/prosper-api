import json
import logging
from datetime import datetime, timedelta
from os import makedirs
from os.path import dirname, isfile

import requests

from prosper_api.config import (
    _CLIENT_ID,
    _CLIENT_SECRET,
    _PASSWORD,
    _TOKEN_CACHE,
    _USERNAME,
    Config,
)

logger = logging.getLogger(__name__)

_AUTH_URL = "https://api.prosper.com/v1/security/oauth/token"
_ACCESS_TOKEN_KEY = "access_token"
_REFRESH_TOKEN_KEY = "refresh_token"
_EXPIRES_IN_KEY = "expires_in"
_EXPIRES_AT_KEY = "expires_at"


class AuthTokenManager:
    """Token manager for Prosper API tokens.

    Uses credentials configured in the config file or in the OS key storage. The
    credentials are cached and reused until they expire. After expiration, the manager
    attempts to refresh the auth token using the refresh token; if that fails, the
    full auth is re-executed.

    See Also:
        https://developers.prosper.com/docs/authenticating-with-oauth-2-0/password-flow/
    """

    def __init__(self, config: Config):
        """Creates and AuthTokenManager instance.

        Args:
            config (Config): A prosper-api config
        """
        self.token_cache_path = config.get_as_str(_TOKEN_CACHE)
        self.client_id = config.get_as_str(_CLIENT_ID)
        self.client_secret = config.get_as_str(_CLIENT_SECRET)
        self.username = config.get_as_str(_USERNAME)
        self.password = config.get_as_str(_PASSWORD)

        if self.client_secret or self.password:
            logger.warning(
                "Providing secrets via config files or the command line is not secure. Please switch to the "
                "[more secure](https://github.com/grahamtt/prosper-api#more-secure) storage method."
            )

        self.token = None
        if isfile(self.token_cache_path):
            with open(self.token_cache_path) as token_cache_file:
                self.token = json.load(token_cache_file)

    def _initial_auth(self):
        payload = {
            "grant_type": "password",
            "client_id": self.client_id,
            "client_secret": self.client_secret
            if self.client_secret
            else self._fetch_secret(self.client_id),
            "username": self.username,
            "password": self.password
            if self.password
            else self._fetch_secret(self.username),
        }
        headers = {"accept": "application/json"}
        response = requests.request("POST", _AUTH_URL, data=payload, headers=headers)
        response.raise_for_status()
        self.token = response.json()
        self._cache_token()

    def _refresh_auth(self):
        payload = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret
            if self.client_secret
            else self._fetch_secret(self.client_id),
            "refresh_token": self.token[_REFRESH_TOKEN_KEY],
        }
        headers = {"accept": "application/json"}
        response = requests.request("POST", _AUTH_URL, data=payload, headers=headers)
        response.raise_for_status()
        self.token = response.json()
        self._cache_token()

    def _cache_token(self):
        self.token[_EXPIRES_AT_KEY] = (
            datetime.now() + timedelta(seconds=self.token[_EXPIRES_IN_KEY] - 10)
        ).timestamp()
        logging.debug(f"Set expires at to {self.token[_EXPIRES_AT_KEY]}")
        makedirs(dirname(self.token_cache_path), exist_ok=True)
        with open(self.token_cache_path, "w") as token_cache_file:
            json.dump(self.token, token_cache_file)

    def _fetch_secret(self, id):
        import keyring  # noqa: autoimport

        return keyring.get_password("prosper-api", id)

    def get_token(self):
        """Get the auth token, generating it or refreshing it if necessary.

        Returns
            str: A valid authorization token for Prosper APIs.
        """
        try:
            if self.token is None:
                logger.info(
                    "No cached auth token found; performing initial authentication"
                )
                self._initial_auth()
            elif self.token[_EXPIRES_AT_KEY] <= datetime.now().timestamp():
                logger.info("Cached auth token is expired; attempting to refresh it")
                try:
                    self._refresh_auth()
                except Exception as ex:
                    logger.info(
                        "Failed to refresh auth token; performing full authentication"
                    )
                    logging.debug("Refresh auth token failure", exc_info=ex)
                    self._initial_auth()
        except Exception as ex:
            logger.error("Failed to authenticate", exc_info=ex)
            return None

        return self.token[_ACCESS_TOKEN_KEY]
