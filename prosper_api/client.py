import logging

import requests
from backoff import expo, on_exception
from ratelimit import RateLimitException, limits

from prosper_api.auth_token_manager import AuthTokenManager
from prosper_api.config import Config
from prosper_api.models import (
    Account,
    AmountsByRating,
    Listing,
    ListNotesResponse,
    ListOrdersResponse,
    Note,
    SearchListingsRequest,
    SearchListingsResponse,
    build_order,
)

logger = logging.getLogger(__name__)


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

    def get_account_info(self) -> Account:
        resp = self._do_get(
            self.ACCOUNT_API_URL,
            {},
        )
        resp["invested_notes"] = AmountsByRating(**resp["invested_notes"])
        resp["pending_bids"] = AmountsByRating(**resp["pending_bids"])
        return Account(**resp)

    def search_listings(self, request: SearchListingsRequest):
        resp = self._do_get(
            self.SEARCH_API_URL,
            {
                "sort_by": f"{request.sort_by} {request.sort_dir}",
                "offset": request.offset,
                "limit": request.limit,
                "biddable": "true"
                if request.biddable or request.biddable is None
                else "false",
                "invested": "true"
                if request.invested
                else "false"
                if request.invested is False
                else None,
                "prosper_rating": ",".join(request.prosper_rating),
                # Probably exclusive
                "listing_number": ",".join(request.listing_number),
                "percent_funded_min": request.percent_funded_lower_bound,
                "percent_funded_max": request.percent_funded_upper_bound,
                "listing_end_date_min": request.listing_end_date_lower_bound,
                "listing_end_date_max": request.listing_end_date_upper_bound,
                "lender_yield_min": request.lender_yield_lower_bound,
                "lender_yield_max": request.lender_yield_upper_bound,
            },
        )
        resp["result"] = [Listing(**r) for r in resp["result"]]
        return SearchListingsResponse(**resp)

    def list_notes(
        self,
        sort_by="prosper_rating",
        sort_dir="desc",
        offset: int = None,
        limit: int = None,
    ):
        resp = self._do_get(
            self.NOTES_API_URL,
            {
                "sort_by": f"{sort_by} {sort_dir}",
                "offset": offset,
                "limit": limit,
            },
        )
        resp["result"] = [Note(**r) for r in resp["result"]]
        return ListNotesResponse(**resp)

    def order(
        self,
        listing_id,
        amount,
    ):
        resp = self._do_post(
            self.ORDERS_API_URL,
            {"bid_requests": [{"listing_id": listing_id, "bid_amount": amount}]},
        )
        return build_order(resp)

    def list_orders(
        self,
        offset: int = None,
        limit: int = None,
    ):
        resp = self._do_get(
            self.ORDERS_API_URL, query_params={"limit": limit, "offset": offset}
        )
        resp["result"] = [build_order(r) for r in resp["result"]]
        return ListOrdersResponse(**resp)

    def _do_get(self, url, query_params={}):
        return self._do_request("GET", url, params=query_params)

    def _do_post(self, url, data={}):
        return self._do_request("POST", url, data=data)

    @on_exception(
        expo,
        RateLimitException,
        max_tries=8,
    )
    @limits(calls=20, period=1)
    def _do_request(self, method, url, params={}, data={}):
        auth_token = self.auth_token_manager.get_token()

        response = requests.request(
            method,
            url,
            params=params,
            json=data,
            headers={
                "Authorization": f"bearer {auth_token}",
                "Accept": "application/json",
            },
        )
        response.raise_for_status()
        return response.json()
