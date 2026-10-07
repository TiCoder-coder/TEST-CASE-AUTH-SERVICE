# C01 — Core Auth — Request Body Examples

<div align="center">

![Cluster](https://img.shields.io/badge/C01-Core+Auth-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Evidence Type](https://img.shields.io/badge/Evidence-Request+Body+Examples-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)

</div>

- [Error Responses](./C01-core-auth-error-responses.md)
- [Success Responses](./C01-core-auth-success-responses.md)

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
| 12 | [Session Context (No Body)](#session-context-no-body) |

---

## Overview
This document provides representative request body examples for each operation in the **Core Auth** cluster (login, session management, MFA enrollment/verification, password change/reset, account activation). Field types follow the TypeScript DTOs from `apps/sgod-sam-v2/src/services/types.ts` (e.g., `ParamLoginEnterpriseDto`, `ParamMfaVerifyDto`, `ParamChangePasswordDto`).

---

## Enterprise Login

**Endpoint:** `POST /sgod-auth/v1/enterprises/sessions`
**DTO Source:** `ParamLoginEnterpriseDto` from `types.ts`
**Actor:** Enterprise user (email or userName)

### Sample Request Body
```json
{
  "credential": "user@example.com",
  "password": "MySecureP@ss123"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| credential | string | ✅ | Email or username of the enterprise user |
| password | string | ✅ | Plain-text password (sent over TLS only) |

---

## Enterprise User Login

**Endpoint:** `POST /sgod-auth/v1/enterprise-users/sessions`
**DTO Source:** `ParamLoginEnterpriseUserDto` from `types.ts`
**Actor:** Enterprise user (member of an enterprise tenant)

### Sample Request Body
```json
{
  "credential": "member@enterprise.test",
  "password": "MySecureP@ss123"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| credential | string | ✅ | Email of the enterprise user |
| password | string | ✅ | Plain-text password |

---

## MFA — Enable

**Endpoint:** `POST /sgod-auth/v1/mfa/enable`
**DTO Source:** `ParamMfaEnableDto` from `types.ts`
**Actor:** Logged-in enterprise user

### Sample Request Body
```json
{
  "twoFactorCodeOrRecoveryCode": "123456"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| twoFactorCodeOrRecoveryCode | string | ✅ | 6-digit TOTP from authenticator app |

---

## MFA — Verify

**Endpoint:** `POST /sgod-auth/v1/mfa/verify`
**DTO Source:** `ParamMfaVerifyDto` from `types.ts`
**Actor:** User with an interim (post-login) token

### Sample Request Body
```json
{
  "twoFactorCodeOrRecoveryCode": "654321"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| twoFactorCodeOrRecoveryCode | string | ✅ | 6-digit TOTP or recovery code |

---

## MFA — Disable

**Endpoint:** `POST /sgod-auth/v1/mfa/disable`
**DTO Source:** `ParamMfaDisableDto` from `types.ts`
**Actor:** Logged-in enterprise user with MFA enrolled

### Sample Request Body
```json
{
  "password": "MySecureP@ss123",
  "twoFactorCodeOrRecoveryCode": "111222",
  "removeEnrollment": false
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| password | string | ✅ | Current password for confirmation |
| twoFactorCodeOrRecoveryCode | string | ✅ | Current TOTP code |
| removeEnrollment | boolean | ❌ | If true, removes TOTP enrollment entirely |

---

## Password Change

**Endpoint:** `POST /sgod-auth/v1/passwords/change`
**DTO Source:** `ParamChangePasswordDto` from `types.ts`
**Actor:** Authenticated user

### Sample Request Body
```json
{
  "oldPassword": "OldPass123!",
  "newPassword": "NewP@ssw0rd!"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| oldPassword | string | ✅ | Current password |
| newPassword | string | ✅ | New password (must meet policy) |

---

## Password Reset Request

**Endpoint:** `POST /sgod-auth/v1/passwords/reset-request`
**DTO Source:** `ParamPasswordResetRequestDto` from `types.ts`
**Actor:** Anonymous (no auth required)

### Sample Request Body
```json
{
  "email": "user@enterprise.test"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | ✅ | Email of the account |

---

## Password Reset (Submit)

**Endpoint:** `POST /sgod-auth/v1/passwords/reset`
**DTO Source:** `ParamPasswordResetDto` from `types.ts`
**Actor:** Anonymous (token-bearing)

### Sample Request Body
```json
{
  "selector": "abcdef1234567890",
  "token": "long-token-string-from-email",
  "newPassword": "NewP@ssw0rd!"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| selector | string | ✅ | Selector cookie value (identifies record) |
| token | string | ✅ | Token from reset email |
| newPassword | string | ✅ | New password |

---

## Account Activation

**Endpoint:** `POST /sgod-auth/v1/activate-account`
**DTO Source:** `ParamActivateAccountDto` from `types.ts`
**Actor:** Invited user with an interim token

### Sample Request Body
```json
{
  "interimToken": "interim.token.from.email",
  "newPassword": "FirstP@ss123!"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| interimToken | string | ✅ | Token delivered in activation email |
| newPassword | string | ✅ | Password to set on first activation |

---

## Session Refresh

**Endpoint:** `POST /sgod-auth/v1/sessions/refresh`
**DTO Source:** `ParamSessionRefreshDto` from `types.ts`
**Actor:** User with refresh token

### Sample Request Body
```json
{
  "refreshToken": "eyJhbGciOi..."
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| refreshToken | string | ✅ | Refresh token issued during login |

---

## Session Logout

**Endpoint:** `POST /sgod-auth/v1/sessions/logout`
**DTO Source:** None (no payload)
**Actor:** Authenticated user

### Sample Request Body
```json
{}
```

### Field Descriptions
No body fields. The Authorization Bearer access token is the only required context.

---

## Session Context (No Body)

**Endpoint:** `GET /sgod-auth/v1/session/context`
**DTO Source:** None (no payload)
**Actor:** Authenticated user

### Sample Request Body
```json
{}
```

### Field Descriptions
No body. Requires `Authorization: Bearer <accessToken>` header.