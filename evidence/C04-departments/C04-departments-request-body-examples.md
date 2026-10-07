# C04 — Departments — Request Body Examples

<div align="center">

![Cluster](https://img.shields.io/badge/C04-Departments-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Evidence Type](https://img.shields.io/badge/Evidence-Request+Body+Examples-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)

</div>

- [Error Responses](./C04-departments-error-responses.md)
- [Success Responses](./C04-departments-success-responses.md)

---

## 🧭 Mục Lục (Table of Contents)

| # | Endpoint |
|---|---|
| 01 | [Department Create(#department-create) |
| 02 | [Department Update(#department-update) |
| 03 | [Department Delete(#department-delete) |
| 04 | [Department Get by ID(#department-get-by-id) |
| 05 | [Department Tree (by Tenant)(#department-tree-by-tenant) |
| 06 | [Department Preview Change(#department-preview-change) |

---

## Overview
This document provides representative request body examples for each operation in the **Departments** cluster. Departments are tree-structured entities within a tenant.

---

## Department Create

**Endpoint:** `POST /sgod-auth/v1/departments`
**DTO Source:** `ParamCreateDepartmentDto` from `types.ts`
**Actor:** SGOD admin (or tenant admin)

### Sample Request Body
```json
{
  "name": "Engineering",
  "code": "ENG001",
  "description": "Software engineering department",
  "parent_id": "parent-dept-uuid"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | ✅ | Department display name |
| code | string | ✅ | Unique department code within tenant |
| description | string | ❌ | Department description |
| parent_id | string | ❌ | Parent department ID (null = root) |

---

## Department Update

**Endpoint:** `PATCH /sgod-auth/v1/departments/{id}`
**DTO Source:** `ParamUpdateDepartmentDto` from `types.ts`
**Actor:** SGOD admin

### Sample Request Body
```json
{
  "name": "Engineering — Platform",
  "description": "Updated description",
  "parent_id": "new-parent-uuid"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | ❌ | New department name |
| description | string | ❌ | New description |
| parent_id | string | ❌ | New parent ID |

---

## Department Delete

**Endpoint:** `DELETE /sgod-auth/v1/departments/{id}`
**DTO Source:** None
**Actor:** SGOD admin

### Sample Request Body
```json
{}
```

---

## Department Get by ID

**Endpoint:** `GET /sgod-auth/v1/departments/{id}`
**DTO Source:** None
**Actor:** SGOD admin

### Sample Request Body
```json
{}
```

---

## Department Tree (by Tenant)

**Endpoint:** `GET /sgod-auth/v1/departments/tree?tenantId=...`
**DTO Source:** Query string
**Actor:** SGOD admin

### Sample Request Body
```json
{}
```

---

## Department Preview Change

**Endpoint:** `POST /sgod-auth/v1/departments/preview-change`
**DTO Source:** `ParamPreviewDeptChangeDto` from `types.ts`
**Actor:** SGOD admin

### Sample Request Body
```json
{
  "departmentId": "dept-uuid",
  "newParentId": "new-parent-uuid"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| departmentId | string | ✅ | Department being moved |
| newParentId | string | ❌ | Proposed new parent (omit for root) |