import sys

import pytest
from prosper_shared.omni_config import Config
from schema import SchemaMissingKeyError


class TestConfig:
    def test_integration_autoconfig_validation_error(self, mocker):
        mocker.patch.object(sys, "argv", ["prog-name"])

        with pytest.raises(SchemaMissingKeyError):
            Config.autoconfig("unknown-app", validate=True)
