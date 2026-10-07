#!/usr/bin/env python3
from _paths import CSV_PATH


"""Repair remaining column shifts in C10 rows that have Expected HTTP set
to a non-3-digit value (means it's been shifted).

For these rows, shift all columns from Steps onward LEFT by 1 to align."""
import csv
import copy
import re


HEADER = [
    "TC_ID", "Cluster", "Feature", "Method", "Full Endpoint", "Scenario",
    "Type", "Technique", "Priority", "Actor", "Tenant", "Contract Status",
    "Preconditions", "Test Data Alias", "Headers", "Path/Query Params",
    "Request Body (JSON)", "Steps", "Expected HTTP", "Expected Schema/Fields",
    "Side Effects", "Postconditions", "Cleanup", "Dependency", "FE Mapping",
    "Postman Request Name", "Notes"
]


def main():
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    new_rows = []
    repaired = 0
    for r in rows:
        if not r["TC_ID"].startswith("AUTH-C10-"):
            new_rows.append(r)
            continue
        r2 = copy.deepcopy(r)
        # Check if Expected HTTP column doesn't match 3-digit pattern
        eh = r2["Expected HTTP"]
        if eh and not re.match(r"^2\d{2}$", eh.strip()) and not re.match(r"^2\d{2}\s", eh.strip()):
            # Shift Steps...Notes left by 1
            r2["Steps"] = r["Request Body (JSON)"]
            r2["Expected HTTP"] = r["Steps"]
            r2["Expected Schema/Fields"] = r["Expected HTTP"]
            r2["Side Effects"] = r["Expected Schema/Fields"]
            r2["Postconditions"] = r["Side Effects"]
            r2["Cleanup"] = r["Postconditions"]
            r2["Dependency"] = r["Cleanup"]
            r2["FE Mapping"] = r["Dependency"]
            r2["Postman Request Name"] = r["FE Mapping"]
            r2["Notes"] = r["Postman Request Name"]
            r2["Request Body (JSON)"] = ""
            repaired += 1
            print(f"  Repaired {r['TC_ID']} (shifted 1 from Steps)")
        new_rows.append(r2)

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for r in new_rows:
            writer.writerow(r)

    print(f"\nC10 shift-repair: {repaired} rows repaired")


if __name__ == "__main__":
    main()