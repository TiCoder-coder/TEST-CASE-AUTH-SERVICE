# C02 — Enterprise / Permission / Email — Success Response Schemas

<div align="center">

![Cluster](https://img.shields.io/badge/C02-Enterprise+++Permission+++Email-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Evidence Type](https://img.shields.io/badge/Evidence-Success+Responses-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)

</div>

- [Error Responses](./C02-enterprise-email-error-responses.md)
- [Request Body Examples](./C02-enterprise-email-request-body-examples.md)

---

## 🧭 Mục Lục (Table of Contents)

| # | Endpoint |
|---|---|
| 01 | [Enterprise Registration](#enterprise-registration) |
| 02 | [Permissions List](#permissions-list) |
| 03 | [Permission Assign / Remove](#permission-assign--remove) |
| 04 | [Email — Send Verification Code](#email--send-verification-code) |
| 05 | [Email — Verify Code](#email--verify-code) |
| 06 | [Email — Check Availability](#email--check-availability) |
| 07 | [Email — Verify Token](#email--verify-token) |

---

## Overview
This document describes expected 200 OK response schemas for each endpoint in the Enterprise / Permission / Email cluster.

---

## Enterprise Registration

**Endpoint:** `POST /sgod-auth/v1/enterprises/register`
**Response Type:** `IBeApiEnvelope<IEnterprise>` (owner tenant + admin user)
**Success HTTP Code:** 200 or 201

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "id": "tenant-uuid",
    "name": "Acme Corp",
    "address": "123 Main St",
    "phone": "0901234567",
    "ownerUserId": "user-uuid",
    "status": "active",
    "createdAt": "2026-10-06T10:00:00.000Z",
    "subscriptionEnd": "2027-10-06T10:00:00.000Z"
  },
  "message": "Enterprise registered",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

### Response Field Descriptions
| Field | Type | Description |
|-------|------|-------------|
| data.id | string | Tenant identifier |
| data.name | string | Enterprise display name |
| data.ownerUserId | string | User ID of the owner |
| data.status | string | `active` / `blocked` |
| data.subscriptionEnd | string | ISO8601 subscription end date |

---

## Permissions List

**Endpoint:** `GET /sgod-auth/v1/permissions`
**Response Type:** `IBeApiEnvelope<IPermission[]>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": [
    {
      "id": "perm-uuid",
      "key": "user.read",
      "description": "Read users"
    },
    {
      "id": "perm-uuid2",
      "key": "user.write",
      "description": "Modify users"
    }
  ],
  "message": "OK",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

### Response Field Descriptions
| Field | Type | Description |
|-------|------|-------------|
| data[].id | string | Permission ID |
| data[key].key | string | Permission key (used in code) |
| data[].description | string | Human-readable description |

---

## Permission Assign / Remove

**Endpoint:** `POST/DELETE /sgod-auth/v1/permissions/{permissionId}/roles/{roleId}`
**Response Type:** `IBeApiEnvelope<{ assigned: boolean }>` or `{ removed: boolean }`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "assigned": true
  },
  "message": "Permission assigned to role",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Email — Send Verification Code

**Endpoint:** `POST /sgod-auth/v1/emails/send`
**Response Type:** `IBeApiEnvelope<{ sent: boolean }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "sent": true
  },
  "message": "Verification email sent",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

### Response Field Descriptions
| Field | Type | Description |
|-------|------|-------------|
| data.sent | boolean | Always true on success |

---

## Email — Verify Code

**Endpoint:** `POST /sgod-auth/v1/emails/verifications/code`
**Response Type:** `IBeApiEnvelope<{ verified: boolean; token: string }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "verified": true,
    "token": "long-token-string-for-next-step"
  },
  "message": "Email verified",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

### Response Field Descriptions
| Field | Type | Description |
|-------|------|-------------|
| data.verified | boolean | True on success |
| data.token | string | Token for downstream flows (activation/reset) |

---

## Email — Check Availability

**Endpoint:** `GET /sgod-auth/v1/emails/check?email=...`
**Response Type:** `IBeApiEnvelope<{ available: boolean }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "available": true
  },
  "message": "OK",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

### Response Field Descriptions
| Field | Type | Description |
|-------|------|-------------|
| data.available | boolean | True if email is not yet registered |

---

## Email — Verify Token

**Endpoint:** `POST /sgod-auth/v1/emails/verifications/token`
**Response Type:** `IBeApiEnvelope<{ verified: boolean }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "verified": true
  },
  "message": "Email verified",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```