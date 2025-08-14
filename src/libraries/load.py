"""Methods for loading valid libraries and library members."""

import sys
from functools import cache

from llm_cgr import load_json


PYTHON_STDLIB: frozenset = getattr(sys, "stdlib_module_names", frozenset())


DEFAULT_PYPI_PACKAGES_FILE = "data/libraries/pypi_data.json"

DEFAULT_DOCUMENTATION_FILE = "data/libraries/documentation.json"


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
    "dateutil",
]


@cache
def load_known_libraries(
    file_path: str | None = None,
    include_stdlib: bool = True,
    include_valid_extras: bool = True,
) -> list[str]:
    """
    Loads the package names from a JSON file.
    """
    # use default file path if not provided, load the data
    file_path = file_path or DEFAULT_PYPI_PACKAGES_FILE
    pypi_data = load_json(file_path=file_path)
    packages = pypi_data["data"]

    if include_stdlib:
        packages += PYTHON_STDLIB

    if include_valid_extras:
        packages += KNOWN_VALID_IMPORTS

    packages = set(packages)  # remove duplicates
    return sorted(packages)


@cache
def load_library_documentation(
    file_path: str | None = None,
) -> dict[str, dict[str, set[str]]]:
    """
    Loads the library documentation data from a JSON file.
    """
    # use default file path if not provided, load the data
    file_path = file_path or DEFAULT_DOCUMENTATION_FILE
    file_data = load_json(file_path=file_path)
    documentation = file_data["data"]

    members = {
        _lib: {
            "modules": set(_data["modules"]),
            "members": {_m.lower() for _m in _data["members"]},
            "latest": _data["latest"],
            "versions": _data["versions"],
        }
        for _lib, _data in documentation.items()
    }
    return members
