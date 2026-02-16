"""Methods for formatting python objects."""

import re


def python_normalise(name: str) -> str:
    """
    Normalise a python object name to a consistent format, as per the Python Packaging User Guide.

    Source: https://packaging.python.org/en/latest/specifications/name-normalization/
    """
    return re.sub(r"[-_. ]+", "_", name.strip()).lower().strip("_")


def javascript_normalise(name: str) -> str:
    """
    Normalise a javascript object name to a consistent, valid format.

    Source: https://www.npmjs.com/package/validate-npm-package-name
    """
    name = name.strip().lower()
    return name


def library_normalise(
    name: str,
    language: str = "python",
) -> str:
    """Normalise the given library name."""
    if language == "python":
        name = python_normalise(name=name)
    elif language == "javascript":
        name = javascript_normalise(name=name)

    return name


def format_library_list(
    libraries: list[str],
    language: str = "python",
    normalise: bool = True,
) -> list[str]:
    """
    Format queried list of python objects by normalising them, and removing duplicates.

    Returns the formatted list of python objects.
    """
    if normalise:
        # clean up each library name
        if language == "python":
            libraries = [python_normalise(lib) for lib in libraries]
        elif language == "javascript":
            libraries = [javascript_normalise(lib) for lib in libraries]
            libraries = [lib for lib in libraries if lib and lib[0] not in (".", "_")]

    # remove duplicates and empty strings (preserving order)
    libraries = list(dict.fromkeys([lib for lib in libraries if lib]))

    return libraries
