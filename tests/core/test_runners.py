"""Tests of the core projects management."""
from pathlib import Path
from textwrap import dedent

from .conftest import execute


def test_empty(exec_cmd):
    execute(exec_cmd, "-- echo 1")
    assert exec_cmd.io.fetch_output() == ""


def test_smoke(exec_cmd, add_cmd):
    execute(add_cmd, "project1")
    execute(exec_cmd, "-- echo 1")
    assert exec_cmd.io.fetch_output() == dedent(
        """\
        ============================== project1 ==============================
        1

        ======================================================================


        ✅ project1 Ok
        """
    )


def test_envvars(exec_cmd, add_cmd):
    execute(add_cmd, "project1")
    execute(
        exec_cmd, '-- echo "Name: $ALLTHETHINGS_PROJECT_NAME, path: $ALLTHETHINGS_PROJECT_PATH"'
    )
    assert exec_cmd.io.fetch_output() == dedent(
        f"""\
        ============================== project1 ==============================
        Name: project1, path: { Path().joinpath("project1").resolve() }

        ======================================================================


        ✅ project1 Ok
        """
    )


def test_failure(exec_cmd, add_cmd):
    execute(add_cmd, "project1")
    execute(exec_cmd, "-- >&2 echo Failure; exit 1")
    assert exec_cmd.io.fetch_output() == dedent(
        """\
        ============================== project1 ==============================

        ======================================================================
        Failure


        ⛔ project1 Failure
        """
    )
