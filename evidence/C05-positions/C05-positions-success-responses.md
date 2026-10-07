# C05 — Positions — Success Response Schemas

<div align="center">

![Cluster](https://img.shields.io/badge/C05-Positions-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Evidence Type](https://img.shields.io/badge/Evidence-Success+Responses-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)

</div>

- [Error Responses](./C05-positions-error-responses.md)
- [Request Body Examples](./C05-positions-request-body-examples.md)

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
This document describes expected 200 OK response schemas for each endpoint in the Positions cluster.

---

## Position Create

**Endpoint:** `POST /sgod-auth/v1/positions`
**Response Type:** `IBeApiEnvelope<IPosition>`
**Success HTTP Code:** 200 or 201

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "id": "pos-uuid",
    "name": "Engineering Manager",
    "code": "ENG_MGR",
    "department_id": "dept-uuid",
    "layer": "2",
    "description": "Manages engineers",
    "parent_id": "parent-pos-uuid",
    "tenantId": "tenant-uuid",
    "createdAt": "2026-10-06T10:00:00.000Z",
    "updatedAt": "2026-10-06T10:00:00.000Z"
  },
  "message": "Position created",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

### Response Field Descriptions
| Field | Type | Description |
|-------|------|-------------|
| data.id | string | Position ID |
| data.name | string | Position name |
| data.code | string | Position code |
| data.department_id | string | Department ID |
| data.layer | string | Layer number |
| data.parent_id | string | Parent position ID |

---

## Position Update

**Endpoint:** `PATCH /sgod-auth/v1/positions/{id}`
**Response Type:** `IBeApiEnvelope<IPosition>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "id": "pos-uuid",
    "name": "Senior Engineering Manager",
    "description": "Updated description",
    "parent_id": "new-parent-pos-uuid"
  },
  "message": "Position updated",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Position Delete

**Endpoint:** `DELETE /sgod-auth/v1/positions/{id}`
**Response Type:** `IBeApiEnvelope<{ deleted: boolean }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "deleted": true
  },
  "message": "Position deleted",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Position Get by ID

**Endpoint:** `GET /sgod-auth/v1/positions/{id}`
**Response Type:** `IBeApiEnvelope<IPosition>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "id": "pos-uuid",
    "name": "Engineering Manager",
    "code": "ENG_MGR",
    "department_id": "dept-uuid",
    "layer": "2",
    "parent_id": null
  },
  "message": "OK",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Position List by Department

**Endpoint:** `GET /sgod-auth/v1/positions?departmentId=...`
**Response Type:** `IBeApiEnvelope<IPosition[]>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": [
    {
      "id": "pos-uuid",
      "name": "Engineering Manager",
      "code": "ENG_MGR"
    },
    {
      "id": "pos-uuid2",
      "name": "Senior Engineer",
      "code": "SENG"
    }
  ],
  "message": "OK",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Position Preview Change

**Endpoint:** `POST /sgod-auth/v1/positions/preview-change`
**Response Type:** `IBeApiEnvelope<{ impactedCount: number; users: IUserSummary[] }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "impactedCount": 3,
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