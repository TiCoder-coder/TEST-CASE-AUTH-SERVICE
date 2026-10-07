#!/usr/bin/env python3
from _paths import POSTMAN_PATH
"""Refactor C09 (Sub-Enterprises) Postman folder:
1. CREATE: body userType sub_enterprise -> EnterpriseUser
2. STATS: URL /statistics -> /stats
3. UPDATE: body adds avatarUrl + email + gender=MALE
4. ORG: POST -> PATCH, body removes primaryRoleId, adds userType=EnterpriseUser
5. ROLES: POST -> PATCH, body keeps roleIds[]
6. SET-BOSS: path /boss -> /bosses, body adds userType=EnterpriseUser
7. PROFILE/ME/MY-PROFILE: body keeps email + gender=MALE
8. Append 3 NEW items: PERMANENT, GET-ORG, GET-ROLES
"""

import json
import copy

COLLECTION_PATH = POSTMAN_PATH

BASE = "{{baseUrlAuth}}"
PREFIX = "/sgod-auth/v1/sub-enterprises"

STD_HEADERS = [
    {"key": "x-api-key", "value": "{{authApiKey}}", "type": "text"},
    {"key": "Authorization", "value": "Bearer {{accessToken}}", "type": "text"},
    {"key": "x-device-id", "value": "{{deviceId}}", "type": "text"},
]

CT_HEADER = {"key": "Content-Type", "value": "application/json", "type": "text"}


def make_request(name, method, raw_url, path_parts, headers, body_raw=None):
    req = {
        "method": method,
        "header": headers,
        "url": {
            "raw": raw_url,
            "host": [BASE],
            "path": path_parts,
        },
    }
    if body_raw is not None:
        req["body"] = {"mode": "raw", "raw": body_raw}
    return {
        "name": name,
        "event": [
            {
                "listen": "test",
                "script": {
                    "exec": [
                        "pm.test(\"Status is 200\", function () { pm.response.to.have.status(200); });",
                        "pm.test(\"Response has expected fields\", function () { var d=pm.response.json(); pm.expect(d).to.have.property(\"data\"); });"
                    ]
                },
            }
        ],
        "request": req,
        "description": f"TC_ID: {name.split(']')[0].lstrip('[')}",
    }


def make_path(parts):
    """Build path string '/sgod-auth/v1/sub-enterprises/...' from parts."""
    return PREFIX + ("/" + "/".join(parts) if parts else "")


def main():
    with open(COLLECTION_PATH, "r", encoding="utf-8") as f:
        collection = json.load(f)

    # Find C09 folder
    c09_folder = None
    c10_idx = -1
    for i, item in enumerate(collection.get("item", [])):
        if item.get("name") == "C09 — Sub-Enterprises":
            c09_folder = item
            c09_idx = i
        elif item.get("name") == "C10 — SGOD Enterprises / Organizational":
            c10_idx = i
            break

    if c09_folder is None:
        print("C09 folder not found")
        return

    # REWRITE each item
    items = c09_folder["item"]
    new_items = []

    for item in items:
        name = item["name"]
        req = item.get("request", {})
        method = req.get("method", "GET").upper()
        body = req.get("body", {})
        old_raw = body.get("raw") if isinstance(body, dict) else None

        new_item = copy.deepcopy(item)

        if name == "[AUTH-C09-SUBENT-CREATE-001] Create sub-enterprise":
            new_item["request"]["body"]["raw"] = (
                '{"email":"{{newSubentEmail}}","userName":"{{newSubentName}}",'
                '"fullName":{"firstName":"Sub","lastName":"Enterprise"},'
                '"phone":"0900000005","gender":"Male",'
                '"departmentId":"{{deptId}}","positionId":"{{posId}}",'
                '"roleIds":["{{roleId1}}"],"userType":"EnterpriseUser"}'
            )
        elif name == "[AUTH-C09-SUBENT-STATS-001] Sub-enterprise statistics":
            url = new_item["request"]["url"]
            url["raw"] = f"{BASE}{make_path(['stats'])}"
            url["path"] = ["sgod-auth", "v1", "sub-enterprises", "stats"]
        elif name == "[AUTH-C09-SUBENT-UPDATE-001] Update sub-enterprise":
            new_item["request"]["body"]["raw"] = (
                '{"fullName":{"firstName":"Updated","lastName":"SubEnt"},'
                '"email":"{{newSubentEmail}}","phone":"0900000001",'
                '"gender":"MALE",'
                '"avatarUrl":"https://cdn.sgod.test/avatars/subent-a-001.png"}'
            )
        elif name == "[AUTH-C09-SUBENT-ROLES-001] Set sub-ent roles":
            new_item["request"]["method"] = "PATCH"
            url = new_item["request"]["url"]
            url["raw"] = f"{BASE}{make_path(['{{subentAId}}', 'roles'])}"
            url["path"] = ["sgod-auth", "v1", "sub-enterprises", "{{subentAId}}", "roles"]
            new_item["request"]["body"]["raw"] = '{"roleIds":["{{roleId1}}","{{roleId2}}"]}'
        elif name == "[AUTH-C09-SUBENT-ORG-001] Set organizational":
            new_item["request"]["method"] = "PATCH"
            url = new_item["request"]["url"]
            url["raw"] = f"{BASE}{make_path(['{{subentAId}}', 'organizational'])}"
            url["path"] = ["sgod-auth", "v1", "sub-enterprises", "{{subentAId}}", "organizational"]
            new_item["request"]["body"]["raw"] = (
                '{"departmentId":"{{deptId}}","positionId":"{{posId}}",'
                '"bossId":"{{bossId}}","userType":"EnterpriseUser"}'
            )
        elif name == "[AUTH-C09-SUBENT-BOSS-001] Set boss":
            url = new_item["request"]["url"]
            url["raw"] = f"{BASE}{make_path(['{{subentAId}}', 'bosses'])}"
            url["path"] = ["sgod-auth", "v1", "sub-enterprises", "{{subentAId}}", "bosses"]
            new_item["request"]["body"]["raw"] = '{"bossId":"{{bossId}}","userType":"EnterpriseUser"}'
        elif name in (
            "[AUTH-C09-SUBENT-MY-PROFILE-001] Update my-profile",
            "[AUTH-C09-SUBENT-PROFILE-001] Update profile",
            "[AUTH-C09-SUBENT-ME-001] Update me",
        ):
            new_item["request"]["body"]["raw"] = (
                '{"fullName":{"firstName":"Updated","lastName":"SubEnt"},'
                '"email":"{{actorEmail}}","phone":"0900000001","gender":"MALE"}'
            )

        new_items.append(new_item)

    # APPEND 3 NEW ITEMS
    headers_post = STD_HEADERS + [CT_HEADER]

    new_items.append(
        make_request(
            name="[AUTH-C09-SUBENT-PERMANENT-001] Permanent delete sub-enterprise",
            method="DELETE",
            raw_url=f"{BASE}{make_path(['{{subentPermanentId}}', 'permanent'])}",
            path_parts=["sgod-auth", "v1", "sub-enterprises", "{{subentPermanentId}}", "permanent"],
            headers=STD_HEADERS,
            body_raw=None,
        )
    )

    new_items.append(
        make_request(
            name="[AUTH-C09-SUBENT-GET-ORG-001] Get organizational",
            method="GET",
            raw_url=f"{BASE}{make_path(['{{subentAId}}', 'organizational'])}",
            path_parts=["sgod-auth", "v1", "sub-enterprises", "{{subentAId}}", "organizational"],
            headers=STD_HEADERS,
            body_raw=None,
        )
    )

    new_items.append(
        make_request(
            name="[AUTH-C09-SUBENT-GET-ROLES-001] Get roles",
            method="GET",
            raw_url=f"{BASE}{make_path(['{{subentAId}}', 'roles'])}",
            path_parts=["sgod-auth", "v1", "sub-enterprises", "{{subentAId}}", "roles"],
            headers=STD_HEADERS,
            body_raw=None,
        )
    )

    c09_folder["item"] = new_items

    with open(COLLECTION_PATH, "w", encoding="utf-8") as f:
        json.dump(collection, f, indent=2, ensure_ascii=False)

    print(f"C09 Postman refactor complete: {len(new_items)} items in C09 folder")


if __name__ == "__main__":
    main()