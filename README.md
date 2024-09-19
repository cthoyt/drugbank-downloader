<!--
<p align="center">
  <img src="https://github.com/cthoyt/drugbank-downloader/raw/main/docs/source/logo.png" height="150">
</p>
-->

<h1 align="center">
  DrugBank Downloader
</h1>

<p align="center">
    <a href="https://github.com/cthoyt/drugbank-downloader/actions/workflows/tests.yml">
        <img alt="Tests" src="https://github.com/cthoyt/drugbank-downloader/actions/workflows/tests.yml/badge.svg" /></a>
    <a href="https://pypi.org/project/drugbank_downloader">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/drugbank_downloader" /></a>
    <a href="https://pypi.org/project/drugbank_downloader">
        <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/drugbank_downloader" /></a>
    <a href="https://github.com/cthoyt/drugbank-downloader/blob/main/LICENSE">
        <img alt="PyPI - License" src="https://img.shields.io/pypi/l/drugbank_downloader" /></a>
    <a href='https://drugbank_downloader.readthedocs.io/en/latest/?badge=latest'>
        <img src='https://readthedocs.org/projects/drugbank_downloader/badge/?version=latest' alt='Documentation Status' /></a>
    <a href="https://codecov.io/gh/cthoyt/drugbank-downloader/branch/main">
        <img src="https://codecov.io/gh/cthoyt/drugbank-downloader/branch/main/graph/badge.svg" alt="Codecov status" /></a>  
    <a href="https://github.com/cthoyt/cookiecutter-python-package">
        <img alt="Cookiecutter template from @cthoyt" src="https://img.shields.io/badge/Cookiecutter-snekpack-blue" /></a>
    <a href='https://github.com/psf/black'>
        <img src='https://img.shields.io/badge/code%20style-black-000000.svg' alt='Code style: black' /></a>
    <a href="https://github.com/cthoyt/drugbank-downloader/blob/main/.github/CODE_OF_CONDUCT.md">
        <img src="https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg" alt="Contributor Covenant"/></a>
    <a href="https://zenodo.org/doi/10.5281/zenodo.4321184">
        <img src="https://zenodo.org/badge/321374043.svg" alt="DOI">
    </a>
</p>

Don't worry about DrugBank licensing and distribution rules - just use ``drugbank_downloader`` to write code that knows
how to download it and use it automatically.

## Installation

```bash
$ pip install drugbank-downloader
```

## Download A Specific Version

```python
import os
from drugbank_downloader import download_drugbank

username = ...  # suggestion: load from environment with os.getenv('DRUGBANK_USERNAME')
password = ...

path = download_drugbank(version='5.1.7', username=username, password=password)

# This is where it gets downloaded: ~/.data/drugbank/5.1.7/full database.xml.zip
expected_path = os.path.join(os.path.expanduser('~'), '.data', 'drugbank', '5.1.7', 'full database.xml.zip')
assert expected_path == path.as_posix()
```

After it's been downloaded once, it's smart and doesn't need to download again. It gets stored
using [`pystow`](https://github.com/cthoyt/pystow) automatically in the `~/.data/drugbank`
directory.

## Automating Configuration of DrugBank Credentials

There are two ways to automatically set the username and password so you don't have to worry about getting it and
passing it around in your python code:

1. Set `DRUGBANK_USERNAME` and `DRUGBANK_PASSWORD` in the environment
2. Create `~/.config/drugbank.ini` and set in the `[drugbank]` section a `username` and `password` key.

```python
from drugbank_downloader import download_drugbank

# Same path as before
path = download_drugbank(version='5.1.7')
```

The `username` and `password` keyword arguments are available for all functions in this package, but will be omitted in
the tutorial for brevity.

## Download the Latest Version

First, you'll have to install [`bioversions`](https://github.com/cthoyt/bioversions)
with `pip install bioversions`, whose job it is to look up the latest version of many databases. Then, you can modify
the previous code slightly by omitting the `version` keyword argument:

```python
import os
from drugbank_downloader import download_drugbank

path = download_drugbank()

# This is where it gets downloaded: ~/.data/drugbank/5.1.7/full database.xml.zip based on the latest
# version, as of December 14th, 2020.
expected_path = os.path.join(os.path.expanduser('~'), '.data', 'drugbank', '5.1.7', 'full database.xml.zip')
assert expected_path == path.as_posix()
```

The `version` keyword argument is available for all functions in this package, but like the username and password will
be omitted for brevity.

## Don't Bother Unpacking - read `full database.xml.zip` Directly

DrugBank is a single XML (could be JSON in a better future) file inside a zip archive. Normally, people manually unzip
this folder then do something with the resulting file. Don't do this, it's not reproducible!
Instead, it can be opened as a file object in Python with the following code.

```python
import zipfile
from drugbank_downloader import download_drugbank

path = download_drugbank()

with zipfile.ZipFile(path) as zip_file:
    with zip_file.open('full database.xml') as file:
        pass  # do something with the file
```

You don't have time to remember this. Just use `drugbank_downloader.open_drugbank()` instead:

```python
from drugbank_downloader import open_drugbank

with open_drugbank() as file:
    pass  # do something with the file, same as above
```

## Reading DrugBank's XML

After you've opened the file, you probably want to read it with an XML parser like:

```python
from xml.etree import ElementTree
from drugbank_downloader import open_drugbank

with open_drugbank() as file:
    tree = ElementTree.parse(file)
```

You don't have time to remember this either. Just use `drugbank_downloader.parse_drugbank()` instead:

```python
from xml.etree import ElementTree
from drugbank_downloader import parse_drugbank

tree = parse_drugbank()
root = tree.getroot()
```

If your first thing to do to the tree is always to get its root, just use
`drugbank_downloader.get_drugbank_root()`:

```python
from drugbank_downloader import get_drugbank_root

root = get_drugbank_root()
```

You now know everything I can teach you. Please use these tools to do re-usable, reproducible 
science!

## Store in a Different Place

If you want to store the data elsewhere using `pystow` (e.g., in [`pyobo`](https://github.com/pyobo/pyobo)
I also keep a copy of this file), you can use the `prefix` argument.

```python
import os
from drugbank_downloader import download_drugbank

path = download_drugbank(prefix=['pyobo', 'raw', 'drugbank'])

# This is where it gets downloaded: ~/.data/pyobo/raw/drugbank/5.1.7/full database.xml.zip
expected_path = os.path.join(os.path.expanduser('~'), '.data', 'pyobo', 'raw', 'drugbank', '5.1.7',
                             'full database.xml.zip')
assert expected_path == path.as_posix()
```

See the `pystow` [documentation](https://github.com/cthoyt/pystow#%EF%B8%8F-configuration) on configuring the storage
location further.

## Download via CLI

After installing, run the following CLI command to ensure it and send the path to stdout

```bash
$ drugbank_downloader
```

If you haven't pre-configured the username and password, you can specify them with the `--username` and `--password`
options.

## 👐 Contributing

Contributions, whether filing an issue, making a pull request, or forking, are appreciated. See
[CONTRIBUTING.md](https://github.com/cthoyt/drugbank-downloader/blob/master/.github/CONTRIBUTING.md)
for more information on getting involved.

## 👋 Attribution

### ⚖️ License

The code in this package is licensed under the MIT License.

### 🍪 Cookiecutter

This package was created with [@audreyfeldroy](https://github.com/audreyfeldroy)'s
[cookiecutter](https://github.com/cookiecutter/cookiecutter) package using [@cthoyt](https://github.com/cthoyt)'s
[cookiecutter-snekpack](https://github.com/cthoyt/cookiecutter-snekpack) template.

## 🛠️ For Developers

<details>
  <summary>See developer instructions</summary>

The final section of the README is for if you want to get involved by making a code contribution.

### Development Installation

To install in development mode, use the following:

```bash
git clone git+https://github.com/cthoyt/drugbank-downloader.git
cd drugbank-downloader
pip install -e .
```

### Updating Package Boilerplate

This project uses `cruft` to keep boilerplate (i.e., configuration, contribution guidelines, documentation
configuration)
up-to-date with the upstream cookiecutter package. Update with the following:

```shell
pip install cruft
cruft update
```

More info on Cruft's update command is
available [here](https://github.com/cruft/cruft?tab=readme-ov-file#updating-a-project).

### 🥼 Testing

After cloning the repository and installing `tox` with `pip install tox tox-uv`, 
the unit tests in the `tests/` folder can be run reproducibly with:

```shell
tox -e py
```

Additionally, these tests are automatically re-run with each commit in a
[GitHub Action](https://github.com/cthoyt/drugbank-downloader/actions?query=workflow%3ATests).

### 📖 Building the Documentation

The documentation can be built locally using the following:

```shell
git clone git+https://github.com/cthoyt/drugbank-downloader.git
cd drugbank-downloader
tox -e docs
open docs/build/html/index.html
``` 

The documentation automatically installs the package as well as the `docs`
extra specified in the [`pyproject.toml`](pyproject.toml). `sphinx` plugins
like `texext` can be added there. Additionally, they need to be added to the
`extensions` list in [`docs/source/conf.py`](docs/source/conf.py).

The documentation can be deployed to [ReadTheDocs](https://readthedocs.io) using
[this guide](https://docs.readthedocs.io/en/stable/intro/import-guide.html).
The [`.readthedocs.yml`](.readthedocs.yml) YAML file contains all the configuration you'll need.
You can also set up continuous integration on GitHub to check not only that
Sphinx can build the documentation in an isolated environment (i.e., with ``tox -e docs-test``)
but also that [ReadTheDocs can build it too](https://docs.readthedocs.io/en/stable/pull-requests.html).

#### Configuring ReadTheDocs

1. Log in to ReadTheDocs with your GitHub account to install the integration
   at https://readthedocs.org/accounts/login/?next=/dashboard/
2. Import your project by navigating to https://readthedocs.org/dashboard/import then clicking the plus icon next to
   your repository
3. You can rename the repository on the next screen using a more stylized name (i.e., with spaces and capital letters)
4. Click next, and you're good to go!

### 📦 Making a Release

#### Configuring Zenodo

[Zenodo](https://zenodo.org) is a long-term archival system that assigns a DOI to each release of your package.

1. Log in to Zenodo via GitHub with this link: https://zenodo.org/oauth/login/github/?next=%2F. This brings you to a
   page that lists all of your organizations and asks you to approve installing the Zenodo app on GitHub. Click "grant"
   next to any organizations you want to enable the integration for, then click the big green "approve" button. This
   step only needs to be done once.
2. Navigate to https://zenodo.org/account/settings/github/, which lists all of your GitHub repositories (both in your
   username and any organizations you enabled). Click the on/off toggle for any relevant repositories. When you make
   a new repository, you'll have to come back to this

After these steps, you're ready to go! After you make "release" on GitHub (steps for this are below), you can navigate
to https://zenodo.org/account/settings/github/repository/cthoyt/drugbank-downloader
to see the DOI for the release and link to the Zenodo record for it.

#### Registering with the Python Package Index (PyPI)

You only have to do the following steps once.

1. Register for an account on the [Python Package Index (PyPI)](https://pypi.org/account/register)
2. Navigate to https://pypi.org/manage/account and make sure you have verified your email address. A verification email
   might not have been sent by default, so you might have to click the "options" dropdown next to your address to get to
   the "re-send verification email" button
3. 2-Factor authentication is required for PyPI since the end of 2023 (see
   this [blog post from PyPI](https://blog.pypi.org/posts/2023-05-25-securing-pypi-with-2fa/)). This means
   you have to first issue account recovery codes, then set up 2-factor authentication
4. Issue an API token from https://pypi.org/manage/account/token

#### Configuring your machine's connection to PyPI

You have to do the following steps once per machine. Create a file in your home directory called
`.pypirc` and include the following:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = <the API token you just got>

# This block is optional in case you want to be able to make test releases to the Test PyPI server
[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = <an API token from test PyPI>
```

Note that since PyPI is requiring token-based authentication, we use `__token__` as the user, verbatim.
If you already have a `.pypirc` file with a `[distutils]` section, just make sure that there is an `index-servers`
key and that `pypi` is in its associated list. More information on configuring the `.pypirc` file can
be found [here](https://packaging.python.org/en/latest/specifications/pypirc).

#### Uploading to PyPI

After installing the package in development mode and installing
`tox` with `pip install tox tox-uv`,
run the following from the shell:

```shell
tox -e finish
```

This script does the following:

1. Uses [Bump2Version](https://github.com/c4urself/bump2version) to switch the version number in
   the `pyproject.toml`, `CITATION.cff`, `src/drugbank_downloader/version.py`,
   and [`docs/source/conf.py`](docs/source/conf.py) to not have the `-dev` suffix
2. Packages the code in both a tar archive and a wheel using [`build`](https://github.com/pypa/build)
3. Uploads to PyPI using [`twine`](https://github.com/pypa/twine).
4. Push to GitHub. You'll need to make a release going with the commit where the version was bumped.
5. Bump the version to the next patch. If you made big changes and want to bump the version by minor, you can
   use `tox -e bumpversion -- minor` after.

#### Releasing on GitHub

1. Navigate
   to https://github.com/cthoyt/drugbank-downloader/releases/new
   to draft a new release
2. Click the "Choose a Tag" dropdown and select the tag corresponding to the release you just made
3. Click the "Generate Release Notes" button to get a quick outline of recent changes. Modify the title and description
   as you see fit
4. Click the big green "Publish Release" button

This will trigger Zenodo to assign a DOI to your release as well.

</details>
