import logging

import pytest


@pytest.fixture(autouse=True)
def configure_logging(caplog):
    caplog.set_level(logging.DEBUG)


@pytest.fixture
def mock_import(mocker):
    import builtins

    real_import = builtins.__import__

    def myimport(name, _globals, _locals, fromlist, level):
        if True:
            raise ImportError
        return real_import(name, _globals, _locals, fromlist, level)

    builtins.__import__ = myimport

    yield myimport

    builtins.__import__ = real_import
