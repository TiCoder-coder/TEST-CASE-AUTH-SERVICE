# C02 — Enterprise / Permission / Email — Error Response Schemas

<div align="center">

![Cluster](https://img.shields.io/badge/C02-Enterprise+++Permission+++Email-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Evidence Type](https://img.shields.io/badge/Evidence-Error+Responses-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)

</div>

- [Request Body Examples](./C02-enterprise-email-request-body-examples.md)
- [Success Responses](./C02-enterprise-email-success-responses.md)

---

## 🧭 Mục Lục (Table of Contents)

| # | Endpoint |
|---|---|
| 01 | [Standard Error Envelope](#standard-error-envelope) |
| 02 | [HTTP Status Code Mapping](#http-status-code-mapping) |
| 03 | [Cluster-Specific Error Codes](#cluster-specific-error-codes) |

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
| 404 | Resource not found | "Role not found" |
| 409 | Conflict (duplicate) | "Email already exists" |
| 429 | Rate-limited (email throttling) | "Too many requests" |
| 500 | Internal server error | "Internal server error" |

## Cluster-Specific Error Codes

### Registration Errors
- **REG_EMAIL_EXISTS** (409): "Email already exists"
- **REG_USERNAME_EXISTS** (409): "Username already exists"
- **REG_INVALID_EMAIL** (400): "Invalid email format"
- **REG_WEAK_PASSWORD** (400): "Password does not meet policy"
- **REG_MISSING_FIELDS** (400): "Required fields are missing"

### Email Errors
- **EMAIL_REQUIRED** (400): "email is required"
- **EMAIL_INVALID** (400): "Invalid email format"
- **EMAIL_INVALID_OTP** (400): "Invalid verification code"
- **EMAIL_EXPIRED_OTP** (400): "Verification code expired"
- **EMAIL_RATE_LIMIT** (429): "Too many email requests"
- **EMAIL_SEND_FAILED** (500): "Failed to send email"

### Permission Errors
- **PERM_UNAUTHORIZED** (401): "Unauthorized"
- **PERM_FORBIDDEN** (403): "Access denied"
- **PERM_NOT_FOUND** (404): "Permission not found"
- **PERM_ALREADY_ASSIGNED** (409): "Permission already assigned to role"