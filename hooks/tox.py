import subprocess
import sys
from typing import Iterable, List, Optional, Union

from autohooks.api import error, ok
from autohooks.api.git import (
    get_staged_status,
    stage_files_from_status_list,
    stash_unstaged_changes,
)
from autohooks.config import Config
from autohooks.precommit.run import ReportProgress
from autohooks.terminal import out

DEFAULT_ARGUMENTS = (
    "--parallel",
    "-q",
)


def check_tox_installed() -> None:
    try:
        import tox  # pylint: disable=unused-import, import-outside-toplevel # noqa: F401,E501
    except ImportError:
        raise RuntimeError(
            "Could not find tox. " "Please add tox to your python environment."
        ) from None


def get_tox_config(config: Config) -> Config:
    return config.get("tool", "autohooks", "plugins", "tox")


def ensure_iterable(value: Union[str, List[str]]) -> List[str]:
    if isinstance(value, str):
        return [value]
    return value


def get_tox_arguments(config: Optional[Config]) -> Iterable[str]:
    if not config:
        return DEFAULT_ARGUMENTS

    tox_config = get_tox_config(config)
    arguments = ensure_iterable(tox_config.get_value("arguments", DEFAULT_ARGUMENTS))

    return arguments


def precommit(
    config: Optional[Config] = None,
    report_progress: Optional[ReportProgress] = None,
    **kwargs,  # pylint: disable=unused-argument
) -> int:
    check_tox_installed()

    files = get_staged_status()

    if report_progress:
        report_progress.init(1)

    ret = 0
    arguments = ["tox"]
    arguments.extend(get_tox_arguments(config))

    with stash_unstaged_changes(files):
        try:
            subprocess.check_output(arguments)
            ok("Running tox")
            if report_progress:
                report_progress.update()
        except subprocess.CalledProcessError as e:
            error("Running tox")
            ret = e.returncode
            lint_errors = e.stdout.decode(
                encoding=sys.getdefaultencoding(), errors="replace"
            ).split("\n")
            for line in lint_errors:
                out(line)

        stage_files_from_status_list(files)

    return ret
