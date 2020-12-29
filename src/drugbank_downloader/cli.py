# -*- coding: utf-8 -*-

"""Command line interface for :mod:`drugbank_downloader`.

Why does this file exist, and why not put this in ``__main__``? You might be tempted to import things from ``__main__``
later, but that will cause problems--the code will get executed twice:

- When you run ``python3 -m drugbank_downloader`` python will execute``__main__.py`` as a script. That means there
  won't be any ``drugbank_downloader.__main__`` in ``sys.modules``.
- When you import __main__ it will get executed again (as a module) because
  there's no ``drugbank_downloader.__main__`` in ``sys.modules``.

.. seealso:: https://click.palletsprojects.com/en/7.x/setuptools/#setuptools-integration
"""

import click

from .api import download_drugbank, download_latest_drugbank


@click.command()
@click.option('--version')
@click.option('--username')
@click.option('--password')
def main(version: str, username: str, password: str):
    if version is not None:
        path = download_drugbank(version, username, password)
    else:
        path = download_latest_drugbank(username, password)
    click.echo(path.as_posix())


if __name__ == '__main__':
    main()
