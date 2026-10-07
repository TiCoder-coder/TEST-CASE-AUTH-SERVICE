#!/usr/bin/env python3
from _paths import POSTMAN_PATH
"""Add concrete request examples (200 success + 401 unauthorized) to every request
in the SGOD Auth Service Postman collection.

Reads the existing collection, for every request it builds an example object
containing a concrete request body (with {{var}} placeholders replaced) and a
realistic response body. Then writes the modified collection back.
"""

import json
import re
import copy

COLLECTION_PATH = POSTMAN_PATH

# Concrete variable values — DO NOT change these. Mirrored from the user prompt.
PRIMARY_VALUES = {
    'actorEmail': 'voanhnhatTicoder@gmail.com',
    'actorPassword': 'TI@6789',
    'oldPassword': 'TI@6789',
    'newPassword': 'NewPass@16122006',
    'currentTotp': '123456',
    'otpCode': '654321',
    'runId': 'test2026q4',
    'deviceId': 'device-test-001',
    'tenantIdA': 'tenant-a-001',
    'tenantIdB': 'tenant-b-002',
    'deptId': 'dept-parent-001',
    'posId': 'pos-parent-001',
    'roleId1': 'role-custom-001',
    'roleId2': 'role-custom-002',
    'permissionId': 'perm-read-001',
    'newPermissionId': 'perm-write-001',
    'parentRoleId': 'role-parent-001',
    'entUserAId': 'ent-user-a-001',
    'entUserBId': 'ent-user-b-002',
    'sgodUserAId': 'sgod-user-a-001',
    'adminIdA': 'sgod-admin-a-001',
    'subentAId': 'subent-a-001',
    'bossId': 'boss-user-001',
    'primaryRoleId': 'role-primary-001',
    'userId': 'ent-user-a-001',
    'selector': 'sel-abc123',
    'resetToken': 'reset-token-xyz789',
    'interimToken': 'interim.jwt.token.here',
    'accessToken': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlbnQtdXNlci1hLTAwMSIsImlhdCI6MTcyODIwOTYwMCwiZXhwIjoxNzI4MjEzMjAwfQ.test',
    'refreshToken': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlbnQtdXNlci1hLTAwMSIsImlhdCI6MTcyODIwOTYwMCwiZXhwIjoxNzI4ODE0NDAwfQ.refresh',
    'authApiKey': 'test-api-key-sgod-auth-2026',
    'baseUrlAuth': 'https://auth-staging.sgod.internal',
    'deptParentId': 'dept-parent-001',
    'posParentId': 'pos-parent-001',
}

# Additional values used in URL path placeholders and bodies that are NOT in
# the user-supplied list. These keep examples realistic but must not override
# anything in PRIMARY_VALUES. Order matters: more specific keys first.
EXTRA_VALUES = {
    'roleId': 'role-custom-001',
    'roleDeleteId': 'role-deleted-001',
    'adminBlockId': 'admin-block-001',
    'adminDeleteId': 'admin-delete-001',
    'adminDeletedId': 'admin-deleted-001',
    'adminPermId': 'admin-perm-001',
    'entUserBlockedId': 'ent-user-blocked-001',
    'entUserDeleteId': 'ent-user-deleted-001',
    'deletedUserEntId': 'ent-user-deleted-001',
    'walletUserId': 'ent-user-wallet-001',
    'deptChildId': 'dept-child-001',
    'deptDeleteId': 'dept-deleted-001',
    'posChildId': 'pos-child-001',
    'posDeleteId': 'pos-deleted-001',
    'sgodUserBlockedId': 'sgod-user-blocked-001',
    'sgodUserDeleteId': 'sgod-user-deleted-001',
    'sgodUserDeletedId': 'sgod-user-deleted-001',
    'sgodUserPermId': 'sgod-user-perm-001',
    'subentBlockId': 'subent-block-001',
    'subentDeleteId': 'subent-deleted-001',
    'subentDeletedId': 'subent-deleted-001',
    'subentPermanentId': 'subent-permanent-001',
    'tenantDeletedId': 'tenant-deleted-001',
    'tenantIdC': 'tenant-c-003',
    'managerId': 'boss-user-001',
    'subordinateId': 'ent-user-b-002',
    'moveParentRoleId': 'role-parent-001',
    'deptMoveParentId': 'dept-parent-001',
    'newParentPosId': 'pos-parent-001',
    'ciphertextFromEncrypt': 'U2FsdGVkX1+v2g5xQJ8kE5yhY3Z9PJ4kTQrLn1bF8+M=',
    'ciphertextFromFileEncrypt': 'FILE_CIPHERTEXT_BASE64_PLACEHOLDER',
}

ALL_VALUES = {**EXTRA_VALUES, **PRIMARY_VALUES}


def replace_vars(text):
    """Replace {{var}} and {var} with concrete values. Preserves JSON validity."""
    if not isinstance(text, str):
        return text
    # Sort by key length descending so longer names get precedence (avoids
    # accidentally replacing a prefix when a longer var shares one).
    for var in sorted(ALL_VALUES.keys(), key=len, reverse=True):
        text = text.replace('{{' + var + '}}', ALL_VALUES[var])
        text = text.replace('{' + var + '}', ALL_VALUES[var])
    return text


def get_url_path_parts(url_obj):
    """Extract path components from a Postman URL object (string or dict),
    with {{var}} and {var} replaced by concrete values."""
    if isinstance(url_obj, str):
        raw = url_obj
    elif isinstance(url_obj, dict):
        raw = url_obj.get('raw', '')
    else:
        raw = ''
    raw = replace_vars(raw) if raw else raw
    # Strip baseUrlAuth prefix to leave just the API path
    base = PRIMARY_VALUES['baseUrlAuth']
    if raw.startswith(base):
        raw = raw[len(base):]
    return raw


def is_public_auth_endpoint(path):
    """Returns True if the request does NOT require a Bearer token."""
    public_patterns = [
        '/sessions',                  # all sessions endpoints (login/refresh/logout contexts)
        '/mfa/enable',
        '/mfa/disable',
        '/mfa/unenroll',
        '/mfa/verification',
        '/mfa/verify',
        '/passwords/forgot',
        '/passwords/reset',
        '/passwords/change',
        '/emails/send',
        '/emails/verifications',
        '/emails/verify',
        '/emails/payment-code',
        '/emails/token',
        '/emails/check',
        '/enterprises/register',
        '/enterprises/verifications',
        '/activate-account',
        '/iam/step-up',
        '/test-crypto',
        '/users/{userId}/actions/',   # admin-reset / resend-activation
    ]
    for p in public_patterns:
        if p in path:
            return True
    return False


def build_concrete_request(req_obj, path):
    """Construct an example request object with concrete values."""
    method = req_obj.get('method', 'GET').upper()
    headers = [
        {"key": "x-api-key", "value": PRIMARY_VALUES['authApiKey'], "type": "text"},
        {"key": "Content-Type", "value": "application/json", "type": "text"},
        {"key": "x-device-id", "value": PRIMARY_VALUES['deviceId'], "type": "text"},
    ]
    if not is_public_auth_endpoint(path):
        headers.insert(0, {"key": "Authorization", "value": "Bearer " + PRIMARY_VALUES['accessToken'], "type": "text"})

    concrete_req = {
        "method": method,
        "header": headers,
        "url": {
            "raw": PRIMARY_VALUES['baseUrlAuth'] + path,
            "host": [PRIMARY_VALUES['baseUrlAuth']],
            "path": [p for p in path.split('/') if p],
        },
    }

    # Carry over query params if any exist on the original request
    url_obj = req_obj.get('url', {})
    if isinstance(url_obj, dict):
        query = url_obj.get('query')
        if query:
            concrete_req['url']['query'] = [
                {"key": q.get('key', ''), "value": replace_vars(q.get('value', '')), "type": "text"}
                for q in query
            ]

    body = req_obj.get('body')
    if isinstance(body, dict) and body.get('mode') == 'raw' and body.get('raw'):
        concrete_req['body'] = {
            "mode": "raw",
            "raw": replace_vars(body['raw']),
            "options": {"raw": {"language": "json"}},
        }

    return concrete_req


def customize_success_body(path, method, base):
    """Return a more realistic success body for known endpoint shapes."""
    p = path
    m = method.upper()

    # Session login → tokens
    if '/sessions/refresh' in p:
        base['data'] = {
            "accessToken": PRIMARY_VALUES['accessToken'],
            "refreshToken": PRIMARY_VALUES['refreshToken'],
            "expiresIn": 3600,
            "tokenType": "Bearer",
        }
        return base
    if ('/enterprise-users/sessions' in p or '/sgod-users/sessions' in p or
        '/sgod-admins/sessions' in p or '/sub-enterprises/sessions' in p or
        '/enterprises/sessions' in p):
        base['data'] = {
            "accessToken": PRIMARY_VALUES['accessToken'],
            "refreshToken": PRIMARY_VALUES['refreshToken'],
            "expiresIn": 3600,
            "tokenType": "Bearer",
            "userType": "enterprise_user",
            "nextStep": None,
        }
        return base

    # Sessions/me === (current session)
    if '/sessions/current' in p or '/sessions/me' in p:
        base['data'] = {
            "id": PRIMARY_VALUES['accessToken'],
            "userId": PRIMARY_VALUES['entUserAId'],
            "userType": "enterprise_user",
            "deviceId": PRIMARY_VALUES['deviceId'],
            "createdAt": "2026-10-06T10:00:00.000Z",
            "expiresAt": "2026-10-06T11:00:00.000Z",
        }
        return base

    # Logout (delete session) → empty ack
    if '/sessions' in p and m == 'DELETE':
        base['data'] = {"acknowledged": True}
        return base

    # Session context
    if '/session/context' in p:
        base['data'] = {
            "id": PRIMARY_VALUES['entUserAId'],
            "email": PRIMARY_VALUES['actorEmail'],
            "type": "enterprise_user",
            "tenantId": PRIMARY_VALUES['tenantIdA'],
            "deviceId": PRIMARY_VALUES['deviceId'],
            "isUse2FA": False,
            "is2FAVerifiedInSession": True,
        }
        return base

    # Session devices (list)
    if '/sessions/devices' in p and m == 'GET':
        base['data'] = [
            {
                "deviceId": PRIMARY_VALUES['deviceId'],
                "trusted": True,
                "lastActiveAt": "2026-10-06T10:00:00.000Z",
            }
        ]
        return base

    # MFA enable
    if '/mfa/enable' in p and m == 'POST':
        base['data'] = {
            "qrUri": "otpauth://totp/SGOD:" + PRIMARY_VALUES['entUserAId'] + "?secret=JBSWY3DPEHPK3PXP&issuer=SGOD",
            "recoveryCodes": ["recovery-001", "recovery-002", "recovery-003"],
            "nextStep": "VERIFY_2FA_SETUP",
            "isNewEnrollment": True,
        }
        return base

    # MFA verify / verification / disable / unenroll
    if '/mfa/verify' in p or '/mfa/verification' in p or '/mfa/disable' in p or '/mfa/unenroll' in p:
        base['data'] = {
            "verified": True,
            "nextStep": None,
        }
        return base

    # Password change
    if '/passwords/change' in p and m == 'POST':
        base['data'] = {"success": True}
        return base

    # Password forgot
    if '/passwords/forgot' in p and m == 'POST':
        base['data'] = {
            "selector": "test2026q4_selector_abc123",
            "expiresAt": "2026-10-06T11:00:00.000Z",
        }
        return base

    # Password reset
    if '/passwords/reset' in p and m == 'POST':
        base['data'] = {
            "success": True,
            "userId": PRIMARY_VALUES['entUserAId'],
        }
        return base

    # Activate account / initiate reset / resend activation
    if '/activate-account' in p or '/initiate-reset-password' in p or '/resend-activation' in p:
        base['data'] = {
            "success": True,
            "expiresAt": "2026-10-06T11:00:00.000Z",
        }
        return base

    # IAM step-up
    if '/iam/step-up' in p:
        base['data'] = {
            "interimToken": PRIMARY_VALUES['interimToken'],
            "expiresIn": 300,
            "tokenType": "Bearer",
        }
        return base

    # Profile (get)
    if '/profile-with-assets' in p and m == 'GET':
        base['data'] = {
            "id": PRIMARY_VALUES['entUserAId'],
            "email": PRIMARY_VALUES['actorEmail'],
            "fullName": {"firstName": "Nhat", "lastName": "Tester"},
            "tenantId": PRIMARY_VALUES['tenantIdA'],
        }
        return base
    if '/profile-with-assets' in p and m in ('PUT', 'PATCH', 'POST'):
        base['data'] = {
            "id": PRIMARY_VALUES['entUserAId'],
            "fullName": {"firstName": PRIMARY_VALUES['runId'] + "_updated", "lastName": "User"},
            "updatedAt": "2026-10-06T10:00:00.000Z",
        }
        return base

    # Myself / Me
    if ('/users/myself' in p or '/me' in p) and m == 'GET':
        base['data'] = {
            "id": PRIMARY_VALUES['entUserAId'],
            "email": PRIMARY_VALUES['actorEmail'],
            "type": "enterprise_user",
        }
        return base

    # Trust / untrust device
    if '/devices/' in p and ('/trust' in p or '/untrust' in p):
        base['data'] = {
            "deviceId": PRIMARY_VALUES['deviceId'],
            "trusted": '/untrust' not in p,
        }
        return base

    # Enterprise register
    if '/enterprises/register' in p:
        base['data'] = {
            "id": PRIMARY_VALUES['tenantIdA'],
            "name": PRIMARY_VALUES['runId'] + "_Enterprise",
            "status": "pending_verification",
        }
        return base

    # Enterprise profile
    if '/enterprises/profile' in p and m == 'GET':
        base['data'] = {
            "id": PRIMARY_VALUES['tenantIdA'],
            "name": PRIMARY_VALUES['runId'] + "_Enterprise",
            "status": "active",
        }
        return base

    # Enterprise verifications / emails
    if '/verifications' in p or '/emails/send' in p or '/emails/verifications' in p:
        base['data'] = {
            "sent": True,
            "purpose": "verify-account",
            "expiresAt": "2026-10-06T11:00:00.000Z",
        }
        return base
    if '/emails/verify' in p:
        base['data'] = {"verified": True, "email": PRIMARY_VALUES['actorEmail']}
        return base
    if '/emails/payment-code' in p:
        base['data'] = {"sent": True, "purpose": "payment-code"}
        return base
    if '/emails/payment-code/verify' in p:
        base['data'] = {"verified": True, "amount": 100000}
        return base
    if '/emails/token' in p:
        base['data'] = {"token": "email-token-abc123", "purpose": "verify-account"}
        return base
    if '/emails/check' in p:
        base['data'] = {"exists": True, "email": PRIMARY_VALUES['actorEmail']}
        return base

    # Permissions list
    if '/permissions' in p and m == 'GET' and '{' not in p:
        base['data'] = [
            {"id": "perm-read-001", "name": "READ_USER", "description": "Can read users", "layer": "enterprise_user"},
            {"id": "perm-write-001", "name": "WRITE_USER", "description": "Can write users", "layer": "enterprise_user"},
        ]
        return base

    # Roles list/tree
    if '/roles' in p and '{' not in p and m == 'GET':
        base['data'] = [
            {
                "id": "role-custom-001",
                "name": PRIMARY_VALUES['runId'] + "_RoleParent",
                "layer": "enterprise_user",
                "parentId": None,
                "children": [
                    {"id": "role-custom-002", "name": PRIMARY_VALUES["runId"] + "_RoleChild", "layer": "enterprise_user"}
                ],
            }
        ]
        return base

    # Single role by id
    if re.search(r'/roles/\{?role', p):
        base['data'] = {
            "id": "role-custom-001",
            "name": PRIMARY_VALUES['runId'] + "_RoleParent",
            "layer": "enterprise_user",
            "permissions": ["perm-read-001"],
        }
        return base

    # Roles statistics
    if '/roles/statistics' in p:
        base['data'] = {"total": 12, "deleted": 1, "active": 11}
        return base
    if '/roles/creatable-layers' in p:
        base['data'] = ["enterprise_user", "sub_enterprise", "sgod_user", "sgod_admin"]
        return base

    # Departments
    if '/departments/tree' in p:
        base['data'] = [
            {
                "id": "dept-parent-001",
                "name": PRIMARY_VALUES['runId'] + "_ParentDept",
                "parentId": None,
                "children": [
                    {"id": "dept-child-001", "name": PRIMARY_VALUES["runId"] + "_ChildDept", "parentId": "dept-parent-001"}
                ],
            }
        ]
        return base
    if '/departments' in p and '/tree' not in p and '/statistics' not in p and '{' not in p and m == 'GET':
        base['data'] = [
            {"id": "dept-parent-001", "name": PRIMARY_VALUES['runId'] + "_ParentDept", "parentId": None}
        ]
        return base
    if '/departments/statistics' in p and '{' not in p:
        base['data'] = {"total": 5, "deleted": 0, "active": 5}
        return base
    if re.search(r'/departments/\{', p):
        base['data'] = {"id": "dept-parent-001", "name": PRIMARY_VALUES['runId'] + "_ParentDept", "parentId": None}
        return base

    # Positions
    if '/positions' in p and '/tree' not in p and '/statistics' not in p and '/available' not in p and '/preview' not in p and '{' not in p and m == 'GET':
        base['data'] = [
            {"id": "pos-parent-001", "name": PRIMARY_VALUES['runId'] + "_ParentPos", "departmentId": "dept-parent-001"}
        ]
        return base
    if '/positions/tree' in p:
        base['data'] = [
            {
                "id": "pos-parent-001",
                "name": PRIMARY_VALUES['runId'] + "_ParentPos",
                "departmentId": "dept-parent-001",
                "children": [],
            }
        ]
        return base
    if '/positions/available' in p:
        base['data'] = [
            {"id": "pos-parent-001", "name": PRIMARY_VALUES['runId'] + "_ParentPos", "departmentId": "dept-parent-001"}
        ]
        return base
    if '/positions/preview-change' in p:
        base['data'] = {
            "impactedUsers": [PRIMARY_VALUES['entUserBId']],
            "conflicts": [],
        }
        return base
    if '/positions/statistics' in p and '{' not in p:
        base['data'] = {"total": 4, "deleted": 0, "active": 4}
        return base
    if re.search(r'/positions/\{', p):
        base['data'] = {"id": "pos-parent-001", "name": PRIMARY_VALUES['runId'] + "_ParentPos", "departmentId": "dept-parent-001"}
        return base

    # Enterprise users
    if '/enterprise-users' in p and m == 'GET' and '{' not in p:
        base['data'] = [
            {"id": PRIMARY_VALUES['entUserAId'], "email": PRIMARY_VALUES['actorEmail'], "type": "enterprise_user"}
        ]
        return base
    if '/enterprise-users/statistics' in p and '{' not in p:
        base['data'] = {"total": 25, "blocked": 1, "deleted": 2, "active": 22}
        return base
    if re.search(r'/enterprise-users/\{', p):
        base['data'] = {
            "id": PRIMARY_VALUES['entUserBId'],
            "email": "another" + PRIMARY_VALUES['runId'] + "@example.com",
            "type": "enterprise_user",
            "tenantId": PRIMARY_VALUES['tenantIdA'],
        }
        return base

    # SGOD users
    if '/sgod-users' in p and m == 'GET' and '{' not in p and '/sgod/' not in p:
        base['data'] = [
            {"id": PRIMARY_VALUES['sgodUserAId'], "email": "sgod" + PRIMARY_VALUES['runId'] + "@example.com", "type": "sgod_user"}
        ]
        return base
    if re.search(r'/sgod-users/\{', p):
        base['data'] = {
            "id": PRIMARY_VALUES['sgodUserAId'],
            "email": "sgod" + PRIMARY_VALUES['runId'] + "@example.com",
            "type": "sgod_user",
        }
        return base

    # SGOD admins
    if '/sgod/admins' in p and m == 'GET' and '{' not in p and '/statistics' not in p and '/deleted' not in p:
        base['data'] = [
            {"id": PRIMARY_VALUES['adminIdA'], "email": "admin" + PRIMARY_VALUES['runId'] + "@example.com", "type": "sgod_admin"}
        ]
        return base
    if re.search(r'/sgod/admins/\{', p):
        base['data'] = {
            "id": PRIMARY_VALUES['adminIdA'],
            "email": "admin" + PRIMARY_VALUES['runId'] + "@example.com",
            "type": "sgod_admin",
        }
        return base

    # Sub-enterprises
    if '/sub-enterprises' in p and m == 'GET' and '{' not in p and '/statistics' not in p and '/deleted' not in p:
        base['data'] = [
            {"id": PRIMARY_VALUES['subentAId'], "name": PRIMARY_VALUES['runId'] + "_SubEnt", "type": "sub_enterprise"}
        ]
        return base
    if re.search(r'/sub-enterprises/\{', p):
        base['data'] = {
            "id": PRIMARY_VALUES['subentAId'],
            "name": PRIMARY_VALUES['runId'] + "_SubEnt",
            "type": "sub_enterprise",
            "tenantId": PRIMARY_VALUES['tenantIdA'],
        }
        return base

    # SGOD enterprises
    if '/sgod/enterprises' in p and m == 'GET' and '{' not in p and '/statistics' not in p and '/deleted' not in p:
        base['data'] = [
            {"id": PRIMARY_VALUES['tenantIdA'], "name": PRIMARY_VALUES['runId'] + "_Enterprise"},
            {"id": PRIMARY_VALUES['tenantIdB'], "name": PRIMARY_VALUES['runId'] + "_EnterpriseB"},
        ]
        return base
    if re.search(r'/sgod/enterprises/\{', p):
        base['data'] = {
            "id": PRIMARY_VALUES['tenantIdA'],
            "name": PRIMARY_VALUES['runId'] + "_Enterprise",
            "status": "active",
        }
        return base

    # Audit logs
    if '/audit-logs' in p or '/audit/logs' in p or '/organizations/audit' in p:
        base['data'] = [
            {
                "id": "log-001",
                "action": "USER_LOGIN",
                "actorId": PRIMARY_VALUES['entUserAId'],
                "tenantId": PRIMARY_VALUES['tenantIdA'],
                "timestamp": "2026-10-06T10:00:00.000Z",
            }
        ]
        return base

    # Crypto helpers
    if '/test-crypto/encrypt' in p:
        base['data'] = {
            "ciphertext": "U2FsdGVkX1+v2g5xQJ8kE5yhY3Z9PJ4kTQrLn1bF8+M=",
            "algorithm": "AES-256-GCM",
            "context": "test",
        }
        return base
    if '/test-crypto/decrypt' in p:
        base['data'] = {
            "plaintext": "Xin chao SGOD Auth Test",
            "algorithm": "AES-256-GCM",
            "context": "test",
        }
        return base

    # Available parents / bosses
    if '/available-parents' in p or '/available-bosses' in p:
        base['data'] = [
            {"id": PRIMARY_VALUES['parentRoleId'], "name": PRIMARY_VALUES['runId'] + "_AvailableParent"}
        ]
        return base
    if '/bosses' in p and m == 'GET':
        base['data'] = [{"id": PRIMARY_VALUES['bossId'], "name": PRIMARY_VALUES['runId'] + "_Boss"}]
        return base

    # Check subordinate
    if '/check-subordinate' in p:
        base['data'] = {"isSubordinate": True, "managerId": PRIMARY_VALUES['bossId']}
        return base

    # Statistics endpoints (generic)
    if '/statistics' in p:
        base['data'] = {"total": 10, "active": 9, "deleted": 1}
        return base

    # Users in role / department / position
    if re.search(r'/(roles|departments|positions)/\{[^}]+\}/users', p):
        base['data'] = [
            {"id": PRIMARY_VALUES['entUserAId'], "email": PRIMARY_VALUES['actorEmail']}
        ]
        return base

    # Block/unblock endpoints
    if '/block' in p or '/unblock' in p:
        base['data'] = {"blocked": '/unblock' not in p, "id": PRIMARY_VALUES['entUserBId']}
        return base

    # Restore endpoints
    if '/restore' in p:
        base['data'] = {"restored": True, "id": PRIMARY_VALUES['entUserBId']}
        return base

    # Permanent delete
    if '/permanent' in p:
        base['data'] = {"deleted": True, "permanent": True}
        return base

    return base


def build_examples(req_obj, path):
    """Build 200 success + 401 unauthorized example objects."""
    concrete_req = build_concrete_request(req_obj, path)

    base_success = {
        "success": True,
        "data": {
            "id": "sample-id-001",
            "createdAt": "2026-10-06T10:00:00.000Z",
            "updatedAt": "2026-10-06T10:00:00.000Z",
        },
        "message": "Operation successful",
        "timestamp": "2026-10-06T10:00:00.000Z",
    }
    method = req_obj.get('method', 'GET').upper()
    success_body = customize_success_body(path, method, base_success)

    # Build a no-auth version of the request for the 401 example
    no_auth_req = copy.deepcopy(concrete_req)
    no_auth_req['header'] = [h for h in no_auth_req['header'] if h.get('key') != 'Authorization']

    unauthorized_body = {
        "success": False,
        "statusCode": 401,
        "message": "Unauthorized: Invalid or missing authentication token",
        "error": "UNAUTHORIZED",
        "timestamp": "2026-10-06T10:00:00.000Z",
    }

    examples = [
        {
            "name": "200 OK - Sample request with concrete credentials",
            "originalRequest": concrete_req,
            "status": "OK",
            "code": 200,
            "_postman_previewlanguage": "json",
            "header": [{"key": "Content-Type", "value": "application/json", "name": "Content-Type", "description": ""}],
            "cookie": [],
            "body": json.dumps(success_body, indent=2, ensure_ascii=False),
        },
        {
            "name": "401 Unauthorized - Missing or invalid token",
            "originalRequest": no_auth_req,
            "status": "Unauthorized",
            "code": 401,
            "_postman_previewlanguage": "json",
            "header": [{"key": "Content-Type", "value": "application/json", "name": "Content-Type", "description": ""}],
            "cookie": [],
            "body": json.dumps(unauthorized_body, indent=2, ensure_ascii=False),
        },
    ]
    return examples


def process_items(items):
    """Walk the collection tree, adding example arrays to each request."""
    count = 0
    for item in items:
        if isinstance(item, dict) and 'request' in item and isinstance(item.get('request'), dict):
            req = item['request']
            # URL can be sibling to request or nested under it. Prefer sibling.
            url_obj = item.get('url') or req.get('url')
            path = get_url_path_parts(url_obj)
            item['response'] = build_examples(req, path)
            count += 1
        if isinstance(item, dict) and 'item' in item and isinstance(item['item'], list):
            count += process_items(item['item'])
    return count


def main():
    with open(COLLECTION_PATH, 'r') as f:
        collection = json.load(f)

    total = process_items(collection.get('item', []))

    with open(COLLECTION_PATH, 'w') as f:
        json.dump(collection, f, indent=2, ensure_ascii=False)

    print(f"Added 2 examples (200 + 401) to {total} requests")


if __name__ == '__main__':
    main()