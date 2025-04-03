# **research-template**

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

todo

## *structure*

todo

## *installation*

Clone the repository code:

```shell
git clone https://github.com/itsluketwist/research-template.git
```

Once cloned, install the requirements locally in a virtual environment:

```shell
python -m venv .venv

. .venv/bin/activate

pip install -r requirements.lock
```

## *development*

Install and use pre-commit to ensure code is in a good state:

```shell
pre-commit install

pre-commit autoupdate

pre-commit run --all-files
```

Use `uv` for dependency management, first add to `requirements.txt`. Then install `uv` and version lock with:

```shell
pip install uv

uv pip compile requirements.txt -o requirements.lock
```


## *citation*

todo
