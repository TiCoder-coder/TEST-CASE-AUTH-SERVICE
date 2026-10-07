# C03 — Roles — Request Body Examples

<div align="center">

![Cluster](https://img.shields.io/badge/C03-Roles-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Evidence Type](https://img.shields.io/badge/Evidence-Request+Body+Examples-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)

</div>

- [Error Responses](./C03-roles-error-responses.md)
- [Success Responses](./C03-roles-success-responses.md)

---

## 🧭 Mục Lục (Table of Contents)

| # | Endpoint |
|---|---|
| 01 | [Role Create(#role-create) |
| 02 | [Role Update(#role-update) |
| 03 | [Role Move (Re-parent)(#role-move-re-parent) |
| 04 | [Role Delete(#role-delete) |
| 05 | [Role Get by ID(#role-get-by-id) |
| 06 | [Role List by Tenant(#role-list-by-tenant) |
| 07 | [Role Clone(#role-clone) |

---

## Overview
This document provides representative request body examples for each operation in the **Roles** cluster. Roles are tenant-scoped and may have a parent role for hierarchy.

---

## Role Create

**Endpoint:** `POST /sgod-auth/v1/roles`
**DTO Source:** `ParamCreateRoleDto` from `types.ts`
**Actor:** SGOD admin (or tenant admin)

### Sample Request Body
```json
{
  "name": "Department Manager",
  "description": "Manages a department",
  "permission_ids": [
    "perm-uuid-1",
    "perm-uuid-2"
  ],
  "role_type": "CUSTOM",
  "layer": "enterprise_user",
  "parent_role_id": "parent-role-uuid"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | ✅ | Unique role name within layer |
| description | string | ❌ | Role description |
| permission_ids | string[] | ❌ | Permission IDs to attach |
| role_type | enum | ✅ | `SYSTEM` / `CUSTOM` |
| layer | enum | ✅ | `enterprise_user` / `sgod_user` / `sub_enterprise` |
| parent_role_id | string | ❌ | Parent role ID for hierarchy |

---

## Role Update

**Endpoint:** `PATCH /sgod-auth/v1/roles/{id}`
**DTO Source:** `ParamUpdateRoleDto` from `types.ts`
**Actor:** SGOD admin

### Sample Request Body
```json
{
  "name": "Senior Department Manager",
  "description": "Updated description",
  "parent_role_id": "new-parent-uuid"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | ❌ | New role name |
| description | string | ❌ | New description |
| parent_role_id | string | ❌ | New parent role ID |

---

## Role Move (Re-parent)

**Endpoint:** `PATCH /sgod-auth/v1/roles/{id}/move`
**DTO Source:** `ParamMoveRoleDto` from `types.ts`
**Actor:** SGOD admin

### Sample Request Body
```json
{
  "new_parent_role_id": "new-parent-uuid"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| new_parent_role_id | string | ✅ | Target parent role ID (null = root) |

---

## Role Delete

**Endpoint:** `DELETE /sgod-auth/v1/roles/{id}`
**DTO Source:** None (path param)
**Actor:** SGOD admin

### Sample Request Body
```json
{}
```

### Field Descriptions
No body. The role ID is in the URL.

---

## Role Get by ID

**Endpoint:** `GET /sgod-auth/v1/roles/{id}`
**DTO Source:** None
**Actor:** SGOD admin

### Sample Request Body
```json
{}
```

---

## Role List by Tenant

**Endpoint:** `GET /sgod-auth/v1/roles/tenant/{tenantId}`
**DTO Source:** None
**Actor:** SGOD admin

### Sample Request Body
```json
{}
```

---

## Role Clone

**Endpoint:** `POST /sgod-auth/v1/roles/{id}/clone`
**DTO Source:** `ParamCloneRoleDto` from `types.ts`
**Actor:** SGOD admin

### Sample Request Body
```json
{
  "name": "Department Manager (Copy)",
  "description": "Cloned role",
  "layer": "enterprise_user"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | ✅ | Name for the cloned role |
| description | string | ❌ | Description for the clone |
| layer | enum | ✅ | Layer of the clone |