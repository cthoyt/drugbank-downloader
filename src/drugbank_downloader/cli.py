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
