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
        client_for_api_tests.search_listings()

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

    def test_list_notes(self, client_for_api_tests):
        client_for_api_tests.list_notes()

        client_for_api_tests._do_get.assert_called_once_with(
            "https://api.prosper.com/v1/notes/",
            {"limit": None, "offset": None, "sort_by": "prosper_rating desc"},
        )

    def test_get_account_info(self, client_for_api_tests):
        client_for_api_tests._do_get.return_value = {
            "available_cash_balance": 8.735266,
            "pending_investments_primary_market": 0.0,
            "pending_investments_secondary_market": 0.0,
            "pending_quick_invest_orders": 0.0,
            "total_principal_received_on_active_notes": 379.2,
            "total_amount_invested_on_active_notes": 4213.53,
            "outstanding_principal_on_active_notes": 3834.329863,
            "total_account_value": 3843.069863,
            "pending_deposit": 0.0,
            "last_deposit_amount": 30.0,
            "last_deposit_date": "2023-10-23 07:00:00 +0000",
            "last_withdraw_amount": -14.31,
            "last_withdraw_date": "2012-11-07 08:00:00 +0000",
            "external_user_id": "AAAAAAAAA-0000-AAAA-AAAA-AAAAAAAA",
            "prosper_account_digest": "Aa=",
            "invested_notes": {
                "NA": 0,
                "HR": 68.080180,
                "E": 1021.056157,
                "D": 891.837770,
                "C": 820.719430,
                "B": 599.842790,
                "A": 213.991266,
                "AA": 214.641243,
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
        assert account.total_account_value == 3843.069863
        assert account.invested_notes.E == 1021.056157

    def test_order(self, client_for_api_tests):
        client_for_api_tests.order("listing_id", 1234)

        client_for_api_tests._do_post.assert_called_once_with(
            "https://api.prosper.com/v1/orders/",
            {"bid_requests": [{"listing_id": "listing_id", "bid_amount": 1234}]},
        )

    def test_list_orders(self, client_for_api_tests):
        client_for_api_tests.list_orders()

        client_for_api_tests._do_get.assert_called_once_with(
            "https://api.prosper.com/v1/orders/",
            query_params={"limit": None, "offset": None},
        )

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
