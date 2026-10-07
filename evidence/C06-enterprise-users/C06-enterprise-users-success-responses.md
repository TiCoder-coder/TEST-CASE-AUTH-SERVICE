# C06 — Enterprise Users — Success Response Schemas

<div align="center">

![Cluster](https://img.shields.io/badge/C06-Enterprise+Users-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Evidence Type](https://img.shields.io/badge/Evidence-Success+Responses-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)

</div>

- [Error Responses](./C06-enterprise-users-error-responses.md)
- [Request Body Examples](./C06-enterprise-users-request-body-examples.md)

---

## 🧭 Mục Lục (Table of Contents)

| # | Endpoint |
|---|---|
| 01 | [Enterprise User Create(#enterprise-user-create) |
| 02 | [Enterprise User Update(#enterprise-user-update) |
| 03 | [Enterprise User Get by ID(#enterprise-user-get-by-id) |
| 04 | [Enterprise User Delete(#enterprise-user-delete) |
| 05 | [Enterprise User List(#enterprise-user-list) |
| 06 | [Enterprise User Assign Roles(#enterprise-user-assign-roles) |
| 07 | [Enterprise User Set Department/Position(#enterprise-user-set-departmentposition) |
| 08 | [Enterprise User Block(#enterprise-user-block) |
| 09 | [Enterprise User Unblock(#enterprise-user-unblock) |
| 10 | [Enterprise User Change Password (Admin)(#enterprise-user-change-password-admin) |

---

## Overview
This document describes expected 200 OK response schemas for each endpoint in the Enterprise Users cluster.

---

## Enterprise User Create

**Endpoint:** `POST /sgod-auth/v1/enterprise-users`
**Response Type:** `IBeApiEnvelope<IEnterpriseUser>`
**Success HTTP Code:** 200 or 201

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "id": "user-uuid",
    "email": "member@enterprise.test",
    "userName": "member01",
    "fullName": {
      "firstName": "Jane",
      "lastName": "Smith"
    },
    "phone": "0909876543",
    "gender": "female",
    "departmentId": "dept-uuid",
    "positionId": "pos-uuid",
    "roleIds": [
      "role-uuid-1"
    ],
    "userType": "enterprise_user",
    "tenantId": "tenant-uuid",
    "status": "active",
    "createdAt": "2026-10-06T10:00:00.000Z"
  },
  "message": "User created",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

### Response Field Descriptions
| Field | Type | Description |
|-------|------|-------------|
| data.id | string | User ID |
| data.email | string | User email |
| data.userType | string | `enterprise_user` |
| data.status | string | `active` / `blocked` |
| data.tenantId | string | Tenant ID |

---

## Enterprise User Update

**Endpoint:** `PATCH /sgod-auth/v1/enterprise-users/{id}`
**Response Type:** `IBeApiEnvelope<IEnterpriseUser>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "id": "user-uuid",
    "fullName": {
      "firstName": "Janet",
      "lastName": "Doe"
    },
    "phone": "0901112222",
    "gender": "female"
  },
  "message": "User updated",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Enterprise User Get by ID

**Endpoint:** `GET /sgod-auth/v1/enterprise-users/{id}`
**Response Type:** `IBeApiEnvelope<IEnterpriseUser>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "id": "user-uuid",
    "email": "member@enterprise.test",
    "userName": "member01",
    "fullName": {
      "firstName": "Jane",
      "lastName": "Smith"
    },
    "departmentId": "dept-uuid",
    "positionId": "pos-uuid",
    "roleIds": [
      "role-uuid-1"
    ],
    "userType": "enterprise_user",
    "status": "active"
  },
  "message": "OK",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Enterprise User Delete

**Endpoint:** `DELETE /sgod-auth/v1/enterprise-users/{id}`
**Response Type:** `IBeApiEnvelope<{ deleted: boolean }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "deleted": true
  },
  "message": "User deleted",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Enterprise User List

**Endpoint:** `GET /sgod-auth/v1/enterprise-users?tenantId=...`
**Response Type:** `IBeApiEnvelope<IPaginatedResponse<IEnterpriseUser>>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "user-uuid",
        "email": "member@enterprise.test",
        "status": "active"
      }
    ],
    "total": 25,
    "page": 1,
    "pageSize": 20
  },
  "message": "OK",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Enterprise User Assign Roles

**Endpoint:** `PATCH /sgod-auth/v1/enterprise-users/{id}/roles`
**Response Type:** `IBeApiEnvelope<{ roleIds: string[] }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "roleIds": [
      "role-uuid-1",
      "role-uuid-2"
    ]
  },
  "message": "Roles updated",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Enterprise User Set Department/Position

**Endpoint:** `PATCH /sgod-auth/v1/enterprise-users/{id}/department-position`
**Response Type:** `IBeApiEnvelope<{ departmentId: string; positionId: string }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "departmentId": "new-dept-uuid",
    "positionId": "new-pos-uuid"
  },
  "message": "Department and position updated",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Enterprise User Block

**Endpoint:** `POST /sgod-auth/v1/enterprise-users/{id}/block`
**Response Type:** `IBeApiEnvelope<{ blocked: boolean }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "blocked": true
  },
  "message": "User blocked",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Enterprise User Unblock

**Endpoint:** `POST /sgod-auth/v1/enterprise-users/{id}/unblock`
**Response Type:** `IBeApiEnvelope<{ unblocked: boolean }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "unblocked": true
  },
  "message": "User unblocked",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Enterprise User Change Password (Admin)

**Endpoint:** `POST /sgod-auth/v1/enterprise-users/{id}/password`
**Response Type:** `IBeApiEnvelope<{ changed: boolean }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "changed": true
  },
  "message": "Password changed",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```