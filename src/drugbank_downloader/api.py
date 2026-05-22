"""Implementation of :mod:`drugbank_downloader`."""

import contextlib
import logging
import xml.etree.ElementTree
import zipfile
from collections.abc import Generator, Sequence
from operator import itemgetter
from pathlib import Path
from textwrap import dedent
from typing import IO, Optional, Union, cast

import pystow.utils
import requests
from lxml import etree as ElementTree  # noqa: N812
from pystow import ensure, get_config

from .version import get_version

__all__ = [
    "download_drugbank",
    "get_drugbank_root",
    "open_drugbank",
    "parse_drugbank",
]

logger = logging.getLogger(__name__)

VERSION_URL = "https://go.drugbank.com/releases.json"

USER_AGENT = f"drugbank-downloader v{get_version()}"


def _get_version(auth: tuple[str, str]) -> str:
    """Get the latest DrugBank version.

    Based on the ``Querying Downloads`` section of
    https://go.drugbank.com/releases/help, this should work,
    but instead an anti-scraping mechanism gets returned.
    """
    res = requests.get(VERSION_URL, timeout=5, auth=auth, headers={"User-Agent": USER_AGENT})
    res.raise_for_status()
    latest = max(res.json(), key=itemgetter("released_on"))
    return cast(str, latest["version"])


def get_drugbank_root(
    *,
    username: Optional[str] = None,
    password: Optional[str] = None,
    version: Optional[str] = None,
    prefix: Optional[Sequence[str]] = None,
) -> "xml.etree.ElementTree.Element[str]":
    """Download, open, and parse the XML of a given version of DrugBank then get its root."""
    element_tree = parse_drugbank(
        username=username, password=password, version=version, prefix=prefix
    )
    rv = element_tree.getroot()
    if rv is None:
        raise ValueError
    return rv


def parse_drugbank(
    *,
    username: Optional[str] = None,
    password: Optional[str] = None,
    version: Optional[str] = None,
    prefix: Optional[Sequence[str]] = None,
) -> "xml.etree.ElementTree.ElementTree":
    """Download, open, and parse the XML of a given version of DrugBank."""
    with open_drugbank(
        version=version, username=username, password=password, prefix=prefix
    ) as file:
        logger.info("loading DrugBank XML")
        tree = ElementTree.parse(file)
        logger.info("done parsing DrugBank XML")
    return tree  # type:ignore


@contextlib.contextmanager
def open_drugbank(
    *,
    username: Optional[str] = None,
    password: Optional[str] = None,
    version: Optional[str] = None,
    prefix: Optional[Sequence[str]] = None,
) -> Generator[IO[bytes], None, None]:
    """Download the given version of DrugBank and open it up with :mod:`zipfile`."""
    path = download_drugbank(version=version, username=username, password=password, prefix=prefix)
    with zipfile.ZipFile(path) as zip_file:
        with zip_file.open("full database.xml") as file:
            yield file


def _ensure_auth(username: str | None, password: str | None) -> tuple[str, str]:
    username = get_config("drugbank", "username", passthrough=username, raise_on_missing=True)
    password = get_config("drugbank", "password", passthrough=password, raise_on_missing=True)
    return username, password


def download_drugbank(
    *,
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
        The DrugBank version. If not passed, look up the most recent version.
    :param prefix:
        The prefix and subkeys passed to :func:`pystow.ensure` to specify
        a non-default location to download the data to.
    :param force:
        Should the data be re-downloaded, even if it exists?
    :returns: The path to the local DrugBank file after it's been downloaded

    :raises RuntimeError: If the credentials are invalid or not yet approved
    """
    auth = _ensure_auth(username, password)

    if version is None:
        raise RuntimeError(
            "DrugBank has currently put anti-scraping mechanisms in place that do not allow for "
            "the automated determination of the current version. Please manually pass the version "
            "of DrugBank you would like to use."
        )

    url = (
        f"https://go.drugbank.com/releases/{version.replace('.', '-')}/downloads/all-full-database"
    )

    if prefix is None:
        prefix = ["drugbank"]
    elif isinstance(prefix, str):
        prefix = [prefix]

    try:
        path = ensure(
            *prefix,
            version,
            url=url,
            name="full database.xml.zip",
            download_kwargs={
                "backend": "requests",
                "stream": True,
                "auth": auth,
            },
            force=force,
        )
    except pystow.utils.DownloadError:
        raise RuntimeError(_get_failure_message(version)) from None

    # the drugbank download file should be over 200 megabytes.
    # if you don't have valid credentials, then you will get an
    # HTML page (i.e., https://go.drugbank.com/releases/latest)
    # that is only a few hundred kilobytes
    size = path.stat().st_size
    if size < 5 * 1024 * 1024:
        path.unlink()
        raise RuntimeError(_get_failure_message(version))

    return path


def _get_failure_message(version: str) -> str:
    return dedent(
        f"""

        Download was not possible due to insufficient permissions.
        This can be for several reasons:

        1. Your credentials are invalid (e.g., your credentials don't
           refer to an actual account, or you made a typo in the username
           or password)

        2. Your credentials have not yet been approved for downloads

           Even after signing up for a DrugBank account and getting
           a valid username/password combination, DrugBank still has
           to manually approve your account to make an academic
           download of its data.

           You can tell if your credentials have not been approved by
           visiting https://go.drugbank.com/releases/{version}#full.
           If the download button says "Ineligible for download", then
           you might need to contact DrugBank to get approved, e.g.,
           via https://go.drugbank.com/contact.

        3. Your credentials are academic. As of 2026, DrugBank has temporarily
           halted distributing their data to academics. See the message at
           https://go.drugbank.com/releases/latest

        Note, `drugbank-downloader` is a third party, open source software
        package that is not affiliated with DrugBank.
        """
    )
