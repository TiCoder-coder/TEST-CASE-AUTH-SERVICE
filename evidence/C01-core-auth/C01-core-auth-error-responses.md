# C01 — Core Auth — Error Response Schemas

<div align="center">

![Cluster](https://img.shields.io/badge/C01-Core+Auth-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Evidence Type](https://img.shields.io/badge/Evidence-Error+Responses-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)

</div>

- [Request Body Examples](./C01-core-auth-request-body-examples.md)
- [Success Responses](./C01-core-auth-success-responses.md)

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

Some responses also include an `errors` array for validation errors:
```json
{
  "success": false,
  "message": "Validation failed",
  "errors": [
    {
      "field": "credential",
      "message": "credential is required"
    }
  ],
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

## HTTP Status Code Mapping
| HTTP Code | Trigger | Example Message |
|-----------|---------|----------------|
| 400 | Validation error / Bad request | "credential is required" |
| 401 | Missing or invalid token / wrong creds | "Unauthorized" / "Invalid credentials" |
| 403 | Account blocked or forbidden | "Account is blocked" |
| 404 | Resource not found | "User not found" |
| 409 | Conflict (duplicate) | "Email already exists" |
| 429 | Rate-limited | "Too many requests" |
| 500 | Internal server error | "Internal server error" |

## Cluster-Specific Error Codes

### Login Errors
- **AUTH_INVALID_CREDENTIALS** (401): "Invalid credentials" — wrong email or password
- **AUTH_ACCOUNT_BLOCKED** (403): "Account is blocked" — user is blocked
- **AUTH_ACCOUNT_INACTIVE** (403): "Account is inactive" — pending activation
- **AUTH_MFA_REQUIRED** (200 with `mfaRequired: true`): Next step is MFA verify
- **AUTH_RATE_LIMIT** (429): "Too many login attempts"

### MFA Errors
- **MFA_NOT_ENROLLED** (400): "MFA not enrolled" — verify/enable requested without enrollment
- **MFA_INVALID_CODE** (401): "Invalid verification code" — wrong TOTP or recovery code
- **MFA_INVALID_RECOVERY** (401): "Invalid recovery code"
- **MFA_ALREADY_ENROLLED** (400): "MFA already enrolled"

### Password Errors
- **PWD_INCORRECT_OLD** (400): "Old password is incorrect"
- **PWD_SAME_AS_OLD** (400): "New password must differ from old password"
- **PWD_POLICY_VIOLATION** (400): "Password does not meet policy"
- **PWD_INVALID_RESET_TOKEN** (400): "Invalid or expired token"
- **PWD_INVALID_SELECTOR** (400): "Invalid selector"

### Session Errors
- **SESSION_UNAUTHORIZED** (401): "Unauthorized" — no Authorization header
- **SESSION_TOKEN_INVALID** (401): "Invalid token" — bad/expired JWT
- **SESSION_TOKEN_EXPIRED** (401): "Token expired"

### Activation Errors
- **ACTIVATION_INVALID_TOKEN** (400): "Invalid or expired token" — bad interim token
- **ACTIVATION_EXPIRED** (400): "Token expired"

### Common Headers
| Header | Required | Notes |
|--------|----------|-------|
| x-api-key | ✅ | Per request (gateway enforced) |
| Authorization | ✅ (except anon endpoints) | Bearer JWT |
| x-device-id | Recommended | For device-fingerprinting |
| x-request-id | Recommended | For trace correlation |