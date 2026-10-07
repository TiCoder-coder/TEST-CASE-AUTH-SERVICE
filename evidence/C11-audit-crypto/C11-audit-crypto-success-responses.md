# C11 — Audit Logs / Crypto — Success Response Schemas

<div align="center">

![Cluster](https://img.shields.io/badge/C11-Audit+Logs+++Crypto+PoC-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Evidence Type](https://img.shields.io/badge/Evidence-Success+Responses-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)

</div>

- [Error Responses](./C11-audit-crypto-error-responses.md)
- [Request Body Examples](./C11-audit-crypto-request-body-examples.md)

---

## 🧭 Mục Lục (Table of Contents)

| # | Endpoint |
|---|---|
| 01 | [Audit Logs — List](#audit-logs--list) |
| 02 | [Audit Logs — Get by ID](#audit-logs--get-by-id) |
| 03 | [Audit Logs — Export](#audit-logs--export) |
| 04 | [Test Crypto — Encrypt String](#test-crypto--encrypt-string) |
| 05 | [Test Crypto — Decrypt String](#test-crypto--decrypt-string) |

---

## Overview
This document describes expected 200 OK response schemas for audit log and crypto helper endpoints.

---

## Audit Logs — List

**Endpoint:** `GET /sgod-auth/v1/sgod/audit-logs`
**Response Type:** `IBeApiEnvelope<IPaginatedResponse<IAuditLog>>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "audit-uuid",
        "actorId": "user-uuid",
        "actorEmail": "root@sgod.test",
        "action": "role.create",
        "targetType": "Role",
        "targetId": "role-uuid",
        "ipAddress": "10.0.0.1",
        "userAgent": "PostmanRuntime/7.36.0",
        "createdAt": "2026-10-06T10:00:00.000Z"
      }
    ],
    "total": 1250,
    "page": 1,
    "pageSize": 20
  },
  "message": "OK",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

### Response Field Descriptions
| Field | Type | Description |
|-------|------|-------------|
| data.items[].id | string | Audit log entry ID |
| data.items[].actorId | string | Actor user ID |
| data.items[].actorEmail | string | Actor email at the time |
| data.items[].action | string | Action key (e.g., `role.create`) |
| data.items[].targetType | string | Entity type |
| data.items[].targetId | string | Entity ID |
| data.items[].createdAt | string | ISO8601 timestamp |

---

## Audit Logs — Get by ID

**Endpoint:** `GET /sgod-auth/v1/sgod/audit-logs/{id}`
**Response Type:** `IBeApiEnvelope<IAuditLog>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "id": "audit-uuid",
    "actorId": "user-uuid",
    "actorEmail": "root@sgod.test",
    "action": "role.create",
    "targetType": "Role",
    "targetId": "role-uuid",
    "metadata": {
      "name": "Manager"
    },
    "ipAddress": "10.0.0.1",
    "createdAt": "2026-10-06T10:00:00.000Z"
  },
  "message": "OK",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Audit Logs — Export

**Endpoint:** `GET /sgod-auth/v1/sgod/audit-logs/export`
**Response Type:** `IBeApiEnvelope<{ url: string }>` (signed URL) or CSV stream
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "url": "https://signed-cdn.example.com/audit-export-2026-10-06.csv"
  },
  "message": "OK",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Test Crypto — Encrypt String

**Endpoint:** `POST /sgod-auth/v1/test-crypto/encrypt-string-helper`
**Response Type:** `IBeApiEnvelope<{ ciphertext: string }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "ciphertext": "v1:abc123:base64payload"
  },
  "message": "Encrypted",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

### Response Field Descriptions
| Field | Type | Description |
|-------|------|-------------|
| data.ciphertext | string | Encrypted payload (versioned, base64) |

---

## Test Crypto — Decrypt String

**Endpoint:** `POST /sgod-auth/v1/test-crypto/decrypt-string-helper`
**Response Type:** `IBeApiEnvelope<{ plaintext: string }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "plaintext": "Hello World"
  },
  "message": "Decrypted",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

### Response Field Descriptions
| Field | Type | Description |
|-------|------|-------------|
| data.plaintext | string | Decrypted plaintext |