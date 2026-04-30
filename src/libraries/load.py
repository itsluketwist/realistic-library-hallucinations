"""Methods for loading valid libraries and library members."""

import sys
from functools import cache

from llm_cgr import load_json


PYTHON_STDLIB: frozenset = getattr(sys, "stdlib_module_names", frozenset())


DEFAULT_PYPI_PACKAGES_FILE = "data/libraries/pypi_data.json"

DEFAULT_DOCUMENTATION_FILE = "data/libraries/documentation.json"

DEFAULT_NPM_PACKAGES_FILE = "data/npm_libraries/npm_data.json"

DEFAULT_RUST_CRATES_FILE = "data/rust_libraries/crates_data.json"

# list of known valid import strings that do not match their package name
# they are not hallucinations, but also not in the pypi package list
# note: manually curated and not exhaustive, so may need updates over time
PYTHON_KNOWN_VALID_IMPORTS = [
    # django utils
    "rest_framework",
    "timezone_utils",
    # sk = scikit confusion
    "sklearn_extra",
    "sktensor",
    "skdiscovery",
    "skbio",
    "autosklearn",
    # other mismatches
    "simplecrypt",
    "string_utils",
    "mpl_toolkits",
    "agateremote",
    "github3",
    "cairo",
    "erfa",
    "gnuplot",
    "pyximport",
    "scikitplot",
    "dateutil",
]


# rust's built-in standard library crates (not distributed via crates.io)
RUST_STDLIB: frozenset = frozenset({"std", "core", "alloc", "proc_macro"})


# Node.js standard library modules
JAVASCRIPT_STDLIB = {
    "fs",
    "path",
    "http",
    "https",
    "url",
    "querystring",
    "assert",
    "buffer",
    "child_process",
    "cluster",
    "crypto",
    "dns",
    "domain",
    "events",
    "net",
    "os",
    "process",
    "stream",
    "string_decoder",
    "timers",
    "tls",
    "tty",
    "dgram",
    "util",
    "v8",
    "vm",
    "zlib",
    "readline",
    "repl",
    "console",
    "module",
    "worker_threads",
}


def _load_python_libraries(
    file_path: str | None = None,
    include_stdlib: bool = True,
    include_valid_extras: bool = True,
    **kwargs,
) -> list[str]:
    """Loads the python package names from a JSON file."""
    # use default file path if not provided, load the data
    file_path = file_path or DEFAULT_PYPI_PACKAGES_FILE
    pypi_data = load_json(file_path=file_path)
    packages = pypi_data["data"]

    if include_stdlib:
        packages += PYTHON_STDLIB

    if include_valid_extras:
        packages += PYTHON_KNOWN_VALID_IMPORTS

    packages = set(packages)  # remove duplicates
    return sorted(packages)


def _load_javascript_libraries(
    file_path: str | None = None,
    include_stdlib: bool = True,
    **kwargs,
) -> list[str]:
    """Loads the javascript package names from a JSON file."""
    file_path = file_path or DEFAULT_NPM_PACKAGES_FILE
    npm_data = load_json(file_path=file_path)
    packages = npm_data["data"]

    if include_stdlib:
        packages += JAVASCRIPT_STDLIB

    packages = set(packages)  # remove duplicates
    return sorted(packages)


def _load_rust_libraries(
    file_path: str | None = None,
    include_stdlib: bool = True,
    **kwargs,
) -> list[str]:
    """Loads the rust crate names from a JSON file."""
    file_path = file_path or DEFAULT_RUST_CRATES_FILE
    crates_data = load_json(file_path=file_path)
    packages = crates_data["data"]

    if include_stdlib:
        packages += RUST_STDLIB

    packages = set(packages)  # remove duplicates
    return sorted(packages)


@cache
def load_known_libraries(
    language: str = "python",
    file_path: str | None = None,
    **kwargs,
) -> list[str]:
    """Loads known valid libraries for the given programming language."""
    if language == "python":
        libraries = _load_python_libraries(
            file_path=file_path,
            **kwargs,
        )
        return libraries

    elif language == "javascript":
        libraries = _load_javascript_libraries(
            file_path=file_path,
            **kwargs,
        )
        return libraries

    elif language == "rust":
        libraries = _load_rust_libraries(
            file_path=file_path,
            **kwargs,
        )
        return libraries

    else:
        raise ValueError(f"Unsupported language: {language}")


@cache
def load_library_documentation(
    file_path: str | None = None,
) -> dict[str, dict[str, set[str]]]:
    """
    Loads the library documentation data from a JSON file.
    """
    # use default file path if not provided, load the data
    file_path = file_path or DEFAULT_DOCUMENTATION_FILE
    file_data = load_json(file_path=file_path)
    documentation = file_data["data"]

    members = {
        _lib: {
            "modules": set(_data["modules"]),
            "members": {_m.lower() for _m in _data["members"]},
            "latest": _data["latest"],
            "versions": _data["versions"],
        }
        for _lib, _data in documentation.items()
    }
    return members
