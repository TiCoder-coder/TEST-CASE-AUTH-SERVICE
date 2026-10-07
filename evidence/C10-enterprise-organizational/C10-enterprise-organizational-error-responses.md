# C10 — SGOD Enterprises / Organizational — Error Response Schemas

<div align="center">

![Cluster](https://img.shields.io/badge/C10-Tenant+Management-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Evidence Type](https://img.shields.io/badge/Evidence-Error+Responses-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)

</div>

- [Request Body Examples](./C10-enterprise-organizational-request-body-examples.md)
- [Success Responses](./C10-enterprise-organizational-success-responses.md)

---

## 🧭 Mục Lục (Table of Contents)

| # | Endpoint |
|---|---|
| 01 | [Standard Error Envelope(#standard-error-envelope) |
| 02 | [HTTP Status Code Mapping(#http-status-code-mapping) |
| 03 | [Cluster-Specific Error Codes(#cluster-specific-error-codes) |

---

## Overview
All auth-service endpoints return consistent error envelopes following the `IBeApiEnvelope` pattern. Error responses always include `success: false`.

## Standard Error Envelope
```json
{
  "success": false,
  "message": "Human-readable error message",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

## HTTP Status Code Mapping
| HTTP Code | Trigger | Example Message |
|-----------|---------|----------------|
| 400 | Validation error / Bad request | "durationDays must be positive" |
| 401 | Missing or invalid token | "Unauthorized" |
| 403 | Insufficient permissions | "Access denied" |
| 404 | Resource not found | "Tenant not found" |
| 409 | Conflict (duplicate / state conflict) | "Already exists" |
| 500 | Internal server error | "Internal server error" |

## Cluster-Specific Error Codes

### Tenant Errors (C10-TENANT-*)

| Code | HTTP | Trigger | Example |
|------|------|---------|---------|
| TENANT_NOT_FOUND | 404 | Tenant ID does not exist | "Tenant not found" |
| TENANT_ALREADY_BLOCKED | 409 | Block already applied | "Tenant is already blocked" |
| TENANT_NOT_BLOCKED | 409 | Unblock on non-blocked tenant | "Tenant is not blocked" |
| TENANT_INVALID_DURATION | 400 | durationDays <= 0 | "durationDays must be positive" |
| TENANT_INVALID_FEATURE | 400 | Unknown feature key | "Invalid feature" |
| TENANT_INVALID_USER_TYPE | 400 | userType not allowed | "Invalid user type for assign" |
| TENANT_ALREADY_ASSIGNED | 409 | Duplicate assign | "Tenant already assigned to user" |
| TENANT_NOT_ASSIGNED | 409 | Unassign on non-assigned tenant | "Tenant not assigned to user" |
| TENANT_DELETED | 409 | Operation on soft-deleted tenant | "Tenant has been deleted" |

### Organizational Errors (C10-ORG-*)

| Code | HTTP | Trigger | Example |
|------|------|---------|---------|
| ORG_BOSS_NOT_FOUND | 404 | bossId does not exist | "Boss not found" |
| ORG_USER_NOT_FOUND | 404 | userId does not exist | "User not found" |
| ORG_DEPT_NOT_FOUND | 404 | departmentId does not exist | "Department not found" |
| ORG_POS_NOT_FOUND | 404 | positionId does not exist | "Position not found" |
| ORG_ROLE_NOT_FOUND | 404 | primaryRoleId does not exist | "Role not found" |
| ORG_SELF_CHECK | 400 | userId == subordinateId | "Cannot check self" |
| ORG_SELF_BOSS | 400 | userId == bossId | "Cannot set self as boss" |
| ORG_CYCLE_DETECTED | 409 | Boss assignment creates cycle | "Cycle detected in org hierarchy" |
| ORG_DEPT_CEILING | 400 | Department hierarchy ceiling" | "User exceeds department ceiling" |
| ORG_ALREADY_ASSIGNED | 409 | Already assigned to position | "User already assigned to position" |
| ORG_NOT_ASSIGNED | 409 | Remove on non-assigned user | "User has no position to remove" |
| ORG_INVALID_USER_TYPE | 400 | userType not in enum | "Invalid user type for organizational operation" |
| ORG_SUBORDINATE_NOT_FOUND | 404 | subordinateId does not exist | "Subordinate not found" |
| ORG_AUDIT_CONFLICT | 409 | Inconsistencies during audit | "Reporting line conflict detected" |

### Sample Error Responses

#### TENANT_ALREADY_BLOCKED (409)
```json
{
  "success": false,
  "message": "Tenant is already blocked",
  "code": "TENANT_ALREADY_BLOCKED",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

#### TENANT_INVALID_DURATION (400)
```json
{
  "success": false,
  "message": "durationDays must be positive",
  "code": "TENANT_INVALID_DURATION",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

#### ORG_CYCLE_DETECTED (409)
```json
{
  "success": false,
  "message": "Cycle detected in org hierarchy: user-uuid-B → user-manager-uuid → user-uuid-B",
  "code": "ORG_CYCLE_DETECTED",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

#### ORG_INVALID_USER_TYPE (400)
```json
{
  "success": false,
  "message": "Invalid user type for organizational operation: 'invalid_type'. Allowed: EnterpriseUser, SubEnterpriseUser, SgodUser, SgodAdmin",
  "code": "ORG_INVALID_USER_TYPE",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

#### ORG_USER_NOT_FOUND (404)
```json
{
  "success": false,
  "message": "User not found",
  "code": "ORG_USER_NOT_FOUND",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```