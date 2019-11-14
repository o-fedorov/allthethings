"""Tests of the core projects management."""
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


def test_failure(exec_cmd, add_cmd):
    execute(add_cmd, "project1")
    execute(exec_cmd, "-- python -c '1/0'")
    assert exec_cmd.io.fetch_output() == dedent(
        """\
        ============================== project1 ==============================

        ======================================================================
        Traceback (most recent call last):
          File "<string>", line 1, in <module>
        ZeroDivisionError: division by zero


        ⛔ project1 Traceback (most recent call last):   File "<string>", line 1, in
                   <module> ZeroDivisionError: division by zero
        """
    )
