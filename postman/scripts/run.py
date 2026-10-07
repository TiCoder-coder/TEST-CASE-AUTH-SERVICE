#!/usr/bin/env python3
"""Master runner script for all test-case refactor/verify scripts.

Usage:
    python3 docs/test-case/postman/scripts/run.py <script_name> [args...]

Examples:
    python3 docs/test-case/postman/scripts/run.py verify/verify_c09_end_to_end.py
    python3 docs/test-case/postman/scripts/run.py verify/verify_c10_end_to_end.py
    python3 docs/test-case/postman/scripts/run.py csv/refactor_cluster_c09.py

This wrapper:
1. Adds the scripts/ directory to sys.path so `from _paths import ...` works
2. Runs the requested script with any additional arguments
"""
import sys
import os
import importlib.util
import runpy

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 run.py <script_name> [args...]")
        print("Example: python3 run.py verify/verify_c09_end_to_end.py")
        sys.exit(1)

    script_rel = sys.argv[1]
    script_path = os.path.join(SCRIPTS_DIR, script_rel)
    if not os.path.exists(script_path):
        print(f"❌ Script not found: {script_path}")
        sys.exit(1)

    # Add scripts/ to sys.path so _paths can be imported
    if SCRIPTS_DIR not in sys.path:
        sys.path.insert(0, SCRIPTS_DIR)

    # Use runpy to execute the script with arguments
    args = sys.argv[2:]
    sys.argv = [script_path] + args
    try:
        runpy.run_path(script_path, run_name="__main__")
    except SystemExit as e:
        sys.exit(e.code)


if __name__ == "__main__":
    main()