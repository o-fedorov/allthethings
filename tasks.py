"""Management tasks."""
from typing import List

from invoke import Result, UnexpectedExit, task


class _CollectFailures:
    def __init__(self, ctx):
        self._failed: List[Result] = []
        self._ctx = ctx

    def run(self, command: str, **kwargs):
        kwargs.setdefault("warn", True)
        cmd_result: Result = self._ctx.run(command, **kwargs)
        if cmd_result.ok:
            self._ctx.run("echo Ok")
        else:
            self._failed.append(cmd_result)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._failed:
            raise UnexpectedExit(self._failed[0])


@task
def test(ctx):
    """Run tests."""
    ctx.run("poetry run pytest --cov -vv .")


@task
def check(ctx):
    """Run static checks."""
    with _CollectFailures(ctx) as new_ctx:
        print("Checking Black formatting.")
        new_ctx.run("poetry run black . --check")

        print("Checking the style.")
        new_ctx.run("poetry run flake8")

        print("Checking type safety.")
        new_ctx.run("poetry run mypy .")

        print("Checking the libraries.")
        new_ctx.run("poetry run safety check")


@task
def fmt(ctx):
    """Apply automatic code formatting."""
    with _CollectFailures(ctx) as new_ctx:
        new_ctx.run("poetry run isort -rc .")
        new_ctx.run("poetry run black .")
