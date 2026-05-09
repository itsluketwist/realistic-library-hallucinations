"""Tool definitions for tool-augmented generation experiments."""

from llm_cgr import Tool

from src.libraries.format import python_normalise
from src.libraries.load import load_known_libraries


def create_library_check_tool() -> tuple[Tool, list[dict]]:
    """
    Creates a PyPI-existence checking tool with its own per-sample call log.

    The returned list is mutated in-place each time the tool is invoked, so
    callers can inspect it after generation completes. Call this once per sample
    to get a fresh log for that sample.
    Returns a (Tool, call_log) pair.
    """
    # load_known_libraries is cached, so this is effectively free after the first call
    valid_set: set[str] = set(load_known_libraries())
    call_log: list[dict] = []

    def check_library_exists(library: str) -> str:
        # normalise to match how the pypi cache stores names
        normalised = python_normalise(library)
        exists = normalised in valid_set
        call_log.append(
            {
                "library": library,
                "normalised": normalised,
                "exists": exists,
            }
        )
        return "true" if exists else "false"

    tool = Tool(
        name="check_library_exists",
        description=(
            "Check whether a Python library is a real, installable PyPI package. "
            "Returns 'true' if the library exists, 'false' if it does not."
        ),
        parameters={
            "type": "object",
            "properties": {
                "library": {
                    "type": "string",
                    "description": "The Python import name to check (e.g. 'numpy', 'pandas').",
                },
            },
            "required": ["library"],
        },
        fn=check_library_exists,
    )
    return tool, call_log
