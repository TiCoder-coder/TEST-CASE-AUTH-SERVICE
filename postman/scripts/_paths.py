"""
Common path constants for all test-case refactor / verify scripts.

These paths are computed relative to the REPO ROOT using:
- REPO_ROOT = parent of `docs/test-case/postman/scripts/`

This means scripts can be run from anywhere using either:
  python3 docs/test-case/postman/scripts/csv/refactor_cluster_c09.py
  python3 docs/test-case/postman/scripts/verify/verify_c09_end_to_end.py

Paths:
- CSV_PATH: docs/test-case/auth_test_cases.csv
- POSTMAN_PATH: docs/test-case/postman/collections/SGOD_Auth_Service.postman_collection.json
- EVIDENCE_DIR_C09: docs/test-case/evidence/C09-sub-enterprises
- EVIDENCE_DIR_C10: docs/test-case/evidence/C10-enterprise-organizational
"""
import os

# scripts/ -> postman/ -> test-case/ -> repo_root
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))           # .../postman/scripts/
POSTMAN_DIR = os.path.dirname(SCRIPTS_DIR)                          # .../postman/
TESTCASE_DIR = os.path.dirname(POSTMAN_DIR)                         # .../docs/test-case/
REPO_ROOT = os.path.dirname(TESTCASE_DIR)                           # .../SAM-V2/

CSV_PATH = os.path.join(TESTCASE_DIR, "auth_test_cases.csv")
POSTMAN_PATH = os.path.join(POSTMAN_DIR, "collections", "SGOD_Auth_Service.postman_collection.json")
EVIDENCE_DIR = os.path.join(TESTCASE_DIR, "evidence")
EVIDENCE_DIR_C09 = os.path.join(EVIDENCE_DIR, "C09-sub-enterprises")
EVIDENCE_DIR_C10 = os.path.join(EVIDENCE_DIR, "C10-enterprise-organizational")