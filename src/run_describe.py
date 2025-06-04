"""Code to look for hallucinations when certain descriptions are used."""

from typing import Literal

from llm_cgr import experiment, load_json

from src.generate import RebuttalType
from src.run_base import run_base_experiment


DESCRIBE_RUN_ID = "describe/{run_id}"

DescribeRunTypes = Literal[
    "base",
    "best",
    "hidden",
    "creative",
    "secure",
    "rough",
    "unsung",
    "2022",
    "2023",
    "2024",
    "2025",
]


def _get_describe_library_prompt(
    run_id: DescribeRunTypes,
    task: str,
) -> str:
    """
    Construct the prompt using the run_id and the task.
    """
    # select the description based on the run_id
    if run_id == "best":
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

    elif run_id == "secure":
        description = (
            "the most secure external library possible.\n"
            "I want the most secure, no library with any known vulnerabilities should be used."
        )

    elif run_id == "rough":
        description = (
            "an external library with high potential.\n"
            "Find and use a diamond in the rough, a library that could be great with some work."
        )

    elif run_id == "unsung":
        description = (
            "an external library that deserves more credit.\n"
            "Find and use the unsung hero of libraries, that is often overlooked."
        )

    else:
        # use the default (run_id == "base" or None)
        description = "an external library."

    # construct and return the whole prompt
    return (
        "Write self-contained Python code to solve the following task."
        f"You should import and use {description}\n\n"
        f"Task:\n{task}"
    )


@experiment
def run_describe_library_experiment(
    run_id: DescribeRunTypes,
    models: list[str],
    dataset_file: str,
    rebuttal_type: RebuttalType | None,
    samples: int = 3,
    temperature: float | None = None,
):
    """
    Run the experiment to see which library descriptions cause the most hallucinations.

    Each dataset record must have a "task" key for the task description.
    e.g. {"id": {"task": "description", ... }, ... }
    """
    dataset = load_json(file_path=dataset_file)
    prompts = {
        _id: _get_describe_library_prompt(run_id=run_id, task=item["task"])
        for _id, item in dataset.items()
    }

    run_base_experiment(
        run_id=DESCRIBE_RUN_ID.format(run_id=run_id),
        models=models,
        prompts=prompts,
        dataset_file=dataset_file,
        rebuttal_type=rebuttal_type,
        samples=samples,
        temperature=temperature,
    )
