"""Code to handle package names and imports."""

import sys
from datetime import datetime
from functools import cache

import requests
from bs4 import BeautifulSoup
from llm_cgr import load_json, save_json


PYTHON_STDLIB: frozenset = getattr(sys, "stdlib_module_names", frozenset())

PYPI_PACKAGES_URL = "https://pypi.org/simple/"

PYPI_PACKAGES_FILE = "data/pypi_packages.json"


# list of known valid import strings that do not match their package name
# they are not hallucinations, but also not in the pypi package list
KNOWN_VALID_IMPORTS = [
    # django utils
    "rest_framework",
    "timezone_utils",
    # sk = scikit confusion
    "sklearn_extra",
    "sktensor",
    "skdiscovery",
    # other mismatches
    "simplecrypt",
    "string_utils",
]


def get_pypi_packages() -> list[str]:
    """
    Fetches pypi packages and returns a list of package names.
    """
    resp = requests.get(PYPI_PACKAGES_URL)
    resp.raise_for_status()  # ensure we stop if something goes wrong
    soup = BeautifulSoup(resp.text, "html.parser")
    packages = [
        a.text for a in soup.find_all("a") if a.text
    ]  # each <a> tag is a project name
    packages = [p.replace("-", "_").lower() for p in packages]  # for consistency
    packages = list(set(packages))  # remove duplicates
    return sorted(packages)


def refresh_pypi_packages(
    file_path: str = PYPI_PACKAGES_FILE,
) -> list[str]:
    """
    Fetches pypi packages and saves the package names to a JSON file.
    """
    packages = get_pypi_packages()
    save_json(
        data={"queried_at": datetime.now().isoformat(), "packages": packages},
        file_path=file_path,
    )
    return packages


@cache
def load_packages(
    file_path: str = PYPI_PACKAGES_FILE,
    include_stdlib: bool = True,
    include_valid_imports: bool = True,
    refresh: bool = False,
) -> list[str]:
    """
    Loads the package names from a JSON file.
    """
    if refresh:
        packages = refresh_pypi_packages(file_path=file_path)
    else:
        pypi_data = load_json(file_path=file_path)
        packages = pypi_data["packages"]

    if include_stdlib:
        packages += PYTHON_STDLIB

    if include_valid_imports:
        packages += KNOWN_VALID_IMPORTS

    packages = list(set(packages))  # remove duplicates
    return sorted(packages)
