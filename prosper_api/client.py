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
    ListNotesRequest,
    ListNotesResponse,
    ListOrdersRequest,
    ListOrdersResponse,
    Note,
    Order,
    SearchListingsRequest,
    SearchListingsResponse,
    _build_order,
)

logger = logging.getLogger(__name__)


class Client:
    """Main client for calling Prosper APIs."""

    _config: Config
    _auth_token_manager: AuthTokenManager

    _ACCOUNT_API_URL = "https://api.prosper.com/v1/accounts/prosper/"
    _SEARCH_API_URL = "https://api.prosper.com/listingsvc/v2/listings/"
    _NOTES_API_URL = "https://api.prosper.com/v1/notes/"
    _ORDERS_API_URL = "https://api.prosper.com/v1/orders/"

    def __init__(
        self,
        auth_token_manager: AuthTokenManager | None = None,
        config: Config | None = None,
    ):
        """Constructs an instance of the Client class.

        Args:
            auth_token_manager (AuthTokenManager | None): A pre-configured
                AuthTokenManager. Omit to use the default one.
            config (Config | None): The Config instance to use. Omit to use the default
                config.
        """
        if config is None:
            config = Config()

        if auth_token_manager is None:
            auth_token_manager = AuthTokenManager(config)

        self._config = config
        self._auth_token_manager = auth_token_manager

    def get_account_info(self) -> Account:
        """Get the account metadata.

        Returns:
            Account: The current information about the account.

        See Also:
            https://developers.prosper.com/docs/investor/accounts-api/
        """
        resp = self._do_get(
            self._ACCOUNT_API_URL,
            {},
        )
        resp["invested_notes"] = AmountsByRating(**resp["invested_notes"])
        resp["pending_bids"] = AmountsByRating(**resp["pending_bids"])
        return Account(**resp)

    def search_listings(self, request: SearchListingsRequest) -> SearchListingsResponse:
        """Search the Prosper listings.

        Args:
            request (SearchListingsRequest): Configures the search, sort, and
                pagination parameters.

        Returns:
            SearchListingsResponse: Holds the search results as well as pagination
                information.
        """
        resp = self._do_get(
            self._SEARCH_API_URL,
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

    def list_notes(self, request: ListNotesRequest = None) -> ListNotesResponse:
        """List notes in the account.

        Args:
            request (ListNotesRequest): Configures the sort and pagination parameters.

        Returns:
            ListNotesResponse: Holds the list results and pagination information.
        """
        if request is None:
            request = ListNotesRequest()

        resp = self._do_get(
            self._NOTES_API_URL,
            {
                "sort_by": f"{request.sort_by} {request.sort_dir}",
                "offset": request.offset,
                "limit": request.limit,
            },
        )
        resp["result"] = [Note(**r) for r in resp["result"]]
        return ListNotesResponse(**resp)

    def order(
        self,
        listing_id: int,
        amount: float,
    ) -> Order:
        """Execute an order for a given listing and amount.

        Args:
            listing_id (int): Identifies the listing to make an order against.
            amount (float): The amount to bid for the order.

        Returns:
            Order: The in-progress order.
        """
        resp = self._do_post(
            self._ORDERS_API_URL,
            {"bid_requests": [{"listing_id": listing_id, "bid_amount": amount}]},
        )
        return _build_order(resp)

    def list_orders(self, request: ListOrdersRequest = None) -> ListOrdersResponse:
        """Lists orders in the account.

        Args:
            request (ListOrdersRequest): Configures the sort and pagination parameters.

        Returns:
            ListOrdersResponse: Holds the list results and pagination information.
        """
        if request is None:
            request = ListOrdersRequest()

        resp = self._do_get(
            self._ORDERS_API_URL,
            query_params={
                "sort_by": f"{request.sort_by} {request.sort_dir}",
                "offset": request.offset,
                "limit": request.limit,
            },
        )
        resp["result"] = [_build_order(r) for r in resp["result"]]
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
        auth_token = self._auth_token_manager.get_token()

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
