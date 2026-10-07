#!/usr/bin/env python3
from _paths import CSV_PATH


"""Refactor C10 (SGOD Enterprises / Organizational) test cases:
- AUTH-C10-TENANT-008/009: body {} -> {"reason": "..."} per Swagger
- AUTH-C10-ORG-001/004: userType enterprise_user -> EnterpriseUser
- AUTH-C10-ORG-001/003/004/006: FE Mapping updated to reflect missing hook methods
- AUTH-C10-ORG-003: query userType noted as REQUIRED per Swagger
- AUTH-C10-ORG-006: query tenantId (optional) added per Swagger
- Add gap notes about useAuthUserOrganizational hook missing assign/available-bosses/set-boss/audit methods
"""
import csv
import copy


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
        assert reader.fieldnames == HEADER
        rows = list(reader)

    new_rows = []
    for r in rows:
        tc = r["TC_ID"]
        if not tc.startswith("AUTH-C10-"):
            new_rows.append(r)
            continue
        r2 = copy.deepcopy(r)

        if tc == "AUTH-C10-TENANT-001":  # LIST
            r2["Path/Query Params"] = "page, cursor, limit, search, departmentId, positionId, roleId, status"
            r2["Postman Request Name"] = "[AUTH-C10-SGOD-ENT-LIST-001] List SGOD enterprises"
        elif tc == "AUTH-C10-TENANT-002":  # STATS OVERVIEW
            r2["Postman Request Name"] = "[AUTH-C10-SGOD-ENT-OVERVIEW-001] SGOD enterprises overview stats"
        elif tc == "AUTH-C10-TENANT-003":  # ASSIGN
            r2["Request Body (JSON)"] = '{"userId": "{{userId}}", "tenantIds": ["{{tenantIdB}}"]}'
            r2["Postman Request Name"] = "[AUTH-C10-SGOD-ENT-ASSIGN-001] Assign tenant to user"
        elif tc == "AUTH-C10-TENANT-004":  # UNASSIGN
            r2["Request Body (JSON)"] = '{"userId": "{{userId}}", "tenantId": "{{tenantIdB}}"}'
            r2["Postman Request Name"] = "[AUTH-C10-SGOD-ENT-UNASSIGN-001] Unassign tenant from user"
        elif tc == "AUTH-C10-TENANT-005":  # SET-ASSIGNED
            r2["Request Body (JSON)"] = '{"userId": "{{userId}}", "tenantIds": ["{{tenantIdA}}", "{{tenantIdC}}"]}'
            r2["Postman Request Name"] = "[AUTH-C10-SGOD-ENT-SET-ASSIGNED-001] Set assigned enterprises"
        elif tc == "AUTH-C10-TENANT-006":  # DELETED
            r2["Path/Query Params"] = "page, cursor, limit, search, departmentId, positionId, roleId, status"
            r2["Postman Request Name"] = "[AUTH-C10-SGOD-ENT-DELETED-001] List deleted enterprises"
        elif tc == "AUTH-C10-TENANT-007":  # GET DETAIL
            r2["Postman Request Name"] = "[AUTH-C10-SGOD-ENT-GET-001] Get enterprise details"
        elif tc == "AUTH-C10-TENANT-008":  # BLOCK
            r2["Request Body (JSON)"] = '{"reason": "Policy violation - manual review"}'
            r2["Steps"] = "1) POST /sgod/enterprises/{{tenantIdB}}/block with body {reason:...}"
            r2["Expected Schema/Fields"] = (
                "Enterprise blocked; GET /sgod/enterprises/{tenantId} shows state=blocked; "
                "login for users in tenant blocked; body has reason field (optional in DTO "
                "ParamBlockSgodEnterprise, but Swagger shows as required for compliance audit)"
            )
            r2["Postman Request Name"] = "[AUTH-C10-SGOD-ENT-BLOCK-001] Block enterprise"
            r2["Notes"] = (
                "Swagger ảnh 8: body {reason: string} REQUIRED. "
                "DTO ParamBlockSgodEnterprise.reason is OPTIONAL. "
                "Step-up required per Swagger."
            )
        elif tc == "AUTH-C10-TENANT-009":  # UNBLOCK
            r2["Request Body (JSON)"] = '{"reason": "Audit complete - unblock"}'
            r2["Steps"] = "1) POST /sgod/enterprises/{{tenantIdB}}/unblock with body {reason:...}"
            r2["Expected Schema/Fields"] = (
                "Enterprise active; login for users in tenant succeeds; state=active; "
                "body has reason field (optional in DTO ParamUnblockSgodEnterprise, "
                "but Swagger shows as required for compliance audit)"
            )
            r2["Postman Request Name"] = "[AUTH-C10-SGOD-ENT-UNBLOCK-001] Unblock enterprise"
            r2["Notes"] = (
                "Swagger ảnh 9: body {reason: string} REQUIRED. "
                "DTO ParamUnblockSgodEnterprise.reason is OPTIONAL."
            )
        elif tc == "AUTH-C10-TENANT-010":  # RESTORE
            r2["Postman Request Name"] = "[AUTH-C10-SGOD-ENT-RESTORE-001] Restore deleted enterprise"
        elif tc == "AUTH-C10-TENANT-011":  # SUBSCRIPTION
            r2["Request Body (JSON)"] = '{"durationDays": 365}'
            r2["Postman Request Name"] = "[AUTH-C10-SGOD-ENT-SUBSCRIPTION-001] Update enterprise subscription"
        elif tc == "AUTH-C10-TENANT-012":  # FEATURES
            r2["Request Body (JSON)"] = '{"features": ["audit_logging", "sso", "mfa_required"]}'
            r2["Postman Request Name"] = "[AUTH-C10-SGOD-ENT-FEATURES-001] Update enterprise features"
            r2["Notes"] = (
                "Body per Swagger ảnh 12: features is array of FEATURE_* keys. "
                "DTO ParamUpdateSgodEnterpriseFeatures.features: string[]"
            )
        elif tc == "AUTH-C10-TENANT-013":  # STATS BY TENANT
            r2["Postman Request Name"] = "[AUTH-C10-SGOD-ENT-STATS-BY-TENANT-001] Get enterprise statistics by ID"
        elif tc == "AUTH-C10-ORG-001":  # ASSIGN
            r2["Request Body (JSON)"] = (
                '{"departmentId": "{{deptId}}", "positionId": "{{posId}}", '
                '"primaryRoleId": "{{primaryRoleId}}", "bossId": "{{bossId}}", '
                '"userType": "EnterpriseUser"}'
            )
            r2["Expected Schema/Fields"] = (
                "Profile reflects new department/position; boss assigned; "
                "IAssignUserDeptPositionResponse has departmentId, positionId, primaryRoleId?, "
                "bossId?; userType required per Swagger (PascalCase enum)"
            )
            r2["FE Mapping"] = "[useAuthUserOrganizational] → organizational assign (GAP-07: hook method not yet implemented)"
            r2["Postman Request Name"] = "[AUTH-C10-USERS-ORG-ASSIGN-001] Assign organizational"
            r2["Notes"] = (
                "Swagger ảnh 14: POST /users/{userId}/organizational/assign, "
                "userType enum PascalCase: EnterpriseUser/SubEnterpriseUser/SgodUser/SgodAdmin. "
                "GAP-07: authUsersOrganizationalService currently has only "
                "removeUserOrganizational + checkSubordinate — assign method missing."
            )
        elif tc == "AUTH-C10-ORG-002":  # REMOVE
            r2["Path/Query Params"] = "userId={{entUserBId}}, userType=enterprise_user (query, REQUIRED per Swagger ảnh 15)"
            r2["Postman Request Name"] = "[AUTH-C10-USERS-ORG-REMOVE-001] Remove organizational"
            r2["Notes"] = (
                "Swagger ảnh 15: POST /users/{userId}/organizational/remove, "
                "query userType REQUIRED. FE: handleRemoveUserOrganizational(p) exists."
            )
        elif tc == "AUTH-C10-ORG-003":  # BOSSES AVAILABLE
            r2["Path/Query Params"] = "userId={{entUserBId}}, userType=enterprise_user (query, REQUIRED per Swagger ảnh 16)"
            r2["FE Mapping"] = "[useAuthUserOrganizational] → get available bosses (GAP-07: hook method not yet implemented)"
            r2["Postman Request Name"] = "[AUTH-C10-USERS-ORG-BOSSES-AVAILABLE-001] Get available bosses"
            r2["Notes"] = (
                "Swagger ảnh 16: GET /users/{userId}/organizational/bosses/available, "
                "query userType REQUIRED. GAP-07: getAvailableBosses method missing in service."
            )
        elif tc == "AUTH-C10-ORG-004":  # SET BOSS
            r2["Request Body (JSON)"] = '{"bossId": "{{bossId}}", "userType": "EnterpriseUser"}'
            r2["Expected Schema/Fields"] = (
                "Profile boss matches MANAGER; department/position unchanged; "
                "ISetBossRequest.bossId + userType; userType PascalCase per Swagger"
            )
            r2["FE Mapping"] = "[useAuthUserOrganizational] → set boss (GAP-07: hook method not yet implemented)"
            r2["Postman Request Name"] = "[AUTH-C10-USERS-ORG-BOSSES-SET-001] Set boss"
            r2["Notes"] = (
                "Swagger ảnh 17: POST /users/{userId}/organizational/bosses/set, "
                "body {bossId, userType}. GAP-07: setBoss method missing in service."
            )
        elif tc == "AUTH-C10-ORG-005":  # CHECK SUBORDINATE
            r2["Path/Query Params"] = "userId={{managerId}}, subordinateId={{subordinateId}} (subordinateId query REQUIRED per Swagger ảnh 18)"
            r2["FE Mapping"] = "[useAuthUsersOrganizational] → check subordinate"
            r2["Postman Request Name"] = "[AUTH-C10-USERS-ORG-CHECK-SUBORDINATE-001] Check subordinate relation"
            r2["Notes"] = (
                "Swagger ảnh 18: GET /users/{userId}/organizational/check-subordinate, "
                "query subordinateId REQUIRED. FE handleCheckSubordinate exists."
            )
        elif tc == "AUTH-C10-ORG-006":  # AUDIT
            r2["Path/Query Params"] = "tenantId={{tenantIdA}} (query, optional per Swagger ảnh 19)"
            r2["FE Mapping"] = "[useAuthUserOrganizational] → audit organization (GAP-07: hook method not yet implemented)"
            r2["Postman Request Name"] = "[AUTH-C10-ORG-AUDIT-001] Audit organizational reporting lines"
            r2["Notes"] = (
                "Swagger ảnh 19: GET /organizations/audit, query tenantId OPTIONAL. "
                "GAP-07: auditOrganization method missing in service."
            )

        new_rows.append(r2)

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for r in new_rows:
            writer.writerow(r)

    print(f"C10 CSV refactor complete: {len(new_rows)} total rows")
    c10 = [r for r in new_rows if r["TC_ID"].startswith("AUTH-C10-")]
    print(f"  - C10 rows: {len(c10)}")


if __name__ == "__main__":
    main()