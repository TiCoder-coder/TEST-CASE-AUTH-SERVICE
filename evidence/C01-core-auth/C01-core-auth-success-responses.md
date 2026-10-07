# C01 — Core Auth — Success Response Schemas

<div align="center">

![Cluster](https://img.shields.io/badge/C01-Core+Auth-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Evidence Type](https://img.shields.io/badge/Evidence-Success+Responses-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)

</div>

- [Error Responses](./C01-core-auth-error-responses.md)
- [Request Body Examples](./C01-core-auth-request-body-examples.md)

---

## 🧭 Mục Lục (Table of Contents)

| # | Endpoint |
|---|---|
| 01 | [Enterprise Login](#enterprise-login) |
| 02 | [Enterprise User Login](#enterprise-user-login) |
| 03 | [MFA — Enable](#mfa--enable) |
| 04 | [MFA — Verify](#mfa--verify) |
| 05 | [MFA — Disable](#mfa--disable) |
| 06 | [Password Change](#password-change) |
| 07 | [Password Reset Request](#password-reset-request) |
| 08 | [Password Reset (Submit)](#password-reset-submit) |
| 09 | [Account Activation](#account-activation) |
| 10 | [Session Refresh](#session-refresh) |
| 11 | [Session Logout](#session-logout) |
| 12 | [Session Context](#session-context) |

---

## Overview
This document describes expected 200 OK response schemas for each endpoint in the Core Auth cluster. All responses follow the `IBeApiEnvelope<T>` pattern from `@sgod-sam/types/entities/`.

---

## Enterprise Login

**Endpoint:** `POST /sgod-auth/v1/enterprises/sessions`
**Response Type:** `IBeApiEnvelope<ILoginResponse>` or `ISessionResponse`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "interimToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "mfaRequired": false,
    "expiresIn": 3600,
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "userName": "username",
      "fullName": {
        "firstName": "First",
        "lastName": "Last"
      },
      "tenantId": "tenant-uuid",
      "userType": "enterprise_user"
    }
  },
  "message": "Login successful",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

### Response Field Descriptions
| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Always true for success |
| data.accessToken | string | JWT for authenticated requests |
| data.refreshToken | string | JWT used to refresh the access token |
| data.interimToken | string | Interim token when MFA must be verified |
| data.mfaRequired | boolean | True if MFA verification still required |
| data.expiresIn | number | Access token TTL in seconds |
| data.user | object | User profile summary |
| message | string | Human-readable success message |
| timestamp | string | Server ISO8601 timestamp |

---

## Enterprise User Login

**Endpoint:** `POST /sgod-auth/v1/enterprise-users/sessions`
**Response Type:** `IBeApiEnvelope<ISessionResponse>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "mfaRequired": false,
    "expiresIn": 3600,
    "user": {
      "id": "uuid",
      "email": "member@enterprise.test",
      "userType": "enterprise_user",
      "tenantId": "tenant-uuid",
      "departmentId": "dept-uuid",
      "positionId": "pos-uuid"
    }
  },
  "message": "OK",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

### Response Field Descriptions
| Field | Type | Description |
|-------|------|-------------|
| data.accessToken | string | JWT access token |
| data.refreshToken | string | JWT refresh token |
| data.mfaRequired | boolean | Whether an MFA verify step is needed |
| data.user | object | User summary (no password fields) |
| data.expiresIn | number | Token TTL in seconds |

---

## MFA — Enable

**Endpoint:** `POST /sgod-auth/v1/mfa/enable`
**Response Type:** `IBeApiEnvelope<{ recoveryCodes: string[] }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "recoveryCodes": [
      "abcd-1234-efgh-5678",
      "ijkl-9012-mnop-3456",
      "qrst-7890-uvwx-1234"
    ]
  },
  "message": "MFA enabled",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

### Response Field Descriptions
| Field | Type | Description |
|-------|------|-------------|
| data.recoveryCodes | string[] | One-time recovery codes (must be saved) |

---

## MFA — Verify

**Endpoint:** `POST /sgod-auth/v1/mfa/verify`
**Response Type:** `IBeApiEnvelope<{ accessToken: string, refreshToken: string }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  },
  "message": "MFA verified",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

### Response Field Descriptions
| Field | Type | Description |
|-------|------|-------------|
| data.accessToken | string | Upgraded access token after MFA |
| data.refreshToken | string | Refresh token issued post MFA |

---

## MFA — Disable

**Endpoint:** `POST /sgod-auth/v1/mfa/disable`
**Response Type:** `IBeApiEnvelope<{ disabled: boolean }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "disabled": true
  },
  "message": "MFA disabled",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

### Response Field Descriptions
| Field | Type | Description |
|-------|------|-------------|
| data.disabled | boolean | Always true when MFA is disabled |

---

## Password Change

**Endpoint:** `POST /sgod-auth/v1/passwords/change`
**Response Type:** `IBeApiEnvelope<{ changed: boolean }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "changed": true
  },
  "message": "Password updated",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

### Response Field Descriptions
| Field | Type | Description |
|-------|------|-------------|
| data.changed | boolean | Always true when password changed |

---

## Password Reset Request

**Endpoint:** `POST /sgod-auth/v1/passwords/reset-request`
**Response Type:** `IBeApiEnvelope<{ sent: boolean }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "sent": true
  },
  "message": "Reset email sent if account exists",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

### Response Field Descriptions
| Field | Type | Description |
|-------|------|-------------|
| data.sent | boolean | Always true (avoids account-enumeration responses) |

---

## Password Reset (Submit)

**Endpoint:** `POST /sgod-auth/v1/passwords/reset`
**Response Type:** `IBeApiEnvelope<{ reset: boolean }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "reset": true
  },
  "message": "Password reset successful",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

### Response Field Descriptions
| Field | Type | Description |
|-------|------|-------------|
| data.reset | boolean | Always true when password reset |

---

## Account Activation

**Endpoint:** `POST /sgod-auth/v1/activate-account`
**Response Type:** `IBeApiEnvelope<ISessionResponse>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "mfaRequired": false,
    "expiresIn": 3600,
    "user": {
      "id": "uuid",
      "email": "new@enterprise.test",
      "userType": "enterprise_user"
    }
  },
  "message": "Account activated",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

### Response Field Descriptions
| Field | Type | Description |
|-------|------|-------------|
| data.accessToken | string | Issued access token after activation |
| data.refreshToken | string | Issued refresh token |
| data.user | object | Newly activated user summary |

---

## Session Refresh

**Endpoint:** `POST /sgod-auth/v1/sessions/refresh`
**Response Type:** `IBeApiEnvelope<{ accessToken: string; refreshToken: string }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  },
  "message": "Refreshed",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

### Response Field Descriptions
| Field | Type | Description |
|-------|------|-------------|
| data.accessToken | string | New access token |
| data.refreshToken | string | New refresh token (rotated) |

---

## Session Logout

**Endpoint:** `POST /sgod-auth/v1/sessions/logout`
**Response Type:** `IBeApiEnvelope<{ loggedOut: boolean }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "loggedOut": true
  },
  "message": "Logout successful",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

### Response Field Descriptions
| Field | Type | Description |
|-------|------|-------------|
| data.loggedOut | boolean | Always true after successful logout |

---

## Session Context

**Endpoint:** `GET /sgod-auth/v1/session/context`
**Response Type:** `IBeApiEnvelope<ISessionContext>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "userId": "uuid",
    "email": "user@enterprise.test",
    "userName": "username",
    "userType": "enterprise_user",
    "tenantId": "tenant-uuid",
    "roles": [
      {
        "id": "role-uuid",
        "name": "Manager",
        "layer": "admin"
      }
    ],
    "permissions": [
      "user.read",
      "user.write"
    ],
    "departmentId": "dept-uuid",
    "positionId": "pos-uuid",
    "mfaEnabled": true
  },
  "message": "OK",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

### Response Field Descriptions
| Field | Type | Description |
|-------|------|-------------|
| data.userId | string | Authenticated user ID |
| data.email | string | Email of user |
| data.userType | string | enterprise_user / sgod_user / sub_enterprise |
| data.tenantId | string | Tenant identifier |
| data.roles | array | List of role assignments |
| data.permissions | string[] | Effective permission strings |
| data.mfaEnabled | boolean | Whether MFA is enrolled |