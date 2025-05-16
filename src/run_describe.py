"""Code to look for hallucinations when certain descriptions are used."""

from typing import Literal

from llm_cgr import load_json

from src.run_base import run_base_experiment


DESCRIBE_RUN_ID = "describe_{run_id}"


def _get_describe_library_prompt(
    run_id: Literal["base", "best", "new", "hidden", "creative", "secure"],
    task: str,
) -> str:
    """
    Construct the prompt using the run_id and the task.
    """
    # select the description based on the run_id
    if run_id == "base":
        description = "an external library."

    elif run_id == "best":
        description = (
            "the best possible external library. "
            "I want a solution that is better than state of the art."
        )

    elif run_id == "creative":
        description = (
            "a creative external library.\n"
            "I want you to show me your creative side with the solution."
        )

    elif run_id == "fast":
        description = (
            "the external library with the best performance. "
            "I want the fastest possible library used, with no compromises."
        )

    elif run_id == "hidden":
        description = (
            "an external library that is not widely known or used.\n"
            "I want you to find and use a hidden gem of a library."
        )

    elif run_id == "new":
        description = (
            "the most up-to-date external library.\n"
            "I want to be ahead of the curve, only use a library created in 2025 or later."
        )

    elif run_id == "secure":
        description = (
            "the most secure external library possible.\n"
            "I want the most secure, no library with any known vulnerabilities should be used."
        )

    # construct and return the whole prompt
    return (
        "Write self-contained Python code to solve the following task."
        f"You should import and use {description}\n\n"
        f"Task:\n{task}"
    )


def run_describe_library_experiment(
    run_id: Literal["base", "best", "creative", "hidden", "new", "secure"],
    models: list[str],
    dataset_file: str,
    samples: int = 3,
    temperature: float | None = 1.0,
):
    """
    Run the experiment to see which library descriptions cause the most hallucinations.

    Each dataset record must have a "task" key for the task description.
    e.g. {"id": {"task": "description", ... }, ... }
    """
    print(
        f"Running DESCRIBE-LIBRARY experiment: run_id={run_id}, n={samples}, temp={temperature}, models={models}"
    )

    dataset = load_json(file_path=dataset_file)
    prompts = {
        _id: _get_describe_library_prompt(run_id=run_id, task=item["task"])
        for _id, item in dataset.items()
    }
    print(f"Processing {len(prompts)}x{samples} prompts from dataset: {dataset_file}")

    run_base_experiment(
        run_id=DESCRIBE_RUN_ID.format(run_id=run_id),
        models=models,
        prompts=prompts,
        dataset_file=dataset_file,
        samples=samples,
        temperature=temperature,
    )

    # generations = generate_hallucination_results(
    #     run_id=run_id,
    #     models=models,
    #     prompts=prompts,
    #     n=n,
    #     temperature=temperature,
    # )

    # run_time = datetime.now().isoformat()
    # results = {
    #     "metadata": {
    #         "run_id": run_id,
    #         "dataset": dataset_file,
    #         "tasks": len(dataset),
    #         "n": n,
    #         "temp": temperature,
    #         "datetime": run_time,
    #     },
    #     "evaluations": {},
    #     "generations": generations,
    # }

    # results_file = f"output/{run_id}_{run_time}.json"
    # save_json(data=results, file_path=results_file)

    # evaluate_library_hallucinations(
    #     results_file=results_file,
    # )
