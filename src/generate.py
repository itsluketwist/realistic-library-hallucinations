"""Code to generate responses from LLMs."""

from llm_cgr import get_llm
from tqdm import tqdm

from src.check_library import check_for_library, check_unknown_libraries
from src.constants import LIB_SEP


def generate_model_responses(
    models: list[str],
    prompts: dict[str, str],
    samples: int = 3,
    temperature: float | None = None,
) -> tuple[dict, list]:
    """
    Generate responses for the given model and tasks.

    Returns a tuple containing the dictionary of model generations for each prompt,
    and the list of errors hit when generating responses.
    """
    results: dict[str, dict] = {}  # _id -> {prompt, responses}
    errors = []
    for _id, prompt in tqdm(prompts.items()):
        task_library = _id.split(LIB_SEP)[1] if LIB_SEP in _id else None
        responses: dict[str, list[list[str]]] = {}  # model -> [responses]
        for model in models:
            responses[model] = []
            for _ in range(samples):
                try:
                    # do each query in a new session
                    llm = get_llm(model=model)
                    response_one = llm.chat(
                        user=prompt,
                        temperature=temperature,
                    )
                    _responses = [response_one]

                    # check for hallucinations
                    if task_library:
                        imported, _ = check_for_library(
                            response=response_one,
                            library=task_library,
                        )
                        hallus = {task_library} if imported else set()
                    else:
                        hallus = check_unknown_libraries(response=response_one)

                    if hallus:
                        # give the model a chance to fix its mistake
                        response_two = llm.chat(
                            user=_get_rebuttal_prompt(hallus=hallus),
                            temperature=temperature,
                        )
                        _responses.append(response_two)

                    responses[model].append(_responses)

                except Exception as e:
                    # handle any errors
                    errors.append(
                        {
                            "prompt": _id,
                            "model": model,
                            "error": str(e),
                        }
                    )

        # save prompt responses
        results[_id] = {
            "prompt": prompt,
            "responses": responses,
        }

    return results, errors


def _get_rebuttal_prompt(hallus: set[str]) -> str:
    """
    Create the rebuttal prompt for the hallucinated libraries.
    """
    if len(hallus) == 1:
        libraries = f"library {hallus.pop()} does"
    elif len(hallus) == 2:
        libraries = f"libraries {hallus.pop()} and {hallus.pop()} do"
    else:
        _hallu = hallus.pop()
        libraries = f"libraries {', '.join(hallus)}, and {_hallu} do"

    return f"The imported Python {libraries} not seem to exist, can you try again?"
