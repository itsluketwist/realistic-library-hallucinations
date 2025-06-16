"""Methods for loading valid library names from PyPI."""

import sys
from functools import cache

from llm_cgr import load_json


PYTHON_STDLIB: frozenset = getattr(sys, "stdlib_module_names", frozenset())


DEFAULT_PYPI_PACKAGES_FILE = "../data/pypi/package_names.json"


# list of known valid import strings that do not match their package name
# they are not hallucinations, but also not in the pypi package list
# note: manually curated and not exhaustive, so may need updates over time
KNOWN_VALID_IMPORTS = [
    # django utils
    "rest_framework",
    "timezone_utils",
    # sk = scikit confusion
    "sklearn_extra",
    "sktensor",
    "skdiscovery",
    "skbio",
    "autosklearn",
    # other mismatches
    "simplecrypt",
    "string_utils",
    "mpl_toolkits",
    "agateremote",
    "github3",
    "cairo",
    "erfa",
    "gnuplot",
    "pyximport",
    "scikitplot",
]


@cache
def load_known_imports(
    file_path: str | None = None,
    include_stdlib: bool = True,
    include_valid_extras: bool = True,
) -> list[str]:
    """
    Loads the package names from a JSON file.
    """
    # use default file path if not provided
    file_path = file_path or DEFAULT_PYPI_PACKAGES_FILE

    pypi_data = load_json(file_path=file_path)
    packages = pypi_data["data"]

    if include_stdlib:
        packages += PYTHON_STDLIB

    if include_valid_extras:
        packages += KNOWN_VALID_IMPORTS

    packages = set(packages)  # remove duplicates
    return sorted(packages)
