import pytest

from prosper_api.models import Listing, Loan, Note
from prosper_api.serde import get_type_introspecting_object_hook


class TestSerde:
    @pytest.fixture
    def config_mock(self, mocker):
        return mocker.patch("prosper_api.client.Config")

    def test_get_type_introspecting_object_hook_cache(self, config_mock):
        assert get_type_introspecting_object_hook(
            Note, config_mock
        ) is get_type_introspecting_object_hook(Note, config_mock)
        assert get_type_introspecting_object_hook(
            Listing, config_mock
        ) is not get_type_introspecting_object_hook(Loan, config_mock)

    @pytest.mark.skip
    def test_get_type_introspecting_object_hook_untyped_object(
        self, config_mock, caplog
    ):
        class TempClass:
            untyped = "asdf"

        object_hook = get_type_introspecting_object_hook(TempClass, config_mock)
        object_hook({"untyped": 4})

        # TODO: Add assertions

    def test_get_type_introspecting_object_hook_no_matching_type(self, config_mock):
        object_hook = get_type_introspecting_object_hook(TestSerde, config_mock)
        result = object_hook({"unrecognized": 1234})

        assert result == {"unrecognized": 1234}
