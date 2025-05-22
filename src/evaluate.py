"""Code to identify hallucinations in responses."""

from collections import defaultdict

from llm_cgr import load_json, save_json

from src.check_library import check_for_library, check_unknown_libraries


def evaluate_library_hallucinations(
    results_file: str,
) -> dict:
    """
    Evaluate the libraries found in model responses, identifying any hallucinations.
    Saves the analysis to the results file.
    """
    # load the generations to evaluate
    results_data = load_json(file_path=results_file)
    generations = results_data["generations"]
    tasks = results_data["metadata"]["tasks"]
    n = results_data["metadata"]["n"]

    # extract models from generations
    for _gen in generations.values():
        models = list(_gen["responses"].keys())
        break

    hallucinations: defaultdict[str, list[str]] = defaultdict(list)
    libraries: dict[str, set] = {m: set() for m in models}
    task_ids: dict[str, set] = {m: set() for m in models}
    counts = {m: 0 for m in models}

    # loop through models and tasks, checking for hallucinations
    for _id, data in generations.items():
        for model, responses in data["responses"].items():
            if "//" in _id:
                # check for hallucinations of the given library
                check_library = _id.split("//")[1]
                for _response in responses:
                    imported, _ = check_for_library(
                        response=_response, library=check_library
                    )
                    if imported:
                        task_ids[model].add(_id)
                        counts[model] += 1

            else:
                # check for any hallucinated libraries
                for _response in responses:
                    if hallus := check_unknown_libraries(response=_response):
                        libraries[model].update(hallus)
                        task_ids[model].add(_id)
                        counts[model] += 1

                        for hallu in hallus:
                            hallucinations[hallu].append(_response)

            # else:
            #     print(f"Incorrect type for prompt responses: {type(responses)}")

    evaluations = {}
    for model in models:
        evaluations[model] = {
            "total": counts[model],
            "response_rate": counts[model] / (tasks * n),
            "task_ids": list(task_ids[model]),
            "task_count": len(task_ids[model]),
            "task_rate": len(task_ids[model]) / tasks,
            "libraries": list(libraries[model]),
            "lib_count": len(libraries[model]),
        }

    # save the evaluation data
    results_data["evaluations"] = evaluations
    results_data["hallucinations"] = dict(hallucinations)
    save_json(data=results_data, file_path=results_file)
    return results_data
