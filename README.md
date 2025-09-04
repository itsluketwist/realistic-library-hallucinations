# **library-hallucinations**

Todo: fix up the test here...

<div>
    <!-- badges from : https://shields.io/ -->
    <!-- logos available : https://simpleicons.org/ -->
    <a href="https://creativecommons.org/licenses/by-sa/4.0/">
        <img alt="CC-BY-SA-4.0 License" src="https://img.shields.io/badge/Licence-CC_BY_SA_4.0-yellow?style=for-the-badge&logo=docs&logoColor=white" />
    </a>
    <a href="https://www.python.org/">
        <img alt="Python 3.11" src="https://img.shields.io/badge/Python_3.11-blue?style=for-the-badge&logo=python&logoColor=white" />
    </a>
    <a href="https://openai.com/blog/openai-api/">
        <img alt="OpenAI API" src="https://img.shields.io/badge/OpenAI_API-412991?style=for-the-badge&logo=openai&logoColor=white" />
    </a>
    <a href="https://docs.mistral.ai/api/">
        <img alt="Mistral API" src="https://img.shields.io/badge/Mistral_API-FA520F?style=for-the-badge&logo=mistralai&logoColor=white" />
    </a>
    <a href="https://api-docs.deepseek.com/">
        <img alt="DeepSeek API" src="https://img.shields.io/badge/DeepSeek_API-4E6CFA?style=for-the-badge&logoColor=white" />
    </a>
    <a href="https://api.together.ai/">
        <img alt="together.ai API" src="https://img.shields.io/badge/together.ai_API-B5B5B5?style=for-the-badge&logoColor=white" />
    </a>
</div>

## *about*

Just some prototyping and initial code for various code-hallucinations projects!

## *installation*

The code requires Python 3.11 or later to run.
Ensure you have it installed with the command below, otherwise download and install it from
[here](https://www.python.org/downloads/).

```shell
python --version
```

Now clone the repository code:

```shell
git clone **redacted**
```

Once cloned, install the requirements locally in a virtual environment:

```shell
python -m venv .venv

. .venv/bin/activate

pip install .
```

## *usage*

After [*installation*](#installation), there are 2 ways to run the experiment code.
The easiest of which is via the the [`main.ipynb`](main.ipynb) notebook, which fully describes
each experiment and provides the methods to run them.

You can also use the `run` command from your terminal - this is likely best if you want to
reproduce the experiments on an external server or in a [docker](https://www.docker.com/)
container.

```shell
run --dataset-file data/example.json
```

All other non-experiment code that likely only needed to be ran a single time is explained in,
and can be interfaced with, via it's corresponding Jupyter notebook.
These notebooks are contained in the [`notebooks/`](notebooks/) directory, and are described in the
[*structure*](#structure) section.

## *structure*

todo

- [`data/`](data/) - The data used in the project.
    - [`bigcodebench/`](data/bigcodebench/) - our versions and splits of the [BigCodeBench](https://bigcode-bench.github.io/) dataset.
        - [`bigcodebench_eval/`](data/bigcodebench/bigcodebench_eval/) - evaluation split used for our final experiments (*len=321*).
        - [`bigcodebench_full/`](data/bigcodebench/bigcodebench_full/) - our full dataset of processed BigCodeBench records (*len=356*).
        - [`bigcodebench_raw/`](data/bigcodebench/bigcodebench_raw/) - the fields we need from all records of the base [BigCodeBench](https://bigcode-bench.github.io/) dataset (*len=1140*).
        - [`bigcodebench_test/`](data/bigcodebench/bigcodebench_test/) - test split used for initial further testing, subset of the eval split (*len=100*).
        - [`bigcodebench_tune/`](data/bigcodebench/bigcodebench_tune/) - tune split used for initial prompt development, no overlap with the eval split (*len=35*).
    - [`libraries/`](data/libraries/) - ground truth library data used to detect hallucinations.
        - [`pypi_data.json`](data/libraries/pypi_data.json) - list of libraries available for download via [PyPI](https://pypi.org/).
        - [`documentation.json`](data/libraries/documentation.json) - library documentation data containing all members of the libraries used in the study.
    - [`stackexchange/`](data/stackexchange/) - question data from [Software Recommendations StackExchange](https://softwarerecs.stackexchange.com/), to determine common library descriptions by developers.
        - [`clusters_2025-07-06.json`](data/stackexchange/clusters_2025-07-06.json) - question ids clustered by their descriptive words, to determine the most common library descriptions.
        - [`library_questions_2025-07-04.json`](data/stackexchange/library_questions_2025-07-04.json) - questions related to libraries.
        - [`manual_analysis_2025-06-30.json`](data/stackexchange/manual_analysis_2025-06-30.json) - manual classification of 200 random questions to verify the automatic assignment of which questions are related to libraries.
        - [`ngrams_2025-07-04.json`](data/stackexchange/ngrams_2025-07-04.json) - n-grams extracted from library questions, mapped to the questions where they are contained.
        - [`recent_questions_2025-06-30.json`](data/stackexchange/recent_questions_2025-06-30.json) - the 2500 most recent questions.
- [`notebooks/`](notebooks/) - Jupyter notebooks containing one-time code and processes used to download and process data for experiments.
    - [`download_documentation.ipynb`](notebooks/download_documentation.ipynb) - code to download all library documentation containing their members.
    - [`download_python_libraries.ipynb`](notebooks/download_python_libraries.ipynb) - code to download all available libraries from [PyPI](https://pypi.org/).
    - [`generate_clusters.ipynb`](notebooks/generate_clusters.ipynb) - code to process the library questions and generate the clusters of questions based on the descriptive words they use.
    - [`generate_fabrications.ipynb`](notebooks/generate_fabrications.ipynb) - code to generate library/member typos and fabrications that could be used to solve tasks.
    - [`process_bigcodebench.ipynb`](notebooks/process_bigcodebench.ipynb) - code to download and process the [BigCodeBench](https://bigcode-bench.github.io/) dataset to suit our requirements.
    - [`query_stackexchange.ipynb`](notebooks/query_stackexchange.ipynb) - code that queries the [StackExchange API](https://api.stackexchange.com/) for library questions.
- [`output/`](output/) - The generated results.
    - todo
- [`src/`](src/) - The main project code that runs the experiments.
    - todo
- [`main.ipynb`](main.ipynb) - The main entrypoint for project code, allowing easy reproduction of all experiments.

## *development*

We use a few extra processes to ensure the code maintains a high quality.
First clone the project and create a virtual environment - as described above.
Now install the editable version of the project, with the development dependencies.

```shell
pip install --editable ".[dev]"
```

### *tests*

This project includes unit tests to ensure correct functionality.
Use [`pytest`](https://docs.pytest.org/en/stable/) to run the tests with:

```shell
pytest tests
```

### *linting*

We use [`pre-commit`](https://pre-commit.com/) to lint the code, run it using:

```shell
pre-commit run --all-files
```

### *dependencies*

We use [`uv`](https://astral.sh/blog/uv) for dependency management.
First add new dependencies to `requirements.in`.
Then version lock with [`uv`](https://astral.sh/blog/uv) using:

```shell
uv pip compile requirements.in --output-file requirements.txt --upgrade
```

## *paper*

todo

## *citation*

todo
