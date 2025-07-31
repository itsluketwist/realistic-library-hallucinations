"""Test member methods from the src.libraries.check module."""

from src.libraries.check import check_for_member, check_for_unknown_members


def test_check_for_member():
    """Test the check_for_member function."""
    response = (
        "Here is some code that uses a specific member:\n"
        "```python\n"
        "import numpy as np\n"
        "x = np.array([1, 2, 3])\n"
        "print(x)\n"
        "```\n"
    )

    # check for a member that is used
    assert (
        check_for_member(
            response=response,
            member="numpy.array",
        )
        is True
    )

    # check for a member that is not used
    assert (
        check_for_member(
            response=response,
            member="numpy.mean",
        )
        is False
    )


def test_check_for_unknown_members():
    """Test the check_for_unknown_members function."""
    # no unknown members
    response = (
        "Here is some code that uses a specific member:\n"
        "```python\n"
        "import numpy as np\n"
        "x = np.array([1, 2, 3])\n"
        "print(x)\n"
        "```\n"
    )
    assert (
        check_for_unknown_members(
            response=response,
            library="numpy",
        )
        == set()
    )

    # a single unknown member
    response = (
        "Here is some code that uses a specific member:\n"
        "```python\n"
        "import numpy as np\n"
        "x = np.hallucinated_member([1, 2, 3])\n"
        "print(x)\n"
        "```\n"
    )
    assert check_for_unknown_members(
        response=response,
        library="numpy",
    ) == {"numpy.hallucinated_member"}

    # many unknown members
    response = (
        "Here is some code that uses a many library members:\n"
        "```python\n"
        "import numpy as np\n"
        "from numpy.hallucinated_module import do_thing\n"
        "from pandas import DataFramingStuff\n"
        "x = np.hallucinated_member(DataFramingStuff([1, 2, 3]))\n"
        "print(x)\n"
        "```\n"
    )
    assert check_for_unknown_members(
        response=response,
        library="numpy",
    ) == {
        "numpy.hallucinated_member",
        "numpy.hallucinated_module.do_thing",
    }
    assert check_for_unknown_members(
        response=response,
        library="pandas",
    ) == {
        "pandas.DataFramingStuff",
    }

    # check for unknown member when module is different than expected
    response = (
        "Here is some code that uses a specific member:\n"
        "```python\n"
        "from mpl_toolkits import hallucination\n"
        "```\n"
    )
    assert check_for_unknown_members(
        response=response,
        library="matplotlib",
    ) == {
        "mpl_toolkits.hallucination",
    }
