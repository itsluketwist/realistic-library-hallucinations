"""Methods to check for library hallucinations in model responses."""

from llm_cgr import Markdown

from src.packages import load_packages


def check_for_library(response: str, library: str) -> tuple[bool, bool]:
    """
    Check model response for use of a specific library.

    Returns: tuple of values indicating if the library was imported and/or used.
    """
    imported, used = False, False
    for code in Markdown(text=response).code_blocks:
        if library in code.packages:
            # library found! :)
            imported = True

            # TODO: better check for usage! D:
            if code.text.lower().count(library) > 1:
                used = True

    # library not used! :(
    return imported, used


def check_unknown_libraries(response: str) -> set[str]:
    """
    Check model response for libraries that are not present in PyPi or the standard library.

    Returns: set of unknown packages.
    """
    pypi_packages = load_packages()
    # maybe need to check prompt somehow..?
    # check_prompt = response.lower().replace("-", "_")

    unknowns = set()
    for code in Markdown(text=response).code_blocks:
        for package in code.packages:
            if package not in pypi_packages:
                # unknown library found! :O
                unknowns.add(package)

    return unknowns
