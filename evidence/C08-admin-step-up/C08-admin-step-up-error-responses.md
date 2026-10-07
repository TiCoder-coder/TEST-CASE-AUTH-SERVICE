# C08 — IAM Step-up / SGOD Admins — Error Response Schemas

<div align="center">

![Cluster](https://img.shields.io/badge/C08-IAM+Step-up+++SGOD+Admins-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Evidence Type](https://img.shields.io/badge/Evidence-Error+Responses-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)

</div>

- [Request Body Examples](./C08-admin-step-up-request-body-examples.md)
- [Success Responses](./C08-admin-step-up-success-responses.md)

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
| 400 | Validation error / Bad request | "MFA not enrolled" |
| 401 | Missing or invalid token / wrong creds | "Unauthorized" / "Invalid verification code" |
| 403 | Insufficient permissions | "Access denied" |
| 404 | Resource not found | "Admin not found" |
| 409 | Conflict (duplicate) | "Email already exists" |
| 500 | Internal server error | "Internal server error" |

## Cluster-Specific Error Codes

### Step-up Errors
- **STEP_UP_MFA_NOT_ENROLLED** (400): "MFA not enrolled"
- **STEP_UP_INVALID_TOTP** (401): "Invalid verification code"
- **STEP_UP_REQUIRED** (401): "Step-up required"

### Admin Lifecycle Errors
- **ADMIN_LAST_ADMIN** (400): "Cannot delete last admin"
- **ADMIN_SELF_BLOCK** (400): "Cannot block yourself"
- **ADMIN_SELF_DELETE** (400): "Cannot delete yourself"
- **ADMIN_ALREADY_BLOCKED** (400): "Admin is already blocked"

### Not Found Errors
- **ADMIN_NOT_FOUND** (404): "Admin not found"