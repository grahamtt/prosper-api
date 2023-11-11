import subprocess
import sys
from subprocess import STDOUT
from typing import Iterable, List, Optional, Union

from autohooks.api import error, ok
from autohooks.api.git import get_staged_status, stage_files, stash_unstaged_changes
from autohooks.config import Config
from autohooks.precommit.run import ReportProgress
from autohooks.terminal import out

DEFAULT_ARGUMENTS = ()


def check_dynamic_versioning_installed() -> None:
    try:
        subprocess.check_output(["poetry-dynamic-versioning", "--help"], stderr=STDOUT)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f'Could not find dynamic_versioning. Please install via `poetry self add "poetry-dynamic-versioning[plugin]"`.\nDebug: {e.stdout.decode("utf-8")}'
        ) from None


def get_dynamic_versioning_config(config: Config) -> Config:
    return config.get("tool", "autohooks", "plugins", "dynamic_versioning")


def ensure_iterable(value: Union[str, List[str]]) -> List[str]:
    if isinstance(value, str):
        return [value]
    return value


def get_dynamic_versioning_arguments(config: Optional[Config]) -> Iterable[str]:
    if not config:
        return DEFAULT_ARGUMENTS

    dynamic_versioning_config = get_dynamic_versioning_config(config)
    arguments = ensure_iterable(
        dynamic_versioning_config.get_value("arguments", DEFAULT_ARGUMENTS)
    )

    return arguments


def precommit(
    config: Optional[Config] = None,
    report_progress: Optional[ReportProgress] = None,
    **kwargs,  # pylint: disable=unused-argument
) -> int:
    check_dynamic_versioning_installed()

    files = get_staged_status()

    if report_progress:
        report_progress.init(1)

    ret = 0
    arguments = ["poetry-dynamic-versioning"]
    arguments.extend(get_dynamic_versioning_arguments(config))

    with stash_unstaged_changes(files):
        try:
            out(subprocess.check_output(arguments, stderr=STDOUT).decode("utf-8"))
            ok("Running version increment")
            if report_progress:
                report_progress.update()
        except subprocess.CalledProcessError as e:
            error("Running version increment")
            ret = e.returncode
            if e.stdout:
                lint_errors = e.stdout.decode(
                    encoding=sys.getdefaultencoding(), errors="replace"
                ).split("\n")
                out("STDOUT")
                for line in lint_errors:
                    out(line)

            if e.stderr:
                lint_errors = e.stderr.decode(
                    encoding=sys.getdefaultencoding(), errors="replace"
                ).split("\n")
                out("STDERR")
                for line in lint_errors:
                    out(line)

            print(f"Error: {e}")

        stage_files(["pyproject.toml"])

    return ret
