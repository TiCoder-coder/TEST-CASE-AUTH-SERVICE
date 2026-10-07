# C03 — Roles — Success Response Schemas

<div align="center">

![Cluster](https://img.shields.io/badge/C03-Roles-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Evidence Type](https://img.shields.io/badge/Evidence-Success+Responses-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)

</div>

- [Error Responses](./C03-roles-error-responses.md)
- [Request Body Examples](./C03-roles-request-body-examples.md)

---

## 🧭 Mục Lục (Table of Contents)

| # | Endpoint |
|---|---|
| 01 | [Role Create(#role-create) |
| 02 | [Role Update(#role-update) |
| 03 | [Role Move(#role-move) |
| 04 | [Role Delete(#role-delete) |
| 05 | [Role Get by ID(#role-get-by-id) |
| 06 | [Role List by Tenant(#role-list-by-tenant) |
| 07 | [Role Clone(#role-clone) |

---

## Overview
This document describes expected 200 OK response schemas for each endpoint in the Roles cluster.

---

## Role Create

**Endpoint:** `POST /sgod-auth/v1/roles`
**Response Type:** `IBeApiEnvelope<IRole>`
**Success HTTP Code:** 200 or 201

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "id": "role-uuid",
    "name": "Department Manager",
    "description": "Manages a department",
    "role_type": "CUSTOM",
    "layer": "enterprise_user",
    "tenantId": "tenant-uuid",
    "parent_role_id": "parent-role-uuid",
    "permission_ids": [
      "perm-uuid-1",
      "perm-uuid-2"
    ],
    "createdAt": "2026-10-06T10:00:00.000Z",
    "updatedAt": "2026-10-06T10:00:00.000Z"
  },
  "message": "Role created",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

### Response Field Descriptions
| Field | Type | Description |
|-------|------|-------------|
| data.id | string | Role ID |
| data.name | string | Role name |
| data.role_type | string | `SYSTEM` / `CUSTOM` |
| data.layer | string | Layer |
| data.parent_role_id | string | Parent role ID (nullable) |
| data.permission_ids | string[] | Attached permission IDs |

---

## Role Update

**Endpoint:** `PATCH /sgod-auth/v1/roles/{id}`
**Response Type:** `IBeApiEnvelope<IRole>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "id": "role-uuid",
    "name": "Senior Department Manager",
    "description": "Updated description",
    "role_type": "CUSTOM",
    "layer": "enterprise_user",
    "parent_role_id": "new-parent-uuid",
    "permission_ids": [
      "perm-uuid-1"
    ]
  },
  "message": "Role updated",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Role Move

**Endpoint:** `PATCH /sgod-auth/v1/roles/{id}/move`
**Response Type:** `IBeApiEnvelope<IRole>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "id": "role-uuid",
    "parent_role_id": "new-parent-uuid",
    "name": "Department Manager"
  },
  "message": "Role moved",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Role Delete

**Endpoint:** `DELETE /sgod-auth/v1/roles/{id}`
**Response Type:** `IBeApiEnvelope<{ deleted: boolean }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "deleted": true
  },
  "message": "Role deleted",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Role Get by ID

**Endpoint:** `GET /sgod-auth/v1/roles/{id}`
**Response Type:** `IBeApiEnvelope<IRole>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "id": "role-uuid",
    "name": "Department Manager",
    "description": "Manages a department",
    "role_type": "CUSTOM",
    "layer": "enterprise_user",
    "permission_ids": [
      "perm-uuid-1"
    ],
    "parent_role_id": null
  },
  "message": "OK",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Role List by Tenant

**Endpoint:** `GET /sgod-auth/v1/roles/tenant/{tenantId}`
**Response Type:** `IBeApiEnvelope<IRole[]>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": [
    {
      "id": "role-uuid",
      "name": "Manager",
      "layer": "enterprise_user"
    },
    {
      "id": "role-uuid2",
      "name": "Employee",
      "layer": "enterprise_user"
    }
  ],
  "message": "OK",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Role Clone

**Endpoint:** `POST /sgod-auth/v1/roles/{id}/clone`
**Response Type:** `IBeApiEnvelope<IRole>`
**Success HTTP Code:** 200 or 201

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "id": "new-role-uuid",
    "name": "Department Manager (Copy)",
    "description": "Cloned role",
    "role_type": "CUSTOM",
    "layer": "enterprise_user",
    "permission_ids": [
      "perm-uuid-1"
    ]
  },
  "message": "Role cloned",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```