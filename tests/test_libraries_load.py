"""Test methods from the src.libraries.load module."""

from src.constants import DOCUMENTED_LIBRARIES
from src.libraries.load import load_known_libraries, load_library_documentation


def test_load_known_libraries():
    """Test the load_known_libraries function."""
    # load full package list
    full_packages = load_known_libraries()
    assert len(full_packages) > 500000
    assert "numpy" in full_packages  # common
    assert "sktensor" in full_packages  # not from pypi
    assert "os" in full_packages  # stdlib

    # load packages without stdlib, check smaller
    no_stdlib_packages = load_known_libraries(
        include_stdlib=False,
    )
    assert len(no_stdlib_packages) > 500000
    assert "numpy" in no_stdlib_packages  # common
    assert "sktensor" in no_stdlib_packages  # not from pypi
    assert "os" not in no_stdlib_packages  # stdlib
    assert len(no_stdlib_packages) < len(full_packages)

    # load packages without valid extra imports, check smaller
    no_valid_extras_packages = load_known_libraries(
        include_valid_extras=False,
    )
    assert len(no_valid_extras_packages) > 500000
    assert "numpy" in no_valid_extras_packages  # common
    assert "sktensor" not in no_valid_extras_packages  # not from pypi
    assert "os" in no_valid_extras_packages  # stdlib
    assert len(no_valid_extras_packages) < len(full_packages)

    # load only pypi packages
    pypi_packages = load_known_libraries(
        include_stdlib=False,
        include_valid_extras=False,
    )
    assert len(pypi_packages) > 500000
    assert "numpy" in pypi_packages  # common
    assert "sktensor" not in pypi_packages  # not from pypi
    assert "os" not in pypi_packages  # stdlib
    assert len(pypi_packages) < len(full_packages)


def test_load_known_members():
    """Test the load_known_members function."""
    full_members = load_library_documentation()

    # check all expected libraries are present
    assert set(full_members.keys()) == set(DOCUMENTED_LIBRARIES)

    # check all libraries have expected data
    for data in full_members.values():
        assert isinstance(data, dict)
        assert "modules" in data
        assert "members" in data
        assert isinstance(data["modules"], set)
        assert isinstance(data["members"], set)

    # check some common library members
    assert "numpy.array" in full_members["numpy"]["members"]
    assert "pandas.dataframe" in full_members["pandas"]["members"]
