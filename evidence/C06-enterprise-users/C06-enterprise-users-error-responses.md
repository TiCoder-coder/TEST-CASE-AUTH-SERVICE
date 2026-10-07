# C06 — Enterprise Users — Error Response Schemas

<div align="center">

![Cluster](https://img.shields.io/badge/C06-Enterprise+Users-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Evidence Type](https://img.shields.io/badge/Evidence-Error+Responses-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)

</div>

- [Request Body Examples](./C06-enterprise-users-request-body-examples.md)
- [Success Responses](./C06-enterprise-users-success-responses.md)

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
| 400 | Validation error / Bad request | "Invalid email" |
| 401 | Missing or invalid token | "Unauthorized" |
| 403 | Insufficient permissions | "Access denied" |
| 404 | Resource not found | "User not found" |
| 409 | Conflict (duplicate) | "Email already exists" |
| 500 | Internal server error | "Internal server error" |

## Cluster-Specific Error Codes

### Validation Errors
- **USER_EMAIL_INVALID** (400): "Invalid email"
- **USER_REQUIRED_FIELDS** (400): "Required fields are missing"

### Conflict Errors
- **USER_EMAIL_EXISTS** (409): "Email already exists"
- **USER_USERNAME_EXISTS** (409): "Username already exists"

### Dependency Errors
- **USER_ROLE_NOT_FOUND** (400): "Role not found"
- **USER_DEPT_NOT_FOUND** (400): "Department not found"
- **USER_POS_NOT_FOUND** (400): "Position not found"

### Block State Errors
- **USER_ALREADY_BLOCKED** (400): "User is already blocked"
- **USER_NOT_BLOCKED** (400): "User is not blocked"

### Lifecycle Errors
- **USER_ALREADY_DELETED** (404): "User not found"
- **USER_NOT_FOUND** (404): "User not found"