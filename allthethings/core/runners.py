import os
import subprocess

from .base import BaseCommand


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

        for key, conf in self.list_projects(groups):
            path = self.root / key
            if path.exists():
                os.chdir(path)
            subprocess.run(cmd, shell=True)
