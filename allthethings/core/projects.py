"""Projects registry manipulation."""
from typing import List, Tuple

from .base import CORE_NAMESPACE, GROUPS_KEY, PROJECTS_KEY, BaseCommand

__all__ = ["ListProjects", "AddProject", "RemoveProject"]


class _CoreCommand(BaseCommand):
    """A command with explicitly defined config namespace."""

    namespace = CORE_NAMESPACE


class ListProjects(_CoreCommand):
    """
    List available projects.  Increase verbosity to see additional info.

    list
        {--g|group=?* : List only the projects of specific group.}

    """

    def handle(self):  # noqa: WPS110
        """Handle the command."""
        groups = set(self.option("group") or {})

        output: List[Tuple[str, str]] = []
        for key, conf in self.list_projects(groups):
            cur_groups = conf.get(GROUPS_KEY, [])
            output.append((key, ", ".join(cur_groups)))

        if self.io.is_verbose():
            self.render_table(["Project", "Groups"], output)
        else:
            for row in output:
                self.line(row[0])


class AddProject(_CoreCommand):
    """
    Add a project to a registry.

    add
        {name* : Project name(s).  If exist, should meet its directory name.}
        {--g|group=?* : Group to add a project to.
            If a project is already registered, just append it to groups.}
    """

    def handle(self):  # noqa: WPS110
        """Handle the command."""
        projects = self._get_projects()
        names = self.argument("name")
        groups = self.option("group") or []

        for name in names:
            project_conf = projects.setdefault(name, {})

            cur_groups = project_conf.get(GROUPS_KEY, [])
            cur_groups.extend(groups)

            project_conf[GROUPS_KEY] = sorted(set(cur_groups))

        self.set_config({PROJECTS_KEY: projects})


class RemoveProject(_CoreCommand):
    """
    Remove a project from a group or from a global registry.

    del
        {name* : Project name(s).}
        {--g|group=?* : Group to remove a project from.
            If not provided, completely remove a project from a registry.}
    """

    def handle(self):  # noqa: WPS110
        """Handle the command."""
        projects = self._get_projects()
        names = self.argument("name")
        groups = self.option("group") or []

        for name in names:
            if not groups:
                projects.pop(name)
                continue

            project_conf = projects.setdefault(name, {})

            cur_groups = project_conf.get(GROUPS_KEY, [])
            project_conf[GROUPS_KEY] = [g for g in cur_groups if g not in groups]

        self.set_config({PROJECTS_KEY: projects})
