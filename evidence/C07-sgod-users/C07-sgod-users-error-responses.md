# C07 — SGOD Users — Error Response Schemas

<div align="center">

![Cluster](https://img.shields.io/badge/C07-SGOD+Users-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Evidence Type](https://img.shields.io/badge/Evidence-Error+Responses-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)

</div>

- [Request Body Examples](./C07-sgod-users-request-body-examples.md)
- [Success Responses](./C07-sgod-users-success-responses.md)

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
| 400 | Validation error / Bad request | "At least one role required" |
| 401 | Missing or invalid token | "Unauthorized" |
| 403 | Insufficient permissions | "Access denied" |
| 404 | Resource not found | "User not found" |
| 409 | Conflict (duplicate) | "Username already exists" |
| 500 | Internal server error | "Internal server error" |

## Cluster-Specific Error Codes

### Validation Errors
- **SGOD_USER_MISSING_FIELDS** (400): "Required fields are missing"
- **SGOD_USER_ROLES_REQUIRED** (400): "At least one role required"

### Conflict Errors
- **SGOD_USER_EMAIL_EXISTS** (409): "Email already exists"
- **SGOD_USER_USERNAME_EXISTS** (409): "Username already exists"

### Permission Errors
- **SGOD_USER_PERMANENT_DELETE_FORBIDDEN** (403): "Access denied"
- **SGOD_USER_BLOCK_FORBIDDEN** (403): "Access denied"

### Lifecycle Errors
- **SGOD_USER_NOT_FOUND** (404): "User not found"
- **SGOD_USER_ALREADY_DELETED** (404): "User not found"