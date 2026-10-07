#!/usr/bin/env python3
from _paths import CSV_PATH


"""Final manual fix for remaining C10 column shifts.
Specifically targets rows where Expected HTTP is descriptive text (not 2xx)
and Body may or may not be present.
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


def is_2xx(s):
    if not s:
        return False
    return bool(re.match(r"^2\d{2}$", s.strip()))


def is_step_text(s):
    if not s:
        return False
    return bool(re.match(r"^\d+\)\s+[A-Z]+\s+/", s.strip()))


def is_postman_name(s):
    if not s:
        return False
    return bool(re.match(r"^\[AUTH-C\d{2}-", s))


def is_femapping(s):
    if not s:
        return False
    return s.startswith("[useAuth") or "GAP-" in s


# Manual fix for each remaining problematic TC
MANUAL_FIXES = {
    "AUTH-C10-TENANT-007": {
        # Body: empty, Steps: descriptive, Expected HTTP: short descriptive, FE Mapping: postman_name
        "Request Body (JSON)": "",
        "Steps": "1) GET /sgod/enterprises/{{tenantIdA}}",
        "Expected HTTP": "200",
        "Expected Schema/Fields": "Enterprise identity/fields/state matches ENTERPRISE_A fixture; id, name, state, subscription correct",
        "Side Effects": "Enterprise detail correct; no unauthorized data",
        "Postconditions": "None",
        "Cleanup": "SGOD_ADMIN_A session",
        "Dependency": "",
        "FE Mapping": "[useAuthSgodEnteprise] → get enterprise by ID",
        "Postman Request Name": "[AUTH-C10-SGOD-ENT-GET-001] Get enterprise details",
        "Notes": "Per Swagger ảnh 7: GET /sgod/enterprises/{tenantId}",
    },
    "AUTH-C10-TENANT-010": {
        "Request Body (JSON)": "",
        "Steps": "1) POST /sgod/enterprises/{{tenantDeletedId}}/restore",
        "Expected HTTP": "200",
        "Expected Schema/Fields": "Enterprise active; GET /detail/list returns active state; state restored per contract",
        "Side Effects": "Enterprise active again; restored to previous state",
        "Postconditions": "None",
        "Cleanup": "TENANT_DELETED soft-deleted (via BE fixture)",
        "Dependency": "G",
        "FE Mapping": "[AUTH-C10-TENANT-010] Restore enterprise (BE fixture procedure required)",
        "Postman Request Name": "[AUTH-C10-SGOD-ENT-RESTORE-001] Restore deleted enterprise",
        "Notes": "BE fixture procedure required; no enterprise-delete endpoint in inventory",
    },
    "AUTH-C10-ORG-006": {
        "Request Body (JSON)": "",
        "Steps": "1) GET /organizations/audit",
        "Expected HTTP": "200",
        "Expected Schema/Fields": "Audit graph/report correct fixture; schema matches contract; organizational structure accurate; no inconsistencies introduced artificially",
        "Side Effects": "Graph reflects actual organizational structure; inconsistencies detected/reported per contract",
        "Postconditions": "None",
        "Cleanup": "ORG_AUDIT_FIXTURE",
        "Dependency": "G",
        "FE Mapping": "[useAuthUserOrganizational] → audit organization (GAP-07: hook method not yet implemented)",
        "Postman Request Name": "[AUTH-C10-ORG-AUDIT-001] Audit organizational reporting lines",
        "Notes": "Swagger ảnh 19: GET /organizations/audit, query tenantId OPTIONAL. GAP-07: auditOrganization method missing in service.",
    },
    # Also fix TENANT-008 and TENANT-009 if Steps has JSON
    "AUTH-C10-TENANT-008": {
        "Request Body (JSON)": '{"reason": "Policy violation - manual review"}',
        "Steps": "1) POST /sgod/enterprises/{{tenantIdB}}/block with body {reason:...}",
        "Expected HTTP": "200",
        "Expected Schema/Fields": "Enterprise blocked; GET /detail/list shows state=blocked; login for users in tenant blocked; body has reason field (optional in DTO ParamBlockSgodEnterprise, but Swagger shows as required for compliance audit)",
        "Side Effects": "Enterprise blocked; users in ENTERPRISE_B cannot login; actor unaffected",
        "Postconditions": "Unblock enterprise",
        "Cleanup": "SGOD_ADMIN_A with block permission",
        "Dependency": "S",
        "FE Mapping": "[useAuthSgodEnteprise] → block enterprise",
        "Postman Request Name": "[AUTH-C10-SGOD-ENT-BLOCK-001] Block enterprise",
        "Notes": "Swagger ảnh 8: body {reason: string} REQUIRED. DTO ParamBlockSgodEnterprise.reason is OPTIONAL. Step-up required per Swagger.",
    },
    "AUTH-C10-TENANT-009": {
        "Request Body (JSON)": '{"reason": "Audit complete - unblock"}',
        "Steps": "1) POST /sgod/enterprises/{{tenantIdB}}/unblock with body {reason:...}",
        "Expected HTTP": "200",
        "Expected Schema/Fields": "Enterprise active; login for users in tenant succeeds; state=active; body has reason field (optional in DTO ParamUnblockSgodEnterprise, but Swagger shows as required for compliance audit)",
        "Side Effects": "Enterprise active; users can login again; block state removed",
        "Postconditions": "None",
        "Cleanup": "TENANT_BLOCK_TARGET blocked",
        "Dependency": "S",
        "FE Mapping": "[useAuthSgodEnteprise] → unblock enterprise",
        "Postman Request Name": "[AUTH-C10-SGOD-ENT-UNBLOCK-001] Unblock enterprise",
        "Notes": "Swagger ảnh 9: body {reason: string} REQUIRED. DTO ParamUnblockSgodEnterprise.reason is OPTIONAL.",
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
            print(f"  Manually fixed {r['TC_ID']}")
        new_rows.append(r)

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for r in new_rows:
            writer.writerow(r)

    print(f"\nC10 manual fix: {fixed} rows repaired")


if __name__ == "__main__":
    main()