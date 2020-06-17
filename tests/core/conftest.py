"""Fixtures and helpers used by tests."""
import os
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from cleo import Application, CommandTester

from allthethings.core import AddProject, Execute, ListProjects, RemoveProject


def execute(command: CommandTester, *args, **kwargs):
    """Shorthand function to execute a command and check it's return code."""
    res = command.execute(*args, **kwargs)
    assert res == 0, command.io.fetch_error()


@pytest.fixture
def tempdir():
    """Temporary directory fixture."""
    with TemporaryDirectory(dir=os.getcwd()) as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def application(tempdir: Path):
    """Commandline application fixture."""
    app = Application()
    for cmd_class in (ListProjects, AddProject, RemoveProject, Execute):
        command = cmd_class(config_file=tempdir / "config.toml")
        app.add(command)

    return app


@pytest.fixture
def list_cmd(application):
    """`allthethings list` command fixture."""
    return CommandTester(application.find("list"))


@pytest.fixture
def add_cmd(application):
    """`allthethings add` command fixture."""
    return CommandTester(application.find("add"))


@pytest.fixture
def del_cmd(application):
    """`allthethings del` command fixture."""
    return CommandTester(application.find("del"))


@pytest.fixture
def exec_cmd(application):
    """`allthethings exec` command fixture."""
    return CommandTester(application.find("exec"))
