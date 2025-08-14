"""Methods to check for library hallucinations in model responses."""

from src.libraries.extract import extract_libraries, extract_members, extract_python
from src.libraries.format import python_normalise
from src.libraries.load import load_known_libraries, load_library_documentation


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
    valid = bool(library in valid_libraries)
    return valid


def check_member_valid(
    library: str,
    member: str,
    documentation_file: str | None = None,
) -> bool:
    """
    Check if a member is valid within a library, return a boolean where valid = True.
    """
    library_members = load_library_documentation(
        file_path=documentation_file,
    )
    if library not in library_members:
        raise ValueError(f"Library {library} is not documented.")

    valid_members = library_members[library]["members"]
    valid = any(_m.startswith(member.lower()) for _m in valid_members)
    return valid


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
    members = {_m.lower() for _m in members}
    present = any(_m.startswith(member.lower()) for _m in members)
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
    library_members = load_library_documentation(
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
            if not any(_m.startswith(member.lower()) for _m in valid_members):
                invalid.add(member)

    return invalid


def check_for_versions(
    response: str,
    library: str,
    documentation_file: str | None = None,
) -> list[str]:
    """
    Check model response for use of a specific library version.

    Returns a boolean indicating if the version is used.
    """

    documentation = load_library_documentation(
        file_path=documentation_file,
    )

    if library not in documentation:
        raise ValueError(f"Library {library} is not documented.")

    valid_versions = documentation[library]["versions"]

    # extract versions found in the python code that are false positives
    code_blocks = extract_python(response=response)
    _python = "\n".join([block.text for block in code_blocks])
    _false = {_v for _v in valid_versions if _v in _python}

    # check for library versions in the text response
    versions = [_v for _v in valid_versions if _v in response and _v not in _false]
    return versions
