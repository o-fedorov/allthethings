"""Management tasks."""
from typing import List

from invoke import Result, UnexpectedExit, task


class _CollectFailures:
    def __init__(self, ctx):
        self._failed: List[Result] = []
        self._ctx = ctx

    def run(self, command: str, **kwargs):
        kwargs.setdefault("warn", True)
        result: Result = self._ctx.run(command, **kwargs)
        if result.ok:
            self._ctx.run("echo Ok")
        else:
            self._failed.append(result)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for result in self._failed:
            raise UnexpectedExit(result)


@task
def test(ctx):
    """Run tests."""
    ctx.run("poetry run pytest --cov .")


@task
def check(ctx):
    """Run static checks."""
    with _CollectFailures(ctx) as new_ctx:
        new_ctx.run("poetry run black . --check")
        new_ctx.run("poetry run flake8")
        new_ctx.run("poetry run safety check")


@task
def fmt(ctx):
    """Apply automatic code formatting."""
    with _CollectFailures(ctx) as new_ctx:
        new_ctx.run("poetry run isort -rc .")
        new_ctx.run("poetry run black .")
