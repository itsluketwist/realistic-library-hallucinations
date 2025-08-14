"""Code to identify hallucinations in responses and calculate metrics."""

from collections import defaultdict

from llm_cgr import load_json, save_json

from src.constants import HallucinationLevel
from src.libraries.check import (
    check_for_unknown_libraries,
    check_for_unknown_members,
    check_for_versions,
)
from src.libraries.extract import extract_python


def evaluate_hallucinations(
    results_file: str,
    check_installs_only: bool = False,
    ground_truth_file: str | None = None,
) -> dict:
    """
    Evaluate the libraries found in model responses, identifying any hallucinations.
    Saves the analysis to the results file.
    """
    # load the generations to evaluate
    results_data = load_json(file_path=results_file)
    generations = results_data["generations"]
    tasks: int = results_data["metadata"]["total_tasks"]
    samples: int = results_data["metadata"]["samples"]
    hallucination_level: HallucinationLevel = results_data["metadata"][
        "hallucination_level"
    ]

    # extract models from generations
    models = []
    for _gen in generations.values():
        models = list(_gen["responses"].keys())
        break

    response_ids: dict[str, set] = {
        m: set() for m in models
    }  # response ids with hallucinations
    task_ids: dict[str, set] = {
        m: set() for m in models
    }  # task ids with hallucinations
    hallus_per_model: dict[str, set] = {
        m: set() for m in models
    }  # libraries hallucinated by each model
    responses_per_hallu: defaultdict[str, dict[str, str]] = defaultdict(dict)

    responses_with_version: dict[str, list[str]] = {m: list() for m in models}
    no_code_responses: dict[str, list[str]] = {m: list() for m in models}

    # loop through models and tasks, checking for hallucinations
    for task_id, _task_data in generations.items():
        for model, _responses in _task_data["responses"].items():
            for _idx, _response in enumerate(_responses):
                response_id = f"{task_id} | {_idx}"

                # check the response contains python code
                if len(extract_python(response=_response)) == 0:
                    no_code_responses[model].append(response_id)
                    continue

                # handle library hallucinations
                if hallucination_level == HallucinationLevel.LIBRARY:
                    # check for any hallucinated libraries
                    _hallus = check_for_unknown_libraries(
                        response=_response,
                        installs_only=check_installs_only,
                        pypi_packages_file=ground_truth_file,
                    )

                # handle member hallucinations
                elif hallucination_level == HallucinationLevel.MEMBER:
                    # check for hallucinated members of the base library
                    _hallus = check_for_unknown_members(
                        response=_response,
                        library=_task_data["base_library"],
                        documentation_file=ground_truth_file,
                    )
                    _versions = check_for_versions(
                        response=_response,
                        library=_task_data["base_library"],
                        documentation_file=ground_truth_file,
                    )
                    if _hallus and _versions:
                        responses_with_version[model].append(
                            f"{response_id} | {_versions}"
                        )

                # handle errors
                else:
                    raise ValueError(
                        f"Invalid {hallucination_level=}, must be one of: "
                        f"{HallucinationLevel.options()}"
                    )

                # save all responses with hallucinations
                hallus_per_model[model].update(_hallus)
                for _hallu in _hallus:
                    responses_per_hallu[_hallu][response_id] = _response

                # check if a target fabrication is provided
                if _target := _task_data.get(f"target_{hallucination_level}"):
                    # update stats if the target library/member is hallucinated
                    if _target in _hallus:
                        response_ids[model].add(response_id)
                        task_ids[model].add(task_id)

                else:
                    # otherwise update stats if any library/member is hallucinated
                    if _hallus:
                        response_ids[model].add(response_id)
                        task_ids[model].add(task_id)

    # save the evaluation data
    results_data["evaluations"] = {
        model: {
            # core statistics
            "response_count": len(response_ids[model]),
            "response_rate": len(response_ids[model]) / (tasks * samples),
            "task_count": len(task_ids[model]),
            "task_rate": len(task_ids[model]) / tasks,
            # library details
            "hallucination_count": len(hallus_per_model[model]),
            "hallucinations": sorted(hallus_per_model[model]),
            # version details
            "version_count": responses_with_version[model],
        }
        for model in models
    }
    results_data["hallucinations"] = dict(responses_per_hallu)
    results_data["no_code_responses"] = dict(no_code_responses)
    save_json(data=results_data, file_path=results_file)
    return results_data
