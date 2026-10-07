# C02 — Enterprise / Permission / Email — Request Body Examples

<div align="center">

![Cluster](https://img.shields.io/badge/C02-Enterprise+++Permission+++Email-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Evidence Type](https://img.shields.io/badge/Evidence-Request+Body+Examples-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)

</div>

- [Error Responses](./C02-enterprise-email-error-responses.md)
- [Success Responses](./C02-enterprise-email-success-responses.md)

---

## 🧭 Mục Lục (Table of Contents)

| # | Endpoint |
|---|---|
| 01 | [Enterprise Registration](#enterprise-registration) |
| 02 | [Permissions List](#permissions-list) |
| 03 | [Permission Assign to Role](#permission-assign-to-role) |
| 04 | [Permission Remove from Role](#permission-remove-from-role) |
| 05 | [Email — Send Verification Code](#email--send-verification-code) |
| 06 | [Email — Verify Code](#email--verify-code) |
| 07 | [Email — Check Availability](#email--check-availability) |
| 08 | [Email — Verify Token (from link)](#email--verify-token-from-link) |

---

## Overview
This document provides representative request body examples for each operation in the **Enterprise / Permission / Email** cluster. Field types follow the TypeScript DTOs from `apps/sgod-sam-v2/src/services/types.ts`.

---

## Enterprise Registration

**Endpoint:** `POST /sgod-auth/v1/enterprises/register`
**DTO Source:** `ParamRegisterEnterpriseDto` from `types.ts`
**Actor:** Anonymous (no auth required)

### Sample Request Body
```json
{
  "userName": "johndoe",
  "email": "owner@newenterprise.test",
  "password": "StrongP@ss123!",
  "fullName": {
    "firstName": "John",
    "lastName": "Doe"
  },
  "enterpriseName": "Acme Corp",
  "phone": "0901234567",
  "address": "123 Main St, District 1, HCMC"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| userName | string | ✅ | Unique username for the owner account |
| email | string | ✅ | Email of the enterprise owner (login credential) |
| password | string | ✅ | Password (must meet policy) |
| fullName.firstName | string | ✅ | First name |
| fullName.lastName | string | ✅ | Last name |
| enterpriseName | string | ✅ | Display name of the new enterprise tenant |
| phone | string | ✅ | Phone number |
| address | string | ✅ | Enterprise address |

---

## Permissions List

**Endpoint:** `GET /sgod-auth/v1/permissions`
**DTO Source:** None (no payload)
**Actor:** Authenticated user

### Sample Request Body
```json
{}
```

### Field Descriptions
No body. Returns the list of available permissions.

---

## Permission Assign to Role

**Endpoint:** `POST /sgod-auth/v1/permissions/{permissionId}/roles/{roleId}`
**DTO Source:** None (path params)
**Actor:** SGOD admin

### Sample Request Body
```json
{}
```

### Field Descriptions
No body. Assignment is encoded in the URL.

---

## Permission Remove from Role

**Endpoint:** `DELETE /sgod-auth/v1/permissions/{permissionId}/roles/{roleId}`
**DTO Source:** None (path params)
**Actor:** SGOD admin

### Sample Request Body
```json
{}
```

### Field Descriptions
No body. Removal is encoded in the URL.

---

## Email — Send Verification Code

**Endpoint:** `POST /sgod-auth/v1/emails/send`
**DTO Source:** `ParamSendEmailDto` from `types.ts`
**Actor:** Anonymous or logged-in user

### Sample Request Body
```json
{
  "email": "user@enterprise.test",
  "filter": "verify-account"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | ✅ | Recipient email |
| filter | enum | ✅ | One of: `verify-account`, `reset-password`, `invite` |

---

## Email — Verify Code

**Endpoint:** `POST /sgod-auth/v1/emails/verifications/code`
**DTO Source:** `ParamVerifyEmailCodeDto` from `types.ts`
**Actor:** Anonymous (token from email)

### Sample Request Body
```json
{
  "email": "user@enterprise.test",
  "verificationCode": "123456"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | ✅ | Email address being verified |
| verificationCode | string | ✅ | 6-digit OTP |

---

## Email — Check Availability

**Endpoint:** `GET /sgod-auth/v1/emails/check?email=...`
**DTO Source:** Query string only
**Actor:** Anonymous

### Sample Request Body
```json
{}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email (query) | string | ✅ | Email to check for availability |

---

## Email — Verify Token (from link)

**Endpoint:** `POST /sgod-auth/v1/emails/verifications/token`
**DTO Source:** `ParamVerifyEmailTokenDto` from `types.ts`
**Actor:** Anonymous (token from email)

### Sample Request Body
```json
{
  "token": "long-token-string-from-email"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| token | string | ✅ | Token from verification link |