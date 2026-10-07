#!/usr/bin/env python3
from _paths import POSTMAN_PATH


"""Pretty-print all JSON bodies in Postman collection (request + response).

For each item:
- Parse the body as JSON if possible
- Re-serialize with 2-space indent (matching example structure)
- Preserve fields in original order
- Skip non-JSON bodies (e.g. tenantId=enterprise_user, plain strings)
- Skip bodies that contain Postman placeholder syntax like {{var}}

For response bodies (examples), also format the body field.
"""
import json
import sys
import re



def is_json_parsable(s):
    """Check if string can be parsed as JSON."""
    if not s or not isinstance(s, str):
        return False
    s = s.strip()
    if not (s.startswith("{") or s.startswith("[")):
        return False
    try:
        json.loads(s)
        return True
    except (json.JSONDecodeError, ValueError):
        return False


def is_postman_placeholders_only(s):
    """Check if body is just placeholder syntax like {{var}}=value pairs (not JSON)."""
    # Query-like: userId={{userId}}
    if re.match(r"^[a-zA-Z]+\s*=\s*\{\{", s):
        return True
    return False


def pretty_json(s):
    """Pretty-print JSON string with 2-space indent matching example."""
    if not s:
        return s
    parsed = json.loads(s)
    return json.dumps(parsed, indent=2, ensure_ascii=False)


def format_request_body(body_dict):
    """If body is raw + JSON, pretty-print it."""
    if not isinstance(body_dict, dict):
        return body_dict
    if body_dict.get("mode") != "raw":
        return body_dict
    raw = body_dict.get("raw", "")
    if not raw:
        return body_dict
    if is_postman_placeholders_only(raw):
        return body_dict
    if not is_json_parsable(raw):
        return body_dict
    new_raw = pretty_json(raw)
    body_dict["raw"] = new_raw
    return body_dict


def format_response_body(resp_obj):
    """If response body is JSON string, pretty-print it."""
    if not isinstance(resp_obj, dict):
        return resp_obj
    body = resp_obj.get("body", "")
    if not body or not isinstance(body, str):
        return resp_obj
    if is_postman_placeholders_only(body):
        return resp_obj
    if not is_json_parsable(body):
        return resp_obj
    new_body = pretty_json(body)
    resp_obj["body"] = new_body
    return resp_obj


def walk(items):
    """Walk Postman items, format bodies in-place."""
    formatted_req = 0
    formatted_resp = 0
    skipped_req = 0
    skipped_resp = 0
    for item in items:
        if isinstance(item.get("item"), list):
            sub_r, sub_resp = walk(item["item"])
            formatted_req += sub_r
            formatted_resp += sub_resp
        else:
            req = item.get("request", {})
            body = req.get("body")
            if isinstance(body, dict):
                old_raw = body.get("raw", "")
                if old_raw and is_json_parsable(old_raw) and not is_postman_placeholders_only(old_raw):
                    format_request_body(body)
                    if body.get("raw") != old_raw:
                        formatted_req += 1
                elif old_raw:
                    skipped_req += 1
            for resp in item.get("response", []) or []:
                old_body = resp.get("body", "")
                if old_body and isinstance(old_body, str) and is_json_parsable(old_body) and not is_postman_placeholders_only(old_body):
                    format_response_body(resp)
                    if resp.get("body") != old_body:
                        formatted_resp += 1
                elif old_body:
                    skipped_resp += 1
    return formatted_req, formatted_resp


def main():
    with open(POSTMAN_PATH, "r", encoding="utf-8") as f:
        col = json.load(f)

    total_req, total_resp = walk(col["item"])

    with open(POSTMAN_PATH, "w", encoding="utf-8") as f:
        json.dump(col, f, ensure_ascii=False, indent=2)

    print(f"Formatted {total_req} request bodies")
    print(f"Formatted {total_resp} response bodies")
    return 0


if __name__ == "__main__":
    sys.exit(main())