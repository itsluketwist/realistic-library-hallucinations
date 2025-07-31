"""Methods to check for library hallucinations in model responses."""

from src.libraries.extract import extract_libraries, extract_members
from src.libraries.format import python_normalise
from src.libraries.load import load_known_libraries, load_known_members


def check_library_valid(
    library: str,
    pypi_packages_file: str | None = None,
) -> bool:
    """
    Check if a library is valid, return a boolean where valid = True.
    """
    valid_libraries = load_known_libraries(
        file_path=pypi_packages_file,
    )
    library = python_normalise(name=library)
    return bool(library in valid_libraries)


def check_member_valid(
    library: str,
    member: str,
    documentation_file: str | None = None,
) -> bool:
    """
    Check if a member is valid within a library, return a boolean where valid = True.
    """
    valid_members = load_known_members(
        file_path=documentation_file,
    )
    if library not in valid_members:
        raise ValueError(f"Library {library} is not documented.")
    return bool(member in valid_members[library]["members"])


def check_for_library(
    response: str,
    library: str,
) -> tuple[bool, bool]:
    """
    Check model response for use of a specific library.

    Returns a tuple of booleans indicating if the library is present, and if it was used.
    """
    library = python_normalise(name=library)
    installs, imports, usages = extract_libraries(response=response)
    present = bool(library in (installs | imports))  # is library present?
    used = bool(library in usages)  # is library used?
    return present, used


def check_for_member(
    response: str,
    member: str,
) -> bool:
    """
    Check model response for use of a specific library member.

    Returns a boolean indicating if the member is used.
    """
    members = extract_members(response=response)
    present = bool(member in members)
    return present


def check_for_unknown_libraries(
    response: str,
    installs_only: bool = False,
    pypi_packages_file: str | None = None,
) -> set[str]:
    """
    Check model response for libraries that are not present in PyPi or the standard library.

    Returns a set of unknown libraries.
    """
    installs, imports, _ = extract_libraries(response=response)
    valid_libraries = load_known_libraries(file_path=pypi_packages_file)

    # not every response has installs, so only check installs if requested and they exist
    if installs_only and installs:
        invalid = {library for library in installs if library not in valid_libraries}

    # if not installs_only, or no installs, then check all libraries
    else:
        invalid = {
            library
            for library in (installs | imports)
            if library not in valid_libraries
        }

    return invalid


def check_for_unknown_members(
    response: str,
    library: str,
    documentation_file: str | None = None,
) -> set[str]:
    """
    Check model response for members of a specific library that are not present in the
    library documentation.

    Returns a set of unknown members of the given library.
    """
    response_members = extract_members(response=response)
    library_members = load_known_members(
        file_path=documentation_file,
    )

    if library not in library_members:
        raise ValueError(f"Library {library} is not documented.")

    valid_modules = library_members[library]["modules"]
    valid_members = library_members[library]["members"]

    invalid = set()
    for member in response_members:
        # check if the member is from a module of the given library
        if any(member.startswith(module + ".") for module in valid_modules):
            # check if member is valid within the library
            if member not in valid_members:
                invalid.add(member)

    return invalid
