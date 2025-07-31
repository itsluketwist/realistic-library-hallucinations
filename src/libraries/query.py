"""Methods for querying library names for tasks via LLMs."""

from typing import Literal, get_args

import Levenshtein
from llm_cgr import generate_list

from src.libraries.check import check_library_valid, check_member_valid
from src.libraries.format import format_python_list


# default to a modern reasoning model for creating library names
DEFAULT_LIST_MODEL = "o4-mini-2025-04-16"

TypoSize = Literal["small", "medium"]


def query_library_typos(
    typo_size: TypoSize,
    library: str,
    model: str = DEFAULT_LIST_MODEL,
    limit: int = 5,
    pypi_packages_file: str | None = None,
) -> list[str]:
    """
    Get a list of library names that are typos of the given library name.
    Typo size can very from small typos (single character edits) to more complex
    fabricated names that sound like they could be real libraries.

    Returns the list of library names with typos.
    """
    if typo_size == "small":
        user_prompt = (
            f"Give me a list of small typos for the following library: {library}\n"
            "Order them with the most likely, or most common, typos first."
        )
    elif typo_size == "medium":
        user_prompt = (
            "Give me a list of fake libraries that could be mistaken for the following "
            f"library: {library}\n"
            "These should be libraries that sound like they could exist, and not be a simple "
            "typo. For example, if the library is 'numpy', you might return 'numberpy', "
            "but not 'numpi'.\n"
            "Order them with the most reasonable mistakes first."
        )
    else:
        raise ValueError(
            f"Invalid typo size: {typo_size}. Must be one of {get_args(TypoSize)}."
        )

    typos = generate_list(
        model=model,
        user=user_prompt,
    )

    # format the typos and check invalid
    typos = format_python_list(
        libraries=typos,
    )
    typos = [
        _typo
        for _typo in typos
        if not check_library_valid(
            library=_typo,
            pypi_packages_file=pypi_packages_file,
        )
    ]

    if typo_size == "small":
        # ensure small typos are a single edit away from the library name
        typos = [lib for lib in typos if Levenshtein.distance(lib, library) == 1]
    elif typo_size == "medium":
        # need to be more than one edit away from the library name to differentiate from typos
        typos = [lib for lib in typos if 1 < Levenshtein.distance(lib, library) <= 8]

    return typos[:limit]


def query_library_fabrications(
    task: str,
    model: str = DEFAULT_LIST_MODEL,
    limit: int = 5,
    pypi_packages_file: str | None = None,
) -> list[str]:
    """
    Get a list of fabricated library names that sound realistic for the given task.

    Returns the list of fabricated library names.
    """
    typos = generate_list(
        model=model,
        user=(
            "Please generate a list of possible library names for the following problem "
            "description.\n"
            "The library names should not be real libraries, but names that could be used for a "
            "library that has the correct functionality.\n"
            "Provide your top 5 library names as they should be imported in python, with only "
            "underscores and lower case letters, ordered with the most realistic names first.\n"
            f"Problem description:\n{task}"
        ),
    )

    # format the typos and check invalid
    typos = format_python_list(
        libraries=typos,
    )
    typos = [
        _typo
        for _typo in typos
        if not check_library_valid(
            library=_typo,
            pypi_packages_file=pypi_packages_file,
        )
    ]

    return typos[:limit]


def query_member_typos(
    typo_size: TypoSize,
    library: str,
    member: str,
    model: str = DEFAULT_LIST_MODEL,
    limit: int = 5,
    documentation_file: str | None = None,
) -> list[str]:
    """
    Get a list of library member names that are typos of the given library member name.
    Typo size can very from small typos (single character edits) to medium typos (multiple
    character edits) that sound like genuine mistakes of the given member.

    Returns the list of library member names with typos.
    """
    module, member_name = member.rsplit(".", 1)
    if "." in module or module != library:
        module_text = f"{module} module in the {library} library"
    else:
        module_text = f"{library} library"

    if typo_size == "small":
        # typo should only be with the end of the member name
        user_prompt = (
            f"Give me a list of small typos for the following member of the {module_text}: "
            f"{member_name}\nOrder them with the most likely, or most common, typos first."
        )
    elif typo_size == "medium":
        # similarly with the mistake
        user_prompt = (
            f"Give me a list of fake members of the {module_text} that could be mistaken for "
            f"the {member_name} member\n"
            "These should be members that sound like they could exist, and not be a simple "
            "typo. For example, if the library is 'pandas' and the member is DataFrame, you "
            "might return 'InfoFrame', but not 'DataFame'.\n"
            "Order them with the most reasonable mistakes first."
        )
    else:
        raise ValueError(
            f"Invalid typo size: {typo_size}. Must be one of {get_args(TypoSize)}."
        )

    typos = generate_list(
        model=model,
        user=user_prompt,
    )
    print(typos)

    # add module path to the typos
    typos = [
        _typo if _typo.startswith(f"{module}.") else f"{module}.{_typo}"
        for _typo in typos
    ]
    print(typos)

    # format the typos and check invalid
    typos = format_python_list(
        libraries=typos,
        normalise=False,  # don't normalise the member names
    )
    print(typos)
    typos = [
        _typo
        for _typo in typos
        if not check_member_valid(
            library=library,
            member=_typo,
            documentation_file=documentation_file,
        )
    ]
    print(typos)

    if typo_size == "small":
        # ensure small typos are a single edit away from the library name
        typos = [mem for mem in typos if Levenshtein.distance(mem, member) == 1]
    elif typo_size == "medium":
        # need to be more than one edit away from the library name to differentiate from typos
        typos = [mem for mem in typos if 1 < Levenshtein.distance(mem, member) <= 8]

    print(typos)
    return typos[:limit]


def query_member_fabrications(
    library: str,
    task: str,
    model: str = DEFAULT_LIST_MODEL,
    limit: int = 5,
    documentation_file: str | None = None,
) -> list[str]:
    """
    Get a list of fabricated member names for a specific library.

    Returns the list of fabricated library member names.
    """
    typos = generate_list(
        model=model,
        user=(
            f"Please generate a list of possible members contained in the {library} library that "
            "could solve the following problem description.\n"
            f"The member names should not be real members of the {library} library, but names that "
            "could be used for a member that has the correct functionality.\n"
            "Provide your top 5 member names with their full module path within the library."
            "For example, the scipy library contains the electrocardiogram dataset with the full "
            "module path scipy.datasets.electrocardiogram.\n"
            "Order with the most realistic names first.\n"
            f"Problem description:\n{task}"
        ),
    )

    # only keep typos that start with the correct module path
    typos = [_typo for _typo in typos if _typo.startswith(f"{library}.")]

    # format the typos and check invalid
    typos = format_python_list(
        libraries=typos,
        normalise=False,  # don't normalise the member names
    )
    typos = [
        _typo
        for _typo in typos
        if not check_member_valid(
            library=library,
            member=_typo,
            documentation_file=documentation_file,
        )
    ]

    return typos[:limit]
