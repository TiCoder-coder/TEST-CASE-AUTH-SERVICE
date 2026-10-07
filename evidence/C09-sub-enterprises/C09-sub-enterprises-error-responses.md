# C09 — Sub-Enterprises — Error Response Schemas

<div align="center">

![Cluster](https://img.shields.io/badge/C09-Sub-Enterprises-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Evidence Type](https://img.shields.io/badge/Evidence-Error+Responses-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)

</div>

- [Request Body Examples](./C09-sub-enterprises-request-body-examples.md)
- [Success Responses](./C09-sub-enterprises-success-responses.md)

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
| 400 | Validation error / Bad request | "email is required" |
| 401 | Missing or invalid token | "Unauthorized" |
| 403 | Insufficient permissions | "Access denied" |
| 404 | Resource not found | "Sub-enterprise not found" |
| 409 | Conflict (duplicate) | "Email already exists" |
| 500 | Internal server error | "Internal server error" |

## Cluster-Specific Error Codes

### Validation Errors
- **SUBENT_EMAIL_REQUIRED** (400): "email is required"
- **SUBENT_MISSING_FIELDS** (400): "Required fields are missing"
- **SUBENT_INVALID_GENDER** (400): "gender must be Male/Female/Other"
- **SUBENT_INVALID_USER_TYPE** (400): "userType must be EnterpriseUser"

### Dependency Errors
- **SUBENT_BOSS_NOT_FOUND** (400): "Boss not found"
- **SUBENT_DEPARTMENT_NOT_FOUND** (404): "Department not found"
- **SUBENT_POSITION_NOT_FOUND** (404): "Position not found"
- **SUBENT_ROLE_NOT_FOUND** (404): "Role not found"

### State Errors
- **SUBENT_ALREADY_BLOCKED** (400): "User is already blocked"
- **SUBENT_NOT_BLOCKED** (400): "User is not blocked"
- **SUBENT_ALREADY_DELETED** (400): "User is already deleted"
- **SUBENT_PERMANENT_REQUIRES_SOFT_DELETE** (400): "User must be soft-deleted before permanent delete"

### Not Found Errors
- **SUBENT_NOT_FOUND** (404): "Sub-enterprise not found"

### Conflict Errors
- **SUBENT_EMAIL_EXISTS** (409): "Email already exists"
- **SUBENT_USERNAME_EXISTS** (409): "Username already exists"

### Step-Up (MFA) Errors
- **SUBENT_STEPUP_REQUIRED** (401): "MFA step-up required for this action"