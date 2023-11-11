import subprocess
import sys
from typing import Iterable, List, Optional, Union

from autohooks.api import error, ok
from autohooks.api.git import (
    get_staged_status,
    stage_files_from_status_list,
    stash_unstaged_changes,
)
from autohooks.api.path import match
from autohooks.config import Config
from autohooks.precommit.run import ReportProgress
from autohooks.terminal import out

DEFAULT_INCLUDE = ("*.toml", "poetry.lock")
DEFAULT_ARGUMENTS = ()


def check_toml_sort_installed() -> None:
    try:
        import toml_sort  # pylint: disable=unused-import, import-outside-toplevel # noqa: F401,E501
    except ImportError:
        raise RuntimeError(
            "Could not find toml_sort. "
            "Please add toml_sort to your python environment."
        ) from None


def get_toml_sort_config(config: Config) -> Config:
    return config.get("tool", "autohooks", "plugins", "toml_sort")


def ensure_iterable(value: Union[str, List[str]]) -> List[str]:
    if isinstance(value, str):
        return [value]
    return value


def get_include_from_config(config: Optional[Config]) -> Iterable[str]:
    if not config:
        return DEFAULT_INCLUDE

    toml_sort_config = get_toml_sort_config(config)
    include = ensure_iterable(toml_sort_config.get_value("include", DEFAULT_INCLUDE))

    return include


def get_toml_sort_arguments(config: Optional[Config]) -> Iterable[str]:
    if not config:
        return DEFAULT_ARGUMENTS

    toml_sort_config = get_toml_sort_config(config)
    arguments = ensure_iterable(
        toml_sort_config.get_value("arguments", DEFAULT_ARGUMENTS)
    )

    return arguments


def precommit(
    config: Optional[Config] = None,
    report_progress: Optional[ReportProgress] = None,
    **kwargs,  # pylint: disable=unused-argument
) -> int:
    check_toml_sort_installed()

    include = get_include_from_config(config)
    files = [f for f in get_staged_status() if match(f.path, include)]

    if report_progress:
        report_progress.init(len(files))

    ret = 0
    arguments = ["toml-sort"]
    arguments.extend(get_toml_sort_arguments(config))

    with stash_unstaged_changes(files):
        for f in files:
            try:
                args = arguments.copy()
                args.append(str(f.absolute_path()))
                subprocess.check_output(args)
                ok(f"Running toml_sort on {f.path}")
                if report_progress:
                    report_progress.update()
            except subprocess.CalledProcessError as e:
                ret = e.returncode
                error(f"Running toml_sort on {f.path}")
                lint_errors = e.stdout.decode(
                    encoding=sys.getdefaultencoding(), errors="replace"
                ).split("\n")
                for line in lint_errors:
                    out(line)

        stage_files_from_status_list(files)

    return ret
