"""Code to generate responses from LLMs."""

from llm_cgr import get_llm, timeout

from src.constants import MODEL_DEFAULTS
from src.libraries.tools import create_library_check_tool


def generate_model_responses(
    prompt: str,
    models: list[str],
    samples: int = 3,
    system_prompt: str | None = None,
    temperature: float | None = None,
    top_p: float | None = None,
    max_tokens: int | None = None,
    timeout_seconds: int = 60,
    tools: bool = False,
) -> tuple[dict[str, list[str]], list[dict[str, str]], dict[str, list[list[dict]]]]:
    """
    Generate responses for the given model and tasks.

    When tools=True, OpenAI models are given a PyPI-checking tool during generation;
    non-OpenAI models are unaffected and receive empty tool-call logs.
    Returns a 3-tuple of (responses, errors, tool_calls), where tool_calls maps
    each model to a per-sample list of tool call records.
    """
    responses: dict[str, list[str]] = {}
    errors: list[dict[str, str]] = []
    tool_calls: dict[str, list[list[dict]]] = {}

    for model in models:
        # configure model parameters, falling back to per-model defaults
        _temperature = temperature or MODEL_DEFAULTS.get(model, {}).get("temperature")
        _top_p = top_p or MODEL_DEFAULTS.get(model, {}).get("top_p")
        _max_tokens = max_tokens or MODEL_DEFAULTS.get(model, {}).get("max_tokens")

        # tool calls are only supported for openai models in llm_cgr
        is_openai = "gpt" in model or model.startswith("o")

        responses[model] = []
        tool_calls[model] = []

        for _iter in range(samples):
            try:
                sample_log: list[dict] = []

                if tools and is_openai:
                    # create a fresh tool+log pair per sample so logs don't bleed across samples
                    _tool, sample_log = create_library_check_tool()
                    llm = get_llm(
                        model=model,
                        system=system_prompt,
                        temperature=_temperature,
                        top_p=_top_p,
                        max_tokens=_max_tokens,
                        tools=[_tool],
                    )
                else:
                    # do each query in a new session
                    llm = get_llm(
                        model=model,
                        system=system_prompt,
                        temperature=_temperature,
                        top_p=_top_p,
                        max_tokens=_max_tokens,
                    )

                with timeout(seconds=timeout_seconds):
                    _response = llm.chat(user=prompt)
                    responses[model].append(_response)

            except Exception as e:
                # handle any errors
                errors.append(
                    {
                        "model": model,
                        "index": str(_iter),
                        "error": f"{type(e).__name__}: {str(e)}",
                    }
                )

            tool_calls[model].append(sample_log)

    return responses, errors, tool_calls
