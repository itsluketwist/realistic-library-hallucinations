"""Code to handle package names and imports."""

import sys
from functools import cache

import requests
from bs4 import BeautifulSoup
from llm_cgr import load_json, save_json


PYTHON_STDLIB = getattr(sys, "stdlib_module_names", [])

PYPI_PACKAGES_URL = "https://pypi.org/simple/"

PYPI_PACKAGES_FILE = "output/pypi_packages.json"


# list of valid import strings that do not match their package name
VALID_IMPORTS = [
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


def get_pypi_packages():
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


def save_pypi_packages():
    """
    Fetches pypi packages and saves the package names to a JSON file.
    """
    packages = get_pypi_packages()
    save_json(data=packages, file_path=PYPI_PACKAGES_FILE)


@cache
def load_packages(
    file_path: str = PYPI_PACKAGES_FILE,
    include_stdlib: bool = True,
    include_valid_imports: bool = True,
) -> list[str]:
    """
    Loads the package names from a JSON file.
    """
    packages = load_json(file_path=file_path)

    if include_stdlib:
        packages += PYTHON_STDLIB

    if include_valid_imports:
        packages += VALID_IMPORTS

    packages = list(set(packages))  # remove duplicates
    return sorted(packages)
