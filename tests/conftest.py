import logging

import pytest


@pytest.fixture(autouse=True)
def configure_logging(caplog):
    caplog.set_level(logging.DEBUG)
