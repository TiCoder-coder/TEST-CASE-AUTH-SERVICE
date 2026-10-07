#!/usr/bin/env python3
from _paths import CSV_PATH


"""Fix remaining C09 column shifts where body column has Steps text.
Moves the Steps text back to Steps column and shifts everything left.
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

# Manual fix for the 5 C09 rows with body = Steps text
MANUAL_FIXES = {
    "AUTH-C09-SUBENT-005": {  # GET sub-enterprise (no body)
        "Request Body (JSON)": "",
        "Steps": "1) GET /sub-enterprises/{{subentAId}}",
        "Expected HTTP": "200",
        "Expected Schema/Fields": "Sub-enterprise user details match ENTERPRISE_A seed; id, email, userType=EnterpriseUser; fullName, roleIds visible",
        "Side Effects": "Sub-enterprise detail correct; no unauthorized data",
        "Postconditions": "None",
        "Cleanup": "ENT_USER_A session",
        "Dependency": "",
        "FE Mapping": "[useAuthSubEnterpriseUser] → get sub-enterprise by ID",
        "Postman Request Name": "[AUTH-C09-SUBENT-GET-001] Get sub-enterprise",
        "Notes": "GET /sub-enterprises/{userId}, path userId = sub-enterprise user ID",
    },
    "AUTH-C09-SUBENT-007": {  # DELETE
        "Request Body (JSON)": "",
        "Steps": "1) DELETE /sub-enterprises/{{subentDeleteId}}",
        "Expected HTTP": "204",
        "Expected Schema/Fields": "Soft-delete success; GET returns 404; user cannot login",
        "Side Effects": "Sub-enterprise soft-deleted; login blocked",
        "Postconditions": "None",
        "Cleanup": "Restore sub-enterprise to active",
        "Dependency": "",
        "FE Mapping": "[useAuthSubEnterpriseUser] → delete sub-enterprise",
        "Postman Request Name": "[AUTH-C09-SUBENT-DELETE-001] Delete sub-enterprise",
        "Notes": "Soft-delete only; permanent delete via separate endpoint",
    },
    "AUTH-C09-SUBENT-012": {  # BLOCK
        "Request Body (JSON)": '{"reason": "Manual review - test block"}',
        "Steps": "1) POST /sub-enterprises/{{subentBlockId}}/block",
        "Expected HTTP": "200",
        "Expected Schema/Fields": "Sub-enterprise blocked; login for users blocked; state=blocked",
        "Side Effects": "Sub-enterprise blocked; users cannot login; actor unaffected",
        "Postconditions": "Unblock sub-enterprise",
        "Cleanup": "Restore sub-enterprise state",
        "Dependency": "S",
        "FE Mapping": "[useAuthSubEnterpriseUser] → block sub-enterprise",
        "Postman Request Name": "[AUTH-C09-SUBENT-BLOCK-001] Block sub-enterprise",
        "Notes": "Step-up required per Swagger; body has reason (optional in DTO, REQUIRED per Swagger)",
    },
    "AUTH-C09-SUBENT-013": {  # UNBLOCK
        "Request Body (JSON)": '{"reason": "Audit done - unblock"}',
        "Steps": "1) POST /sub-enterprises/{{subentBlockId}}/unblock",
        "Expected HTTP": "200",
        "Expected Schema/Fields": "Sub-enterprise active; login succeeds; state=active",
        "Side Effects": "Sub-enterprise unblocked; users can login",
        "Postconditions": "None",
        "Cleanup": "Verify active state",
        "Dependency": "S",
        "FE Mapping": "[useAuthSubEnterpriseUser] → unblock sub-enterprise",
        "Postman Request Name": "[AUTH-C09-SUBENT-UNBLOCK-001] Unblock sub-enterprise",
        "Notes": "Body has reason (optional in DTO, REQUIRED per Swagger)",
    },
    "AUTH-C09-SUBENT-016": {  # BOSSES
        "Request Body (JSON)": "",
        "Steps": "1) GET /sub-enterprises/{{subentAId}}/bosses",
        "Expected HTTP": "200",
        "Expected Schema/Fields": "Boss list returned; MANAGER in list; array of bosses; correctly scoped",
        "Side Effects": "Available bosses returned",
        "Postconditions": "None",
        "Cleanup": "ENT_USER_A session",
        "Dependency": "",
        "FE Mapping": "[useAuthSubEnterpriseUser] → get available bosses",
        "Postman Request Name": "[AUTH-C09-SUBENT-BOSSES-001] List bosses",
        "Notes": "GET /sub-enterprises/{userId}/bosses",
    },
}


def main():
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    new_rows = []
    fixed = 0
    for r in rows:
        if r["TC_ID"] in MANUAL_FIXES:
            fix = MANUAL_FIXES[r["TC_ID"]]
            for k, v in fix.items():
                r[k] = v
            fixed += 1
            print(f"  Fixed {r['TC_ID']}")
        new_rows.append(r)

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for r in new_rows:
            writer.writerow(r)

    print(f"\nDone. {fixed} rows fixed.")


if __name__ == "__main__":
    main()