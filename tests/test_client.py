from copy import deepcopy
from datetime import datetime
from decimal import Decimal
from json import dumps

import pytest

from prosper_api.client import Client, _bool_val
from prosper_api.models import BidStatus, ListPaymentsRequest, SearchListingsRequest


class TestClient:
    @pytest.fixture
    def auth_token_manager_mock(self, mocker):
        return mocker.patch("prosper_api.client.AuthTokenManager")

    @pytest.fixture
    def config_mock(self, mocker):
        return mocker.patch("prosper_api.client.Config")

    @pytest.fixture
    def request_mock(self, mocker):
        return mocker.patch("requests.request")

    @pytest.fixture
    def client_for_api_tests(self, mocker, auth_token_manager_mock, config_mock):
        client = Client()
        mocker.patch.object(client, "_do_get", mocker.MagicMock())
        mocker.patch.object(client, "_do_post", mocker.MagicMock())
        return client

    def test_init_default(self, config_mock, auth_token_manager_mock):
        client: Client = Client()

        config_mock.autoconfig.assert_called_once()
        auth_token_manager_mock.assert_called_once_with(
            config_mock.autoconfig.return_value
        )
        assert client._auth_token_manager == auth_token_manager_mock.return_value

    def test_init_default_auth_token_manager(
        self, config_mock, auth_token_manager_mock
    ):
        client = Client(config_mock.return_value)

        config_mock.assert_not_called()
        auth_token_manager_mock.assert_called_once_with(config_mock.return_value)
        assert client._auth_token_manager == auth_token_manager_mock.return_value

    def test_init_no_default(self, config_mock, auth_token_manager_mock):
        client = Client(config_mock.return_value, auth_token_manager_mock.return_value)

        config_mock.assert_not_called()
        auth_token_manager_mock.assert_not_called()
        assert client._auth_token_manager == auth_token_manager_mock.return_value

    _DEFAULT_SEARCH_FILTERS = {
        "amount_funded_max": None,
        "amount_funded_min": None,
        "amount_remaining_max": None,
        "amount_remaining_min": None,
        "biddable": "true",
        "borrower_rate_max": None,
        "borrower_rate_min": None,
        "borrower_state": None,
        "co_borrower_application": None,
        "combined_dti_wprosper_loan_max": None,
        "combined_dti_wprosper_loan_min": None,
        "combined_stated_monthly_income_max": None,
        "combined_stated_monthly_income_min": None,
        "dti_wprosper_loan_max": None,
        "dti_wprosper_loan_min": None,
        "employment_status_description": None,
        "estimated_monthly_housing_expense_max": None,
        "estimated_monthly_housing_expense_min": None,
        "fico_score": None,
        "has_mortgage": None,
        "income_range": None,
        "invested": None,
        "lender_yield_max": None,
        "lender_yield_min": None,
        "limit": None,
        "listing_amount_max": None,
        "listing_amount_min": None,
        "listing_category_id": None,
        "listing_creation_date_max": None,
        "listing_creation_date_min": None,
        "listing_end_date_max": None,
        "listing_end_date_min": None,
        "listing_monthly_payment_max": None,
        "listing_monthly_payment_min": None,
        "listing_number": None,
        "listing_start_date_max": None,
        "listing_start_date_min": None,
        "listing_status": None,
        "listing_term": None,
        "loan_origination_date_max": None,
        "loan_origination_date_min": None,
        "months_employed_max": None,
        "months_employed_min": None,
        "occupation": None,
        "offset": None,
        "partial_funding_indicator": None,
        "percent_funded_max": None,
        "percent_funded_min": None,
        "prior_prosper_loans_active_max": None,
        "prior_prosper_loans_active_min": None,
        "prior_prosper_loans_balance_outstanding_max": None,
        "prior_prosper_loans_balance_outstanding_min": None,
        "prior_prosper_loans_cycles_billed_max": None,
        "prior_prosper_loans_cycles_billed_min": None,
        "prior_prosper_loans_late_cycles_max": None,
        "prior_prosper_loans_late_cycles_min": None,
        "prior_prosper_loans_late_payments_one_month_plus_max": None,
        "prior_prosper_loans_late_payments_one_month_plus_min": None,
        "prior_prosper_loans_max": None,
        "prior_prosper_loans_min": None,
        "prior_prosper_loans_ontime_payments_max": None,
        "prior_prosper_loans_ontime_payments_min": None,
        "prior_prosper_loans_principal_borrowed_max": None,
        "prior_prosper_loans_principal_borrowed_min": None,
        "prior_prosper_loans_principal_outstanding_max": None,
        "prior_prosper_loans_principal_outstanding_min": None,
        "prosper_rating": "AA,A,B,C,D,E,HR",
        "prosper_score_max": None,
        "prosper_score_min": None,
        "sort_by": "lender_yield desc",
        "stated_monthly_income_max": None,
        "stated_monthly_income_min": None,
        "verification_stage_max": None,
        "verification_stage_min": None,
        "whole_loan_end_date_max": None,
        "whole_loan_end_date_min": None,
        "whole_loan_start_date_max": None,
        "whole_loan_start_date_min": None,
    }

    _SEARCH_LISTINGS_RESULT = dumps(
        {
            "result": [
                {
                    "credit_bureau_values_transunion_indexed": {
                        "g102s_months_since_most_recent_inquiry": -4.0,
                        "credit_report_date": "2023-08-28 17:35:20 +0000",
                        "at02s_open_accounts": 6.0,
                        "g041s_accounts_30_or_more_days_past_due_ever": 0.0,
                        "g093s_number_of_public_records": 0.0,
                        "g094s_number_of_public_record_bankruptcies": -4.0,
                        "g095s_months_since_most_recent_public_record": -4.0,
                        "g218b_number_of_delinquent_accounts": 0.0,
                        "g980s_inquiries_in_the_last_6_months": -4.0,
                        "re20s_age_of_oldest_revolving_account_in_months": 142.0,
                        "s207s_months_since_most_recent_public_record_bankruptcy": -4.0,
                        "re33s_balance_owed_on_all_revolving_accounts": 6565.0,
                        "at57s_amount_delinquent": 0.0,
                        "g099s_public_records_last_24_months": -4.0,
                        "at20s_oldest_trade_open_date": 189.0,
                        "at03s_current_credit_lines": 6.0,
                        "re101s_revolving_balance": 6565.0,
                        "bc34s_bankcard_utilization": 17.0,
                        "at01s_credit_lines": 28.0,
                        "fico_score": "780-799",
                    },
                    "listing_number": 11111111,
                    "listing_start_date": "2023-08-28 22:00:47 +0000",
                    "historical_return": 0.04485,
                    "historical_return_10th_pctl": 0.03404,
                    "historical_return_90th_pctl": 0.05707,
                    "employment_status_description": "Employed",
                    "occupation": "Nurse (RN)",
                    "has_mortgage": True,
                    "co_borrower_application": False,
                    "investment_type_description": "Fractional",
                    "last_updated_date": "2023-08-29 14:33:41 +0000",
                    "invested": True,
                    "biddable": False,
                    "lender_yield": 0.1295,
                    "borrower_rate": 0.1395,
                    "borrower_apr": 0.1677,
                    "listing_term": 48,
                    "listing_monthly_payment": 273.01,
                    "prosper_score": 11,
                    "listing_category_id": 7,
                    "listing_title": "Other",
                    "income_range": 6,
                    "income_range_description": "$100,000+",
                    "stated_monthly_income": 8333.33,
                    "income_verifiable": True,
                    "dti_wprosper_loan": 0.2478,
                    "borrower_state": "AL",
                    "prior_prosper_loans_active": 0,
                    "prior_prosper_loans": 0,
                    "prior_prosper_loans_late_cycles": 0,
                    "prior_prosper_loans_late_payments_one_month_plus": 0,
                    "lender_indicator": 0,
                    "channel_code": "40000",
                    "amount_participation": 0.0,
                    "investment_typeid": 1,
                    "loan_number": 2119830,
                    "months_employed": 46.0,
                    "investment_product_id": 1,
                    "decision_bureau": "TransUnion",
                    "member_key": "AAAAAAAAAAAAAAAAAAAAAAAAA",
                    "listing_end_date": "2023-08-29 14:33:31 +0000",
                    "listing_creation_date": "2023-08-28 17:42:57 +0000",
                    "loan_origination_date": "2023-08-30 07:00:00 +0000",
                    "listing_status": 6,
                    "listing_status_reason": "Completed",
                    "listing_amount": 10000.0,
                    "amount_funded": 10000.0,
                    "amount_remaining": 0.0,
                    "percent_funded": 1.0,
                    "partial_funding_indicator": True,
                    "funding_threshold": 0.7,
                    "prosper_rating": "AA",
                },
            ],
            "result_count": 1,
            "total_count": 1,
        },
        default=str,
    )

    @pytest.mark.parametrize(
        ("input", "expected_call"),
        [
            (None, {}),
            ({}, {}),
            ({"sort_by": "fico_score"}, {"sort_by": "fico_score desc"}),
            (
                {"sort_by": "fico_score", "sort_dir": "desc"},
                {"sort_by": "fico_score desc"},
            ),
            # Boolean filters
            ({"invested": True}, {"invested": "true"}),
            ({"invested": False}, {"invested": "false"}),
            (
                {"partial_funding_indicator": True},
                {"partial_funding_indicator": "true"},
            ),
            (
                {"partial_funding_indicator": False},
                {"partial_funding_indicator": "false"},
            ),
            ({"co_borrower_application": True}, {"co_borrower_application": "true"}),
            ({"co_borrower_application": False}, {"co_borrower_application": "false"}),
            # Range filters
            ({"amount_funded_min": 300}, {"amount_funded_min": 300}),
            ({"amount_funded_max": 300}, {"amount_funded_max": 300}),
            ({"amount_remaining_min": 300}, {"amount_remaining_min": 300}),
            ({"amount_remaining_max": 300}, {"amount_remaining_max": 300}),
            ({"borrower_rate_max": 300}, {"borrower_rate_max": 300}),
            ({"borrower_rate_min": 300}, {"borrower_rate_min": 300}),
            (
                {"combined_dti_wprosper_loan_max": 300},
                {"combined_dti_wprosper_loan_max": 300},
            ),
            (
                {"combined_dti_wprosper_loan_min": 300},
                {"combined_dti_wprosper_loan_min": 300},
            ),
            (
                {"combined_stated_monthly_income_max": 300},
                {"combined_stated_monthly_income_max": 300},
            ),
            (
                {"combined_stated_monthly_income_min": 300},
                {"combined_stated_monthly_income_min": 300},
            ),
            ({"dti_wprosper_loan_max": 300}, {"dti_wprosper_loan_max": 300}),
            ({"dti_wprosper_loan_min": 300}, {"dti_wprosper_loan_min": 300}),
            (
                {"estimated_monthly_housing_expense_max": 300},
                {"estimated_monthly_housing_expense_max": 300},
            ),
            (
                {"estimated_monthly_housing_expense_min": 300},
                {"estimated_monthly_housing_expense_min": 300},
            ),
            ({"lender_yield_max": 300}, {"lender_yield_max": 300}),
            ({"lender_yield_min": 300}, {"lender_yield_min": 300}),
            ({"listing_amount_max": 300}, {"listing_amount_max": 300}),
            ({"listing_amount_min": 300}, {"listing_amount_min": 300}),
            (
                {"listing_monthly_payment_max": 300},
                {"listing_monthly_payment_max": 300},
            ),
            (
                {"listing_monthly_payment_min": 300},
                {"listing_monthly_payment_min": 300},
            ),
            ({"months_employed_max": 300}, {"months_employed_max": 300}),
            ({"months_employed_min": 300}, {"months_employed_min": 300}),
            ({"percent_funded_max": 300}, {"percent_funded_max": 300}),
            ({"percent_funded_min": 300}, {"percent_funded_min": 300}),
            (
                {"prior_prosper_loans_active_max": 300},
                {"prior_prosper_loans_active_max": 300},
            ),
            (
                {"prior_prosper_loans_active_min": 300},
                {"prior_prosper_loans_active_min": 300},
            ),
            (
                {"prior_prosper_loans_balance_outstanding_max": 300},
                {"prior_prosper_loans_balance_outstanding_max": 300},
            ),
            (
                {"prior_prosper_loans_balance_outstanding_min": 300},
                {"prior_prosper_loans_balance_outstanding_min": 300},
            ),
            (
                {"prior_prosper_loans_cycles_billed_max": 300},
                {"prior_prosper_loans_cycles_billed_max": 300},
            ),
            (
                {"prior_prosper_loans_cycles_billed_min": 300},
                {"prior_prosper_loans_cycles_billed_min": 300},
            ),
            (
                {"prior_prosper_loans_late_cycles_max": 300},
                {"prior_prosper_loans_late_cycles_max": 300},
            ),
            (
                {"prior_prosper_loans_late_cycles_min": 300},
                {"prior_prosper_loans_late_cycles_min": 300},
            ),
            (
                {"prior_prosper_loans_late_payments_one_month_plus_max": 300},
                {"prior_prosper_loans_late_payments_one_month_plus_max": 300},
            ),
            (
                {"prior_prosper_loans_late_payments_one_month_plus_min": 300},
                {"prior_prosper_loans_late_payments_one_month_plus_min": 300},
            ),
            ({"prior_prosper_loans_max": 300}, {"prior_prosper_loans_max": 300}),
            ({"prior_prosper_loans_min": 300}, {"prior_prosper_loans_min": 300}),
            (
                {"prior_prosper_loans_ontime_payments_max": 300},
                {"prior_prosper_loans_ontime_payments_max": 300},
            ),
            (
                {"prior_prosper_loans_ontime_payments_min": 300},
                {"prior_prosper_loans_ontime_payments_min": 300},
            ),
            (
                {"prior_prosper_loans_principal_borrowed_max": 300},
                {"prior_prosper_loans_principal_borrowed_max": 300},
            ),
            (
                {"prior_prosper_loans_principal_borrowed_min": 300},
                {"prior_prosper_loans_principal_borrowed_min": 300},
            ),
            (
                {"prior_prosper_loans_principal_outstanding_max": 300},
                {"prior_prosper_loans_principal_outstanding_max": 300},
            ),
            (
                {"prior_prosper_loans_principal_outstanding_min": 300},
                {"prior_prosper_loans_principal_outstanding_min": 300},
            ),
            ({"prosper_score_max": 3}, {"prosper_score_max": 3}),
            ({"prosper_score_min": 7}, {"prosper_score_min": 7}),
            ({"stated_monthly_income_max": 300}, {"stated_monthly_income_max": 300}),
            ({"stated_monthly_income_min": 300}, {"stated_monthly_income_min": 300}),
            ({"verification_stage_max": 2}, {"verification_stage_max": 2}),
            ({"verification_stage_min": 2}, {"verification_stage_min": 2}),
            # Date range filters
            (
                {"listing_creation_date_max": "2023-11-04"},
                {"listing_creation_date_max": "2023-11-04"},
            ),
            (
                {"listing_creation_date_min": "2023-11-04"},
                {"listing_creation_date_min": "2023-11-04"},
            ),
            (
                {"listing_end_date_max": "2023-11-04"},
                {"listing_end_date_max": "2023-11-04"},
            ),
            (
                {"listing_end_date_min": "2023-11-04"},
                {"listing_end_date_min": "2023-11-04"},
            ),
            (
                {"listing_start_date_max": "2023-11-04"},
                {"listing_start_date_max": "2023-11-04"},
            ),
            (
                {"listing_start_date_min": "2023-11-04"},
                {"listing_start_date_min": "2023-11-04"},
            ),
            (
                {"loan_origination_date_max": "2023-11-04"},
                {"loan_origination_date_max": "2023-11-04"},
            ),
            (
                {"loan_origination_date_min": "2023-11-04"},
                {"loan_origination_date_min": "2023-11-04"},
            ),
            (
                {"whole_loan_end_date_max": "2023-11-04"},
                {"whole_loan_end_date_max": "2023-11-04"},
            ),
            (
                {"whole_loan_end_date_min": "2023-11-04"},
                {"whole_loan_end_date_min": "2023-11-04"},
            ),
            (
                {"whole_loan_start_date_max": "2023-11-04"},
                {"whole_loan_start_date_max": "2023-11-04"},
            ),
            (
                {"whole_loan_start_date_min": "2023-11-04"},
                {"whole_loan_start_date_min": "2023-11-04"},
            ),
            # Multi-value filters
            (
                {
                    "employment_status_description": [
                        "Employed",
                        "Self-employed",
                        "Retired",
                    ]
                },
                {"employment_status_description": "Employed,Self-employed,Retired"},
            ),
            (
                {"fico_score": ["<600", "600-619", "620-639"]},
                {"fico_score": "<600,600-619,620-639"},
            ),
            ({"income_range": [1, 2, 3]}, {"income_range": "1,2,3"}),
            ({"listing_category_id": [1, 2, 3]}, {"listing_category_id": "1,2,3"}),
            ({"listing_number": [1, 2, 3]}, {"listing_number": "1,2,3"}),
            ({"listing_term": [24, 36, 48]}, {"listing_term": "24,36,48"}),
            (
                {"occupation": ["Analyst", "Architect", "Attorney"]},
                {"occupation": "Analyst,Architect,Attorney"},
            ),
            ({"prosper_rating": ["N/A", "HR", "E"]}, {"prosper_rating": "N/A,HR,E"}),
        ],
    )
    def test_search(self, client_for_api_tests, input, expected_call):
        client_for_api_tests._do_get.return_value = deepcopy(
            self._SEARCH_LISTINGS_RESULT
        )
        request = None if input is None else SearchListingsRequest(**input)

        result = client_for_api_tests.search_listings(request)

        client_for_api_tests._do_get.assert_called_once_with(
            "https://api.prosper.com/listingsvc/v2/listings/",
            {**self._DEFAULT_SEARCH_FILTERS, **expected_call},
        )
        assert len(result.result) == 1
        assert result.result[0].listing_number == 11111111
        assert result.result[0].borrower_rate == Decimal("0.1395")

    def test_search_when_invested(self, client_for_api_tests):
        client_for_api_tests._do_get.return_value = deepcopy(
            self._SEARCH_LISTINGS_RESULT
        )

        result = client_for_api_tests.search_listings(
            SearchListingsRequest(invested=True)
        )

        client_for_api_tests._do_get.assert_called_once_with(
            "https://api.prosper.com/listingsvc/v2/listings/",
            {**self._DEFAULT_SEARCH_FILTERS, "invested": "true"},
        )
        assert len(result.result) == 1
        assert result.result[0].listing_number == 11111111
        assert result.result[0].borrower_rate == Decimal("0.1395")

    def test_search_when_not_invested(self, client_for_api_tests):
        client_for_api_tests._do_get.return_value = self._SEARCH_LISTINGS_RESULT

        result = client_for_api_tests.search_listings(
            SearchListingsRequest(invested=False)
        )

        client_for_api_tests._do_get.assert_called_once_with(
            "https://api.prosper.com/listingsvc/v2/listings/",
            {**self._DEFAULT_SEARCH_FILTERS, "invested": "false"},
        )
        assert len(result.result) == 1
        assert result.result[0].listing_number == 11111111
        assert result.result[0].borrower_rate == Decimal("0.1395")

    def test_list_notes(self, client_for_api_tests):
        client_for_api_tests._do_get.return_value = dumps(
            {
                "result": [
                    {
                        "principal_balance_pro_rata_share": 69.7381,
                        "service_fees_paid_pro_rata_share": -0.589991,
                        "principal_paid_pro_rata_share": 15.8919,
                        "interest_paid_pro_rata_share": 14.749939,
                        "prosper_fees_paid_pro_rata_share": 0.0,
                        "late_fees_paid_pro_rata_share": 0.0,
                        "collection_fees_paid_pro_rata_share": 0.0,
                        "debt_sale_proceeds_received_pro_rata_share": 0.0,
                        "platform_proceeds_net_received": 0.0,
                        "next_payment_due_amount_pro_rata_share": 3.404649,
                        "note_ownership_amount": 85.63,
                        "note_sale_gross_amount_received": 0.0,
                        "note_sale_fees_paid": 0.0,
                        "loan_note_id": "35659-26",
                        "listing_number": 111111,
                        "note_status": 3,
                        "note_status_description": "DEFAULTED",
                        "note_default_reason": 3,
                        "note_default_reason_description": "Bankruptcy",
                        "is_sold": False,
                        "is_sold_folio": False,
                        "loan_number": 11111,
                        "amount_borrowed": 5000.0,
                        "borrower_rate": 0.25,
                        "lender_yield": 0.24,
                        "prosper_rating": "N/A",
                        "term": 36,
                        "age_in_months": 182,
                        "accrued_interest": 97.871494,
                        "payment_received": 30.051848,
                        "loan_settlement_status": "Unspecified",
                        "loan_extension_status": "Unspecified",
                        "loan_extension_term": 0,
                        "is_in_bankruptcy": False,
                        "co_borrower_application": False,
                        "origination_date": "2008-08-19",
                        "days_past_due": 123,
                        "next_payment_due_date": "2011-08-19",
                        "ownership_start_date": "2008-08-19",
                    },
                ],
                "result_count": 1,
                "total_count": 1,
            }
        )

        result = client_for_api_tests.list_notes()

        client_for_api_tests._do_get.assert_called_once_with(
            "https://api.prosper.com/v1/notes/",
            {"limit": None, "offset": None, "sort_by": "prosper_rating desc"},
        )
        assert len(result.result) == 1
        assert result.result[0].principal_balance_pro_rata_share == Decimal("69.738100")

    def test_get_account_info(self, client_for_api_tests):
        client_for_api_tests._do_get.return_value = dumps(
            {
                "available_cash_balance": 111.1111,
                "pending_investments_primary_market": 0.0,
                "pending_investments_secondary_market": 0.0,
                "pending_quick_invest_orders": 0.0,
                "total_principal_received_on_active_notes": 111.11,
                "total_amount_invested_on_active_notes": 1111.11,
                "outstanding_principal_on_active_notes": 1111.11,
                "total_account_value": 1111.11,
                "pending_deposit": 0.0,
                "last_deposit_amount": 30.0,
                "last_deposit_date": "2023-10-23 07:00:00 +0000",
                "last_withdraw_amount": -14.31,
                "last_withdraw_date": "2012-11-07 08:00:00 +0000",
                "external_user_id": "AAAAAAAAA-0000-AAAA-AAAA-AAAAAAAA",
                "prosper_account_digest": "Aa=",
                "invested_notes": {
                    "NA": 0,
                    "HR": 11.080180,
                    "E": 1111.056157,
                    "D": 111.837770,
                    "C": 111.719430,
                    "B": 111.842790,
                    "A": 111.991266,
                    "AA": 111.641243,
                },
                "pending_bids": {
                    "NA": 0,
                    "HR": 0,
                    "E": 0,
                    "D": 0,
                    "C": 0,
                    "B": 0,
                    "A": 0,
                    "AA": 0,
                },
            }
        )
        account = client_for_api_tests.get_account_info()

        client_for_api_tests._do_get.assert_called_once_with(
            "https://api.prosper.com/v1/accounts/prosper/", {}
        )
        assert account.total_account_value == Decimal("1111.11")
        assert account.invested_notes.E == Decimal("1111.056157")

    def test_order(self, client_for_api_tests):
        client_for_api_tests._do_post.return_value = dumps(
            {
                "order_id": "AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAA",
                "bid_requests": [
                    {
                        "listing_id": 11111111,
                        "bid_amount": 25.0,
                        "bid_status": "PENDING",
                    }
                ],
                "order_status": "IN_PROGRESS",
                "source": "AI",
                "order_date": "2023-09-18 16:08:23 +0000",
            }
        )

        result = client_for_api_tests.order("listing_id", 1234)

        client_for_api_tests._do_post.assert_called_once_with(
            "https://api.prosper.com/v1/orders/",
            {"bid_requests": [{"listing_id": "listing_id", "bid_amount": 1234}]},
        )
        assert result.order_id == "AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAA"
        assert len(result.bid_requests) == 1
        assert result.bid_requests[0].bid_status == BidStatus.PENDING

    def test_list_orders(self, client_for_api_tests):
        client_for_api_tests._do_get.return_value = dumps(
            {
                "result": [
                    {
                        "order_id": "AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAA",
                        "bid_requests": [
                            {
                                "listing_id": 11111111,
                                "bid_amount": 25.0,
                                "bid_status": "INVESTED",
                                "bid_result": "BID_SUCCEEDED",
                                "bid_amount_placed": 25.0,
                            }
                        ],
                        "order_amount": 25.0,
                        "order_amount_placed": 25.0,
                        "order_amount_invested": 25.0,
                        "order_status": "COMPLETED",
                        "source": "AI",
                        "order_date": "2023-09-18 16:08:23 +0000",
                    },
                ],
                "result_count": 1,
                "total_count": 1,
            }
        )
        result = client_for_api_tests.list_orders()

        client_for_api_tests._do_get.assert_called_once_with(
            "https://api.prosper.com/v1/orders/",
            query_params={
                "sort_by": "prosper_rating desc",
                "limit": None,
                "offset": None,
            },
        )
        assert len(result.result) == 1
        assert result.result[0].order_id == "AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAA"

    def test_list_loans(self, client_for_api_tests):
        client_for_api_tests._do_get.return_value = dumps(
            {
                "result": [
                    {
                        "loan_number": 11111,
                        "amount_borrowed": 3000.0,
                        "borrower_rate": 0.29,
                        "prosper_rating": "N/A",
                        "term": 36,
                        "age_in_months": 192,
                        "origination_date": "2007-10-19",
                        "days_past_due": 0,
                        "principal_balance": 0.0,
                        "service_fees_paid": -37.59,
                        "principal_paid": 3000.0,
                        "interest_paid": 1090.03,
                        "prosper_fees_paid": 0.0,
                        "late_fees_paid": 0.0,
                        "collection_fees_paid": 0.0,
                        "debt_sale_proceeds_received": 0.0,
                        "loan_status": 4,
                        "loan_status_description": "COMPLETED",
                        "loan_default_reason": 0,
                        "next_payment_due_date": "2010-10-19",
                        "next_payment_due_amount": 0.0,
                    },
                ],
                "result_count": 1,
                "total_count": 1,
            }
        )
        result = client_for_api_tests.list_loans()

        client_for_api_tests._do_get.assert_called_once_with(
            "https://api.prosper.com/v1/loans/",
            query_params={
                "sort_by": "prosper_rating desc",
                "limit": None,
                "offset": None,
            },
        )
        assert len(result.result) == 1
        assert result.result[0].loan_number == 11111

    def test_list_payments(self, client_for_api_tests):
        client_for_api_tests._do_get.return_value = dumps(
            {
                "result": [
                    {
                        "loan_number": 2300367,
                        "transaction_id": 318744581,
                        "funds_available_date": "2025-02-03T08:00:00.000+0000",
                        "investor_disbursement_date": "2025-02-04T08:00:00.000+0000",
                        "transaction_effective_date": "2025-02-02T08:00:00.000+0000",
                        "account_effective_date": "2025-02-02T08:00:00.000+0000",
                        "payment_transaction_code": "ACH",
                        "payment_status": "Success",
                        "match_back_id": "B4F8003ADFD16ECEA608C5859BA2CB2E5E481F03",
                        "prior_match_back_id": None,
                        "loan_payment_cashflow_type": "Payment",
                        "payment_amount": "0.7812",
                        "principal_amount": "0.2169",
                        "interest_amount": "0.5643",
                        "origination_interest_amount": "0",
                        "late_fee_amount": "0",
                        "service_fee_amount": "0.0223",
                        "collection_fee_amount": "0",
                        "gl_reward_amount": "0",
                        "nsf_fee_amount": "0",
                        "pre_days_past_due": 0,
                        "post_days_past_due": None,
                        "resulting_principal_balance": "26.0107",
                    },
                    {
                        "loan_number": 2300367,
                        "transaction_id": 317088207,
                        "funds_available_date": "2025-01-05T08:00:00.000+0000",
                        "investor_disbursement_date": "2025-01-06T08:00:00.000+0000",
                        "transaction_effective_date": "2025-01-02T08:00:00.000+0000",
                        "account_effective_date": "2025-01-02T08:00:00.000+0000",
                        "payment_transaction_code": "ACH",
                        "payment_status": "Success",
                        "match_back_id": "10F603DD91EB3F3C0408850CD0A6EBD25A03070B",
                        "prior_match_back_id": None,
                        "loan_payment_cashflow_type": "Payment",
                        "payment_amount": "0.7812",
                        "principal_amount": "0.2124",
                        "interest_amount": "0.5688",
                        "origination_interest_amount": "0",
                        "late_fee_amount": "0",
                        "service_fee_amount": "0.0224",
                        "collection_fee_amount": "0",
                        "gl_reward_amount": "0",
                        "nsf_fee_amount": "0",
                        "pre_days_past_due": 0,
                        "post_days_past_due": None,
                        "resulting_principal_balance": "26.2276",
                    },
                ],
                "result_count": 2,
                "total_count": 2,
            }
        )
        result = client_for_api_tests.list_payments(
            ListPaymentsRequest(loan_number=[2300367])
        )

        client_for_api_tests._do_get.assert_called_once_with(
            "https://api.prosper.com/loans/payments",
            query_params={
                "limit": None,
                "loan_number": "2300367",
                "offset": None,
                "transaction_effective_date": None,
            },
        )
        assert len(result.result) == 2
        assert result.result[0].loan_number == 2300367

    @pytest.mark.parametrize(
        [
            "parse_decimals_config",
            "input_val",
            "return_val",
        ],
        [
            (
                True,
                None,
                '{"p1": "v1", "p2": 2.0}',
            ),
            (
                True,
                {"param1": "value1", "param2": 2.0},
                '{"p1": "v1", "p2": 2.0}',
            ),
            (
                False,
                {"param1": "value1", "param2": 2.0},
                '{"p1": "v1", "p2": 2.0}',
            ),
            (
                True,
                {"param1": "value1", "param2": Decimal(2.0)},
                '{"p1": "v1", "p2": 2.0}',
            ),
            (
                False,
                {"param1": "value1", "param2": Decimal(2.0)},
                '{"p1": "v1", "p2": 2.0}',
            ),
        ],
    )
    def test_do_get(
        self,
        auth_token_manager_mock,
        config_mock,
        request_mock,
        caplog,
        parse_decimals_config: bool,
        input_val: dict,
        return_val: str,
    ):
        auth_token_manager_mock.return_value.get_token.return_value = "auth_token"
        request_mock.return_value.text = return_val
        config_mock.autoconfig.return_value.get_as_bool.return_value = (
            parse_decimals_config
        )

        response = Client()._do_get("some_url", input_val)

        assert response == return_val
        request_mock.assert_called_once_with(
            "GET",
            "some_url",
            params=input_val if input_val else {},
            json={},
            headers={
                "Authorization": "bearer auth_token",
                "Accept": "application/json",
            },
        )

    @pytest.mark.parametrize(
        [
            "parse_decimals_config",
            "input_val",
            "return_val",
        ],
        [
            (
                True,
                None,
                '{"p1": "v1", "p2": 2.0}',
            ),
            (
                True,
                {"param1": "value1", "param2": 2.0},
                '{"p1": "v1", "p2": 2.0}',
            ),
            (
                False,
                {"param1": "value1", "param2": 2.0},
                '{"p1": "v1", "p2": 2.0}',
            ),
            (
                True,
                {"param1": "value1", "param2": Decimal(2.0)},
                '{"p1": "v1", "p2": 2.0}',
            ),
            (
                False,
                {"param1": "value1", "param2": Decimal(2.0)},
                '{"p1": "v1", "p2": 2.0}',
            ),
        ],
    )
    def test_do_post(
        self,
        auth_token_manager_mock,
        config_mock,
        request_mock,
        caplog,
        parse_decimals_config: bool,
        input_val: dict,
        return_val: str,
    ):
        auth_token_manager_mock.return_value.get_token.return_value = "auth_token"
        request_mock.return_value.text = return_val
        config_mock.autoconfig.return_value.get_as_bool.return_value = (
            parse_decimals_config
        )

        response = Client()._do_post("some_url", input_val)

        assert response == return_val
        request_mock.assert_called_once_with(
            "POST",
            "some_url",
            params={},
            json=input_val if input_val else {},
            headers={
                "Authorization": "bearer auth_token",
                "Accept": "application/json",
            },
        )

    def test_bool_val_when_invalid(self):
        with pytest.raises(ValueError):
            _bool_val("blah")

    @pytest.mark.skip("Takes too long; refactor to mock the sleeps")
    def test_rate_limiting(self, auth_token_manager_mock, request_mock):
        client: Client = Client()
        start_time = datetime.now().timestamp()
        for i in range(41):
            client._do_request("GET", "http://localhost:12345")
        end_time = datetime.now().timestamp()

        # We allow 20 requests per second; 41 requests are required to ensure the test lasts at least 1 seconds in case it starts at an unlucky time
        assert end_time - start_time >= 1
