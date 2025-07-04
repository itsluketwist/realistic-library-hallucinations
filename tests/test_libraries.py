"""Test library utility methods."""

from src.libraries.check import check_for_library, check_for_unknown_imports
from src.libraries.format import format_library_names
from src.libraries.load import load_known_imports


def test_check_for_library():
    """Test the check_for_library function."""
    response = (
        "Here is some code that imports libraries:\n"
        "```python\n"
        "import numpy as np\n"
        "from pandas import DataFrame\n"
        "import matplotlib\n"
        "x = DataFrame(np.array([1, 2, 3]))\n"
        "print(x)\n"
        "```\n"
    )

    # check for both import types
    imported, used = check_for_library(
        response=response,
        library="numpy",
    )
    assert imported is True
    assert used is True
    imported, used = check_for_library(
        response=response,
        library="pandas",
    )
    assert imported is True
    assert used is True
    imported, used = check_for_library(
        response=response,
        library="matplotlib",
    )
    assert imported is True
    assert used is False

    # check for a library that is not imported
    imported, used = check_for_library(
        response=response,
        library="sklearn",
    )
    assert imported is False
    assert used is False


def test_check_unknown_libraries(test_pypi_packages_file):
    """Test the check_unknown_libraries function."""
    # no unknown libraries
    response = (
        "Here is some code that imports libraries:\n"
        "```python\n"
        "import numpy as np\n"
        "from valid_library import check_valid\n"
        "x = check_valid(np.array([1, 2, 3]))\n"
        "print(x)\n"
        "```\n"
    )
    assert (
        check_for_unknown_imports(
            response=response,
            pypi_packages_file=test_pypi_packages_file,
        )
        == set()
    )

    # a single hallucinated library
    response = (
        "Here is some code that imports libraries:\n"
        "```python\n"
        "import numpy as np\n"
        "from valid_library import check_valid\n"
        "import hallucinated_lib\n"
        "x = check_valid(np.array([1, 2, 3]))\n"
        "print(x)\n"
        "```\n"
    )
    assert check_for_unknown_imports(
        response=response,
        pypi_packages_file=test_pypi_packages_file,
    ) == {
        "hallucinated_lib",
    }

    # many hallucinated libraries
    response = (
        "Here is some code that imports libraries:\n"
        "```python\n"
        "import numpy as np\n"
        "import hallucinated_lib\n"
        "from really_bad_hallucination import something\n"
        "import this_cant_be_real as pd\n"
        "x = np.array([1, 2, 3])\n"
        "print(x)\n"
        "```\n"
    )
    assert check_for_unknown_imports(
        response=response,
        pypi_packages_file=test_pypi_packages_file,
    ) == {
        "hallucinated_lib",
        "really_bad_hallucination",
        "this_cant_be_real",
    }


def test_load_packages():
    """Test the load_packages function."""
    # load full package list
    full_packages = load_known_imports()
    assert len(full_packages) > 500000
    assert "numpy" in full_packages  # common
    assert "sktensor" in full_packages  # not from pypi
    assert "os" in full_packages  # stdlib

    # load packages without stdlib, check smaller
    no_stdlib_packages = load_known_imports(
        include_stdlib=False,
    )
    assert len(no_stdlib_packages) > 500000
    assert "numpy" in no_stdlib_packages  # common
    assert "sktensor" in no_stdlib_packages  # not from pypi
    assert "os" not in no_stdlib_packages  # stdlib
    assert len(no_stdlib_packages) < len(full_packages)

    # load packages without valid extra imports, check smaller
    no_valid_extras_packages = load_known_imports(
        include_valid_extras=False,
    )
    assert len(no_valid_extras_packages) > 500000
    assert "numpy" in no_valid_extras_packages  # common
    assert "sktensor" not in no_valid_extras_packages  # not from pypi
    assert "os" in no_valid_extras_packages  # stdlib
    assert len(no_valid_extras_packages) < len(full_packages)

    # load only pypi packages
    pypi_packages = load_known_imports(
        include_stdlib=False,
        include_valid_extras=False,
    )
    assert len(pypi_packages) > 500000
    assert "numpy" in pypi_packages  # common
    assert "sktensor" not in pypi_packages  # not from pypi
    assert "os" not in pypi_packages  # stdlib
    assert len(pypi_packages) < len(full_packages)


def test_format_library_names(test_pypi_packages_file):
    """Test the format_library_names function."""
    libraries = ["numpy_", ".pandas", "invalid lib with spaces", "valid-library"]

    # return all libraries
    formatted = format_library_names(
        libraries=libraries,
        valid=False,
        pypi_packages_file=test_pypi_packages_file,
    )
    assert formatted == ["invalid_lib_with_spaces"]

    # return only valid libraries
    formatted = format_library_names(
        libraries=libraries,
        valid=True,
        pypi_packages_file=test_pypi_packages_file,
    )
    assert formatted == ["numpy", "pandas", "valid_library"]
