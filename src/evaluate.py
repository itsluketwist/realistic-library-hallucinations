"""Code to identify hallucinations in responses."""

from collections import defaultdict

from llm_cgr import load_json, save_json

from src.constants import HallucinationLevel
from src.libraries.check import check_for_unknown_imports


def evaluate_hallucinations(
    results_file: str,
    pypi_packages_file: str | None = None,
) -> dict:
    """
    Evaluate the libraries found in model responses, identifying any hallucinations.
    Saves the analysis to the results file.
    """
    # load the generations to evaluate
    results_data = load_json(file_path=results_file)
    generations = results_data["generations"]
    tasks = results_data["metadata"]["total_tasks"]
    samples = results_data["metadata"]["samples"]
    run_level = results_data["metadata"]["run_level"]

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
    responses_per_hallu: defaultdict[str, list[str]] = defaultdict(list)

    # loop through models and tasks, checking for hallucinations
    for task_id, _task_data in generations.items():
        for model, _responses in _task_data["responses"].items():
            for _idx, _response in enumerate(_responses):
                # handle library hallucinations
                if run_level == HallucinationLevel.LIBRARY:
                    # check for any hallucinated libraries
                    _hallus = check_for_unknown_imports(
                        response=_response,
                        pypi_packages_file=pypi_packages_file,
                    )

                    # save responses with hallucinations
                    hallus_per_model[model].update(_hallus)
                    for _hallu in _hallus:
                        responses_per_hallu[_hallu].append(_response)

                    if _fake_library := _task_data.get("target_library"):
                        # update stats if the given library is hallucinated
                        if _fake_library in _hallus:
                            response_ids[model].add(f"{task_id} | {_idx}")
                            task_ids[model].add(task_id)

                    else:
                        # otherwise update stats if any library is hallucinated
                        if _hallus:
                            response_ids[model].add(f"{task_id} | {_idx}")
                            task_ids[model].add(task_id)

                # handle member hallucinations
                elif run_level == HallucinationLevel.MEMBER:
                    # member runs require a base library
                    # base_library = _task_data["base_library"]

                    # check for hallucinated members of the base library
                    # _hallus = check_for_unknown_members(
                    #     response=_response,
                    #     base_library=base_library,
                    # )

                    # save responses with hallucinations

                    # update hallucination stats

                    pass

                # handle errors
                else:
                    raise ValueError(
                        f"Invalid {run_level=}, must be one of: {HallucinationLevel.options()}"
                    )

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
        }
        for model in models
    }
    results_data["hallucinations"] = {
        "task_ids": {k: sorted(v) for k, v in task_ids.items()},
        "response_ids": {k: sorted(v) for k, v in response_ids.items()},
        "responses": dict(responses_per_hallu),
    }
    save_json(data=results_data, file_path=results_file)
    return results_data
