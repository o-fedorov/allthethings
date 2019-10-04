import os
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from cleo import Application, CommandTester

from allthethings.core import ListProjects, AddProject, RemoveProject


@pytest.fixture
def tempdir() -> Path:
    with TemporaryDirectory(dir=os.getcwd()) as tempdir:
        yield Path(tempdir)


@pytest.fixture
def application(tempdir: Path):
    application = Application()
    for cls in [ListProjects, AddProject, RemoveProject]:
        command = cls()
        command.config_file = tempdir / "config.toml"
        application.add(command)

    return application


@pytest.fixture
def list_(application):
    return CommandTester(application.find('list'))


@pytest.fixture
def add_(application):
    return CommandTester(application.find('add'))


@pytest.fixture
def del_(application):
    return CommandTester(application.find('del'))
