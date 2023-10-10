import requests

from prosper_api.auth_token_manager import AuthTokenManager
from prosper_api.config import Config


class Client:
    config: Config
    auth_token_manager: AuthTokenManager

    ACCOUNT_API_URL = "https://api.prosper.com/v1/accounts/prosper/"
    SEARCH_API_URL = "https://api.prosper.com/listingsvc/v2/listings/"
    NOTES_API_URL = "https://api.prosper.com/v1/notes/"
    ORDERS_API_URL = "https://api.prosper.com/v1/orders/"

    def __init__(
        self, auth_token_manager: AuthTokenManager = None, config: Config = None
    ):
        if config is None:
            config = Config()

        if auth_token_manager is None:
            auth_token_manager = AuthTokenManager(config)

        self.config = config
        self.auth_token_manager = auth_token_manager

    def get_account_info(self):
        return self._do_get(
            self.ACCOUNT_API_URL,
            {},
        )

    def search_listings(
        self,
        sort_by="lender_yield",
        sort_dir="desc",
        offset: int = None,
        limit: int = None,
        biddable: bool = True,
        invested: bool = None,
        prosper_rating=["AA", "A", "B", "C", "D", "E"],
        listing_number=[],
    ):
        return self._do_get(
            self.SEARCH_API_URL,
            {
                "sort_by": f"{sort_by} {sort_dir}",
                "offset": offset,
                "limit": limit,
                "biddable": "true" if biddable or biddable is None else "false",
                "invested": "true"
                if invested
                else "false"
                if invested is False
                else None,
                "prosper_rating": ",".join(prosper_rating),
                # Probably exclusive
                "listing_number": ",".join(listing_number),
            },
        )

    def list_notes(
        self,
        sort_by="prosper_rating",
        sort_dir="desc",
        offset: int = None,
        limit: int = None,
    ):
        return self._do_get(
            self.NOTES_API_URL,
            {
                "sort_by": f"{sort_by} {sort_dir}",
                "offset": offset,
                "limit": limit,
            },
        )

    def order(
        self,
        listing_id,
        amount,
    ):
        return self._do_post(
            self.ORDERS_API_URL,
            {"bid_requests": [{"listing_id": listing_id, "bid_amount": amount}]},
        )

    def _do_get(self, url, query_params={}):
        auth_token = self.auth_token_manager.get_token()

        response = requests.request(
            "GET",
            url,
            params=query_params,
            headers={
                "Authorization": f"bearer {auth_token}",
                "Accept": "application/json",
            },
        )
        response.raise_for_status()

        return response.json()

    def _do_post(self, url, data={}):
        auth_token = self.auth_token_manager.get_token()

        response = requests.request(
            "POST",
            url,
            json=data,
            headers={
                "Authorization": f"bearer {auth_token}",
                "Accept": "application/json",
            },
        )
        response.raise_for_status()

        return response.json()
