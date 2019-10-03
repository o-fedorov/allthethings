from pathlib import Path

from cleo import Command

from .base import get_config

_CONFIG = Path("./.allthethings.toml")


class ListRepos(Command):
    """
    List available repositories.

    list

    """

    def handle(self):
        self.line("The repos:")
        for key in get_config()["repos"]:
            self.line(key)
