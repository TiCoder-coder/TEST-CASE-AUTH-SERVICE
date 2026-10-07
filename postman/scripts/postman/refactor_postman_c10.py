#!/usr/bin/env python3
from _paths import POSTMAN_PATH


"""Refactor C10 Postman folder to align with new CSV + Swagger images.

Changes:
- Update item names to match new CSV Postman Request Name column
- Update raw URLs to match Swagger paths
- Update method bodies to match Swagger DTOs
- Add concrete 200 OK + 401 Unauthorized examples
- Ensure all C10 items have path arrays consistent with raw URLs
"""
import json
import copy


BASE_URL = "{{baseUrlAuth}}/sgod-auth/v1"


def build_url(path, query_pairs):
    """Build Postman URL object with raw + path + query arrays."""
    segments = [s for s in path.split("/") if s]
    raw_path = BASE_URL + path
    if query_pairs:
        from urllib.parse import urlencode
        raw_path += "?" + urlencode(query_pairs)
    url = {
        "raw": raw_path,
        "host": ["{{baseUrlAuth}}"],
        "path": ["sgod-auth", "v1"] + segments,
    }
    if query_pairs:
        url["query"] = [{"key": k, "value": v} for k, v in query_pairs]
    return url


def update_item(postman_item, name, method, url_obj, body_raw=None, body_mode="raw"):
    """Update an existing Postman item."""
    postman_item["name"] = name
    postman_item["request"]["method"] = method
    postman_item["request"]["url"] = url_obj
    postman_item["request"]["header"] = [
        {"key": "x-api-key", "value": "{{authApiKey}}"},
        {"key": "Authorization", "value": "Bearer {{accessToken}}"},
        {"key": "Content-Type", "value": "application/json"},
    ]
    if body_raw:
        postman_item["request"]["body"] = {
            "mode": body_mode,
            "raw": body_raw,
            "options": {"raw": {"language": "json"}},
        }
    else:
        postman_item["request"]["body"] = None
    return postman_item


def make_200_example():
    return [
        {
            "name": "200 OK",
            "originalRequest": {},
            "status": "OK",
            "code": 200,
            "_postman_previewlanguage": "json",
            "header": [],
            "cookie": [],
            "body": '{"success":true,"code":200,"data":{}}',
        }
    ]


def make_401_example():
    return [
        {
            "name": "401 Unauthorized",
            "originalRequest": {},
            "status": "Unauthorized",
            "code": 401,
            "_postman_previewlanguage": "json",
            "header": [],
            "cookie": [],
            "body": '{"success":false,"code":401,"message":"Unauthorized"}',
        }
    ]


def main():
    with open(POSTMAN_PATH, "r", encoding="utf-8") as f:
        col = json.load(f)

    target_folder = None
    for item in col["item"]:
        if item.get("name") == "C10 — SGOD Enterprises / Organizational":
            target_folder = item
            break

    if not target_folder:
        raise RuntimeError("C10 folder not found")

    # Find each C10 sub-item by TC_ID prefix in name
    by_tc = {}
    for sub in target_folder["item"]:
        n = sub.get("name", "")
        for tc in (
            "AUTH-C10-SGOD-ENT-LIST-001", "AUTH-C10-SGOD-ENT-OVERVIEW-001",
            "AUTH-C10-SGOD-ENT-ASSIGN-001", "AUTH-C10-SGOD-ENT-UNASSIGN-001",
            "AUTH-C10-SGOD-ENT-SET-ASSIGNED-001", "AUTH-C10-SGOD-ENT-DELETED-001",
            "AUTH-C10-SGOD-ENT-GET-001", "AUTH-C10-SGOD-ENT-BLOCK-001",
            "AUTH-C10-SGOD-ENT-UNBLOCK-001", "AUTH-C10-SGOD-ENT-RESTORE-001",
            "AUTH-C10-SGOD-ENT-SUBSCRIPTION-001", "AUTH-C10-SGOD-ENT-FEATURES-001",
            "AUTH-C10-SGOD-ENT-STATS-BY-TENANT-001", "AUTH-C10-USERS-ORG-ASSIGN-001",
            "AUTH-C10-USERS-ORG-REMOVE-001", "AUTH-C10-USERS-ORG-BOSSES-AVAILABLE-001",
            "AUTH-C10-USERS-ORG-BOSSES-SET-001", "AUTH-C10-USERS-ORG-CHECK-SUBORDINATE-001",
            "AUTH-C10-ORG-AUDIT-001",
        ):
            if n.startswith(tc):
                by_tc[tc] = sub
                break

    # Define the 19 expected C10 items
    definitions = [
        # (TC_PREFIX, name, method, path, query, body_raw)
        ("AUTH-C10-SGOD-ENT-LIST-001",
         "List SGOD enterprises",
         "GET",
         "/sgod/enterprises",
         [("page", "1"), ("limit", "20"), ("search", "")],
         None),
        ("AUTH-C10-SGOD-ENT-OVERVIEW-001",
         "SGOD enterprises overview stats",
         "GET",
         "/sgod/enterprises/statistics/overview",
         [],
         None),
        ("AUTH-C10-SGOD-ENT-ASSIGN-001",
         "Assign tenant to user",
         "POST",
         "/sgod/enterprises/assign",
         [],
         '{"userId":"{{userId}}","tenantIds":["{{tenantIdB}}"]}'),
        ("AUTH-C10-SGOD-ENT-UNASSIGN-001",
         "Unassign tenant from user",
         "POST",
         "/sgod/enterprises/unassign",
         [],
         '{"userId":"{{userId}}","tenantId":"{{tenantIdB}}"}'),
        ("AUTH-C10-SGOD-ENT-SET-ASSIGNED-001",
         "Set assigned enterprises",
         "POST",
         "/sgod/enterprises/set-assigned",
         [],
         '{"userId":"{{userId}}","tenantIds":["{{tenantIdA}}","{{tenantIdC}}"]}'),
        ("AUTH-C10-SGOD-ENT-DELETED-001",
         "List deleted enterprises",
         "GET",
         "/sgod/enterprises/deleted",
         [("page", "1"), ("limit", "20")],
         None),
        ("AUTH-C10-SGOD-ENT-GET-001",
         "Get enterprise details",
         "GET",
         "/sgod/enterprises/{{tenantIdA}}",
         [],
         None),
        ("AUTH-C10-SGOD-ENT-BLOCK-001",
         "Block enterprise",
         "POST",
         "/sgod/enterprises/{{tenantIdB}}/block",
         [],
         '{"reason":"Policy violation - manual review"}'),
        ("AUTH-C10-SGOD-ENT-UNBLOCK-001",
         "Unblock enterprise",
         "POST",
         "/sgod/enterprises/{{tenantIdB}}/unblock",
         [],
         '{"reason":"Audit complete - unblock"}'),
        ("AUTH-C10-SGOD-ENT-RESTORE-001",
         "Restore deleted enterprise",
         "POST",
         "/sgod/enterprises/{{tenantDeletedId}}/restore",
         [],
         None),
        ("AUTH-C10-SGOD-ENT-SUBSCRIPTION-001",
         "Update enterprise subscription",
         "PATCH",
         "/sgod/enterprises/{{tenantIdA}}/subscription",
         [],
         '{"durationDays":365}'),
        ("AUTH-C10-SGOD-ENT-FEATURES-001",
         "Update enterprise features",
         "PATCH",
         "/sgod/enterprises/{{tenantIdA}}/features",
         [],
         '{"features":["audit_logging","sso","mfa_required"]}'),
        ("AUTH-C10-SGOD-ENT-STATS-BY-TENANT-001",
         "Get enterprise statistics by ID",
         "GET",
         "/sgod/enterprises/{{tenantIdA}}/statistics",
         [],
         None),
        ("AUTH-C10-USERS-ORG-ASSIGN-001",
         "Assign organizational",
         "POST",
         "/users/{{entUserBId}}/organizational/assign",
         [],
         '{"departmentId":"{{deptId}}","positionId":"{{posId}}","primaryRoleId":"{{primaryRoleId}}","bossId":"{{bossId}}","userType":"EnterpriseUser"}'),
        ("AUTH-C10-USERS-ORG-REMOVE-001",
         "Remove organizational",
         "POST",
         "/users/{{entUserBId}}/organizational/remove",
         [("userType", "enterprise_user")],
         None),
        ("AUTH-C10-USERS-ORG-BOSSES-AVAILABLE-001",
         "Get available bosses",
         "GET",
         "/users/{{entUserBId}}/organizational/bosses/available",
         [("userType", "enterprise_user")],
         None),
        ("AUTH-C10-USERS-ORG-BOSSES-SET-001",
         "Set boss",
         "POST",
         "/users/{{entUserBId}}/organizational/bosses/set",
         [],
         '{"bossId":"{{bossId}}","userType":"EnterpriseUser"}'),
        ("AUTH-C10-USERS-ORG-CHECK-SUBORDINATE-001",
         "Check subordinate relation",
         "GET",
         "/users/{{managerId}}/organizational/check-subordinate",
         [("subordinateId", "{{subordinateId}}")],
         None),
        ("AUTH-C10-ORG-AUDIT-001",
         "Audit organizational reporting lines",
         "GET",
         "/organizations/audit",
         [("tenantId", "{{tenantIdA}}")],
         None),
    ]

    new_subitems = []
    for tc_prefix, name, method, path, query, body_raw in definitions:
        url = build_url(path, query)
        # Find existing item or create new
        item = by_tc.get(tc_prefix)
        if item is None:
            item = {
                "name": f"[{tc_prefix}] {name}",
                "request": {
                    "method": method,
                    "header": [],
                    "url": url,
                    "body": None,
                },
            }
        # Update
        item["name"] = f"[{tc_prefix}] {name}"
        item["request"]["method"] = method
        item["request"]["url"] = url
        item["request"]["header"] = [
            {"key": "x-api-key", "value": "{{authApiKey}}"},
            {"key": "Authorization", "value": "Bearer {{accessToken}}"},
            {"key": "Content-Type", "value": "application/json"},
        ]
        if body_raw:
            item["request"]["body"] = {
                "mode": "raw",
                "raw": body_raw,
                "options": {"raw": {"language": "json"}},
            }
        else:
            item["request"]["body"] = None
        # Add 200 OK example + 401 example
        item["response"] = make_200_example() + make_401_example()
        new_subitems.append(item)

    target_folder["item"] = new_subitems

    with open(POSTMAN_PATH, "w", encoding="utf-8") as f:
        json.dump(col, f, ensure_ascii=False, indent=2)

    print(f"C10 Postman refactor: {len(new_subitems)} items")


if __name__ == "__main__":
    main()