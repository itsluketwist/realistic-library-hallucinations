"""Code to generate responses from LLMs."""

from llm_cgr import get_client
from tqdm import tqdm


def generate_model_responses(
    models: list[str],
    prompts: dict[str, str],
    n: int = 3,
    temperature: float | None = None,
) -> dict:
    """
    Generate potential hallucinations for the given model and tasks.

    Returns the dictionary of model generations for each prompt.
    """
    results = {}
    for _id, prompt in tqdm(prompts.items()):
        responses = {}
        for model in models:
            # query each model
            client = get_client(model=model)
            model_responses = client.complete(
                user=prompt,
                temperature=temperature,
                n=n,
            )
            responses[model] = model_responses

        # save prompt responses
        results[_id] = {
            "prompt": prompt,
            "responses": responses,
        }

    return results
