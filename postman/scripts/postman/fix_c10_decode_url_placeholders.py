#!/usr/bin/env python3
from _paths import POSTMAN_PATH


"""Decode URL-encoded {{var}} placeholders in raw URL for C10 Postman items."""
import json



def main():
    with open(POSTMAN_PATH, "r", encoding="utf-8") as f:
        col = json.load(f)

    for item in col["item"]:
        if item.get("name") == "C10 — SGOD Enterprises / Organizational":
            for sub in item["item"]:
                url = sub["request"]["url"]
                raw = url.get("raw", "")
                if "%7B%7B" in raw:
                    raw = raw.replace("%7B%7B", "{{").replace("%7D%7D", "}}")
                    url["raw"] = raw
            break

    with open(POSTMAN_PATH, "w", encoding="utf-8") as f:
        json.dump(col, f, ensure_ascii=False, indent=2)
    print("Raw URLs fixed")


if __name__ == "__main__":
    main()