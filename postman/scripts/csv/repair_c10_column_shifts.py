#!/usr/bin/env python3
from _paths import CSV_PATH


"""Repair column shifts in C10 (SGOD Enterprises / Organizational) CSV rows.

Detects rows where Request Body (JSON) contains a Steps-like text pattern
or non-JSON content for endpoints that should not have a body, and shifts
all subsequent columns back to the right.

Also detects rows where the FE Mapping column contains the Postman Request Name
content (an obvious column shift marker).
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


def looks_like_step(s):
    return bool(s) and bool(re.match(r"^\d+\)\s", s.strip()))


def looks_like_expected_http(s):
    return bool(s) and bool(re.match(r"^\d{3}$", s.strip()))


def looks_like_femapping(s):
    """FE Mapping should be like '[useAuthFoo] → bar' or contain 'GAP-' marker."""
    if not s:
        return False
    if "useAuth" in s:
        return True
    if "GAP-" in s:
        return True
    if s.startswith("[useAuth"):
        return True
    return False


def is_valid_steps(s):
    return bool(s) and (re.match(r"^\d+\)\s", s) or s.startswith("1)"))


def is_valid_expected_http(s):
    return bool(s) and re.match(r"^2\d{2}$", s.strip())


def is_valid_request_body_json(s):
    """A valid JSON body starts with { or [ or empty, OR is a single token like tenantId=... or userId=..."""
    if not s:
        return True
    s = s.strip()
    if s.startswith("{") or s.startswith("["):
        return True
    # If contains "key=value" or "key=val," — likely params not body
    if "=" in s and not "{" in s:
        return False
    return False


def repair_row(r):
    """Detect and fix column shift. Returns (repaired_row, was_repaired, shift_amount)."""
    r2 = copy.deepcopy(r)
    body = r2["Request Body (JSON)"]
    steps = r2["Steps"]
    expected_http = r2["Expected HTTP"]
    expected_schema = r2["Expected Schema/Fields"]
    fe_mapping = r2["FE Mapping"]
    postman_name = r2["Postman Request Name"]

    # CASE 1: Body contains Steps-like text, shift left
    if looks_like_step(body):
        # All fields from Body onward are shifted right by 1
        # Shift back: Request Body = Steps, Steps = Expected HTTP, etc.
        new_body = steps
        new_steps = expected_http
        new_expected_http = expected_schema
        new_expected_schema = r2["Side Effects"]
        new_side_effects = r2["Postconditions"]
        new_postconditions = r2["Cleanup"]
        new_cleanup = r2["Dependency"]
        new_dependency = r2["FE Mapping"]
        new_fe_mapping = r2["Postman Request Name"]
        new_postman_name = r2["Notes"]

        r2["Request Body (JSON)"] = new_body
        r2["Steps"] = new_steps
        r2["Expected HTTP"] = new_expected_http
        r2["Expected Schema/Fields"] = new_expected_schema
        r2["Side Effects"] = new_side_effects
        r2["Postconditions"] = new_postconditions
        r2["Cleanup"] = new_cleanup
        r2["Dependency"] = new_dependency
        r2["FE Mapping"] = new_fe_mapping
        r2["Postman Request Name"] = new_postman_name
        r2["Notes"] = ""
        return r2, True, 1

    # CASE 2: FE Mapping contains Postman Request Name (shift by 4 columns)
    if postman_name and fe_mapping and postman_name in fe_mapping and re.match(r"^\[AUTH-C10", fe_mapping):
        # Shift left by 4
        new_fe_mapping = r2["Postman Request Name"]
        new_postman_name = r2["Notes"]
        new_notes = ""

        # Cleanup was originally FE Mapping position now
        r2["FE Mapping"] = new_fe_mapping
        r2["Postman Request Name"] = new_postman_name
        r2["Notes"] = new_notes
        return r2, True, 0  # special case, doesn't shift 1 but fixes the corruption

    # CASE 3: Body contains "key=value" without braces (params not body)
    if not is_valid_request_body_json(body) and "=" in body:
        # Move body content to Path/Query Params and shift left
        new_params = body
        new_body = ""
        new_steps = expected_http
        new_expected_http = expected_schema
        new_expected_schema = r2["Side Effects"]
        new_side_effects = r2["Postconditions"]
        new_postconditions = r2["Cleanup"]
        new_cleanup = r2["Dependency"]
        new_dependency = r2["FE Mapping"]
        new_fe_mapping = r2["Postman Request Name"]
        new_postman_name = r2["Notes"]

        r2["Path/Query Params"] = new_params
        r2["Request Body (JSON)"] = new_body
        r2["Steps"] = new_steps
        r2["Expected HTTP"] = new_expected_http
        r2["Expected Schema/Fields"] = new_expected_schema
        r2["Side Effects"] = new_side_effects
        r2["Postconditions"] = new_postconditions
        r2["Cleanup"] = new_cleanup
        r2["Dependency"] = new_dependency
        r2["FE Mapping"] = new_fe_mapping
        r2["Postman Request Name"] = new_postman_name
        r2["Notes"] = ""
        return r2, True, 1

    return r2, False, 0


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
        r2, was_repaired, shift = repair_row(r)
        new_rows.append(r2)
        if was_repaired:
            repaired += 1
            print(f"  Repaired {r['TC_ID']} (shift={shift})")

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for r in new_rows:
            writer.writerow(r)

    print(f"\nC10 column-repair: {repaired} rows repaired, {len(new_rows)} total rows")


if __name__ == "__main__":
    main()