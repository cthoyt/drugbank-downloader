"""Command line interface for :mod:`drugbank_downloader`.

Why does this file exist, and why not put this in ``__main__``?
You might be tempted to import things from ``__main__``
later, but that will cause problems--the code will get executed twice:

- When you run ``python3 -m drugbank_downloader`` python will
  execute``__main__.py`` as a script. That means there won't be any
  ``drugbank_downloader.__main__`` in ``sys.modules``.
- When you import __main__ it will get executed again (as a module) because
  there's no ``drugbank_downloader.__main__`` in ``sys.modules``.

.. seealso:: https://click.palletsprojects.com/en/8.1.x/setuptools/#setuptools-integration
"""

import click
from more_click import verbose_option

from .api import download_drugbank


@click.command()
@click.option("--version")
@click.option("--username")
@click.option("--password")
@click.option("-f", "--force", is_flag=True)
@verbose_option  # type:ignore[misc]
def main(version: str, username: str, password: str, force: bool) -> None:
    """Download DrugBank."""
    path = download_drugbank(
        version=version,
        username=username,
        password=password,
        force=force,
    )
    click.echo(path.as_posix())


if __name__ == "__main__":
    main()
