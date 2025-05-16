"""Code to generate responses from LLMs."""

from llm_cgr import get_client
from tqdm import tqdm


def generate_model_responses(
    models: list[str],
    prompts: dict[str, str],
    samples: int = 3,
    temperature: float | None = None,
) -> tuple[dict, list]:
    """
    Generate potential hallucinations for the given model and tasks.

    Returns a tuple containing the dictionary of model generations for each prompt,
    and the list of errors hit when generating responses.
    """
    results = {}
    errors = []
    for _id, prompt in tqdm(prompts.items()):
        responses = {}
        for model in models:
            try:
                # query each model
                client = get_client(model=model)
                model_responses = client.generate(
                    user=prompt,
                    samples=samples,
                    temperature=temperature,
                )
                responses[model] = model_responses

            except Exception as e:
                # handle any errors
                errors.append(
                    {
                        "prompt": _id,
                        "model": model,
                        "error": str(e),
                    }
                )
                responses[model] = []

        # save prompt responses
        results[_id] = {
            "prompt": prompt,
            "responses": responses,
        }

    return results, errors
