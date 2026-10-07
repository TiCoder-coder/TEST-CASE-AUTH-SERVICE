# C04 — Departments — Success Response Schemas

<div align="center">

![Cluster](https://img.shields.io/badge/C04-Departments-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Evidence Type](https://img.shields.io/badge/Evidence-Success+Responses-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)

</div>

- [Error Responses](./C04-departments-error-responses.md)
- [Request Body Examples](./C04-departments-request-body-examples.md)

---

## 🧭 Mục Lục (Table of Contents)

| # | Endpoint |
|---|---|
| 01 | [Department Create(#department-create) |
| 02 | [Department Update(#department-update) |
| 03 | [Department Delete(#department-delete) |
| 04 | [Department Get by ID(#department-get-by-id) |
| 05 | [Department Tree(#department-tree) |
| 06 | [Department Preview Change(#department-preview-change) |

---

## Overview
This document describes expected 200 OK response schemas for each endpoint in the Departments cluster.

---

## Department Create

**Endpoint:** `POST /sgod-auth/v1/departments`
**Response Type:** `IBeApiEnvelope<IDepartment>`
**Success HTTP Code:** 200 or 201

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "id": "dept-uuid",
    "name": "Engineering",
    "code": "ENG001",
    "description": "Software engineering department",
    "parent_id": "parent-dept-uuid",
    "tenantId": "tenant-uuid",
    "createdAt": "2026-10-06T10:00:00.000Z",
    "updatedAt": "2026-10-06T10:00:00.000Z"
  },
  "message": "Department created",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

### Response Field Descriptions
| Field | Type | Description |
|-------|------|-------------|
| data.id | string | Department ID |
| data.name | string | Department name |
| data.code | string | Department code |
| data.parent_id | string | Parent department ID |
| data.tenantId | string | Tenant ID |

---

## Department Update

**Endpoint:** `PATCH /sgod-auth/v1/departments/{id}`
**Response Type:** `IBeApiEnvelope<IDepartment>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "id": "dept-uuid",
    "name": "Engineering — Platform",
    "description": "Updated description",
    "parent_id": "new-parent-uuid"
  },
  "message": "Department updated",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Department Delete

**Endpoint:** `DELETE /sgod-auth/v1/departments/{id}`
**Response Type:** `IBeApiEnvelope<{ deleted: boolean }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "deleted": true
  },
  "message": "Department deleted",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Department Get by ID

**Endpoint:** `GET /sgod-auth/v1/departments/{id}`
**Response Type:** `IBeApiEnvelope<IDepartment>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "id": "dept-uuid",
    "name": "Engineering",
    "code": "ENG001",
    "parent_id": null,
    "tenantId": "tenant-uuid"
  },
  "message": "OK",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Department Tree

**Endpoint:** `GET /sgod-auth/v1/departments/tree?tenantId=...`
**Response Type:** `IBeApiEnvelope<IDepartmentNode[]>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": [
    {
      "id": "dept-uuid",
      "name": "Engineering",
      "code": "ENG001",
      "children": [
        {
          "id": "child-uuid",
          "name": "Platform",
          "code": "PLAT",
          "children": []
        }
      ]
    }
  ],
  "message": "OK",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Department Preview Change

**Endpoint:** `POST /sgod-auth/v1/departments/preview-change`
**Response Type:** `IBeApiEnvelope<{ impactedCount: number; users: IUserSummary[] }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "impactedCount": 5,
    "users": [
      {
        "id": "user-uuid",
        "fullName": "John Doe",
        "email": "john@enterprise.test"
      }
    ]
  },
  "message": "OK",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```