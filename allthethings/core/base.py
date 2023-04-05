"""Base application functionality."""
from pathlib import Path
from typing import Dict, Iterable, Iterator, Optional, Tuple

import attr
import toml
from cleo.commands.command import Command

__all__ = ["BaseCommand"]


CORE_NAMESPACE = "core"
PROJECTS_KEY = "projects"
GROUPS_KEY = "groups"


@attr.s(auto_attribs=True)
class Config:
    """Command with config-aware methods."""

    _namespace: Optional[str]
    _config_file: Path

    def get(self, namespace: Optional[str] = None):
        """Get config for given or default namespace."""
        namespace = self._real_namespace(namespace)
        return self._load_config().get(namespace, {})

    def set(self, config: Dict, namespace: Optional[str] = None):  # noqa: WPS125 builtin shadowing
        """Set config for given or default namespace."""
        namespace = self._real_namespace(namespace)
        full_config = self._load_config()
        full_config[namespace] = config
        self._dump_config(full_config)

    def _real_namespace(self, namespace):
        if namespace is None:
            namespace = self._namespace

        if namespace is None:
            raise ValueError(
                "No default namespace is defined for the command, and no one provided explicitly."
            )
        return namespace

    def _load_config(self):
        try:
            return toml.load(self._config_file)
        except FileNotFoundError:
            return {}

    def _dump_config(self, config: Dict):
        with self._config_file.open("w") as out_file:
            return toml.dump(config, out_file)


class BaseCommand(Command):
    """Command with config-aware methods."""

    namespace: Optional[str] = None

    def __init__(self, config_file=".allthethings.toml"):
        super().__init__()
        self.cmd_config = Config(namespace=self.namespace, config_file=Path(config_file))
        self.root = Path(".").resolve()

    def list_projects(self, groups: Optional[Iterable] = None) -> Iterator[Tuple[str, Dict]]:
        """Generate project names and their config for given or all groups."""
        groups = set(groups) if groups else set()

        for key, conf in self._get_projects().items():
            cur_groups = conf.get(GROUPS_KEY, [])
            if not groups or not groups.isdisjoint(cur_groups):
                yield (key, conf)

    def _get_projects(self) -> Dict[str, Dict]:
        return self.cmd_config.get(CORE_NAMESPACE).get(PROJECTS_KEY, {})
