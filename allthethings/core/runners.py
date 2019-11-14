"""Support for per-project commands run."""
import subprocess  # noqa: S404
from dataclasses import dataclass

from .base import BaseCommand

__all__ = ["Result", "Execute"]

RESULTS_TABLE_STYLE = "compact"


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
                out = error.output
                err = error.stderr
            else:
                out = res.stdout
                err = res.stderr

            print_key = f" { key } "
            self.line(
                f"{ print_key :=^70}\n{ out.decode() }\n{ '='*70 }\n{ err.decode() }\n"
            )
            execution_results.append(execution_result)

        self.render_table(
            headers=[],
            rows=[[r.icon, r.name, r.comment] for r in execution_results],
            style=RESULTS_TABLE_STYLE,
        )
