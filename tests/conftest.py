"""Fixtures used for testing the project."""

import shutil
import tempfile

import pytest
from llm_cgr import save_json


TEST_PYPI_PACKAGE_DATA = {
    "datetime": "2025-05-20T14:51:33.223210",
    "data": [
        "numpy",
        "pandas",
        "tensorflow",
        "requests",
        "flask",
        "scikit_learn",
        "valid_library",
    ],
}


@pytest.fixture
def test_pypi_packages_file():
    """
    Fixture to create a temporary file with test PyPI package data.

    Yields the path to the temporary file.
    """
    _temp_dir = tempfile.mkdtemp()
    _file_path = f"{_temp_dir}/test_pypi_packages.json"
    save_json(data=TEST_PYPI_PACKAGE_DATA, file_path=_file_path)

    try:
        yield _file_path

    finally:
        shutil.rmtree(_temp_dir)  # cleanup
