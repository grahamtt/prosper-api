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
                "sort_by": "lender_yield desc",
                "offset": None,
                "limit": None,
                "biddable": "true",
                "invested": None,
                "prosper_rating": "AA,A,B,C,D,E",
                "listing_number": "",
            },
        )

    def test_list_notes(self, client_for_api_tests):
        client_for_api_tests.list_notes()

        client_for_api_tests._do_get.assert_called_once_with(
            "https://api.prosper.com/v1/notes/",
            {"limit": None, "offset": None, "sort_by": "prosper_rating desc"},
        )

    def test_get_account_info(self, client_for_api_tests):
        client_for_api_tests.get_account_info()

        client_for_api_tests._do_get.assert_called_once_with(
            "https://api.prosper.com/v1/accounts/prosper/", {}
        )

    def test_order(self, client_for_api_tests):
        client_for_api_tests.order("listing_id", 1234)

        client_for_api_tests._do_post.assert_called_once_with(
            "https://api.prosper.com/v1/orders/",
            {"bid_requests": [{"listing_id": "listing_id", "bid_amount": 1234}]},
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
            json={"param1": "value1", "param2": 2},
            headers={
                "Authorization": "bearer auth_token",
                "Accept": "application/json",
            },
        )
