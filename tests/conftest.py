import builtins
import logging
import sys

import pytest


@pytest.fixture(autouse=True)
def configure_logging(caplog):
    caplog.set_level(logging.DEBUG)


@pytest.fixture
def mock_import_keyring(monkeypatch):
    real_import = builtins.__import__

    def new_import(name, _globals, _locals, fromlist, level):
        if name == "keyring":
            raise ImportError
        return real_import(name, _globals, _locals, fromlist, level)

    monkeypatch.delitem(sys.modules, "win32security", raising=False)
    monkeypatch.setattr(builtins, "__import__", new_import)
