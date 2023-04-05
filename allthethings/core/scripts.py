"""Scripts registry manipulation."""
from .base import BaseCommand

__all__ = ["ListScripts", "AddScript", "RemoveScript"]


class _CoreCommand(BaseCommand):
    """A command with explicitly defined config namespace."""

    namespace = "scripts"


class ListScripts(_CoreCommand):
    """
    List available scripts.  Increase verbosity to see additional info.
    """

    def handle(self):  # noqa: WPS110
        """Handle the command."""
        scripts = self.get()

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
        projects = dict(self.list_projects())
        names = self.argument("name")
        groups = self.option("group") or []

        for name in names:
            projects.setdefault(name, {})

            cur_groups = projects[name].get(GROUPS_KEY, [])
            cur_groups.extend(groups)

            projects[name][GROUPS_KEY] = sorted(set(cur_groups))

        self.cmd_config.set({PROJECTS_KEY: projects})


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
        projects = dict(self.list_projects())
        names = self.argument("name")
        groups = self.option("group") or []

        for name in names:
            if not groups:
                projects.pop(name)
                continue

            projects.setdefault(name, {})

            cur_groups = projects[name].get(GROUPS_KEY, [])
            projects[name][GROUPS_KEY] = [g for g in cur_groups if g not in groups]

        self.cmd_config.set({PROJECTS_KEY: projects})
