"""Test methods from the src.libraries.format module."""

import pytest

from src.libraries.format import format_python_list, python_normalise


def test_format_python_list():
    """Test the format_python_list function."""
    libraries = ["numpy_", ".pandas", "matplotlib", "matplotlib"]

    # with normalisation
    formatted = format_python_list(
        libraries=libraries,
        normalise=True,
    )
    assert formatted == ["numpy", "pandas", "matplotlib"]

    # only remove duplicates
    formatted = format_python_list(
        libraries=libraries,
        normalise=False,
    )
    assert formatted == ["numpy_", ".pandas", "matplotlib"]


@pytest.mark.parametrize(
    "name,expected",
    (
        ("nochange", "nochange"),
        ("MakeLower", "makelower"),
        (" strip spaces ", "strip_spaces"),
        ("re-place all.things", "re_place_all_things"),
        ("_strip_underscores_", "strip_underscores"),
    ),
)
def test_python_normalise(name, expected):
    """Test the python_normalise function."""
    assert python_normalise(name=name) == expected
