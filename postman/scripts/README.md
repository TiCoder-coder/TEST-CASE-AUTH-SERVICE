# Test-Case Refactor & Verification Scripts

> **Last updated**: 2026-10-07
> **Total scripts**: 20 Python files + 1 master wrapper
> **Verify status**: C09 ✅ PASS | C10 ✅ PASS

This directory contains all Python scripts used to refactor and verify the SGOD Auth Service test case artifacts. All scripts share path constants via `_paths.py` and can be executed via the `run.py` master wrapper.

---

## Table of Contents

1. [Directory Structure](#directory-structure)
2. [Quick Start](#quick-start)
3. [Shared Path Constants](#shared-path-constants)
4. [CSV Refactor Scripts](#csv-refactor-scripts)
5. [Postman Refactor Scripts](#postman-refactor-scripts)
6. [Verify Scripts](#verify-scripts)
7. [Adding a New Script](#adding-a-new-script)
8. [Troubleshooting](#troubleshooting)

---

## Directory Structure

```
scripts/
├── README.md                              ← This file
├── _paths.py                              ← Shared path constants (CSV, POSTMAN, EVIDENCE)
├── run.py                                 ← Master wrapper: adds scripts/ to sys.path
│
├── csv/                                   ← CSV refactor scripts (target: auth_test_cases.csv)
│   ├── refactor_cluster_c09.py            ← Main C09 CSV refactor
│   ├── refactor_cluster_c10.py            ← Main C10 CSV refactor
│   ├── repair_c09_column_shifts.py        ← Repair C09 column shifts
│   ├── repair_c10_column_shifts.py        ← Auto-detect C10 column shifts
│   ├── repair_c10_shift_bodies.py         ← Shift repair for C10 bodies
│   ├── repair_c10_remaining_shifts.py     ← Catch-all shift repair
│   ├── repair_c10_manual_overrides.py     ← Manual overrides for specific TCs
│   └── repair_c10_missing_steps.py        ← Add missing Steps text
│
├── postman/                               ← Postman JSON refactor scripts (target: collections/*.json)
│   ├── refactor_postman_c09.py            ← Main C09 Postman refactor
│   ├── refactor_postman_c10.py            ← Main C10 Postman refactor
│   ├── fix_c01_c02_postman_mismatches.py  ← Fix C01/C02 endpoint mismatches
│   ├── fix_c09_block_unblock_body.py      ← Fix C09 block/unblock body
│   ├── fix_c10_decode_url_placeholders.py ← Fix C10 URL placeholder decoding
│   ├── fix_c10_url_query_arrays.py        ← Fix C10 URL query arrays
│   ├── normalize_collection_schema.py     ← Normalize collection to v2.1.1
│   ├── pretty_print_request_response_bodies.py  ← Pretty-print JSON bodies
│   ├── pretty_print_evidence_markdown.py        ← Pretty-print JSON in evidence .md
│   └── add_concrete_200_401_examples.py         ← Add 200/401 example bodies
│
└── verify/                                ← End-to-end verification scripts
    ├── verify_c09_end_to_end.py           ← C09 verify (CSV + Postman + Evidence)
    └── verify_c10_end_to_end.py           ← C10 verify (CSV + Postman + Evidence)
```

---

## Quick Start

### Master Wrapper (Recommended)

Use `run.py` from the **repository root** to execute any script. The wrapper automatically adds the `scripts/` directory to `sys.path` so `from _paths import ...` works from any subdirectory.

```bash
# From repo root (SAM-V2/)

# Verify C09
python3 docs/test-case/postman/scripts/run.py verify/verify_c09_end_to_end.py

# Verify C10
python3 docs/test-case/postman/scripts/run.py verify/verify_c10_end_to_end.py

# Run a refactor script
python3 docs/test-case/postman/scripts/run.py csv/refactor_cluster_c09.py
python3 docs/test-case/postman/scripts/run.py postman/pretty_print_request_response_bodies.py
```

### Direct Execution

You can execute scripts directly if you're in the `scripts/` directory or have it on your Python path:

```bash
cd docs/test-case/postman/scripts
python3 verify/verify_c10_end_to_end.py
```

---

## Shared Path Constants

All scripts use shared path constants from `_paths.py`. This ensures paths are **relative to the scripts directory** and work regardless of where scripts are executed from.

| Symbol | Resolved Path |
|--------|---------------|
| `CSV_PATH` | `docs/test-case/auth_test_cases.csv` |
| `POSTMAN_PATH` | `docs/test-case/postman/collections/SGOD_Auth_Service.postman_collection.json` |
| `EVIDENCE_DIR_C09` | `docs/test-case/evidence/C09-sub-enterprises/` |
| `EVIDENCE_DIR_C10` | `docs/test-case/evidence/C10-enterprise-organizational/` |
| `REPO_ROOT` | `<repo-root>/` |
| `TESTCASE_DIR` | `<repo-root>/docs/test-case/` |

### Usage Example

```python
from _paths import CSV_PATH, POSTMAN_PATH, EVIDENCE_DIR_C09

# Read CSV
with open(CSV_PATH, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)

# Read Postman collection
with open(POSTMAN_PATH, "r", encoding="utf-8") as f:
    col = json.load(f)

# Read evidence file
fp = os.path.join(EVIDENCE_DIR_C09, "C09-sub-enterprises-request-body-examples.md")
```

---

## CSV Refactor Scripts

These scripts refactor the master CSV file (`auth_test_cases.csv`) — 180 rows × 27 columns.

### `csv/refactor_cluster_c09.py`

**Purpose**: Main C09 (Sub-Enterprises) CSV refactor. Updates:
- CREATE body: `userType: sub_enterprise` → `EnterpriseUser`
- UPDATE body: add `fullName/email/phone/gender` per `ParamUpdateSubEnterpriseUser`
- STATS endpoint: `/statistics` → `/stats`
- PERMANENT: add new `DELETE /sub-enterprises/{userId}/permanent`
- ORG: `POST` → `PATCH` + remove `primaryRoleId`
- ROLES: `POST` → `PATCH`
- GET-ORG: add new `GET /sub-enterprises/{userId}/organizational`
- GET-ROLES: add new `GET /sub-enterprises/{userId}/roles`
- SET-BOSS: `/boss` → `/bosses` + `userType: EnterpriseUser`

**Run**:
```bash
python3 docs/test-case/postman/scripts/run.py csv/refactor_cluster_c09.py
```

### `csv/refactor_cluster_c10.py`

**Purpose**: Main C10 (Tenant Management) CSV refactor. Updates 19 endpoints with corrected methods, paths, and bodies.

**Run**:
```bash
python3 docs/test-case/postman/scripts/run.py csv/refactor_cluster_c10.py
```

### `csv/repair_c09_column_shifts.py`

**Purpose**: Detect and fix column shifts in C09 rows where JSON body contains newlines (breaks CSV parser).

**Run**:
```bash
python3 docs/test-case/postman/scripts/run.py csv/repair_c09_column_shifts.py
```

### `csv/repair_c10_column_shifts.py`

**Purpose**: Auto-detect C10 column shifts based on column header matching.

**Run**:
```bash
python3 docs/test-case/postman/scripts/run.py csv/repair_c10_column_shifts.py
```

### Other CSV repair scripts

| Script | Purpose |
|--------|---------|
| `repair_c10_shift_bodies.py` | Shift repair for C10 request bodies |
| `repair_c10_remaining_shifts.py` | Catch-all shift repair |
| `repair_c10_manual_overrides.py` | Manual overrides for specific TCs |
| `repair_c10_missing_steps.py` | Add missing Steps text |

---

## Postman Refactor Scripts

These scripts refactor the Postman collection v2.1.1 JSON file.

### `postman/refactor_postman_c09.py`

**Purpose**: Main C09 Postman folder refactor. Updates body schemas, adds new items, fixes paths.

**Run**:
```bash
python3 docs/test-case/postman/scripts/run.py postman/refactor_postman_c09.py
```

### `postman/refactor_postman_c10.py`

**Purpose**: Main C10 Postman folder refactor. Updates methods, paths, bodies, headers for 19 endpoints.

**Run**:
```bash
python3 docs/test-case/postman/scripts/run.py postman/refactor_postman_c10.py
```

### `postman/fix_c01_c02_postman_mismatches.py`

**Purpose**: Fix 9 endpoint mismatches in C01 + C02 based on FE source code + Swagger screenshots.

### `postman/fix_c09_block_unblock_body.py`

**Purpose**: Fix C09 block/unblock request bodies to include `{ "reason": "..." }` matching CSV.

### `postman/fix_c10_decode_url_placeholders.py`

**Purpose**: Decode URL-encoded `{{var}}` placeholders (e.g., `%7B%7BuserId%7D%7D` → `{{userId}}`).

### `postman/fix_c10_url_query_arrays.py`

**Purpose**: Convert single-value query params to arrays (e.g., `?status=A` → `?status[]=A`).

### `postman/normalize_collection_schema.py`

**Purpose**: Normalize Postman v2.1.1 schema — move `url` from top-level into `request.url` for all requests.

### `postman/pretty_print_request_response_bodies.py`

**Purpose**: Pretty-print all JSON request and response bodies in the collection with 2-space indent.

**Run**:
```bash
python3 docs/test-case/postman/scripts/run.py postman/pretty_print_request_response_bodies.py
```

### `postman/pretty_print_evidence_markdown.py`

**Purpose**: Pretty-print JSON inside markdown code blocks for evidence files (`evidence/C10-**/*.md`).

**Run**:
```bash
python3 docs/test-case/postman/scripts/run.py postman/pretty_print_evidence_markdown.py
```

### `postman/add_concrete_200_401_examples.py`

**Purpose**: Add concrete 200 success + 401 unauthorized example bodies to every request in the collection.

---

## Verify Scripts

End-to-end verification — checks CSV ↔ Postman ↔ Evidence alignment.

### `verify/verify_c09_end_to_end.py`

**Verifies**:
- ✅ CSV has 20 C09 rows
- ✅ Postman has 20 C09 items
- ✅ CSV `Postman Request Name` matches Postman `item.name` (20 items)
- ✅ All 4 evidence files exist for C09

**Run**:
```bash
python3 docs/test-case/postman/scripts/run.py verify/verify_c09_end_to_end.py
```

**Expected output**:
```
[OK] CSV total rows: 180, C09 rows: 20
[OK] Postman C09 items: 20
[OK] CSV ↔ Postman name alignment (20 items)
[OK] Evidence file: C09-sub-enterprises-request-body-examples.md (8013 bytes)
[OK] Evidence file: C09-sub-enterprises-success-responses.md (10379 bytes)
[OK] Evidence file: C09-sub-enterprises-error-responses.md (2005 bytes)
[OK] Evidence file: C09-sub-enterprises-negative-test-cases.csv (4283 bytes)

============================================================
✅ ALL CHECKS PASSED
```

### `verify/verify_c10_end_to_end.py`

**Verifies**:
- ✅ CSV has 19 C10 rows
- ✅ CSV has 19 aligned columns
- ✅ Postman has 19 C10 items
- ✅ CSV ↔ Postman endpoint match (19 endpoints)
- ✅ Evidence request-body: 19 endpoints documented
- ✅ Evidence success-responses: 19 endpoints documented
- ✅ Removed endpoints purged
- ✅ Negative CSV: 20 rows × 20 cols

**Run**:
```bash
python3 docs/test-case/postman/scripts/run.py verify/verify_c10_end_to_end.py
```

**Expected output**:
```
✅ CSV: 19 C10 rows found
✅ CSV: all 19 rows have aligned columns
✅ Postman: 19 C10 items found
✅ CSV ↔ Postman: 19 endpoints match (method + path structure)
✅ Evidence request-body: 19 endpoints documented
✅ Evidence success-responses: 19 endpoints documented
✅ Evidence: removed endpoints (bosses/add, bosses, subordinates) purged
✅ Negative CSV: 20 rows × 20 cols

✅ ALL C10 VERIFICATIONS PASSED
```

---

## Adding a New Script

1. **Choose the right folder**:
   - `csv/` — if script modifies `auth_test_cases.csv`
   - `postman/` — if script modifies the Postman collection JSON
   - `verify/` — if script verifies end-to-end alignment

2. **Add imports at top** (after shebang/docstring):
   ```python
   from _paths import CSV_PATH, POSTMAN_PATH  # only import what you need
   ```

3. **Use the imported constants** instead of hardcoded paths:
   ```python
   with open(CSV_PATH, "r", encoding="utf-8") as f:
       ...
   ```

4. **Test** by running via `run.py` wrapper:
   ```bash
   python3 docs/test-case/postman/scripts/run.py <subdir>/<script_name>.py
   ```

5. **Update this README** with the new script under the appropriate section.

---

## Troubleshooting

### `ModuleNotFoundError: No module named '_paths'`

**Cause**: Python can't find `_paths.py` because script runs from a subdirectory without `scripts/` on sys.path.

**Solution**: Always use the `run.py` master wrapper:
```bash
python3 docs/test-case/postman/scripts/run.py verify/verify_c09_end_to_end.py
```

The wrapper adds `scripts/` to `sys.path` before running the target script.

### Path constants not resolving correctly

**Cause**: `_paths.py` uses `os.path.dirname(__file__)` which is correct only when the script is run as a file (not imported as a module).

**Solution**: If you must import scripts as modules, prepend `scripts/` to `sys.path` first:
```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from _paths import CSV_PATH
```

### Verify script returns 0 errors but C09/C10 still inconsistent

**Cause**: Verify scripts only check name alignment + file existence, not body content. They don't check if bodies match contracts.

**Solution**: Use Postman Runner in Postman UI to actually execute requests against the BE and verify responses.

### CSV column shifts after edits

**Cause**: Manual edit introduced newlines in JSON body fields, breaking CSV parser.

**Solution**: Run `csv/repair_c09_column_shifts.py` or `csv/repair_c10_column_shifts.py` to auto-detect and fix.

---

## Related Documentation

- [Test Plan (in main README)](../../README.md#11-quy-trình-nghiệp-vụ-test-workflow) — execution order + success criteria + reporting + regression
- [Test Cases CSV](../../auth_test_cases.csv) — master CSV (180 rows × 27 columns)
- [Endpoint Inventory](../../specifications/endpoint_inventory.md) — 176 endpoints
- [Authentication Rules](../../specifications/authentication_rules.md) — auth/MFA/session
- [Authorization Matrix](../../specifications/authorization_matrix.md) — permissions/roles
- [Test Data Strategy](../../specifications/test_data_strategy.md) — fixtures/actors