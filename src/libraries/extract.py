"""Methods to extract libraries and library members from model responses."""

import re

from llm_cgr import CodeBlock, Markdown

from src.libraries.format import python_normalise


# regex to extract libraries from `pip install ...` statements
PIP_INSTALL_REGEX = re.compile(
    pattern=r"[\n`]pip[^\S\n\r]+install[^\S\n\r]+([A-Za-z0-9_.-]+(?:[^\S\n\r]+[A-Za-z0-9_.-]+)*)",
)

# regex to ensure member paths end at a class name
TRIM_MEMBER_PATH_REGEX = re.compile(
    pattern=r"^((?:[A-Za-z_][A-Za-z0-9_]*\.)*?[A-Z][A-Za-z0-9_]*)(?:\..*)?$",
)


def extract_python(response: str) -> list[CodeBlock]:
    """
    Extract the python code blocks from the model response.

    Returns a list of text from the python code blocks.
    """
    # first try to parse the response as markdown
    _markdown = Markdown(text=response)

    if len(_markdown.code_blocks) > 0:
        return _markdown.code_blocks
    else:
        # if no code blocks are found, try to parse the whole response as a codeblock
        _block = CodeBlock(language="python", text=response)
        if _block.valid:
            return [_block]

    return []


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
    for code in extract_python(response=response):
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
    for code in extract_python(response=response):
        members.update(code.lib_imports)

        for lib, usages in code.lib_usage.items():
            for _usage in usages:
                _member = f"{lib}.{_usage['member']}"
                _trimmed = TRIM_MEMBER_PATH_REGEX.match(_member)
                members.add(_trimmed.group(1) if _trimmed else _member)

    return members
