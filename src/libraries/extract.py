"""Methods to extract libraries and library members from model responses."""

import re

from llm_cgr import Markdown

from src.libraries.format import python_normalise


# regex to extract libraries from `pip install ...` statements
PIP_INSTALL_REGEX = re.compile(
    pattern=r"[\n`]pip[^\S\n\r]+install[^\S\n\r]+([A-Za-z0-9_.-]+(?:[^\S\n\r]+[A-Za-z0-9_.-]+)*)",
)


def extract_libraries(response: str) -> tuple[set[str], set[str], set[str]]:
    """
    Extract installed and imported libraries from the model response.

    Returns a tuple of sets containing installed libraries, imported libraries and used libraries.
    """
    # first look for `pip install ...` commands
    installs = set()
    matches = PIP_INSTALL_REGEX.findall(string=response)
    for match in matches:
        installs.update(match.strip().split())

    # then look for imports in python code blocks
    imports, usages = set(), set()
    for code in Markdown(text=response).code_blocks:
        if code.language != "python":
            # only check Python code blocks
            continue

        imports.update(code.ext_libs)
        imports.update(code.std_libs)
        usages.update(code.lib_usage.keys())

    # function to normalise library names before returning
    def _normalise(_libs):
        return {python_normalise(_l) for _l in _libs}

    return _normalise(installs), _normalise(imports), _normalise(usages)


def extract_members(response: str) -> set[str]:
    """
    Extract used library members from the model response.

    Returns a set of members used in the response.
    """
    members: set[str] = set()
    for code in Markdown(text=response).code_blocks:
        if code.language != "python":
            # only check Python code blocks
            continue

        for lib, usages in code.lib_usage.items():
            members.update(f"{lib}.{usage['member']}" for usage in usages)

    return members
