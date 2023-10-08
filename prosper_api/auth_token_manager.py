import json
import logging
from datetime import datetime, timedelta
from os.path import isfile

import requests

from prosper_api.config import *

AUTH_URL = "https://api.prosper.com/v1/security/oauth/token"
ACCESS_TOKEN_KEY = "access_token"
REFRESH_TOKEN_KEY = "refresh_token"
EXPIRES_IN_KEY = "expires_in"
EXPIRES_AT_KEY = "expires_at"


class AuthTokenManager:
    def __init__(self, config: Config):
        self.token_cache_path = config.get(TOKEN_CACHE)
        self.client_id = config.get(CLIENT_ID)
        self.client_secret = config.get(CLIENT_SECRET)
        self.username = config.get(USERNAME)
        self.password = config.get(PASSWORD)

        self.token = None
        if isfile(self.token_cache_path):
            with open(self.token_cache_path) as token_cache_file:
                self.token = json.load(token_cache_file)

    def _initial_auth(self):
        payload = {
            "grant_type": "password",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "username": self.username,
            "password": self.password,
        }
        headers = {"accept": "application/json"}
        response = requests.request("POST", AUTH_URL, data=payload, headers=headers)
        response.raise_for_status()
        self.token = response.json()
        self._cache_token()

    def _refresh_auth(self):
        payload = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.token[REFRESH_TOKEN_KEY],
        }
        headers = {"accept": "application/json"}
        response = requests.request("POST", AUTH_URL, data=payload, headers=headers)
        response.raise_for_status()
        self.token = response.json()
        self._cache_token()

    def _cache_token(self):
        self.token[EXPIRES_AT_KEY] = (
            datetime.now() + timedelta(seconds=self.token[EXPIRES_IN_KEY] - 10)
        ).timestamp()
        logging.debug(f"Set expires at to {self.token[EXPIRES_AT_KEY]}")
        with open(self.token_cache_path, "w") as token_cache_file:
            json.dump(self.token, token_cache_file)

    def get_token(self):
        try:
            if self.token is None:
                logging.info(
                    "No cached auth token found; performing initial authentication"
                )
                self._initial_auth()
            elif self.token[EXPIRES_AT_KEY] >= datetime.now().timestamp():
                logging.info("Cached auth token is expiring; attempting to refresh it")
                try:
                    self._refresh_auth()
                except Exception as ex:
                    logging.info(
                        "Failed to refresh auth token; performing full authentication"
                    )
                    logging.debug("Refresh auth token failure", exc_info=ex)
                    self._initial_auth()
        except Exception as ex:
            logging.error("Failed to authenticate", exc_info=ex)
            return None

        return self.token[ACCESS_TOKEN_KEY]
