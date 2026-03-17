"""Functions for extracting and checking libraries in LLM responses."""

import re

from libhallubench.pypi import _normalise, load_known_libraries
from llm_cgr import CodeBlock, Markdown


# regex to extract libraries from `pip install ...` statements
PIP_INSTALL_REGEX = re.compile(
    pattern=r"[\n`]pip[^\S\n\r]+install[^\S\n\r]+([A-Za-z0-9_.-]+(?:[^\S\n\r]+[A-Za-z0-9_.-]+)*)",
)


def extract_libraries(
    response: str,
) -> tuple[set[str], set[str]]:
    """
    Extract installed and imported libraries from a model response.

    Returns a tuple of sets containing installed and imported library names.
    """
    # look for pip install commands in the response text
    installs = set()
    matches = PIP_INSTALL_REGEX.findall(string=response)
    for match in matches:
        installs.update(match.strip().split())

    # parse code blocks and extract imports
    imports = set()
    _markdown = Markdown(text=response, default_codeblock_language="python")
    code_blocks = _markdown.code_blocks

    # if no code blocks found, try parsing the whole response as code
    if not code_blocks:
        _block = CodeBlock(language="python", text=response)
        if _block.valid:
            code_blocks = [_block]

    for code in code_blocks:
        imports.update(code.ext_libs)
        imports.update(code.std_libs)

    # normalise all library names
    installs = {_normalise(lib) for lib in installs}
    imports = {_normalise(lib) for lib in imports}

    return installs, imports


def check_for_unknown_libraries(
    response: str,
    ground_truth_file: str | None = None,
) -> set[str]:
    """
    Check a model response for libraries that are not known valid packages.

    Returns a set of unknown (potentially hallucinated) library names.
    """
    installs, imports = extract_libraries(response=response)
    valid_libraries = load_known_libraries(file_path=ground_truth_file)

    # check all extracted libraries against the known valid list
    invalid = {
        library for library in (installs | imports) if library not in valid_libraries
    }

    return invalid
