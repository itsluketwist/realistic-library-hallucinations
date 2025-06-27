"""Base experiments to look for hallucinations when generating code."""

from typing import Literal, get_args

from llm_cgr import experiment, load_json

from src.constants import CHOOSE_PROMPT, SPECIFY_PROMPT
from src.experiment import run_experiment


CONTROL_RUN_ID = "control/{run_id}"

ControlRunTypes = Literal["choose", "specify"]


@experiment
def run_control_experiment(
    run_id: ControlRunTypes,
    models: list[str],
    dataset_file: str,
    **kwargs,  # see run_experiment for details
):
    """
    Run a simple experiment to see if hallucinations occur when writing code.

    Each dataset record must have a "task" key for the task description and a "libraries" key,
    containing a dictionary of library names.
    e.g. {"task_id": {"task": "description", "libraries": {"base": ["numpy", ... ], ...}}, ...}
    """
    dataset = load_json(file_path=dataset_file)
    if run_id == "choose":
        # free to choose any library they want
        prompts = {
            _id: CHOOSE_PROMPT.format(
                task=_data["task"],
            )
            for _id, _data in dataset.items()
        }

    elif run_id == "specify":
        # must use the specified library
        prompts = {
            _id: SPECIFY_PROMPT.format(
                library=_data["libraries"]["base"][0],
                task=_data["task"],
            )
            for _id, _data in dataset.items()
        }

    else:
        raise ValueError(
            f"Invalid run_id: {run_id}. Use one of {get_args(ControlRunTypes)}."
        )

    run_experiment(
        run_id=CONTROL_RUN_ID.format(run_id=run_id),
        models=models,
        prompts=prompts,
        dataset_file=dataset_file,
        **kwargs,
    )
