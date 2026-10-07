# C05 — Positions — Request Body Examples

<div align="center">

![Cluster](https://img.shields.io/badge/C05-Positions-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Evidence Type](https://img.shields.io/badge/Evidence-Request+Body+Examples-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)

</div>

- [Error Responses](./C05-positions-error-responses.md)
- [Success Responses](./C05-positions-success-responses.md)

---

## 🧭 Mục Lục (Table of Contents)

| # | Endpoint |
|---|---|
| 01 | [Position Create(#position-create) |
| 02 | [Position Update(#position-update) |
| 03 | [Position Delete(#position-delete) |
| 04 | [Position Get by ID(#position-get-by-id) |
| 05 | [Position List by Department(#position-list-by-department) |
| 06 | [Position Preview Change(#position-preview-change) |

---

## Overview
This document provides representative request body examples for each operation in the **Positions** cluster. Positions are scoped to departments and may have a parent position.

---

## Position Create

**Endpoint:** `POST /sgod-auth/v1/positions`
**DTO Source:** `ParamCreatePositionDto` from `types.ts`
**Actor:** SGOD admin

### Sample Request Body
```json
{
  "name": "Engineering Manager",
  "code": "ENG_MGR",
  "department_id": "dept-uuid",
  "layer": "2",
  "description": "Manages engineers",
  "parent_id": "parent-pos-uuid"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | ✅ | Position name |
| code | string | ✅ | Unique position code |
| department_id | string | ✅ | Department ID |
| layer | string | ✅ | Hierarchy layer (e.g., "1", "2") |
| description | string | ❌ | Position description |
| parent_id | string | ❌ | Parent position ID |

---

## Position Update

**Endpoint:** `PATCH /sgod-auth/v1/positions/{id}`
**DTO Source:** `ParamUpdatePositionDto` from `types.ts`
**Actor:** SGOD admin

### Sample Request Body
```json
{
  "name": "Senior Engineering Manager",
  "description": "Updated description",
  "parent_id": "new-parent-pos-uuid"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | ❌ | New position name |
| description | string | ❌ | New description |
| parent_id | string | ❌ | New parent ID |

---

## Position Delete

**Endpoint:** `DELETE /sgod-auth/v1/positions/{id}`
**DTO Source:** None
**Actor:** SGOD admin

### Sample Request Body
```json
{}
```

---

## Position Get by ID

**Endpoint:** `GET /sgod-auth/v1/positions/{id}`
**DTO Source:** None
**Actor:** SGOD admin

### Sample Request Body
```json
{}
```

---

## Position List by Department

**Endpoint:** `GET /sgod-auth/v1/positions?departmentId=...`
**DTO Source:** Query string
**Actor:** SGOD admin

### Sample Request Body
```json
{}
```

---

## Position Preview Change

**Endpoint:** `POST /sgod-auth/v1/positions/preview-change`
**DTO Source:** `ParamPreviewPositionChangeDto` from `types.ts`
**Actor:** SGOD admin

### Sample Request Body
```json
{
  "positionId": "pos-uuid",
  "newParentPositionId": "new-parent-pos-uuid",
  "tenantId": "tenant-uuid"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| positionId | string | ✅ | Position being moved |
| newParentPositionId | string | ✅ | Proposed new parent |
| tenantId | string | ❌ | Tenant scope for multi-tenant validation |