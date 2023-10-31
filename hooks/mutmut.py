import os.path
import subprocess
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

BASE_ARGUMENTS = ("--no-progress",)


def check_mutmut_installed() -> None:
    try:
        import mutmut  # pylint: disable=unused-import, import-outside-toplevel # noqa: F401,E501
    except ImportError:
        raise RuntimeError(
            "Could not find mutmut. " "Please add mutmut to your python environment."
        ) from None


def get_mutmut_config(config: Config) -> Config:
    return config.get("tool", "autohooks", "plugins", "mutmut")


def ensure_iterable(value: Union[str, List[str]]) -> List[str]:
    if isinstance(value, str):
        return [value]
    return value


def get_mutmut_arguments(config: Optional[Config]) -> Iterable[str]:
    if not config:
        return BASE_ARGUMENTS

    mutmut_config = get_mutmut_config(config)
    arguments = ensure_iterable(mutmut_config.get_value("arguments", []))
    arguments.extend(BASE_ARGUMENTS)

    return arguments


def precommit(
    config: Optional[Config] = None,
    report_progress: Optional[ReportProgress] = None,
    **kwargs,  # pylint: disable=unused-argument
) -> int:
    check_mutmut_installed()

    files = get_staged_status()

    if report_progress:
        report_progress.init(1)

    ret = 0
    arguments = ["mutmut", "run"]
    arguments.extend(get_mutmut_arguments(config))

    with stash_unstaged_changes(files):
        try:
            subprocess.check_output(arguments)
            ok("Running mutmut")
            if report_progress:
                report_progress.update()
        except subprocess.CalledProcessError as e:
            error("Running mutmut")
            ret = e.returncode
            out(
                f"See output at 'file://{os.path.abspath('dist/mutmut/html/index.html')}"
            )

        stage_files_from_status_list(files)

        subprocess.check_output(
            "mutmut html && mkdir -p dist/mutmut && rm -rf dist/mutmut/html && mv html dist/mutmut",
            shell=True,
        )

    return ret
