import os
import subprocess

from dataclasses import dataclass

from .base import BaseCommand


@dataclass
class Result:
    name: str
    icon: str = "✅"
    comment: str = "Ok"

    def set_error(self, text):
        self.icon = "⛔"
        self.comment = text


class Execute(BaseCommand):
    """
    Execute arbitrary shell command for each repo.

    exec
        {--g|group=?* : Run only for the projects of specific group.}
        {cmd* : The command to run.}

    """

    def handle(self):
        groups = set(self.option("group") or {})
        cmd = self.argument("cmd")

        results = []
        for key, conf in self.list_projects(groups):
            path = self.root / key
            cwd = path if path.exists() else self.root
            result = Result(key)

            try:
                res = subprocess.run(
                    " ".join(cmd), cwd=cwd, shell=True, check=True, capture_output=True
                )
            except subprocess.CalledProcessError as error:
                resp_raw = error.stderr if error.stderr else error.output
                result.set_error(resp_raw.decode())
                out = error.output
                err = error.stderr
            else:
                out = res.stdout
                err = res.stderr

            print_key = f" { key } "
            print(
                f"{ print_key :=^70}\n{ out.decode() }\n{ '='*70 }\n{ err.decode() }\n"
            )
            results.append(result)

        self.render_table(
            headers=["", "", ""],
            rows=[[r.icon, r.name, r.comment] for r in results],
            style="compact",
        )
