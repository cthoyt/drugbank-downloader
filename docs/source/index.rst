DrugBank Downloader |release| Documentation
===========================================

Cookiecutter
------------
This package was created with the `cookiecutter <https://github.com/cookiecutter/cookiecutter>`_
package using `cookiecutter-snekpack <https://github.com/cthoyt/cookiecutter-snekpack>`_ template.
It comes with the following:

- Standard ``src/`` layout
- Declarative setup with `pyproject.toml` (following `PEP 621 <https://peps.python.org/pep-0621/>`_)
- Reproducible workflows configured with ``tox``
  - Reproducible tests with ``pytest``
  - A command line interface with ``click``
  - Reproducible notebooks with `treon <https://github.com/reviewNB/treon>`_
  - Documentation build with ``sphinx``
  - Testing of code quality with ``ruff``
  - Testing of documentation coverage with ``docstr-coverage``
  - Testing of documentation format
  - Testing of package metadata completeness with ``pyroma``
  - Testing of MANIFEST correctness with ``check-manifest``
  - Testing of optional static typing with ``mypy``
  - Version management with ``bump2version``
  - Building with ``build[uv]``
  - Releasing to PyPI with ``twine``
- A command line interface with ``click``
- A vanity CLI via python entrypoints
- A `py.typed` file so other packages can use your type hints
- Automated running of tests on each push
  with `GitHub Actions <https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions>`_
- Configuration for `ReadTheDocs <https://readthedocs.org>`_
- A good base `.gitignore` generated from `gitignore.io <https://gitignore.io>`_.
- A pre-formatted README with badges
- A pre-formatted LICENSE file with the MIT License (you can change this to whatever you want, though)
- A pre-formatted CONTRIBUTING guide
- A copy of the `Contributor Covenant <https://www.contributor-covenant.org>`_ as a basic code of conduct

Table of Contents
-----------------
.. toctree::
   :maxdepth: 2
   :caption: Getting Started
   :name: start

   installation
   usage
   cli

Indices and Tables
------------------
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
