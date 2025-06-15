"""Methods for formatting library names."""

import re

from src.libraries.load import load_known_imports


def python_normalise(name: str) -> str:
    """
    Normalise a python package name to a consistent format, as per the Python Packaging User Guide.

    Website: https://packaging.python.org/en/latest/specifications/name-normalization/
    """
    return re.sub(r"[-_.]+", "_", name).lower().strip()


def format_library_names(
    libraries: list[str],
    valid: bool = False,
    pypi_packages_file: str | None = None,
) -> list[str]:
    """
    Format queried list of libraries by replacing spaces and hyphens, and removing duplicates.

    Returns the formatted list of library names.
    """
    # clean up each library name
    libraries = [python_normalise(lib).strip("_") for lib in libraries]

    # remove duplicates and empty strings (preserving order)
    libraries = list(dict.fromkeys([lib for lib in libraries if lib]))

    # remove valid / invalid libraries
    valid_libraries = load_known_imports(
        file_path=pypi_packages_file,
    )
    libraries = [lib for lib in libraries if (lib in valid_libraries) == valid]

    return libraries
