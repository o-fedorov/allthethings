"""Tests of the core projects management."""
import difflib
import re
from textwrap import dedent

import pytest

from .conftest import execute


def assert_re_match(actual, expected):
    expected = dedent(expected)

    if not re.match(expected, actual, flags=re.MULTILINE | re.DOTALL):
        report = "".join(
            difflib.ndiff(actual.splitlines(keepends=True), expected.splitlines(keepends=True))
        )
        pytest.fail(report)


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
    assert_re_match(
        exec_cmd.io.fetch_output(),
        """\
        ============================== project1 ==============================
        Name: project1, path: .*/allthethings/tests/project1

        ======================================================================


        ✅ project1 Ok
        """,
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
