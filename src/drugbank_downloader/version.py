"""Version information for :mod:`drugbank_downloader`.

Run with ``python -m drugbank_downloader.version``
"""

import os
from subprocess import CalledProcessError, check_output

__all__ = [
    "VERSION",
    "get_version",
    "get_git_hash",
]

VERSION = "0.2.0-dev"


def get_git_hash() -> str:
    """Get the :mod:`drugbank_downloader` git hash."""
    with open(os.devnull, "w") as devnull:
        try:
            ret = check_output(
                ["git", "rev-parse", "HEAD"],
                cwd=os.path.dirname(__file__),
                stderr=devnull,
            )
        except CalledProcessError:
            return "UNHASHED"
        else:
            return ret.strip().decode("utf-8")[:8]


def get_version(with_git_hash: bool = False) -> str:
    """Get the :mod:`drugbank_downloader` version string, including a git hash."""
    return f"{VERSION}-{get_git_hash()}" if with_git_hash else VERSION


if __name__ == "__main__":
    print(get_version(with_git_hash=True))  # noqa:T201
