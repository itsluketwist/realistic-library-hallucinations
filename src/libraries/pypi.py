"""Method to download up-to-date list of PyPI packages."""

from datetime import datetime

import requests
from bs4 import BeautifulSoup
from llm_cgr import save_json

from src.libraries.format import python_normalise


PYPI_PACKAGES_URL = "https://pypi.org/simple/"


def download_pypi_data(
    destination: str = "data/libraries/pypi_data.json",
):
    """
    Download the list of packages from PyPI and save it to a file.
    Use this as the basis of the ground truth for detecting library name hallucinations.
    """
    # download html from pypi
    response = requests.get(PYPI_PACKAGES_URL)
    response.raise_for_status()  # ensure we stop if something goes wrong

    # parse the html and extract package names
    soup = BeautifulSoup(response.text, "html.parser")
    packages = {
        a.text for a in soup.find_all("a") if a.text
    }  # each <a> tag is a project name

    # normalise them to avoid conflicts
    normalised = {python_normalise(name) for name in packages}

    # save to file
    save_json(
        data={
            "datetime": datetime.now().isoformat(),
            "data": sorted(normalised),
        },
        file_path=destination,
    )
