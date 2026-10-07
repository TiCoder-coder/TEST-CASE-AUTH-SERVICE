# C07 — SGOD Users — Success Response Schemas

<div align="center">

![Cluster](https://img.shields.io/badge/C07-SGOD+Users-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Evidence Type](https://img.shields.io/badge/Evidence-Success+Responses-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)

</div>

- [Error Responses](./C07-sgod-users-error-responses.md)
- [Request Body Examples](./C07-sgod-users-request-body-examples.md)

---

## 🧭 Mục Lục (Table of Contents)

| # | Endpoint |
|---|---|
| 01 | [SGOD User Create(#sgod-user-create) |
| 02 | [SGOD User Update(#sgod-user-update) |
| 03 | [SGOD User Get by ID(#sgod-user-get-by-id) |
| 04 | [SGOD User List(#sgod-user-list) |
| 05 | [SGOD User Delete(#sgod-user-delete) |
| 06 | [SGOD User Permanent Delete(#sgod-user-permanent-delete) |
| 07 | [SGOD User Assign Roles(#sgod-user-assign-roles) |
| 08 | [SGOD User Set Department/Position(#sgod-user-set-departmentposition) |
| 09 | [SGOD User Block(#sgod-user-block) |
| 10 | [SGOD User Unblock(#sgod-user-unblock) |

---

## Overview
This document describes expected 200 OK response schemas for each endpoint in the SGOD Users cluster.

---

## SGOD User Create

**Endpoint:** `POST /sgod-auth/v1/sgod-users`
**Response Type:** `IBeApiEnvelope<ISgodUser>`
**Success HTTP Code:** 200 or 201

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "id": "user-uuid",
    "email": "sgod@sgod.test",
    "userName": "sgodstaff",
    "fullName": {
      "firstName": "Alice",
      "lastName": "Wong"
    },
    "phone": "0905556666",
    "gender": "female",
    "departmentId": "sgod-dept-uuid",
    "positionId": "sgod-pos-uuid",
    "roleIds": [
      "sgod-role-uuid"
    ],
    "userType": "sgodUser",
    "status": "active",
    "createdAt": "2026-10-06T10:00:00.000Z"
  },
  "message": "SGOD user created",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

### Response Field Descriptions
| Field | Type | Description |
|-------|------|-------------|
| data.id | string | User ID |
| data.email | string | Email |
| data.userName | string | Username |
| data.userType | string | `sgodUser` |
| data.status | string | `active` / `blocked` |

---

## SGOD User Update

**Endpoint:** `PATCH /sgod-auth/v1/sgod-users/{id}`
**Response Type:** `IBeApiEnvelope<ISgodUser>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "id": "user-uuid",
    "fullName": {
      "firstName": "Alicia",
      "lastName": "Wong"
    },
    "phone": "0905557777"
  },
  "message": "SGOD user updated",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## SGOD User Get by ID

**Endpoint:** `GET /sgod-auth/v1/sgod-users/{id}`
**Response Type:** `IBeApiEnvelope<ISgodUser>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "id": "user-uuid",
    "email": "sgod@sgod.test",
    "userName": "sgodstaff",
    "fullName": {
      "firstName": "Alice",
      "lastName": "Wong"
    },
    "userType": "sgodUser",
    "status": "active"
  },
  "message": "OK",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## SGOD User List

**Endpoint:** `GET /sgod-auth/v1/sgod-users`
**Response Type:** `IBeApiEnvelope<IPaginatedResponse<ISgodUser>>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "user-uuid",
        "email": "sgod@sgod.test",
        "userType": "sgodUser",
        "status": "active"
      }
    ],
    "total": 12,
    "page": 1,
    "pageSize": 20
  },
  "message": "OK",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## SGOD User Delete

**Endpoint:** `DELETE /sgod-auth/v1/sgod-users/{id}`
**Response Type:** `IBeApiEnvelope<{ deleted: boolean }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "deleted": true
  },
  "message": "SGOD user deleted",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## SGOD User Permanent Delete

**Endpoint:** `DELETE /sgod-auth/v1/sgod-users/{id}/permanent`
**Response Type:** `IBeApiEnvelope<{ permanentlyDeleted: boolean }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "permanentlyDeleted": true
  },
  "message": "SGOD user permanently deleted",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## SGOD User Assign Roles

**Endpoint:** `PATCH /sgod-auth/v1/sgod-users/{id}/roles`
**Response Type:** `IBeApiEnvelope<{ roleIds: string[] }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "roleIds": [
      "sgod-role-uuid"
    ]
  },
  "message": "Roles updated",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## SGOD User Set Department/Position

**Endpoint:** `PATCH /sgod-auth/v1/sgod-users/{id}/department-position`
**Response Type:** `IBeApiEnvelope<{ departmentId: string; positionId: string }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "departmentId": "new-sgod-dept-uuid",
    "positionId": "new-sgod-pos-uuid"
  },
  "message": "Department and position updated",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## SGOD User Block

**Endpoint:** `POST /sgod-auth/v1/sgod-users/{id}/block`
**Response Type:** `IBeApiEnvelope<{ blocked: boolean }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "blocked": true
  },
  "message": "SGOD user blocked",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## SGOD User Unblock

**Endpoint:** `POST /sgod-auth/v1/sgod-users/{id}/unblock`
**Response Type:** `IBeApiEnvelope<{ unblocked: boolean }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "unblocked": true
  },
  "message": "SGOD user unblocked",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```