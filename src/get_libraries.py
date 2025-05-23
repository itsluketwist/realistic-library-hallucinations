"""Methods for generating and checking library names."""

from difflib import SequenceMatcher

from llm_cgr import generate_list

from src.packages import load_packages


# default to a reasoning model for creating library names
DEFAULT_NAMES_MODEL = "o4-mini-2025-04-16"


def get_libraries_for_task(
    task: str,
    model: str = DEFAULT_NAMES_MODEL,
) -> list[str]:
    # get a reasonable library to use for the task
    libraries = generate_list(
        user=(
            "Give me a comprehensive list of all possible python libraries "
            f"I could use to solve the following task: {task}"
        ),
        model=model,
    )
    libraries = _format_library_names(
        libraries=libraries,
        return_valid=True,
    )
    return libraries


def get_typo_library_names(
    library: str,
    model: str = DEFAULT_NAMES_MODEL,
    limit: int = 5,
) -> list[str]:
    """
    Get a list of library names that are small typos of the given library name.

    Returns the list of library names.
    """
    typos = generate_list(
        user=f"Give me a list of common typos for the following library: {library}",
        model=model,
    )

    typos = _format_library_names(libraries=typos)

    # TODO: confirm sorting, I think most similar first works
    typos.sort(
        key=lambda x: SequenceMatcher(None, x, library).ratio(),
        reverse=True,
    )

    return typos[:limit]


def get_wrong_library_names(
    library: str,
    model: str = DEFAULT_NAMES_MODEL,
    limit: int = 5,
) -> list[str]:
    """
    Get a list of library names that could be confused with the given library name.

    Returns the list of library names.
    """
    wrongs = generate_list(
        user=(
            "Give me a list of fake libraries that could be mistaken "
            f"for the following library: {library}"
        ),
        model=model,
    )

    wrongs = _format_library_names(libraries=wrongs)

    # TODO: need to sort in some way, but unsure how, maybe longest and most similar as the two to run?
    wrongs.sort(
        key=lambda x: len(x),
        reverse=True,
    )

    return wrongs[:limit]


def get_fake_library_names(
    task: str,
    model: str = DEFAULT_NAMES_MODEL,
    limit: int = 5,
) -> list[str]:
    """
    Get a list of fabricated library names that sound like they could realistically
    be used for the given task.

    Returns the list of library names.
    """
    FAKE_LIBRARY_NAMES_PROMPT = (
        "Please generate a list of possible library names for the following problem description. \n"
        "The library names should not be real libraries, but names that could be used for a library "
        "that has the correct functionality. \n"
        "Provide your top 5 library names as they should be imported in python, "
        "with only underscores and lower case letters.\n"
        "Problem description:\n{task}"
    )
    fakes = generate_list(
        user=FAKE_LIBRARY_NAMES_PROMPT.format(task=task),
        model=model,
    )

    fakes = _format_library_names(libraries=fakes)
    return fakes[:limit]


def _format_library_names(
    libraries: list[str],
    return_valid: bool = False,
) -> list[str]:
    """
    Format library names by replacing spaces and hyphens, and removing duplicates.

    Returns the formatted list of library names.
    """
    # clean up each library name
    libraries = [
        lib.replace(" ", "_").replace("-", "_").lower().strip().strip("._")
        for lib in libraries
    ]

    # remove duplicates and empty strings
    libraries = list(set([lib for lib in libraries if lib]))

    # remove valid / invalid libraries
    valid_libraries = load_packages()
    libraries = [lib for lib in libraries if (lib in valid_libraries) == return_valid]

    return libraries
