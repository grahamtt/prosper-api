import pytest

from prosper_api.client import Client


class TestClient:
    @pytest.fixture
    def auto_token_manager_mock(self, mocker):
        return mocker.patch("prosper_api.client.AuthTokenManager")

    @pytest.fixture
    def config_mock(self, mocker):
        return mocker.patch("prosper_api.client.Config")

    @pytest.fixture
    def request_mock(self, mocker):
        return mocker.patch("requests.request")

    @pytest.fixture
    def client_for_api_tests(self, mocker, auto_token_manager_mock, config_mock):
        client = Client()
        mocker.patch.object(client, "_do_get", mocker.MagicMock())
        mocker.patch.object(client, "_do_post", mocker.MagicMock())
        return client

    def test_search(self, client_for_api_tests):
        client_for_api_tests._do_get.return_value = {
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
                    "borrower_state": "AA",
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
        }

        result = client_for_api_tests.search_listings()

        client_for_api_tests._do_get.assert_called_once_with(
            "https://api.prosper.com/listingsvc/v2/listings/",
            {
                "biddable": "true",
                "invested": None,
                "lender_yield_max": None,
                "lender_yield_min": None,
                "limit": None,
                "listing_end_date_max": None,
                "listing_end_date_min": None,
                "listing_number": "",
                "offset": None,
                "percent_funded_max": None,
                "percent_funded_min": None,
                "prosper_rating": "AA,A,B,C,D,E",
                "sort_by": "lender_yield desc",
            },
        )
        assert len(result.result) == 1
        assert result.result[0].listing_number == 11111111
        assert result.result[0].borrower_rate == 0.1395

    def test_list_notes(self, client_for_api_tests):
        client_for_api_tests._do_get.return_value = {
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
                    "note_default_reason": 2,
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

        result = client_for_api_tests.list_notes()

        client_for_api_tests._do_get.assert_called_once_with(
            "https://api.prosper.com/v1/notes/",
            {"limit": None, "offset": None, "sort_by": "prosper_rating desc"},
        )
        assert len(result.result) == 1
        assert result.result[0].principal_balance_pro_rata_share == 69.738100

    def test_get_account_info(self, client_for_api_tests):
        client_for_api_tests._do_get.return_value = {
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
        account = client_for_api_tests.get_account_info()

        client_for_api_tests._do_get.assert_called_once_with(
            "https://api.prosper.com/v1/accounts/prosper/", {}
        )
        assert account.total_account_value == 1111.11
        assert account.invested_notes.E == 1111.056157

    def test_order(self, client_for_api_tests):
        client_for_api_tests._do_post.return_value = {
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

        result = client_for_api_tests.order("listing_id", 1234)

        client_for_api_tests._do_post.assert_called_once_with(
            "https://api.prosper.com/v1/orders/",
            {"bid_requests": [{"listing_id": "listing_id", "bid_amount": 1234}]},
        )
        assert result.order_id == "AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAA"
        assert len(result.bid_requests) == 1
        assert result.bid_requests[0].bid_status == "PENDING"

    def test_list_orders(self, client_for_api_tests):
        client_for_api_tests._do_get.return_value = {
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
        result = client_for_api_tests.list_orders()

        client_for_api_tests._do_get.assert_called_once_with(
            "https://api.prosper.com/v1/orders/",
            query_params={"limit": None, "offset": None},
        )
        assert len(result.result) == 1
        assert result.result[0].order_id == "AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAA"

    def test_do_get(self, auto_token_manager_mock, config_mock, request_mock):
        auto_token_manager_mock.return_value.get_token.return_value = "auth_token"
        request_mock.return_value.json.return_value = {"p1": "v1", "p2": 2}

        response = Client()._do_get("some_url", {"param1": "value1", "param2": 2})

        assert response == {"p1": "v1", "p2": 2}
        request_mock.assert_called_once_with(
            "GET",
            "some_url",
            params={"param1": "value1", "param2": 2},
            json={},
            headers={
                "Authorization": "bearer auth_token",
                "Accept": "application/json",
            },
        )

    def test_do_post(self, auto_token_manager_mock, config_mock, request_mock):
        auto_token_manager_mock.return_value.get_token.return_value = "auth_token"
        request_mock.return_value.json.return_value = {"p1": "v1", "p2": 2}

        response = Client()._do_post("some_url", {"param1": "value1", "param2": 2})

        assert response == {"p1": "v1", "p2": 2}
        request_mock.assert_called_once_with(
            "POST",
            "some_url",
            params={},
            json={"param1": "value1", "param2": 2},
            headers={
                "Authorization": "bearer auth_token",
                "Accept": "application/json",
            },
        )
