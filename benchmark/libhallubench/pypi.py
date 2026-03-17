"""Functions for downloading and loading PyPI package data."""

import re
import sys
from datetime import datetime
from functools import cache
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from llm_cgr import load_json, save_json


# pypi download url
PYPI_PACKAGES_URL = "https://pypi.org/simple/"

# default pypi data file path, stored alongside the package code
DEFAULT_PYPI_FILE = str(Path(__file__).parent / "pypi_data.json")

# python standard library module names
PYTHON_STDLIB: frozenset = getattr(sys, "stdlib_module_names", frozenset())

# known valid import strings that do not match their pypi package name
PYTHON_KNOWN_VALID_IMPORTS = [
    "rest_framework",
    "timezone_utils",
    "sklearn_extra",
    "sktensor",
    "skdiscovery",
    "skbio",
    "autosklearn",
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


def _normalise(name: str) -> str:
    """Normalise a python package name as per PEP 503."""
    return re.sub(r"[-_. ]+", "_", name.strip()).lower().strip("_")


def download_pypi_data(
    destination: str = DEFAULT_PYPI_FILE,
) -> None:
    """
    Download the list of packages from PyPI and save to a file.

    Use this to keep the ground truth for detecting hallucinations up to date.
    """
    # download html from pypi
    response = requests.get(PYPI_PACKAGES_URL)
    response.raise_for_status()

    # parse the html and extract package names
    soup = BeautifulSoup(response.text, "html.parser")
    packages = {a.text for a in soup.find_all("a") if a.text}

    # normalise names to avoid conflicts
    normalised = {_normalise(name) for name in packages}

    # save to file
    save_json(
        data={"datetime": datetime.now().isoformat(), "data": sorted(normalised)},
        file_path=destination,
    )


@cache
def load_known_libraries(
    file_path: str | None = None,
) -> list[str]:
    """
    Load the list of known valid python libraries from a pypi data file.

    Automatically downloads the data from PyPI if the file does not exist.

    Returns a sorted list of valid library names.
    """
    file_path = file_path or DEFAULT_PYPI_FILE

    # automatically download pypi data if the file doesn't exist
    if not Path(file_path).exists():
        print(f"PyPI data not found at {file_path}, downloading...")
        download_pypi_data(destination=file_path)

    pypi_data = load_json(file_path=file_path)

    packages = pypi_data["data"]
    packages += PYTHON_STDLIB
    packages += PYTHON_KNOWN_VALID_IMPORTS

    return sorted(set(packages))
