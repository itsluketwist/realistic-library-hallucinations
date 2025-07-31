"""Test library methods from the src.libraries.check module."""

from src.libraries.check import check_for_library, check_for_unknown_libraries


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
    present, used = check_for_library(
        response=response,
        library="numpy",
    )
    assert present is True
    assert used is True
    present, used = check_for_library(
        response=response,
        library="pandas",
    )
    assert present is True
    assert used is True
    present, used = check_for_library(
        response=response,
        library="matplotlib",
    )
    assert present is True
    assert used is False

    # check for a library that is not imported
    present, used = check_for_library(
        response=response,
        library="sklearn",
    )
    assert present is False
    assert used is False

    response_with_install = (
        "Before running this code do `pip install numpy`, `pip install pandas matplotlib`, or:\n"
        "```bash\n"
        "pip install sklearn\n"
        "```\n"
        "And then run the code:\n"
        "```python\n"
        "from pandas import DataFrame\n"
        "x = DataFrame([1, 2, 3])\n"
        "print(x)\n"
        "```\n"
    )

    # check for libraries included via install commands
    present, used = check_for_library(
        response=response_with_install,
        library="pandas",
    )
    assert present is True
    assert used is True
    present, used = check_for_library(
        response=response_with_install,
        library="numpy",
    )
    assert present is True
    assert used is False
    present, used = check_for_library(
        response=response_with_install,
        library="matplotlib",
    )
    assert present is True
    assert used is False
    present, used = check_for_library(
        response=response_with_install,
        library="sklearn",
    )
    assert present is True
    assert used is False


def test_check_for_unknown_libraries(test_pypi_packages_file):
    """Test the check_for_unknown_libraries function."""
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
        check_for_unknown_libraries(
            response=response,
            pypi_packages_file=test_pypi_packages_file,
        )
        == set()
    )

    # a single hallucinated library
    response = (
        "Here is some code that imports libraries:\n"
        "First do this `pip install numpy`\n"
        "And then run the code:\n"
        "```python\n"
        "import numpy as np\n"
        "from valid_library import check_valid\n"
        "import hallucinated_lib\n"
        "x = check_valid(np.array([1, 2, 3]))\n"
        "print(x)\n"
        "```\n"
    )
    assert check_for_unknown_libraries(
        response=response,
        pypi_packages_file=test_pypi_packages_file,
    ) == {
        "hallucinated_lib",
    }

    # many hallucinated libraries, including installs
    response = (
        "Here is some code that imports libraries:\n"
        "First do this `pip install really_bad_hallucination`\n"
        "Then a multi-line install command:\n"
        "```bash\n"
        "pip install hallucinated_lib\n"
        "pip install hallucinated_numpy\n"
        "```\n"
        "And then run the code:\n"
        "```python\n"
        "import numpy as np\n"
        "from another_bad_hallucination import something\n"
        "import this_cant_be_real as pd\n"
        "x = np.array([1, 2, 3])\n"
        "print(x)\n"
        "```\n"
    )
    assert check_for_unknown_libraries(
        response=response,
        pypi_packages_file=test_pypi_packages_file,
    ) == {
        "hallucinated_lib",
        "really_bad_hallucination",
        "this_cant_be_real",
        "another_bad_hallucination",
        "hallucinated_numpy",
    }
