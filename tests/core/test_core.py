from textwrap import dedent


def execute(command, *args, **kwargs):
    result = command.execute(*args, **kwargs)
    assert result == 0, command.io.fetch_error()


def test_list_empty(list_):
    execute(list_)
    assert list_.io.fetch_output() == ""


def test_list_empty_verbose(list_):
    execute(list_, verbosity=1)
    assert list_.io.fetch_output() == ""


def test_add_and_list(list_, add_):
    execute(add_, "project1")
    execute(list_)
    assert list_.io.fetch_output() == "project1\n"


def test_add_and_list_verbose(list_, add_):
    execute(add_, "project1")
    execute(list_, verbosity=1)
    assert list_.io.fetch_output() == dedent(
        """\
        +----------+--------+
        | Project  | Groups |
        +----------+--------+
        | project1 |        |
        +----------+--------+
        """
    )


def test_add_to_group(list_, add_):
    execute(add_, "project1 -g group1")
    execute(list_)
    assert list_.io.fetch_output() == "project1\n"


def test_add_to_group_verbose(list_, add_):
    execute(add_, "project1 -g group1")
    execute(list_, verbosity=1)
    assert list_.io.fetch_output() == dedent(
        """\
        +----------+--------+
        | Project  | Groups |
        +----------+--------+
        | project1 | group1 |
        +----------+--------+
        """
    )


def test_append_to_group_twice(list_, add_):
    execute(add_, "project1")
    execute(add_, "project1 -g group1")
    execute(add_, "project1 -g group1")
    execute(list_, verbosity=1)
    assert list_.io.fetch_output() == dedent(
        """\
        +----------+--------+
        | Project  | Groups |
        +----------+--------+
        | project1 | group1 |
        +----------+--------+
        """
    )


def test_append_to_groups_sequentially(list_, add_):
    execute(add_, "project1")
    execute(add_, "project1 -g group1")
    execute(add_, "project1 -g group0")
    execute(list_, verbosity=1)
    assert list_.io.fetch_output() == dedent(
        """\
        +----------+----------------+
        | Project  | Groups         |
        +----------+----------------+
        | project1 | group0, group1 |
        +----------+----------------+
        """
    )


def test_append_to_groups_simultaneously(list_, add_):
    execute(add_, "project1")
    execute(add_, "project1 -g group1 -g group0")
    execute(list_, verbosity=1)
    assert list_.io.fetch_output() == dedent(
        """\
        +----------+----------------+
        | Project  | Groups         |
        +----------+----------------+
        | project1 | group0, group1 |
        +----------+----------------+
        """
    )


def test_append_to_groups_simultaneously_v2(list_, add_):
    execute(add_, "project1 -g group1 -g group0")
    execute(list_, verbosity=1)
    assert list_.io.fetch_output() == dedent(
        """\
        +----------+----------------+
        | Project  | Groups         |
        +----------+----------------+
        | project1 | group0, group1 |
        +----------+----------------+
        """
    )


def test_remove_from_group(list_, add_, del_):
    execute(add_, "project1 -g group1 -g group0")
    execute(del_, "project1 -g group1")
    execute(list_, verbosity=1)
    assert list_.io.fetch_output() == dedent(
        """\
        +----------+--------+
        | Project  | Groups |
        +----------+--------+
        | project1 | group0 |
        +----------+--------+
        """
    )


def test_remove_from_all_groups(list_, add_, del_):
    execute(add_, "project1 -g group1 -g group0")
    execute(del_, "project1 -g group1 -g group0")
    execute(list_, verbosity=1)
    assert list_.io.fetch_output() == dedent(
        """\
        +----------+--------+
        | Project  | Groups |
        +----------+--------+
        | project1 |        |
        +----------+--------+
        """
    )


def test_remove_from_missing_group(list_, add_, del_):
    execute(add_, "project1 -g group1 -g group0")
    execute(del_, "project1 -g group2")

    execute(list_, verbosity=1)
    assert list_.io.fetch_output() == dedent(
        """\
        +----------+----------------+
        | Project  | Groups         |
        +----------+----------------+
        | project1 | group0, group1 |
        +----------+----------------+
        """
    )


def test_remove_from_registry(list_, add_, del_):
    execute(add_, "project1 -g group1 -g group0")
    execute(del_, "project1")

    execute(list_, verbosity=1)
    assert list_.io.fetch_output() == ""
