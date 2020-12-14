import contextlib
import logging
import zipfile
from pathlib import Path
from typing import Optional, Sequence
from xml.etree import ElementTree

from pystow import ensure

__all__ = [
    'parse_drugbank',
    'open_drugbank',
    'download_drugbank',
]

logger = logging.getLogger(__name__)


def parse_drugbank(
    username: str,
    password: str,
    version: Optional[str] = None,
    prefix: Optional[Sequence[str]] = None,
) -> ElementTree.Element:
    """Download, open, and parse the given version of DrugBank with :class:`xml.etree.ElementTree`."""
    with open_drugbank(version=version, username=username, password=password, prefix=prefix) as file:
        logger.info('loading DrugBank XML')
        tree = ElementTree.parse(file)
        logger.info('done parsing DrugBank XML')
    return tree.getroot()


@contextlib.contextmanager
def open_drugbank(
    username: str,
    password: str,
    version: Optional[str] = None,
    prefix: Optional[Sequence[str]] = None,
):
    """Download the given version of DrugBank and open it up with :mod:`zipfile`."""
    path = download_drugbank(version=version, username=username, password=password, prefix=prefix)
    with zipfile.ZipFile(path) as zip_file:
        with zip_file.open('full database.xml') as file:
            yield file


def download_drugbank(
    username: str,
    password: str,
    version: Optional[str] = None,
    prefix: Optional[Sequence[str]] = None,
) -> Path:
    """Download the given version of DrugBank."""
    if version is None:
        try:
            import bioversions
        except ImportError:
            raise ImportError('must first `pip install bioversions` to get latest DrugBank version automatically')
        else:
            version = bioversions.get_version('drugbank')

    url = f'https://go.drugbank.com/releases/{version.replace(".", "-")}/downloads/all-full-database'

    if prefix is None:
        prefix = ['drugbank']

    return ensure(
        *prefix,
        version,
        url=url,
        name='full database.xml.zip',
        download_kwargs=dict(
            backend='requests',
            stream=True,
            auth=(username, password),
        ),
    )
