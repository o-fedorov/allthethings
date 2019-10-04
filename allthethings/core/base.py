from pathlib import Path
from typing import Optional, Dict, Type, Iterable, Iterator, Tuple

import toml
from cleo import Command

PROJECTS_KEY = "projects"
GROUPS_KEY = "groups"


class BaseCommand(Command):
    """Command with config-aware methods."""

    config_file = Path(".allthethings.toml")
    namespace = None

    def __init__(self):
        super().__init__()
        self.config_file = self.config_file.resolve()

    def subcommand(self, cls: Type[Command]):
        """A decorator to add a command class as a subcommand."""
        self.add_sub_command(cls())

    def get_config(self, namespace: Optional[str] = None):
        """Get config for given or default namespace."""
        namespace = self._real_namespace(namespace)
        return self._load_config().get(namespace, {})

    def set_config(self, data: Dict, namespace: Optional[str] = None):
        namespace = self._real_namespace(namespace)
        config = self._load_config()
        config[namespace] = data
        self._dump_config(config)

    def list_projects(self, groups: Optional[Iterable] = None) -> Iterator[Tuple[str, Dict]]:
        """Generate project names and their config for given or all groups."""
        for key, conf in self._get_projects().items():
            cur_groups = conf.get(GROUPS_KEY, [])
            if not groups or not groups.isdisjoint(cur_groups):
                yield (key, conf)

    def _real_namespace(self, namespace):
        if namespace is None:
            namespace = self.namespace

        if namespace is None:
            raise ValueError(
                "No default namespace is defined for the command, and no one provided explicitly."
            )
        return namespace

    def _load_config(self):
        try:
            return toml.load(self.config_file)
        except FileNotFoundError:
            return {}

    def _dump_config(self, data: Dict):
        with self.config_file.open("w") as file:
            return toml.dump(data, file)

    def _get_projects(self) -> Dict[str, Dict]:
        return self.get_config().get(PROJECTS_KEY, {})
