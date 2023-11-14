import logging
from datetime import date
from decimal import Decimal
from typing import List, Optional, Union

import requests
import simplejson as json
from backoff import expo, on_exception
from ratelimit import RateLimitException, limits

from prosper_api import serde
from prosper_api.auth_token_manager import AuthTokenManager
from prosper_api.config import Config
from prosper_api.models import (
    Account,
    ListLoansRequest,
    ListLoansResponse,
    ListNotesRequest,
    ListNotesResponse,
    ListOrdersRequest,
    ListOrdersResponse,
    Order,
    SearchListingsRequest,
    SearchListingsResponse,
)

logger = logging.getLogger()


def _bool_val(val: bool, default=None):
    if val is True:
        return "true"
    if val is False:
        return "false"
    if val is None:
        return default

    raise ValueError(f"Unexpected type {type(val)}")


def _list_val(val: List[object]):
    return ",".join(str(v) for v in val) if val else None


def _date_val(val: Union[str, date]):
    if val is None:
        return None

    if isinstance(val, str):
        return date.fromisoformat(val).isoformat()

    if isinstance(val, date):
        return val.isoformat()

    raise ValueError(f"Unexpected type {type(val)}")


class Client:
    """Main client for calling Prosper APIs.

    This client supports most of the operations supported by the Prosper API.

    Examples:
        The client can be created with no args; it then uses the default configuration
        and authentication:

            client = Client()

        The list APIs support pagination using the ``limit`` and ``offset`` parameters:

            loans = []
            offset = 0
            while True:
                response = client.list_loans(ListLoansRequest(limit=25, offset=offset))
                loans += response.result
                offset += 25
                if len(loans) >= response.total_count or len(response.result) < 25:
                    break

            logger.info(pprint(loans))

    Notes:
        * The filters in the ``search_listings()`` method are incomplete.
        * Some *getter* type methods haven't been implemented, e.g. ``get_loan``. The
          corresponding `list` methods exist for every resource type, though.

    See Also:
        https://developers.prosper.com/docs/investor/
    """

    _config: Config
    _auth_token_manager: AuthTokenManager

    _ACCOUNT_API_URL = "https://api.prosper.com/v1/accounts/prosper/"
    _SEARCH_API_URL = "https://api.prosper.com/listingsvc/v2/listings/"
    _NOTES_API_URL = "https://api.prosper.com/v1/notes/"
    _ORDERS_API_URL = "https://api.prosper.com/v1/orders/"
    _LOANS_API_URL = "https://api.prosper.com/v1/loans/"
    _RETURN_FLOATS_CONFIG_PATH = "client.return-floats"

    _has_warned_about_floats = False

    def __init__(
        self,
        config: Optional[Config] = None,
        auth_token_manager: Optional[AuthTokenManager] = None,
    ):
        """Constructs an instance of the Client class.

        Args:
            config (Optional[Config]): Config instance to use.
            auth_token_manager (Optional[AuthTokenManager]): A pre-configured
                AuthTokenManager. Omit to use the default one.
        """
        if config is None:
            config = Config()

        if auth_token_manager is None:
            auth_token_manager = AuthTokenManager(config)

        self.return_floats = config.get_as_bool(self._RETURN_FLOATS_CONFIG_PATH)
        if self.return_floats:
            self._warn_about_floats()

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
        return self._parse_json(resp, Account)

    def search_listings(
        self, request: Union[SearchListingsRequest, None]
    ) -> SearchListingsResponse:
        """Search the Prosper listings.

        Args:
            request (Union[SearchListingsRequest, None]): Configures the search, sort, and
                pagination parameters.

        Returns:
            SearchListingsResponse: Holds the search results as well as pagination
                information.

        See Also:
            https://developers.prosper.com/docs/investor/listings-api/
        """
        if request is None:
            request = SearchListingsRequest()

        resp = self._do_get(
            self._SEARCH_API_URL,
            {
                "sort_by": f"{request.sort_by} {request.sort_dir}",
                "offset": request.offset,
                "limit": request.limit,
                "biddable": _bool_val(request.biddable, "true"),
                "invested": _bool_val(request.invested),
                "amount_funded_min": request.amount_funded_min,
                "amount_funded_max": request.amount_funded_max,
                "amount_remaining_min": request.amount_remaining_min,
                "amount_remaining_max": request.amount_remaining_max,
                "borrower_rate_min": request.borrower_rate_min,
                "borrower_rate_max": request.borrower_rate_max,
                "borrower_state": request.borrower_state,
                "dti_wprosper_loan_min": request.dti_wprosper_loan_min,
                "dti_wprosper_loan_max": request.dti_wprosper_loan_max,
                "employment_status_description": _list_val(
                    request.employment_status_description
                ),
                "estimated_monthly_housing_expense_min": request.estimated_monthly_housing_expense_min,
                "estimated_monthly_housing_expense_max": request.estimated_monthly_housing_expense_max,
                "fico_score": _list_val(request.fico_score),
                "has_mortgage": request.has_mortgage,
                "income_range": _list_val(request.income_range),
                "lender_yield_min": request.lender_yield_min,
                "lender_yield_max": request.lender_yield_max,
                "listing_amount_min": request.listing_amount_min,
                "listing_amount_max": request.listing_amount_max,
                "listing_category_id": _list_val(request.listing_category_id),
                "listing_creation_date_min": _date_val(
                    request.listing_creation_date_min
                ),
                "listing_creation_date_max": _date_val(
                    request.listing_creation_date_max
                ),
                "listing_end_date_min": _date_val(request.listing_end_date_min),
                "listing_end_date_max": _date_val(request.listing_end_date_max),
                "listing_monthly_payment_min": request.listing_monthly_payment_min,
                "listing_monthly_payment_max": request.listing_monthly_payment_max,
                "listing_number": _list_val(request.listing_number),
                "listing_start_date_min": _date_val(request.listing_start_date_min),
                "listing_start_date_max": _date_val(request.listing_start_date_max),
                "listing_status": request.listing_status,
                "listing_term": _list_val(request.listing_term),
                "loan_origination_date_min": _date_val(
                    request.loan_origination_date_min
                ),
                "loan_origination_date_max": _date_val(
                    request.loan_origination_date_max
                ),
                "months_employed_min": request.months_employed_min,
                "months_employed_max": request.months_employed_max,
                "occupation": _list_val(request.occupation),
                "partial_funding_indicator": _bool_val(
                    request.partial_funding_indicator
                ),
                "percent_funded_min": request.percent_funded_min,
                "percent_funded_max": request.percent_funded_max,
                "prior_prosper_loans_min": request.prior_prosper_loans_min,
                "prior_prosper_loans_max": request.prior_prosper_loans_max,
                "prior_prosper_loans_active_min": request.prior_prosper_loans_active_min,
                "prior_prosper_loans_active_max": request.prior_prosper_loans_active_max,
                "prior_prosper_loans_balance_outstanding_min": request.prior_prosper_loans_balance_outstanding_min,
                "prior_prosper_loans_balance_outstanding_max": request.prior_prosper_loans_balance_outstanding_max,
                "prior_prosper_loans_cycles_billed_min": request.prior_prosper_loans_cycles_billed_min,
                "prior_prosper_loans_cycles_billed_max": request.prior_prosper_loans_cycles_billed_max,
                "prior_prosper_loans_late_cycles_min": request.prior_prosper_loans_late_cycles_min,
                "prior_prosper_loans_late_cycles_max": request.prior_prosper_loans_late_cycles_max,
                "prior_prosper_loans_late_payments_one_month_plus_min": request.prior_prosper_loans_late_payments_one_month_plus_min,
                "prior_prosper_loans_late_payments_one_month_plus_max": request.prior_prosper_loans_late_payments_one_month_plus_max,
                "prior_prosper_loans_ontime_payments_min": request.prior_prosper_loans_ontime_payments_min,
                "prior_prosper_loans_ontime_payments_max": request.prior_prosper_loans_ontime_payments_max,
                "prior_prosper_loans_principal_borrowed_min": request.prior_prosper_loans_principal_borrowed_min,
                "prior_prosper_loans_principal_borrowed_max": request.prior_prosper_loans_principal_borrowed_max,
                "prior_prosper_loans_principal_outstanding_min": request.prior_prosper_loans_principal_outstanding_min,
                "prior_prosper_loans_principal_outstanding_max": request.prior_prosper_loans_principal_outstanding_max,
                "prosper_rating": _list_val(request.prosper_rating),
                "prosper_score_min": request.prosper_score_min,
                "prosper_score_max": request.prosper_score_max,
                "stated_monthly_income_min": request.stated_monthly_income_min,
                "stated_monthly_income_max": request.stated_monthly_income_max,
                "verification_stage_min": request.verification_stage_min,
                "verification_stage_max": request.verification_stage_max,
                "whole_loan_end_date_min": _date_val(request.whole_loan_end_date_min),
                "whole_loan_end_date_max": _date_val(request.whole_loan_end_date_max),
                "whole_loan_start_date_min": _date_val(
                    request.whole_loan_start_date_min
                ),
                "whole_loan_start_date_max": _date_val(
                    request.whole_loan_start_date_max
                ),
                "co_borrower_application": _bool_val(request.co_borrower_application),
                "combined_dti_wprosper_loan_min": request.combined_dti_wprosper_loan_min,
                "combined_dti_wprosper_loan_max": request.combined_dti_wprosper_loan_max,
                "combined_stated_monthly_income_min": request.combined_stated_monthly_income_min,
                "combined_stated_monthly_income_max": request.combined_stated_monthly_income_max,
            },
        )
        return self._parse_json(resp, SearchListingsResponse)

    def list_notes(self, request: ListNotesRequest = None) -> ListNotesResponse:
        """List notes in the account.

        Args:
            request (ListNotesRequest): Configures the sort and pagination parameters.

        Returns:
            ListNotesResponse: Holds the list results and pagination information.

        See Also:
            https://developers.prosper.com/docs/investor/notes-api/
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
        return self._parse_json(resp, ListNotesResponse)

    def order(
        self,
        listing_id: int,
        amount: Union[float, Decimal],
    ) -> Order:
        """Execute an order for a given listing and amount.

        Args:
            listing_id (int): Identifies the listing to make an order against.
            amount (Union[float, Decimal]): The amount to bid for the order.

        Returns:
            Order: The in-progress order.

        See Also
            https://developers.prosper.com/docs/investor/orders-api/#submit_new_order
        """
        resp = self._do_post(
            self._ORDERS_API_URL,
            {"bid_requests": [{"listing_id": listing_id, "bid_amount": amount}]},
        )
        return self._parse_json(resp, Order)

    def list_orders(self, request: ListOrdersRequest = None) -> ListOrdersResponse:
        """Lists orders in the account.

        Args:
            request (ListOrdersRequest): Configures the sort and pagination parameters.

        Returns:
            ListOrdersResponse: Holds the list results and pagination information.

        See Also:
            https://developers.prosper.com/docs/investor/orders-api/#get_order_details
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
        return self._parse_json(resp, ListOrdersResponse)

    def list_loans(self, request: ListLoansRequest = None) -> ListLoansResponse:
        """Lists loans associated with the account.

        Args:
            request (ListLoansRequest): Configures the sort and pagination parameters.

        Returns:
            ListLoansResponse: Holds the list results and pagination information.

        See Also:
            https://developers.prosper.com/docs/investor/loans-api/
        """
        if request is None:
            request = ListLoansRequest()

        resp = self._do_get(
            self._LOANS_API_URL,
            query_params={
                "sort_by": f"{request.sort_by} {request.sort_dir}",
                "offset": request.offset,
                "limit": request.limit,
            },
        )
        return self._parse_json(resp, ListLoansResponse)

    def _do_get(self, url, query_params=None):
        if query_params is None:
            query_params = {}
        return self._do_request("GET", url, params=query_params)

    def _do_post(self, url, data=None):
        if data is None:
            data = {}
        return self._do_request("POST", url, data=data)

    @on_exception(
        expo,
        RateLimitException,
        max_tries=8,
    )  # pragma: no mutate
    @limits(calls=20, period=1)  # pragma: no mutate
    def _do_request(self, method, url, params=None, data=None):
        if params is None:
            params = {}
        if data is None:
            data = {}
        self._check_for_floats(params)
        self._check_for_floats(data)

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
        return response.text

    def _parse_json(self, text, type_def: type) -> object:
        return json.loads(
            text,
            use_decimal=not self.return_floats,
            object_hook=serde.get_type_introspecting_object_hook(
                type_def, self._config
            ),
        )

    def _check_for_floats(self, values: dict):
        for val in values.values():
            if isinstance(val, float):
                self._warn_about_floats()

    def _warn_about_floats(self):
        if not self._has_warned_about_floats:
            logger.warning(
                "WARNING: Floating point numbers are not recommended for representing currency values due to their inexact representation of fractional values. You are strongly recommended to use Decimals instead. See https://stackoverflow.com/a/3730040/303601 for more info."
            )
            self._has_warned_about_floats = True  # pragma: no mutate
