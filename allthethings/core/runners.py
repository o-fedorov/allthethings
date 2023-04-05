"""Support for per-project commands run."""
import os
import subprocess  # noqa: S404
from dataclasses import dataclass
from textwrap import dedent

from .base import BaseCommand

__all__ = ["Result", "Execute"]

SEPARATOR_STYLE = "="
SEPARATOR_LEN = 70
OUT_TEMPLATE = dedent(
    f"""\
        {{key:{SEPARATOR_STYLE}^{SEPARATOR_LEN}}}
        {{out}}
        {SEPARATOR_STYLE * SEPARATOR_LEN}
        {{err}}
    """
)
ENV_PREFIX = "ALLTHETHINGS_"


@dataclass
class Result:
    """Command execution result for a project."""

    name: str
    icon: str = "✅"
    comment: str = "Ok"

    def set_error(self, text):
        """Shorthand method for making an error result."""
        self.icon = "⛔"
        self.comment = text

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_val:
            return

        if isinstance(exc_val, subprocess.CalledProcessError):
            resp_raw = exc_val.stderr if exc_val.stderr else exc_val.output
            self.set_error(resp_raw.decode())
        else:
            self.set_error(str(exc_val))


class Execute(BaseCommand):
    """
    Execute arbitrary shell command for each project.

    exec
        {--g|group=?* : Run only for the projects of specific group.}
        {cmd* : The command to run.  The commands
         are executed at the root of a project.
         Use `ALLTHETHINGS_PROJECT_NAME` and `ALLTHETHINGS_PROJECT_PATH`
         environment variables to refer to the project name and path.}

    """

    def handle(self):  # noqa: WPS110
        """Handle the command."""
        groups = set(self.option("group") or {})
        cmd = self.argument("cmd")

        execution_results = []
        for project, _ in self.list_projects(groups):
            execution_result = self._run_for_project(project, cmd)
            execution_results.append(execution_result)

        self.render_table(
            headers=[],
            rows=[[r.icon, r.name, r.comment] for r in execution_results],
            style="compact",
        )

    def _run_for_project(self, key, cmd) -> Result:
        path = self.root / key
        env = {
            **os.environ,
            **{f"{ENV_PREFIX}PROJECT_NAME": key, f"{ENV_PREFIX}PROJECT_PATH": path},
        }
        cwd = path if path.exists() else self.root
        execution_result = Result(key)

        try:
            with execution_result:
                res = subprocess.run(
                    cmd,
                    cwd=cwd,
                    shell=True,  # noqa: S602
                    check=True,
                    capture_output=True,
                    env=env,
                )
        except subprocess.CalledProcessError as error:
            self._print_result(key, error.output, error.stderr)
        else:
            self._print_result(key, res.stdout, res.stderr)

        return execution_result

    def _print_result(self, key: str, out: bytes, err: bytes):
        key = f" {key} "
        self.line(OUT_TEMPLATE.format(key=key, out=out.decode(), err=err.decode()))
