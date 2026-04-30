"""Test library methods from the src.libraries.check module."""

from src.libraries.check import check_for_library, check_for_unknown_libraries
from src.libraries.extract import extract_libraries


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
            installs_only=False,
            ground_truth_file=test_pypi_packages_file,
        )
        == set()
    )
    assert (
        check_for_unknown_libraries(
            response=response,
            installs_only=True,
            ground_truth_file=test_pypi_packages_file,
        )
        == set()
    )

    # a single hallucinated library
    response = (
        "Here is some code that imports libraries:\n"
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
        installs_only=False,
        ground_truth_file=test_pypi_packages_file,
    ) == {
        "hallucinated_lib",
    }
    assert check_for_unknown_libraries(
        response=response,
        installs_only=True,
        ground_truth_file=test_pypi_packages_file,
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
        "pip install numpy pandas\n"
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
        installs_only=False,
        ground_truth_file=test_pypi_packages_file,
    ) == {
        "hallucinated_lib",
        "really_bad_hallucination",
        "this_cant_be_real",
        "another_bad_hallucination",
        "hallucinated_numpy",
    }
    assert check_for_unknown_libraries(
        response=response,
        installs_only=True,
        ground_truth_file=test_pypi_packages_file,
    ) == {
        "hallucinated_lib",
        "really_bad_hallucination",
        "hallucinated_numpy",
    }


def test_extract_rust_libraries():
    """Test that extract_libraries correctly handles Rust cargo add commands and code blocks."""
    # cargo add is the primary extraction signal for rust
    response = (
        "First add the dependencies:\n"
        "`cargo add serde tokio`\n"
        "Then write the code:\n"
        "```rust\n"
        "use serde::{Deserialize, Serialize};\n"
        "use tokio::time::sleep;\n"
        "```\n"
    )
    installs, imports, _ = extract_libraries(
        response=response,
        language="rust",
    )

    # cargo add should populate installs
    assert "serde" in installs
    assert "tokio" in installs

    # use statements in rust code blocks should populate imports (via llm_cgr rust support)
    assert "serde" in imports
    assert "tokio" in imports


def test_check_for_rust_library():
    """Test check_for_library correctly identifies present and used Rust crates."""
    response = (
        "Add the dependency with `cargo add serde`\n"
        "```rust\n"
        "use serde::Deserialize;\n"
        "\n"
        "#[derive(Deserialize)]\n"
        "struct Config { name: String }\n"
        "```\n"
    )

    # serde is installed (cargo add) and imported (use statement), but only used via
    # a derive macro — llm_cgr does not track derive macros as function-call usage
    present, used = check_for_library(
        response=response,
        library="serde",
        language="rust",
    )
    assert present is True
    assert used is False

    # rand is not mentioned at all
    present, used = check_for_library(
        response=response,
        library="rand",
        language="rust",
    )
    assert present is False
    assert used is False


def test_check_for_unknown_rust_libraries(test_crates_packages_file):
    """Test check_for_unknown_libraries flags hallucinated Rust crates."""
    # no hallucinations — serde and tokio are in the test fixture
    response = (
        "```bash\n"
        "cargo add serde tokio\n"
        "```\n"
        "```rust\n"
        "use serde::Deserialize;\n"
        "use tokio::runtime::Runtime;\n"
        "```\n"
    )
    assert (
        check_for_unknown_libraries(
            response=response,
            language="rust",
            ground_truth_file=test_crates_packages_file,
        )
        == set()
    )

    # hallucinated crate included via cargo add
    response = (
        "```bash\n"
        "cargo add serde fake-hallucinated-crate\n"
        "```\n"
        "```rust\n"
        "use serde::Deserialize;\n"
        "use fake_hallucinated_crate::something;\n"
        "```\n"
    )
    unknown = check_for_unknown_libraries(
        response=response,
        language="rust",
        ground_truth_file=test_crates_packages_file,
    )
    assert "fake-hallucinated-crate" in unknown
    assert "serde" not in unknown
