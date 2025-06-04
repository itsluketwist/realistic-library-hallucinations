"""Methods for formatting library names."""

from src.libraries.load import load_packages


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
    libraries = [
        lib.replace(" ", "_").replace("-", "_").lower().strip().strip("._")
        for lib in libraries
    ]

    # remove duplicates (preserving order) and empty strings
    libraries = list(dict.fromkeys([lib for lib in libraries if lib]))

    # remove valid / invalid libraries
    valid_libraries = load_packages(
        file_path=pypi_packages_file,
    )
    libraries = [lib for lib in libraries if (lib in valid_libraries) == valid]

    return libraries
