#!/usr/bin/env python3
from _paths import POSTMAN_PATH


"""Add reason body to C09 BLOCK/UNBLOCK items to match CSV body."""
import json



def main():
    with open(POSTMAN_PATH, "r", encoding="utf-8") as f:
        col = json.load(f)

    updated = []
    for item in col["item"]:
        if item.get("name") == "C09 — Sub-Enterprises":
            for sub in item["item"]:
                name = sub.get("name", "")
                if "SUBENT-BLOCK-001" in name:
                    sub["request"]["body"] = {
                        "mode": "raw",
                        "raw": "{\n  \"reason\": \"Manual review - test block\"\n}",
                        "options": {"raw": {"language": "json"}},
                    }
                    updated.append(name)
                elif "SUBENT-UNBLOCK-001" in name:
                    sub["request"]["body"] = {
                        "mode": "raw",
                        "raw": "{\n  \"reason\": \"Audit done - unblock\"\n}",
                        "options": {"raw": {"language": "json"}},
                    }
                    updated.append(name)
            break

    with open(POSTMAN_PATH, "w", encoding="utf-8") as f:
        json.dump(col, f, ensure_ascii=False, indent=2)

    print(f"Updated {len(updated)} items: {updated}")


if __name__ == "__main__":
    main()