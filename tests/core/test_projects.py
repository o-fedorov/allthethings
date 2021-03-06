"""Tests of the core projects management."""
from textwrap import dedent

from .conftest import execute


def test_list_empty(list_cmd):
    execute(list_cmd)
    assert list_cmd.io.fetch_output() == ""


def test_list_empty_verbose(list_cmd):
    execute(list_cmd, verbosity=1)
    assert list_cmd.io.fetch_output() == ""


def test_add_and_list(list_cmd, add_cmd):
    execute(add_cmd, "project1")
    execute(list_cmd)
    assert list_cmd.io.fetch_output() == "project1\n"


def test_add_and_list_verbose(list_cmd, add_cmd):
    execute(add_cmd, "project1")
    execute(list_cmd, verbosity=1)
    assert list_cmd.io.fetch_output() == dedent(
        """\
        +----------+--------+
        | Project  | Groups |
        +----------+--------+
        | project1 |        |
        +----------+--------+
        """
    )


def test_add_to_group(list_cmd, add_cmd):
    execute(add_cmd, "project1 -g group1")
    execute(list_cmd)
    assert list_cmd.io.fetch_output() == "project1\n"


def test_add_to_group_verbose(list_cmd, add_cmd):
    execute(add_cmd, "project1 -g group1")
    execute(list_cmd, verbosity=1)
    assert list_cmd.io.fetch_output() == dedent(
        """\
        +----------+--------+
        | Project  | Groups |
        +----------+--------+
        | project1 | group1 |
        +----------+--------+
        """
    )


def test_append_to_group_twice(list_cmd, add_cmd):
    execute(add_cmd, "project1")
    execute(add_cmd, "project1 -g group1")
    execute(add_cmd, "project1 -g group1")
    execute(list_cmd, verbosity=1)
    assert list_cmd.io.fetch_output() == dedent(
        """\
        +----------+--------+
        | Project  | Groups |
        +----------+--------+
        | project1 | group1 |
        +----------+--------+
        """
    )


def test_append_to_groups_sequentially(list_cmd, add_cmd):
    execute(add_cmd, "project1")
    execute(add_cmd, "project1 -g group1")
    execute(add_cmd, "project1 -g group0")
    execute(list_cmd, verbosity=1)
    assert list_cmd.io.fetch_output() == dedent(
        """\
        +----------+----------------+
        | Project  | Groups         |
        +----------+----------------+
        | project1 | group0, group1 |
        +----------+----------------+
        """
    )


def test_append_to_groups_simultaneously(list_cmd, add_cmd):
    execute(add_cmd, "project1")
    execute(add_cmd, "project1 -g group1 -g group0")
    execute(list_cmd, verbosity=1)
    assert list_cmd.io.fetch_output() == dedent(
        """\
        +----------+----------------+
        | Project  | Groups         |
        +----------+----------------+
        | project1 | group0, group1 |
        +----------+----------------+
        """
    )


def test_append_to_groups_simultaneously_v2(list_cmd, add_cmd):
    execute(add_cmd, "project1 -g group1 -g group0")
    execute(list_cmd, verbosity=1)
    assert list_cmd.io.fetch_output() == dedent(
        """\
        +----------+----------------+
        | Project  | Groups         |
        +----------+----------------+
        | project1 | group0, group1 |
        +----------+----------------+
        """
    )


def test_remove_from_group(list_cmd, add_cmd, del_cmd):
    execute(add_cmd, "project1 -g group1 -g group0")
    execute(del_cmd, "project1 -g group1")
    execute(list_cmd, verbosity=1)
    assert list_cmd.io.fetch_output() == dedent(
        """\
        +----------+--------+
        | Project  | Groups |
        +----------+--------+
        | project1 | group0 |
        +----------+--------+
        """
    )


def test_remove_from_all_groups(list_cmd, add_cmd, del_cmd):
    execute(add_cmd, "project1 -g group1 -g group0")
    execute(del_cmd, "project1 -g group1 -g group0")
    execute(list_cmd, verbosity=1)
    assert list_cmd.io.fetch_output() == dedent(
        """\
        +----------+--------+
        | Project  | Groups |
        +----------+--------+
        | project1 |        |
        +----------+--------+
        """
    )


def test_remove_from_missing_group(list_cmd, add_cmd, del_cmd):
    execute(add_cmd, "project1 -g group1 -g group0")
    execute(del_cmd, "project1 -g group2")

    execute(list_cmd, verbosity=1)
    assert list_cmd.io.fetch_output() == dedent(
        """\
        +----------+----------------+
        | Project  | Groups         |
        +----------+----------------+
        | project1 | group0, group1 |
        +----------+----------------+
        """
    )


def test_remove_from_registry(list_cmd, add_cmd, del_cmd):
    execute(add_cmd, "project1 -g group1 -g group0")
    execute(del_cmd, "project1")

    execute(list_cmd, verbosity=1)
    assert list_cmd.io.fetch_output() == ""
