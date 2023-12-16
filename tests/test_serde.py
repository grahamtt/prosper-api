from typing import NamedTuple

import pytest

from prosper_api.models import Account
from prosper_api.serde import ModelTreeWalker, Serde


class TestClass1(NamedTuple):
    age: int
    name: str


class TestClass2(NamedTuple):
    num_items: int
    customer: TestClass1


class TestSerde:
    @pytest.fixture
    def config_mock(self, mocker):
        return mocker.patch("prosper_api.client.Config")

    @pytest.mark.parametrize(
        ["json_str", "output_class", "expected_result"],
        [
            (
                '{"age":38,"name": "Sean Spencer"}',
                TestClass1,
                TestClass1(38, "Sean Spencer"),
            ),
            (
                '{"num_items":3,"customer":{"age":38,"name": "Sean Spencer"}}',
                TestClass2,
                TestClass2(3, TestClass1(38, "Sean Spencer")),
            ),
            (
                '{"num_items":3,"customer":{"age":38,"name": "Sean Spencer"},"unknown_key":51}',
                TestClass2,
                {
                    "num_items": 3,
                    "customer": TestClass1(38, "Sean Spencer"),
                    "unknown_key": 51,
                },
            ),
        ],
    )
    def test_serde(self, config_mock, json_str, output_class, expected_result):
        assert Serde(config_mock).deserialize(json_str, output_class) == expected_result

    def test_model_tree_walker(self):
        assert next(ModelTreeWalker(Account)) == Account
