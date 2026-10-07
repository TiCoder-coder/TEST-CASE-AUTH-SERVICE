#!/usr/bin/env python3
from _paths import POSTMAN_PATH
"""
Fix 9 endpoint mismatches in C01 + C02 of SGOD_Auth_Service.postman_collection.json
based on actual FE source code (apps/sgod-sam-v2/src/services/auth/*) and Swagger screenshots.
"""

import json
from copy import deepcopy

PATH = POSTMAN_PATH

with open(PATH, 'r', encoding='utf-8') as f:
    col = json.load(f)

# Helper to build new request with method + url + body + headers
def make_req(method, path_segments, headers, body_raw=None, query=None):
    """Build a request object."""
    req = {
        'method': method,
        'header': headers,
        'url': {
            'raw': '{{baseUrlAuth}}/' + '/'.join(path_segments),
            'host': ['{{baseUrlAuth}}'],
            'path': path_segments,
        },
    }
    if query:
        req['url']['query'] = query
    if body_raw is not None:
        req['body'] = {'mode': 'raw', 'raw': body_raw}
    return req


# Find request by TC_ID
def find_req(target_id):
    for folder in col['item']:
        for req in folder.get('item', []):
            if req.get('description', '').replace('TC_ID: ', '').strip() == target_id:
                return folder, req
    return None, None


# === FIX 1: AUTH-C01-SESSION-ENT-USER-001 ===
# /users/sessions → /enterprise-users/sessions
folder, req = find_req('AUTH-C01-SESSION-ENT-USER-001')
old_body = req['request']['body']['raw'] if 'body' in req['request'] else ''
req['request'] = make_req(
    'POST',
    ['sgod-auth', 'v1', 'enterprise-users', 'sessions'],
    [
        {'key': 'x-api-key', 'value': '{{authApiKey}}', 'type': 'text'},
        {'key': 'x-device-id', 'value': '{{deviceId}}', 'type': 'text'},
        {'key': 'Content-Type', 'value': 'application/json', 'type': 'text'},
    ],
    body_raw=old_body,
)
print('[FIX 1] AUTH-C01-SESSION-ENT-USER-001 → POST /enterprise-users/sessions')


# === FIX 2: AUTH-C01-SESSION-SGOD-USER-001 ===
# /users/sessions → /sgod-users/sessions
folder, req = find_req('AUTH-C01-SESSION-SGOD-USER-001')
old_body = req['request']['body']['raw'] if 'body' in req['request'] else ''
req['request'] = make_req(
    'POST',
    ['sgod-auth', 'v1', 'sgod-users', 'sessions'],
    [
        {'key': 'x-api-key', 'value': '{{authApiKey}}', 'type': 'text'},
        {'key': 'x-device-id', 'value': '{{deviceId}}', 'type': 'text'},
        {'key': 'Content-Type', 'value': 'application/json', 'type': 'text'},
    ],
    body_raw=old_body,
)
print('[FIX 2] AUTH-C01-SESSION-SGOD-USER-001 → POST /sgod-users/sessions')


# === FIX 3: AUTH-C01-SESSION-CURRENT-001 ===
# GET /sessions/current → POST /sessions/current
folder, req = find_req('AUTH-C01-SESSION-CURRENT-001')
old_body = req['request'].get('body', {}).get('raw', '') if 'body' in req['request'] else ''
req['request'] = make_req(
    'POST',
    ['sgod-auth', 'v1', 'sessions', 'current'],
    [
        {'key': 'x-api-key', 'value': '{{authApiKey}}', 'type': 'text'},
        {'key': 'Authorization', 'value': 'Bearer {{accessToken}}', 'type': 'text'},
        {'key': 'x-device-id', 'value': '{{deviceId}}', 'type': 'text'},
        {'key': 'Content-Type', 'value': 'application/json', 'type': 'text'},
    ],
    body_raw='{}',
)
print('[FIX 3] AUTH-C01-SESSION-CURRENT-001 → POST /sessions/current')


# === FIX 4: AUTH-C01-SESSION-DEVICE-001 ===
# POST /sessions/current/devices → DELETE /sessions/devices/{deviceId}
folder, req = find_req('AUTH-C01-SESSION-DEVICE-001')
old_body = req['request'].get('body', {}).get('raw', '') if 'body' in req['request'] else ''
req['request'] = make_req(
    'DELETE',
    ['sgod-auth', 'v1', 'sessions', 'devices', '{{deviceId}}'],
    [
        {'key': 'x-api-key', 'value': '{{authApiKey}}', 'type': 'text'},
        {'key': 'Authorization', 'value': 'Bearer {{accessToken}}', 'type': 'text'},
        {'key': 'x-device-id', 'value': '{{deviceId}}', 'type': 'text'},
        {'key': 'Content-Type', 'value': 'application/json', 'type': 'text'},
    ],
    body_raw=old_body,
)
print('[FIX 4] AUTH-C01-SESSION-DEVICE-001 → DELETE /sessions/devices/{deviceId}')


# === FIX 5: AUTH-C01-SESSION-LOGOUT-001 ===
# POST /sessions/logout → DELETE /sessions
folder, req = find_req('AUTH-C01-SESSION-LOGOUT-001')
req['request'] = make_req(
    'DELETE',
    ['sgod-auth', 'v1', 'sessions'],
    [
        {'key': 'x-api-key', 'value': '{{authApiKey}}', 'type': 'text'},
        {'key': 'Authorization', 'value': 'Bearer {{accessToken}}', 'type': 'text'},
        {'key': 'x-device-id', 'value': '{{deviceId}}', 'type': 'text'},
        {'key': 'Content-Type', 'value': 'application/json', 'type': 'text'},
    ],
    body_raw=None,
)
print('[FIX 5] AUTH-C01-SESSION-LOGOUT-001 → DELETE /sessions')


# === FIX 6: AUTH-C01-SESSION-CTX-001 ===
# /sessions/current/context → /session/context
folder, req = find_req('AUTH-C01-SESSION-CTX-001')
req['request'] = make_req(
    'GET',
    ['sgod-auth', 'v1', 'session', 'context'],
    [
        {'key': 'x-api-key', 'value': '{{authApiKey}}', 'type': 'text'},
        {'key': 'Authorization', 'value': 'Bearer {{accessToken}}', 'type': 'text'},
        {'key': 'x-device-id', 'value': '{{deviceId}}', 'type': 'text'},
    ],
    body_raw=None,
)
print('[FIX 6] AUTH-C01-SESSION-CTX-001 → GET /session/context')


# === FIX 7: AUTH-C01-SESSION-DEVICES-001 ===
# /sessions/current/devices → /sessions/devices
folder, req = find_req('AUTH-C01-SESSION-DEVICES-001')
req['request'] = make_req(
    'GET',
    ['sgod-auth', 'v1', 'sessions', 'devices'],
    [
        {'key': 'x-api-key', 'value': '{{authApiKey}}', 'type': 'text'},
        {'key': 'Authorization', 'value': 'Bearer {{accessToken}}', 'type': 'text'},
        {'key': 'x-device-id', 'value': '{{deviceId}}', 'type': 'text'},
    ],
    body_raw=None,
)
print('[FIX 7] AUTH-C01-SESSION-DEVICES-001 → GET /sessions/devices')


# === FIX 8: AUTH-C02-EMAIL-CHECK-EXISTS-001 ===
# /emails/check-exists → /enterprises/check-exists
folder, req = find_req('AUTH-C02-EMAIL-CHECK-EXISTS-001')
old_body = req['request'].get('body', {}).get('raw', '') if 'body' in req['request'] else ''
req['request'] = make_req(
    'POST',
    ['sgod-auth', 'v1', 'enterprises', 'check-exists'],
    [
        {'key': 'x-api-key', 'value': '{{authApiKey}}', 'type': 'text'},
        {'key': 'Authorization', 'value': 'Bearer {{accessToken}}', 'type': 'text'},
        {'key': 'x-device-id', 'value': '{{deviceId}}', 'type': 'text'},
        {'key': 'Content-Type', 'value': 'application/json', 'type': 'text'},
    ],
    body_raw=old_body,
)
print('[FIX 8] AUTH-C02-EMAIL-CHECK-EXISTS-001 → POST /enterprises/check-exists')


# === FIX 9: AUTH-C02-EMAIL-SEND-001 ===
# /emails/send → /enterprises/verifications/send-email
folder, req = find_req('AUTH-C02-EMAIL-SEND-001')
old_body = req['request'].get('body', {}).get('raw', '') if 'body' in req['request'] else ''
req['request'] = make_req(
    'POST',
    ['sgod-auth', 'v1', 'enterprises', 'verifications', 'send-email'],
    [
        {'key': 'x-api-key', 'value': '{{authApiKey}}', 'type': 'text'},
        {'key': 'Authorization', 'value': 'Bearer {{accessToken}}', 'type': 'text'},
        {'key': 'x-device-id', 'value': '{{deviceId}}', 'type': 'text'},
        {'key': 'Content-Type', 'value': 'application/json', 'type': 'text'},
    ],
    body_raw=old_body,
)
print('[FIX 9] AUTH-C02-EMAIL-SEND-001 → POST /enterprises/verifications/send-email')


# === FIX 10: AUTH-C01-DEV-EMAILS-001 ===
# Just verify the URL is correctly formed (no body)
# The tc_id is missing for this one because of empty URL structure earlier
# Let me also fix the placeholder variable in EMAIL-CHECK-001 + EMAIL-TOKEN-001
folder, req = find_req('AUTH-C02-EMAIL-CHECK-001')
if req:
    req['request']['url'] = {
        'raw': '{{baseUrlAuth}}/sgod-auth/v1/emails/check?email={{actorEmail}}',
        'host': ['{{baseUrlAuth}}'],
        'path': ['sgod-auth', 'v1', 'emails', 'check'],
        'query': [{'key': 'email', 'value': '{{actorEmail}}'}],
    }
    print('[FIX 10a] AUTH-C02-EMAIL-CHECK-001 → query.email uses {{actorEmail}}')

folder, req = find_req('AUTH-C02-EMAIL-TOKEN-001')
if req:
    req['request']['url'] = {
        'raw': '{{baseUrlAuth}}/sgod-auth/v1/emails/token?email={{actorEmail}}&purpose=verify-account',
        'host': ['{{baseUrlAuth}}'],
        'path': ['sgod-auth', 'v1', 'emails', 'token'],
        'query': [
            {'key': 'email', 'value': '{{actorEmail}}'},
            {'key': 'purpose', 'value': 'verify-account'},
        ],
    }
    print('[FIX 10b] AUTH-C02-EMAIL-TOKEN-001 → query.email + purpose')


# Save back
with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(col, f, indent=2, ensure_ascii=False)

print('\n✅ All 9 (10) fixes applied successfully!')