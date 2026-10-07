# C08 — IAM Step-up / SGOD Admins — Success Response Schemas

<div align="center">

![Cluster](https://img.shields.io/badge/C08-IAM+Step-up+++SGOD+Admins-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Evidence Type](https://img.shields.io/badge/Evidence-Success+Responses-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)

</div>

- [Error Responses](./C08-admin-step-up-error-responses.md)
- [Request Body Examples](./C08-admin-step-up-request-body-examples.md)

---

## 🧭 Mục Lục (Table of Contents)

| # | Endpoint |
|---|---|
| 01 | [IAM Step-up(#iam-step-up) |
| 02 | [SGOD Admin List(#sgod-admin-list) |
| 03 | [SGOD Admin Get(#sgod-admin-get) |
| 04 | [SGOD Admin Create(#sgod-admin-create) |
| 05 | [SGOD Admin Update(#sgod-admin-update) |
| 06 | [SGOD Admin Block(#sgod-admin-block) |
| 07 | [SGOD Admin Unblock(#sgod-admin-unblock) |
| 08 | [SGOD Admin Delete(#sgod-admin-delete) |
| 09 | [SGOD Admin Assign Roles(#sgod-admin-assign-roles) |

---

## Overview
This document describes expected 200 OK response schemas for IAM step-up and SGOD admin endpoints.

---

## IAM Step-up

**Endpoint:** `POST /sgod-auth/v1/iam/step-up`
**Response Type:** `IBeApiEnvelope<{ stepUpToken: string; expiresIn: number }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "stepUpToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiresIn": 300
  },
  "message": "Step-up verified",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

### Response Field Descriptions
| Field | Type | Description |
|-------|------|-------------|
| data.stepUpToken | string | Short-lived step-up JWT |
| data.expiresIn | number | TTL in seconds |

---

## SGOD Admin List

**Endpoint:** `GET /sgod-auth/v1/sgod/admins`
**Response Type:** `IBeApiEnvelope<IPaginatedResponse<ISgodAdmin>>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "admin-uuid",
        "email": "root@sgod.test",
        "status": "active"
      }
    ],
    "total": 3,
    "page": 1,
    "pageSize": 20
  },
  "message": "OK",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## SGOD Admin Get

**Endpoint:** `GET /sgod-auth/v1/sgod/admins/{adminId}`
**Response Type:** `IBeApiEnvelope<ISgodAdmin>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "id": "admin-uuid",
    "email": "root@sgod.test",
    "userName": "rootadmin",
    "fullName": {
      "firstName": "Root",
      "lastName": "Admin"
    },
    "roleIds": [
      "root-role-uuid"
    ],
    "status": "active"
  },
  "message": "OK",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## SGOD Admin Create

**Endpoint:** `POST /sgod-auth/v1/sgod/admins`
**Response Type:** `IBeApiEnvelope<ISgodAdmin>`
**Success HTTP Code:** 200 or 201

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "id": "admin-uuid",
    "email": "root@sgod.test",
    "userName": "rootadmin",
    "fullName": {
      "firstName": "Root",
      "lastName": "Admin"
    },
    "status": "active",
    "roleIds": [
      "root-role-uuid"
    ]
  },
  "message": "Admin created",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## SGOD Admin Update

**Endpoint:** `PATCH /sgod-auth/v1/sgod/admins/{adminId}`
**Response Type:** `IBeApiEnvelope<ISgodAdmin>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "id": "admin-uuid",
    "fullName": {
      "firstName": "Root2",
      "lastName": "Admin"
    },
    "phone": "0900009999"
  },
  "message": "Admin updated",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## SGOD Admin Block

**Endpoint:** `POST /sgod-auth/v1/sgod/admins/{adminId}/block`
**Response Type:** `IBeApiEnvelope<{ blocked: boolean }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "blocked": true
  },
  "message": "Admin blocked",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## SGOD Admin Unblock

**Endpoint:** `POST /sgod-auth/v1/sgod/admins/{adminId}/unblock`
**Response Type:** `IBeApiEnvelope<{ unblocked: boolean }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "unblocked": true
  },
  "message": "Admin unblocked",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## SGOD Admin Delete

**Endpoint:** `DELETE /sgod-auth/v1/sgod/admins/{adminId}`
**Response Type:** `IBeApiEnvelope<{ deleted: boolean }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "deleted": true
  },
  "message": "Admin deleted",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## SGOD Admin Assign Roles

**Endpoint:** `PATCH /sgod-auth/v1/sgod/admins/{adminId}/roles`
**Response Type:** `IBeApiEnvelope<{ roleIds: string[] }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "roleIds": [
      "root-role-uuid"
    ]
  },
  "message": "Roles updated",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```