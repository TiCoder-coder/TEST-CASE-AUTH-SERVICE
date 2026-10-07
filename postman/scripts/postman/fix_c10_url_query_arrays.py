#!/usr/bin/env python3
from _paths import POSTMAN_PATH


"""Fix URL encoding issue in Postman C10 query strings.

Postman v2.1.1 schema preserves `{{var}}` placeholders WITHOUT percent-encoding
the curly braces. Update the query array to use disabled=true on encode, or
simply not put them in query array but in raw URL only.

Solution: keep raw URL with literal {{var}} placeholders, and mark query items
with disabled: false but the raw URL is the source of truth.
"""
import json



def main():
    with open(POSTMAN_PATH, "r", encoding="utf-8") as f:
        col = json.load(f)

    for item in col["item"]:
        if item.get("name") == "C10 — SGOD Enterprises / Organizational":
            for sub in item["item"]:
                url = sub["request"]["url"]
                raw = url.get("raw", "")
                if "?" not in raw:
                    continue
                base, qs_str = raw.split("?", 1)
                # Re-parse qs_str manually to keep {{var}} intact
                pairs = []
                if qs_str:
                    for part in qs_str.split("&"):
                        if "=" not in part:
                            continue
                        k, v = part.split("=", 1)
                        pairs.append({"key": k, "value": v})
                url["query"] = pairs
            break

    with open(POSTMAN_PATH, "w", encoding="utf-8") as f:
        json.dump(col, f, ensure_ascii=False, indent=2)
    print("URL query arrays fixed")


if __name__ == "__main__":
    main()