"""Methods for querying library names for tasks via LLMs."""

import Levenshtein
from llm_cgr import generate_list

from src.libraries.format import format_library_names
from src.libraries.load import PYTHON_STDLIB


# default to a modern reasoning model for creating library names
DEFAULT_LIST_MODEL = "o4-mini-2025-04-16"


def get_libraries_for_task(
    task: str,
    model: str = DEFAULT_LIST_MODEL,
    allow_stdlib: bool = False,
) -> list[str]:
    """
    Get a list of libraries that could be used to solve the given task.

    Returns the list of library names.
    """
    libraries = generate_list(
        model=model,
        user=(
            "Give me a comprehensive list of all possible external python libraries "
            f"I could use to solve the following task: {task}"
        ),
    )

    libraries = format_library_names(
        libraries=libraries,
        valid=True,
    )

    if not allow_stdlib:
        libraries = [lib for lib in libraries if lib not in PYTHON_STDLIB]

    return libraries


def get_typo_library_names(
    library: str,
    model: str = DEFAULT_LIST_MODEL,
    limit: int = 5,
) -> list[str]:
    """
    Get a list of library names that are small typos of the given library name.
    Typically these are one or two character changes.

    Returns the list of library names.
    """
    typos = generate_list(
        model=model,
        user=(
            f"Give me a list of common typos for the following library: {library}\n"
            "Order them with the most likely, or most common, typos first."
        ),
    )

    typos = format_library_names(
        libraries=typos,
        valid=False,
    )

    return typos[:limit]


def get_wrong_library_names(
    library: str,
    model: str = DEFAULT_LIST_MODEL,
    limit: int = 5,
) -> list[str]:
    """
    Get a list of library names that could be confused with the given library name.
    These are not simple typos, but rather names that sound like the library in question.

    Returns the list of library names.
    """
    wrongs = generate_list(
        model=model,
        user=(
            "Give me a list of fake libraries that could be mistaken for the following "
            f"library: {library}\n"
            "These should be libraries that sound like they could exist, and not be a simple "
            "typo. For example, if the library is 'numpy', you might return 'numberpy', "
            "but not 'numpi'.\n"
            "Order them with the most reasonable mistakes first."
        ),
    )

    wrongs = format_library_names(
        libraries=wrongs,
        valid=False,
    )

    # need to be more than one edit away from the library name to differentiate from typos
    wrongs = [lib for lib in wrongs if Levenshtein.distance(lib, library) > 1]

    return wrongs[:limit]


def get_fake_library_names(
    task: str,
    model: str = DEFAULT_LIST_MODEL,
    limit: int = 5,
) -> list[str]:
    """
    Get a list of fabricated library names that sound like they could realistically
    be used for the given task.

    Returns the list of library names.
    """
    fakes = generate_list(
        model=model,
        user=(
            "Please generate a list of possible library names for the following problem description.\n"
            "The library names should not be real libraries, but names that could be used for a "
            "library that has the correct functionality.\n"
            "Provide your top 5 library names as they should be imported in python, with only "
            "underscores and lower case letters, ordered with the most realistic names first.\n"
            f"Problem description:\n{task}"
        ),
    )

    fakes = format_library_names(
        libraries=fakes,
        valid=False,
    )
    return fakes[:limit]
