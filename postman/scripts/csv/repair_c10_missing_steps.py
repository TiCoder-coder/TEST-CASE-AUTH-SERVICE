#!/usr/bin/env python3
from _paths import CSV_PATH


"""Add missing Steps text + fix FE Mapping for AUTH-C10-TENANT-010."""
import csv


HEADER = [
    "TC_ID", "Cluster", "Feature", "Method", "Full Endpoint", "Scenario",
    "Type", "Technique", "Priority", "Actor", "Tenant", "Contract Status",
    "Preconditions", "Test Data Alias", "Headers", "Path/Query Params",
    "Request Body (JSON)", "Steps", "Expected HTTP", "Expected Schema/Fields",
    "Side Effects", "Postconditions", "Cleanup", "Dependency", "FE Mapping",
    "Postman Request Name", "Notes"
]

MANUAL = {
    "AUTH-C10-ORG-002": {
        "Steps": "1) POST /users/{{entUserBId}}/organizational/remove?userType=enterprise_user",
    },
    "AUTH-C10-ORG-003": {
        "Steps": "1) GET /users/{{entUserBId}}/organizational/bosses/available?userType=enterprise_user",
    },
    "AUTH-C10-ORG-005": {
        "Steps": "1) GET /users/{{managerId}}/organizational/check-subordinate?subordinateId={{subordinateId}}",
    },
    "AUTH-C10-TENANT-010": {
        "FE Mapping": "[useAuthSgodEnteprise] → restore enterprise (BE fixture procedure required)",
    },
}


def main():
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    new_rows = []
    for r in rows:
        if r["TC_ID"] in MANUAL:
            r.update(MANUAL[r["TC_ID"]])
            print(f"  Updated {r['TC_ID']}")
        new_rows.append(r)

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for r in new_rows:
            writer.writerow(r)

    print(f"\nDone. {len(new_rows)} total rows.")


if __name__ == "__main__":
    main()