# drugbank_downloader

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

## Download the Latest Version

First, you'll have to install `bioversions` with `pip install bioversions`, whose job it is to look up the latest
version of many databases. Then, you can modify the previous code slightly:

```python
import os
from drugbank_downloader import download_drugbank

username = ...  # suggestion: load from environment with os.getenv('DRUGBANK_USERNAME')
password = ...

path = download_drugbank(username=username, password=password)

# This is where it gets downloaded: ~/.data/drugbank/5.1.7/full database.xml.zip based on the latest
# version, as of December 14th, 2020.
expected_path = os.path.join(os.path.expanduser('~'), '.data', 'drugbank', '5.1.7', 'full database.xml.zip')
assert expected_path == path.as_posix()
```

## Store in a Different Place

If you want to store the data elsewhere using `pystow` (e.g., in PyOBO I also keep a copy of this file), you can use
the `prefix` argument.

```python
import os
from drugbank_downloader import download_drugbank

username = ...  # suggestion: load from environment with os.getenv('DRUGBANK_USERNAME')
password = ...

path = download_drugbank(version='5.1.7', username=username, password=password, prefix=['pyobo', 'raw', 'drugbank'])

# This is where it gets downloaded: ~/.data/pyobo/raw/drugbank/5.1.7/full database.xml.zip
expected_path = os.path.join(os.path.expanduser('~'), '.data', 'pyobo', 'raw', 'drugbank', '5.1.7',
                             'full database.xml.zip')
assert expected_path == path.as_posix()
```

## Don't Bother Unpacking - read `full database.xml.zip` Directly

DrugBank is a single XML (could be JSON in a better future) file inside a zip archive. Normally, people
manually unzip this folder then do something with the resulting file. Don't do this, it's not reproducible!
Instead, it can be opened as a file object in Python with the following code. In all of the following
examples, `version` can be explicitly passed if desired.

```python
import zipfile
from drugbank_downloader import download_drugbank

path = download_drugbank(username=..., password=...)

with zipfile.ZipFile(path) as zip_file:
    with zip_file.open('full database.xml') as file:
        pass  # do something with the file
```

You don't have time to remember this. Just use `drugbank_downloader.open_drugbank()` instead:

```python
from drugbank_downloader import open_drugbank

with open_drugbank(username=..., password=...) as file:
    pass  # do something with the file, same as above
```

## Reading Drugbank's XML

After you've opened the file, you probably want to read it with an XML parser like:

```python
from xml.etree import ElementTree
from drugbank_downloader import open_drugbank

with open_drugbank(username=..., password=...) as file:
    tree = ElementTree.parse(file)
root = tree.getroot()
```

You don't have time to remember this either. Just use `drugbank_downloader.parse_drugbank()` instead:

```python
from drugbank_downloader import parse_drugbank

root = parse_drugbank(username=..., password=...)
```

You know everything I can teach you. Please use these tools to do re-usable, reproducible science!

## Download via CLI

After installing, run the following CLI command to ensure it and send the path to stdout

```bash
$ drugbank_downloader --username *** --password ***
```
