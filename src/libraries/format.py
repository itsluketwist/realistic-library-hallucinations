"""Methods for formatting python objects."""

import re


def python_normalise(name: str) -> str:
    """
    Normalise a python object name to a consistent format, as per the Python Packaging User Guide.

    Source: https://packaging.python.org/en/latest/specifications/name-normalization/
    """
    return re.sub(r"[-_. ]+", "_", name).lower().strip()


def format_python_list(
    libraries: list[str],
    normalise: bool = True,  # typically only necessary for library names
) -> list[str]:
    """
    Format queried list of python objects by normalising them, and removing duplicates.

    Returns the formatted list of python objects.
    """
    # clean up each object name
    if normalise:
        libraries = [python_normalise(lib).strip("_") for lib in libraries]

    # remove duplicates and empty strings (preserving order)
    libraries = list(dict.fromkeys([lib for lib in libraries if lib]))

    return libraries
