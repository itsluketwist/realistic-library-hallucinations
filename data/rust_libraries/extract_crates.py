"""Extract crate names from the raw crates.csv and save as a JSON file."""

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


# paths relative to this script
RAW_CSV = Path(__file__).parent / "raw" / "crates.csv"
OUTPUT_JSON = Path(__file__).parent / "crates_data.json"


def extract_crate_names() -> list[str]:
    """Read crates.csv and return a list of all crate names.

    Returns the crate names as a list of strings.
    """
    csv.field_size_limit(sys.maxsize)

    names = []
    with open(RAW_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"].strip()
            if name:
                names.append(name)
    return sorted(names)


def main() -> None:
    """Extract crate names and write them to crates_data.json."""
    print(f"Reading crates from {RAW_CSV} ...")
    names = extract_crate_names()
    print(f"Found {len(names):,} crate names.")

    # match the format used by npm_data.json
    output = {
        "datetime": datetime.now(tz=timezone.utc).isoformat(),
        "data": names,
    }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)

    print(f"Saved to {OUTPUT_JSON}.")


if __name__ == "__main__":
    main()
