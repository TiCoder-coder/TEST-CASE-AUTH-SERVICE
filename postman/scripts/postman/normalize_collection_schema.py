#!/usr/bin/env python3
from _paths import POSTMAN_PATH
"""
Normalize Postman v2.1 schema:
Move 'url' from top-level into 'request.url' for all requests in collection.
This ensures schema compliance and avoids the 'both' state that confuses tools.
"""

import json
from copy import deepcopy

PATH = POSTMAN_PATH

with open(PATH, 'r', encoding='utf-8') as f:
    col = json.load(f)


def normalize_item(item):
    """Normalize a single item (request or folder)."""
    if not isinstance(item, dict):
        return
    # If it's a request (has 'name' but no nested 'item')
    if 'request' in item and 'item' not in item:
        req = item.setdefault('request', {})
        # Move url from top-level to request.url if needed
        top_url = item.get('url')
        req_url = req.get('url')
        if top_url and not req_url:
            req['url'] = top_url
            del item['url']
        elif top_url and req_url:
            # Both exist - prefer request.url (already the correct one)
            del item['url']
    # Recurse into folders
    if 'item' in item and isinstance(item['item'], list):
        for sub in item['item']:
            normalize_item(sub)


# Normalize all top-level folders
for folder in col['item']:
    normalize_item(folder)

# Save back
with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(col, f, indent=2, ensure_ascii=False)

# Verify
with open(PATH, 'r', encoding='utf-8') as f:
    col2 = json.load(f)

in_request = 0
in_toplevel = 0
both = 0
neither = 0
for folder in col2['item']:
    for req in folder.get('item', []):
        if 'item' in req:
            continue
        has_req_url = isinstance(req.get('request', {}).get('url'), dict)
        has_top_url = isinstance(req.get('url'), dict)
        if has_req_url and has_top_url:
            both += 1
        elif has_req_url:
            in_request += 1
        elif has_top_url:
            in_toplevel += 1
        else:
            neither += 1

print('=== After normalization ===')
print(f'URL in request.url: {in_request}')
print(f'URL in top-level:   {in_toplevel}')
print(f'Both:               {both}')
print(f'Neither:            {neither}')
print('\n✅ Normalization done!' if (in_request > 0 and both == 0 and in_toplevel == 0) else '⚠️ Some still need fixing')