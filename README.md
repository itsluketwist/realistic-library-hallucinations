# **code-hallucinations**

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

## *installation*

Clone the repository code:

```shell
git clone https://github.com/itsluketwist/code-hallucinations.git
```

Once cloned, install the requirements locally in a virtual environment:

```shell
python -m venv .venv

. .venv/bin/activate

pip install -r requirements.txt
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

uv pip compile requirements.in -o requirements.txt
```

## *citation*

todo
