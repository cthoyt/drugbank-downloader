# -*- coding: utf-8 -*-

"""Implementation of :mod:`drugbank_downloader`."""

import contextlib
import logging
import zipfile
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Sequence, Union

from pystow import ensure, get_config

try:
    from lxml import etree as ElementTree  # noqa:S410,N812
except ImportError:
    from xml.etree import ElementTree  # noqa:S405

if TYPE_CHECKING:
    import xml.etree.ElementTree  # noqa:S405

__all__ = [
    "get_drugbank_root",
    "parse_drugbank",
    "open_drugbank",
    "download_drugbank",
]

logger = logging.getLogger(__name__)


def get_drugbank_root(
    username: Optional[str] = None,
    password: Optional[str] = None,
    version: Optional[str] = None,
    prefix: Optional[Sequence[str]] = None,
) -> "xml.etree.ElementTree.Element":
    """Download, open, and parse the given version of DrugBank with :class:`xml.etree.ElementTree` then get its root."""
    element_tree = parse_drugbank(
        username=username, password=password, version=version, prefix=prefix
    )
    return element_tree.getroot()


def parse_drugbank(
    username: Optional[str] = None,
    password: Optional[str] = None,
    version: Optional[str] = None,
    prefix: Optional[Sequence[str]] = None,
) -> "xml.etree.ElementTree.ElementTree":
    """Download, open, and parse the given version of DrugBank with :class:`xml.etree.ElementTree`."""
    with open_drugbank(
        version=version, username=username, password=password, prefix=prefix
    ) as file:
        logger.info("loading DrugBank XML")
        tree = ElementTree.parse(file)  # noqa:S314
        logger.info("done parsing DrugBank XML")
    return tree


@contextlib.contextmanager
def open_drugbank(
    username: Optional[str] = None,
    password: Optional[str] = None,
    version: Optional[str] = None,
    prefix: Optional[Sequence[str]] = None,
):
    """Download the given version of DrugBank and open it up with :mod:`zipfile`."""
    path = download_drugbank(version=version, username=username, password=password, prefix=prefix)
    with zipfile.ZipFile(path) as zip_file:
        with zip_file.open("full database.xml") as file:
            yield file


def download_drugbank(
    username: Optional[str] = None,
    password: Optional[str] = None,
    version: Optional[str] = None,
    prefix: Union[None, str, Sequence[str]] = None,
    force: bool = False,
) -> Path:
    """Download the given version of DrugBank.

    :param username:
        The DrugBank username. If not passed, looks up in the environment
        ``DRUGBANK_USERNAME``. If not found, raises a ValueError.
    :param password:
        The DrugBank password. If not passed, looks up in the environment
        ``DRUGBANK_PASSWORD``. If not found, raises a ValueError.
    :param version:
        The DrugBank version. If not passed, uses :mod:`bioversions` to
        look up the most recent version.
    :param prefix:
        The prefix and subkeys passed to :func:`pystow.ensure` to specify
        a non-default location to download the data to.
    :param force:
        Should the data be re-downloaded, even if it exists?
    :returns: The path to the local DrugBank file after it's been downloaded

    :raises ImportError: If no version is specified and :mod:`bioversions`
        is not installed
    """
    if version is None:
        try:
            import bioversions
        except ImportError:
            raise ImportError(
                "must first `pip install bioversions` to get latest DrugBank version automatically"
            )
        else:
            version = bioversions.get_version("drugbank")

    url = (
        f'https://go.drugbank.com/releases/{version.replace(".", "-")}/downloads/all-full-database'
    )

    if prefix is None:
        prefix = ["drugbank"]
    elif isinstance(prefix, str):
        prefix = [prefix]

    username = get_config("drugbank", "username", passthrough=username, raise_on_missing=True)
    password = get_config("drugbank", "password", passthrough=password, raise_on_missing=True)

    return ensure(
        *prefix,
        version,
        url=url,
        name="full database.xml.zip",
        download_kwargs=dict(
            backend="requests",
            stream=True,
            auth=(username, password),
        ),
        force=force,
    )
