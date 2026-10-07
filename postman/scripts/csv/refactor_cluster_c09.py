#!/usr/bin/env python3
from _paths import CSV_PATH


"""Refactor C09 (Sub-Enterprises) test cases:
1. CREATE body userType sub_enterprise -> EnterpriseUser (matches Swagger + DTO)
2. UPDATE body: add fullName/email/phone/gender (per ParamUpdateSubEnterpriseUser)
3. STATS endpoint: `/statistics` -> `/stats` (Swagger uses 'stats')
4. PERMANENT: add new DELETE /sub-enterprises/{userId}/permanent
5. ORG (assignDeptPosition): POST -> PATCH + body removes primaryRoleId (DTO has none)
6. ROLES: POST -> PATCH
7. GET-ORG: add new GET /sub-enterprises/{userId}/organizational
8. GET-ROLES: add new GET /sub-enterprises/{userId}/roles
9. SET-BOSS: path /boss -> /bosses + body userType: EnterpriseUser

Uses csv module with QUOTE_MINIMAL to avoid column shifting.
"""

import csv
import copy


# Standard header (must match existing 27 columns)
HEADER = [
    "TC_ID", "Cluster", "Feature", "Method", "Full Endpoint", "Scenario",
    "Type", "Technique", "Priority", "Actor", "Tenant", "Contract Status",
    "Preconditions", "Test Data Alias", "Headers", "Path/Query Params",
    "Request Body (JSON)", "Steps", "Expected HTTP", "Expected Schema/Fields",
    "Side Effects", "Postconditions", "Cleanup", "Dependency", "FE Mapping",
    "Postman Request Name", "Notes"
]

# Standard headers for all C09 rows
STD_HEADERS = "x-api-key: {{authApiKey}}, Authorization: Bearer {{accessToken}}"


def read_rows():
    rows = []
    with open(CSV_PATH, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == HEADER, f"Header mismatch: {reader.fieldnames}"
        for r in reader:
            rows.append(r)
    return rows


def write_rows(rows):
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def make_row(tc_id, method, endpoint, scenario, technique, priority, actor, tenant,
             contract_status, preconditions, test_data, params, body, steps,
             expected_http, expected_schema, side_effects, postconditions,
             cleanup, dependency, fe_mapping, postman_name, notes,
             cluster="C09", feature="Sub-Enterprise", ttype_label="Positive"):
    return {
        "TC_ID": tc_id,
        "Cluster": cluster,
        "Feature": feature,
        "Method": method,
        "Full Endpoint": endpoint,
        "Scenario": scenario,
        "Type": ttype_label,
        "Technique": technique,
        "Priority": priority,
        "Actor": actor,
        "Tenant": tenant,
        "Contract Status": contract_status,
        "Preconditions": preconditions,
        "Test Data Alias": test_data,
        "Headers": STD_HEADERS,
        "Path/Query Params": params,
        "Request Body (JSON)": body,
        "Steps": steps,
        "Expected HTTP": expected_http,
        "Expected Schema/Fields": expected_schema,
        "Side Effects": side_effects,
        "Postconditions": postconditions,
        "Cleanup": cleanup,
        "Dependency": dependency,
        "FE Mapping": fe_mapping,
        "Postman Request Name": postman_name,
        "Notes": notes,
    }


def main():
    rows = read_rows()
    new_rows = []
    c09_indices = []

    for i, r in enumerate(rows):
        tc = r["TC_ID"]
        if not tc.startswith("AUTH-C09-"):
            new_rows.append(r)
            continue
        c09_indices.append(i)
        # default replacements
        r2 = copy.deepcopy(r)

        if tc == "AUTH-C09-SUBENT-001":  # CREATE
            r2["Method"] = "POST"
            r2["Full Endpoint"] = "/sgod-auth/v1/sub-enterprises"
            r2["Request Body (JSON)"] = (
                '{"email": "{{newSubentEmail}}", "userName": "{{newSubentName}}", '
                '"fullName": {"firstName": "Sub", "lastName": "Enterprise"}, '
                '"phone": "0900000005", "gender": "Male", '
                '"departmentId": "{{deptId}}", "positionId": "{{posId}}", '
                '"roleIds": ["{{roleId1}}"], "userType": "EnterpriseUser"}'
            )
            r2["Expected Schema/Fields"] = (
                "Principal id/type/state correct; belongs to ENTERPRISE_A; "
                "profile/list contains record; activate/login flow available; "
                "userType=EnterpriseUser"
            )
            r2["Postman Request Name"] = "[AUTH-C09-SUBENT-CREATE-001] Create sub-enterprise"
            r2["Notes"] = "userType=EnterpriseUser per Swagger; no enterpriseName field in DTO"
        elif tc == "AUTH-C09-SUBENT-002":  # LIST
            r2["Postman Request Name"] = "[AUTH-C09-SUBENT-LIST-001] List sub-enterprises"
        elif tc == "AUTH-C09-SUBENT-003":  # STATS - CHANGE /statistics -> /stats
            r2["Full Endpoint"] = "/sgod-auth/v1/sub-enterprises/stats"
            r2["Steps"] = "1) GET /sub-enterprises/stats"
            r2["Expected Schema/Fields"] = (
                "Statistics schema correct; counts match seeded sub-enterprises in scope; "
                "not global totals mixed with scope; per Swagger endpoint is /stats (not /statistics)"
            )
            r2["Postman Request Name"] = "[AUTH-C09-SUBENT-STATS-001] Sub-enterprise statistics"
            r2["Notes"] = "Swagger uses /stats not /statistics"
        elif tc == "AUTH-C09-SUBENT-004":  # DELETED
            r2["Postman Request Name"] = "[AUTH-C09-SUBENT-DELETED-001] Deleted sub-enterprises"
        elif tc == "AUTH-C09-SUBENT-005":  # GET by ID
            r2["Postman Request Name"] = "[AUTH-C09-SUBENT-GET-001] Get sub-enterprise"
        elif tc == "AUTH-C09-SUBENT-006":  # UPDATE - fix body per ParamUpdateSubEnterpriseUser
            r2["Request Body (JSON)"] = (
                '{"fullName": {"firstName": "Updated", "lastName": "SubEnt"}, '
                '"email": "{{newSubentEmail}}", "phone": "0900000001", '
                '"gender": "MALE", "avatarUrl": "https://cdn.sgod.test/avatars/subent-a-001.png"}'
            )
            r2["Expected Schema/Fields"] = (
                "Sub-Enterprise updated; GET /detail/profile reflects updated fields; "
                "fields not sent remain unchanged; avatarUrl stored; gender=MALE"
            )
            r2["Postman Request Name"] = "[AUTH-C09-SUBENT-UPDATE-001] Update sub-enterprise"
            r2["Notes"] = "DTO ParamUpdateSubEnterpriseUser has fullName/email/phone/gender/avatarUrl"
        elif tc == "AUTH-C09-SUBENT-007":  # DELETE
            r2["Postman Request Name"] = "[AUTH-C09-SUBENT-DELETE-001] Delete sub-enterprise"
        elif tc == "AUTH-C09-SUBENT-008":  # MY-PROFILE
            r2["Request Body (JSON)"] = (
                '{"fullName": {"firstName": "Updated", "lastName": "SubEnt"}, '
                '"email": "{{actorEmail}}", "phone": "0900000001", "gender": "MALE"}'
            )
            r2["Postman Request Name"] = "[AUTH-C09-SUBENT-MY-PROFILE-001] Update my-profile"
        elif tc == "AUTH-C09-SUBENT-009":  # PROFILE
            r2["Request Body (JSON)"] = (
                '{"fullName": {"firstName": "Updated", "lastName": "SubEnt"}, '
                '"email": "{{actorEmail}}", "phone": "0900000001", "gender": "MALE"}'
            )
            r2["Postman Request Name"] = "[AUTH-C09-SUBENT-PROFILE-001] Update profile"
        elif tc == "AUTH-C09-SUBENT-010":  # ME
            r2["Request Body (JSON)"] = (
                '{"fullName": {"firstName": "Updated", "lastName": "SubEnt"}, '
                '"email": "{{actorEmail}}", "phone": "0900000001", "gender": "MALE"}'
            )
            r2["Postman Request Name"] = "[AUTH-C09-SUBENT-ME-001] Update me"
        elif tc == "AUTH-C09-SUBENT-011":  # RESTORE
            r2["Request Body (JSON)"] = "{}"
            r2["Steps"] = "1) POST /sub-enterprises/{{subentDeletedId}}/restore"
            r2["Postman Request Name"] = "[AUTH-C09-SUBENT-RESTORE-001] Restore sub-enterprise"
        elif tc == "AUTH-C09-SUBENT-012":  # BLOCK
            r2["Steps"] = "1) POST /sub-enterprises/{{subentBlockId}}/block"
            r2["Postman Request Name"] = "[AUTH-C09-SUBENT-BLOCK-001] Block sub-enterprise"
        elif tc == "AUTH-C09-SUBENT-013":  # UNBLOCK
            r2["Steps"] = "1) POST /sub-enterprises/{{subentBlockId}}/unblock"
            r2["Postman Request Name"] = "[AUTH-C09-SUBENT-UNBLOCK-001] Unblock sub-enterprise"
        elif tc == "AUTH-C09-SUBENT-014":  # ROLES - POST -> PATCH
            r2["Method"] = "PATCH"
            r2["Full Endpoint"] = "/sgod-auth/v1/sub-enterprises/{userId}/roles"
            r2["Steps"] = "1) PATCH /sub-enterprises/{{subentAId}}/roles"
            r2["Request Body (JSON)"] = '{"roleIds": ["{{roleId1}}", "{{roleId2}}"]}'
            r2["Expected Schema/Fields"] = (
                "Roles on GET /profile match new list; roles replaced not appended; "
                "DTO ParamAssignRolesSubEnterpriseUser only has userId + roleIds[]"
            )
            r2["FE Mapping"] = "[useAuthSubEnterpriseUser] → assign roles"
            r2["Postman Request Name"] = "[AUTH-C09-SUBENT-ROLES-001] Set sub-ent roles"
            r2["Notes"] = "Swagger specifies PATCH (was POST in old docs); no primaryRoleId in DTO"
        elif tc == "AUTH-C09-SUBENT-015":  # ORG - POST -> PATCH + remove primaryRoleId
            r2["Method"] = "PATCH"
            r2["Full Endpoint"] = "/sgod-auth/v1/sub-enterprises/{userId}/organizational"
            r2["Steps"] = "1) PATCH /sub-enterprises/{{subentAId}}/organizational"
            r2["Request Body (JSON)"] = (
                '{"departmentId": "{{deptId}}", "positionId": "{{posId}}", '
                '"bossId": "{{bossId}}", "userType": "EnterpriseUser"}'
            )
            r2["Expected Schema/Fields"] = (
                "Profile reflects new department/position; boss assigned; "
                "DTO ParamAssignDepartmentPositionSubEnterpriseUser has deptId, positionId, "
                "userType, primaryRoleId?, bossId?; userType=EnterpriseUser required"
            )
            r2["FE Mapping"] = "[useAuthSubEnterpriseUser] → assign organizational"
            r2["Postman Request Name"] = "[AUTH-C09-SUBENT-ORG-001] Set organizational"
            r2["Notes"] = (
                "Swagger specifies PATCH /{userId}/organizational; "
                "DTO does NOT include primaryRoleId in create-org path"
            )
        elif tc == "AUTH-C09-SUBENT-016":  # BOSSES (GET)
            r2["Steps"] = "1) GET /sub-enterprises/{{subentAId}}/bosses"
            r2["Postman Request Name"] = "[AUTH-C09-SUBENT-BOSSES-001] List bosses"
        elif tc == "AUTH-C09-SUBENT-017":  # SET BOSS - /boss -> /bosses + userType=EnterpriseUser
            r2["Full Endpoint"] = "/sgod-auth/v1/sub-enterprises/{userId}/bosses"
            r2["Steps"] = "1) PATCH /sub-enterprises/{{subentAId}}/bosses"
            r2["Request Body (JSON)"] = '{"bossId": "{{bossId}}", "userType": "EnterpriseUser"}'
            r2["Expected Schema/Fields"] = (
                "Profile boss matches MANAGER; department/position unchanged; "
                "DTO ParamSetBossSubEnterpriseUser has userId, bossId?, userType?"
            )
            r2["Postman Request Name"] = "[AUTH-C09-SUBENT-BOSS-001] Set boss"
            r2["Notes"] = (
                "Swagger path is /bosses (plural), not /boss; "
                "userType=EnterpriseUser required per Swagger"
            )

        new_rows.append(r2)

    # Append 3 new rows after last C09 row (last C09 was SUBENT-017 in original)
    # In new_rows, C09 rows are appended; we need to insert 3 new rows after last C09 row
    # Find the last C09 row index in new_rows
    last_c09_idx = -1
    for idx, r in enumerate(new_rows):
        if r["TC_ID"].startswith("AUTH-C09-"):
            last_c09_idx = idx

    # INSERT 3 NEW ROWS
    # PERMANENT DELETE (018)
    new_permanent = make_row(
        tc_id="AUTH-C09-SUBENT-018",
        method="DELETE",
        endpoint="/sgod-auth/v1/sub-enterprises/{userId}/permanent",
        scenario="Permanent delete sub-enterprise user",
        technique="State Transition",
        priority="P1",
        actor="ENT_USER_A",
        tenant="ENTERPRISE_A",
        contract_status="CONTRACT_PENDING",
        preconditions="Sub-enterprise already soft-deleted; actor has permanent-delete permission",
        test_data="SUBENT_PERMANENT_TARGET",
        params="userId={{subentPermanentId}}",
        body="",
        steps="1) DELETE /sub-enterprises/{{subentPermanentId}}/permanent",
        expected_http="200",
        expected_schema=(
            "Permanent deletion acknowledged; GET /sub-enterprises/{id} returns 404; "
            "GET /sub-enterprises/deleted also returns 404; record wiped from storage"
        ),
        side_effects="Sub-Enterprise permanently removed; deleted list also empty",
        postconditions="Sub-Enterprise not recoverable; cannot restore after permanent delete",
        cleanup="None",
        dependency="SUBENT_PERMANENT_TARGET soft-deleted",
        fe_mapping="[useAuthSubEnterpriseUser] → permanent delete sub-enterprise",
        postman_name="[AUTH-C09-SUBENT-PERMANENT-001] Permanent delete sub-enterprise",
        notes="Per Swagger DELETE /sub-enterprises/{userId}/permanent endpoint",
    )

    # GET-ORG (019)
    new_get_org = make_row(
        tc_id="AUTH-C09-SUBENT-019",
        method="GET",
        endpoint="/sgod-auth/v1/sub-enterprises/{userId}/organizational",
        scenario="Get organizational (dept/position) for sub-enterprise user",
        technique="Equivalence Partitioning",
        priority="P1",
        actor="ENT_USER_A",
        tenant="ENTERPRISE_A",
        contract_status="CONTRACT_PENDING",
        preconditions="SUBENT_A has departmentId/positionId set; actor has ReadUser permission",
        test_data="SUBENT_ORG_FIXTURE",
        params="userId={{subentAId}}",
        body="",
        steps="1) GET /sub-enterprises/{{subentAId}}/organizational",
        expected_http="200",
        expected_schema=(
            "Department/position object with departmentId, positionId, primaryRoleId?, bossId?; "
            "fields match the SUBENT_ORG_FIXTURE; userType=EnterpriseUser"
        ),
        side_effects="None",
        postconditions="Org state retrieved; no side effects",
        cleanup="None",
        dependency="SUBENT_A with org",
        fe_mapping="[useAuthSubEnterpriseUser] → get organizational",
        postman_name="[AUTH-C09-SUBENT-GET-ORG-001] Get organizational",
        notes="Per Swagger GET /sub-enterprises/{userId}/organizational",
    )

    # GET-ROLES (020)
    new_get_roles = make_row(
        tc_id="AUTH-C09-SUBENT-020",
        method="GET",
        endpoint="/sgod-auth/v1/sub-enterprises/{userId}/roles",
        scenario="Get roles for sub-enterprise user",
        technique="Equivalence Partitioning",
        priority="P1",
        actor="ENT_USER_A",
        tenant="ENTERPRISE_A",
        contract_status="CONTRACT_PENDING",
        preconditions="SUBENT_A has roles assigned; actor has ReadUser permission",
        test_data="SUBENT_ROLE_FIXTURE",
        params="userId={{subentAId}}",
        body="",
        steps="1) GET /sub-enterprises/{{subentAId}}/roles",
        expected_http="200",
        expected_schema=(
            "Array of role objects (id, name, layer) reflecting SUBENT_ROLE_FIXTURE; "
            "layer=EnterpriseUser or sub_enterprise per DTO"
        ),
        side_effects="None",
        postconditions="None",
        cleanup="None",
        dependency="SUBENT_A with roles",
        fe_mapping="[useAuthSubEnterpriseUser] → get roles",
        postman_name="[AUTH-C09-SUBENT-GET-ROLES-001] Get roles",
        notes="Per Swagger GET /sub-enterprises/{userId}/roles",
    )

    # Insert the 3 new rows right after last C09 row
    insert_at = last_c09_idx + 1
    new_rows[insert_at:insert_at] = [new_permanent, new_get_org, new_get_roles]

    write_rows(new_rows)
    print(f"C09 refactor complete: {len(new_rows)} total rows")
    print(f"  - C09 rows: {sum(1 for r in new_rows if r['TC_ID'].startswith('AUTH-C09-'))}")
    print(f"  - Other rows: {sum(1 for r in new_rows if not r['TC_ID'].startswith('AUTH-C09-'))}")


if __name__ == "__main__":
    main()