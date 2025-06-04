"""Code to generate responses from LLMs."""

from typing import Literal

from llm_cgr import get_llm
from tqdm import tqdm

from src.constants import LIB_SEP
from src.libraries.check import check_for_library, check_unknown_libraries


RebuttalType = Literal["explicit", "check"]


def generate_model_responses(
    models: list[str],
    prompts: dict[str, str],
    rebuttal_type: RebuttalType | None = None,
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
                        imported = check_for_library(
                            response=response_one,
                            library=task_library,
                        )
                        hallus = {task_library} if imported else set()
                    else:
                        hallus = check_unknown_libraries(response=response_one)

                    if hallus and rebuttal_type is not None:
                        # give the model a chance to fix its mistake
                        response_two = llm.chat(
                            user=_get_rebuttal_prompt(
                                type=rebuttal_type, hallus=hallus
                            ),
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


def _get_rebuttal_prompt(
    type: Literal["explicit", "check"],
    hallus: set[str],
) -> str:
    """
    Create the rebuttal prompt for the hallucinated libraries.
    """
    if type == "check":
        return "Please double-check your code and correct any errors you find."

    elif type == "explicit":
        if len(hallus) == 1:
            libraries = f"library {hallus.pop()} does"
        elif len(hallus) == 2:
            libraries = f"libraries {hallus.pop()} and {hallus.pop()} do"
        else:
            _hallu = hallus.pop()
            libraries = f"libraries {', '.join(hallus)}, and {_hallu} do"

        return f"The imported Python {libraries} not seem to exist, can you try again?"

    else:
        raise ValueError(
            f"Unknown rebuttal type: {type}. Must be 'explicit' or 'check'."
        )
