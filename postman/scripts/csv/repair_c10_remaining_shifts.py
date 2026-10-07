#!/usr/bin/env python3
from _paths import CSV_PATH


"""Final column-shift repair for C10 rows.

Detect shift pattern by looking at multiple fields together:
- If Steps looks like JSON body (starts with {) → shift back
- If Steps looks like "200" or "2xx" → swap with Expected HTTP
- If FE Mapping contains "[AUTH-C10-..." pattern → shift
"""
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


def is_json_body(s):
    if not s:
        return False
    s = s.strip()
    return s.startswith("{") and s.endswith("}")


def is_http_code(s):
    if not s:
        return False
    return bool(re.match(r"^2\d{2}$", s.strip()))


def is_step_text(s):
    """A step is like '1) GET /foo' or '1) POST /bar'"""
    if not s:
        return False
    return bool(re.match(r"^\d+\)\s+[A-Z]+\s+/", s.strip()))


def is_femapping(s):
    if not s:
        return False
    return s.startswith("[useAuth") or "useAuth" in s or "GAP-" in s


def is_postman_name(s):
    if not s:
        return False
    return bool(re.match(r"^\[AUTH-C\d{2}-", s))


def is_dependency_marker(s):
    """Dependency column has values like 'S', 'G', 'None', or test data alias names."""
    if not s:
        return True
    return s in ("S", "G", "None", "") or s.startswith("test") or "_FIXTURE" in s


def repair_row(r):
    """Comprehensive shift repair. Returns (repaired_row, list_of_actions)."""
    r2 = copy.deepcopy(r)
    actions = []

    # Snapshot columns we care about
    body = r2["Request Body (JSON)"]
    steps = r2["Steps"]
    expected_http = r2["Expected HTTP"]
    expected_schema = r2["Expected Schema/Fields"]
    side_effects = r2["Side Effects"]
    postconditions = r2["Postconditions"]
    cleanup = r2["Cleanup"]
    dependency = r2["Dependency"]
    fe_mapping = r2["FE Mapping"]
    postman_name = r2["Postman Request Name"]
    notes = r2["Notes"]

    # === Pattern 1: Body contains JSON, Steps contains HTTP code "200"
    # Means everything from Steps onwards is shifted LEFT by 1 (Steps has what should be Expected HTTP)
    if is_json_body(body) and is_http_code(steps):
        # Row is correctly aligned - no shift
        return r2, []

    # === Pattern 2: Steps contains "200" but Body is empty/non-JSON
    # Means Steps should be Expected HTTP, Expected HTTP should be Expected Schema
    if (not body or body.strip() in ("", "—", "-")) and is_http_code(steps) and not is_http_code(expected_http):
        # Shift Steps..Notes left by 1
        r2["Steps"] = expected_http
        r2["Expected HTTP"] = expected_schema
        r2["Expected Schema/Fields"] = side_effects
        r2["Side Effects"] = postconditions
        r2["Postconditions"] = cleanup
        r2["Cleanup"] = dependency
        r2["Dependency"] = fe_mapping
        r2["FE Mapping"] = postman_name
        r2["Postman Request Name"] = notes
        r2["Notes"] = ""
        actions.append("shift-left-1 (Steps=200)")
        return r2, actions

    # === Pattern 3: Steps contains JSON body
    # Means Steps should be Body, Expected HTTP should be Steps, etc.
    if is_json_body(steps):
        r2["Request Body (JSON)"] = steps
        r2["Steps"] = expected_http
        r2["Expected HTTP"] = expected_schema
        r2["Expected Schema/Fields"] = side_effects
        r2["Side Effects"] = postconditions
        r2["Postconditions"] = cleanup
        r2["Cleanup"] = dependency
        r2["Dependency"] = fe_mapping
        r2["FE Mapping"] = postman_name
        r2["Postman Request Name"] = notes
        r2["Notes"] = ""
        actions.append("shift-left-1 (Steps=body)")
        return r2, actions

    # === Pattern 4: FE Mapping contains Postman Request Name pattern
    if is_postman_name(fe_mapping) and is_postman_name(postman_name) and is_postman_name(notes):
        # All 3 columns are postman names - shift them
        r2["FE Mapping"] = postman_name
        r2["Postman Request Name"] = notes
        r2["Notes"] = ""
        actions.append("shift-left-FE-mapping")
        return r2, actions

    # === Pattern 5: FE Mapping looks like a TC_ID pattern [AUTH-C10-...
    if is_postman_name(fe_mapping):
        # FE Mapping is wrong, swap with Postman Request Name
        r2["FE Mapping"] = postman_name if is_femapping(postman_name) else ""
        r2["Postman Request Name"] = fe_mapping
        actions.append("swap-FE-Postman")
        return r2, actions

    return r2, []


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
        r2, actions = repair_row(r)
        new_rows.append(r2)
        if actions:
            repaired += 1
            print(f"  Repaired {r['TC_ID']}: {actions}")

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for r in new_rows:
            writer.writerow(r)

    print(f"\nC10 final-repair: {repaired} rows repaired")


if __name__ == "__main__":
    main()