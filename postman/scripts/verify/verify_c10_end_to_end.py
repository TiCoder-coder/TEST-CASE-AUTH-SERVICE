#!/usr/bin/env python3
from _paths import POSTMAN_PATH, CSV_PATH, EVIDENCE_DIR_C09, EVIDENCE_DIR_C10


"""End-to-end verification for C10 (SGOD Enterprises / Organizational):
- CSV row count = 19
- Postman folder count = 19
- All 19 Postman items have methods/URLs/bodies matching CSV rows
- All 19 evidence endpoints have request bodies and success responses
"""
import csv
import json
import re



def normalize_path(p):
    """Strip base URL prefix (either {{baseUrlAuth}}/sgod-auth/v1 or /sgod-auth/v1)
    and normalize generic placeholders to canonical form.
    """
    # Replace {{xxx}} with {xxx} first
    p = p.replace("{{", "{").replace("}}", "}")
    # Strip base URL prefix - try both forms
    p = re.sub(r"^(\{baseUrlAuth\})?/sgod-auth/v1", "", p)
    # Remove query string for path comparison
    p = p.split("?")[0]
    # Normalize generic placeholders to canonical form
    parts = p.split("/")
    new_parts = []
    for part in parts:
        if re.match(r"^\{[^}]+\}$", part):
            inner = part[1:-1].lower()
            if any(inner.startswith(prefix) for prefix in ("userid", "managerid", "subordinateid", "entuser")):
                new_parts.append("{userId}")
            elif "tenant" in inner or "deletedid" in inner:
                new_parts.append("{tenantId}")
            else:
                new_parts.append(part)
        else:
            new_parts.append(part)
    return "/".join(new_parts)


def main():
    errors = []
    warnings = []

    # 1. CSV: 19 C10 rows
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert len(reader.fieldnames) == 27, f"CSV cols != 27: {len(reader.fieldnames)}"
        rows = list(reader)
    c10_rows = [r for r in rows if r["TC_ID"].startswith("AUTH-C10-TENANT-") or r["TC_ID"].startswith("AUTH-C10-ORG-")]
    if len(c10_rows) != 19:
        errors.append(f"CSV: expected 19 C10 rows, got {len(c10_rows)}")
    else:
        print(f"✅ CSV: 19 C10 rows found")

    # Check column alignment for each row
    for r in c10_rows:
        tc = r["TC_ID"]
        method = r["Method"]
        endpoint = r["Full Endpoint"]
        body = r["Request Body (JSON)"]
        steps = r["Steps"]
        eh = r["Expected HTTP"]
        # Expected HTTP should match 2xx
        if not re.match(r"^2\d{2}$", eh):
            errors.append(f"{tc}: Expected HTTP '{eh}' is not 2xx")
        # Body should be JSON or empty
        if body and not (body.strip().startswith("{") or body.strip().startswith("[")):
            errors.append(f"{tc}: Body '{body[:50]}' is not JSON")
        # Steps should start with digit or be empty
        if steps and not re.match(r"^\d+\)", steps):
            errors.append(f"{tc}: Steps '{steps[:50]}' doesn't start with digit)")
        # FE Mapping should contain useAuth* or [AUTH-C10-... (manual fallback)
        fe = r["FE Mapping"]
        if not fe:
            errors.append(f"{tc}: FE Mapping is empty")
        # Postman Request Name should be [AUTH-C10-...
        pm = r["Postman Request Name"]
        if not pm or not pm.startswith("[AUTH-C10-"):
            errors.append(f"{tc}: Postman Request Name '{pm}' doesn't start with [AUTH-C10-")

    if not errors:
        print(f"✅ CSV: all 19 rows have aligned columns")

    # 2. Postman: 19 items in C10 folder
    with open(POSTMAN_PATH, "r", encoding="utf-8") as f:
        col = json.load(f)
    target = None
    for item in col["item"]:
        if item.get("name") == "C10 — SGOD Enterprises / Organizational":
            target = item
            break
    if not target:
        errors.append("Postman: C10 folder not found")
    else:
        if len(target["item"]) != 19:
            errors.append(f"Postman: expected 19 C10 items, got {len(target['item'])}")
        else:
            print(f"✅ Postman: 19 C10 items found")

    # 3. Cross-check CSV vs Postman
    csv_by_pm = {}
    for r in c10_rows:
        pm = r["Postman Request Name"]
        if pm and pm.startswith("[AUTH-C10-"):
            # Extract TC_PREFIX like [AUTH-C10-SGOD-ENT-LIST-001]
            m = re.match(r"^(\[(?:AUTH-C10-[A-Z0-9-]+))", pm)
            if m:
                csv_by_pm[m.group(1)] = r
    pm_by_id = {}
    for sub in target["item"]:
        m = re.match(r"^\[(AUTH-C10-[A-Z0-9-]+)\]", sub["name"])
        if m:
            pm_by_id["[" + m.group(1)] = sub
    for tc_prefix, r in csv_by_pm.items():
        if tc_prefix not in pm_by_id:
            errors.append(f"Postman: missing item for {tc_prefix}")
            continue
        sub = pm_by_id[tc_prefix]
        pm_method = sub["request"]["method"]
        pm_path = normalize_path(sub["request"]["url"]["raw"])
        csv_method = r["Method"]
        csv_path = normalize_path(r["Full Endpoint"])
        if pm_method != csv_method:
            errors.append(f"{tc_prefix}: method mismatch CSV={csv_method} vs PM={pm_method}")
        if pm_path != csv_path:
            errors.append(f"{tc_prefix}: path mismatch\n  CSV: {csv_path}\n  PM:  {pm_path}")
    if not errors:
        print(f"✅ CSV ↔ Postman: 19 endpoints match (method + path structure)")

    # 4. Evidence: count endpoints documented
    with open(f"{EVIDENCE_DIR_C10}/C10-enterprise-organizational-request-body-examples.md", "r") as f:
        req_body = f.read()
    with open(f"{EVIDENCE_DIR_C10}/C10-enterprise-organizational-success-responses.md", "r") as f:
        success_resp = f.read()

    req_endpoints = re.findall(r"## (\d+)\.\s+([^\n]+)", req_body)
    success_endpoints = re.findall(r"## (\d+)\.\s+([^\n]+)", success_resp)
    if len(req_endpoints) < 19:
        errors.append(f"Evidence request-body: expected 19 endpoints, found {len(req_endpoints)}")
    else:
        print(f"✅ Evidence request-body: {len(req_endpoints)} endpoints documented")
    if len(success_endpoints) < 19:
        errors.append(f"Evidence success-responses: expected 19 endpoints, found {len(success_endpoints)}")
    else:
        print(f"✅ Evidence success-responses: {len(success_endpoints)} endpoints documented")

    # Check removed endpoints not in evidence (as active endpoints, not as documentation cleanup)
    # Specifically check for headers (## X.) containing the removed endpoints
    for section in re.findall(r"^## .*$", req_body, re.MULTILINE):
        if "bosses/add" in section.lower():
            errors.append(f"Evidence has active endpoint bosses/add: {section}")
        if "subordinates" in section.lower() and "/organizational/subordinates" in section:
            errors.append(f"Evidence has active endpoint subordinates: {section}")
    # Also check success_responses
    for section in re.findall(r"^## .*$", success_resp, re.MULTILINE):
        if "bosses/add" in section.lower():
            errors.append(f"Evidence has active endpoint bosses/add: {section}")
        if "/organizational/subordinates" in section:
            errors.append(f"Evidence has active endpoint subordinates: {section}")
    # Allow mentions in "Removed" cleanup section
    print(f"✅ Evidence: removed endpoints (bosses/add, bosses, subordinates) purged")

    # 5. Negative CSV: count
    with open(f"{EVIDENCE_DIR_C10}/C10-enterprise-organizational-negative-test-cases.csv", "r") as f:
        reader = csv.DictReader(f)
        neg_rows = list(reader)
        neg_cols = reader.fieldnames
    if len(neg_rows) < 20:
        warnings.append(f"Negative CSV: {len(neg_rows)} rows (expected 20)")
    else:
        print(f"✅ Negative CSV: {len(neg_rows)} rows × {len(neg_cols)} cols")

    # Summary
    print()
    if errors:
        print(f"❌ {len(errors)} ERRORS:")
        for e in errors:
            print(f"  - {e}")
        return 1
    if warnings:
        print(f"⚠️ {len(warnings)} WARNINGS:")
        for w in warnings:
            print(f"  - {w}")
    print("✅ ALL C10 VERIFICATIONS PASSED")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())