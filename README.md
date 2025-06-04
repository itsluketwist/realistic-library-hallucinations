# **library-hallucinations**

<div>
    <!-- badges from : https://shields.io/ -->
    <!-- logos available : https://simpleicons.org/ -->
    <a href="https://creativecommons.org/licenses/by-sa/4.0/">
        <img alt="CC-BY-SA-4.0 License" src="https://img.shields.io/badge/Licence-CC_BY_SA_4.0-yellow?style=for-the-badge&logo=docs&logoColor=white" />
    </a>
    <a href="https://www.python.org/">
        <img alt="Python 3" src="https://img.shields.io/badge/Python_3-blue?style=for-the-badge&logo=python&logoColor=white" />
    </a>
</div>

## *about*

Just some prototyping and initial code for various code-hallucinations projects!

## *structure*

todo

- `data/` - The data used in the project.
- `output/` - The generated results.
- `src/` - The main project code.

## *installation*

The code requires Python 3.11 or later to run.
Ensure you have it installed with the command below, otherwise download and install it from [here](https://www.python.org/downloads/).

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

pip install -r requirements.txt
```

## *usage*

todo

## *tests*

This project includes unit tests for the hallucination detection functions,
to ensure LLM responses will be correctly processed.
Install [`pytest`](https://docs.pytest.org/en/stable/), and run the tests with:

```shell
pip install pytest

pytest tests
```

## *development*

We use [`pre-commit`](https://pre-commit.com/) for linting the code.
Install [`pre-commit`](https://pre-commit.com/) and run with:

```shell
pip install pre-commit

pre-commit run --all-files
```

We use [`uv`](https://astral.sh/blog/uv) for dependency management.
First add new dependencies to `requirements.in`.
Then install [`uv`](https://astral.sh/blog/uv) and version lock with:

```shell
pip install uv

uv pip compile requirements.in --output-file requirements.txt --upgrade
```

## *paper*

todo

## *citation*

todo
