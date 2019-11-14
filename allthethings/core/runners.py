"""Support for per-project commands run."""
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


class Execute(BaseCommand):
    """
    Execute arbitrary shell command for each repo.

    exec
        {--g|group=?* : Run only for the projects of specific group.}
        {cmd* : The command to run.}

    """

    def handle(self):  # noqa: WPS110
        """Handle the command."""
        groups = set(self.option("group") or {})
        cmd = self.argument("cmd")

        execution_results = []
        for key, _ in self.list_projects(groups):
            path = self.root / key
            cwd = path if path.exists() else self.root
            execution_result = Result(key)

            try:
                res = subprocess.run(
                    " ".join(cmd),
                    cwd=cwd,
                    shell=True,  # noqa: S602
                    check=True,
                    capture_output=True,
                )
            except subprocess.CalledProcessError as error:
                resp_raw = error.stderr if error.stderr else error.output
                execution_result.set_error(resp_raw.decode())
                self._print_result(key, error.output, error.stderr)
            else:
                self._print_result(key, res.stdout, res.stderr)

            execution_results.append(execution_result)

        self.render_table(
            headers=[],
            rows=[[r.icon, r.name, r.comment] for r in execution_results],
            style="compact",
        )

    def _print_result(self, key: str, out: bytes, err: bytes):
        self.line(
            OUT_TEMPLATE.format(key=f" {key} ", out=out.decode(), err=err.decode())
        )
