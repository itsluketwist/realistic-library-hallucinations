"""Code to generate responses from LLMs."""

from llm_cgr import generate
from tqdm import tqdm


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
        responses: dict[str, list[str]] = {}  # model -> [responses]
        for model in models:
            responses[model] = []
            for _ in range(samples):
                try:
                    # do each query in a new session
                    _response = generate(
                        model=model,
                        user=prompt,
                        system=None,
                        temperature=temperature,
                    )
                    responses[model].append(_response)

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
