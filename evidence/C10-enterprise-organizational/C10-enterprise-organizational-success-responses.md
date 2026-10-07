# C10 — SGOD Enterprises / Organizational — Success Response Schemas

<div align="center">

![Cluster](https://img.shields.io/badge/C10-Tenant+Management-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Evidence Type](https://img.shields.io/badge/Evidence-Success+Responses-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)

</div>

- [Error Responses](./C10-enterprise-organizational-error-responses.md)
- [Request Body Examples](./C10-enterprise-organizational-request-body-examples.md)

---

## 🧭 Mục Lục (Table of Contents)

| # | Endpoint |
|---|---|
| 01 | [1. List SGOD Enterprises(#1-list-sgod-enterprises) |
| 02 | [2. Statistics Overview(#2-statistics-overview) |
| 03 | [3. Assign Enterprises to User(#3-assign-enterprises-to-user) |
| 04 | [4. Unassign Enterprise from User(#4-unassign-enterprise-from-user) |
| 05 | [5. Set Assigned Enterprises(#5-set-assigned-enterprises) |
| 06 | [6. List Deleted Enterprises(#6-list-deleted-enterprises) |
| 07 | [7. Get Enterprise by ID(#7-get-enterprise-by-id) |
| 08 | [8. Block Enterprise(#8-block-enterprise) |
| 09 | [9. Unblock Enterprise(#9-unblock-enterprise) |
| 10 | [10. Restore Deleted Enterprise(#10-restore-deleted-enterprise) |
| 11 | [11. Update Enterprise Subscription(#11-update-enterprise-subscription) |
| 12 | [12. Update Enterprise Features(#12-update-enterprise-features) |
| 13 | [13. Get Enterprise Statistics by ID(#13-get-enterprise-statistics-by-id) |
| 14 | [14. Assign Organizational(#14-assign-organizational) |
| 15 | [15. Remove User from Organizational Position(#15-remove-user-from-organizational-position) |
| 16 | [16. Get Available Bosses(#16-get-available-bosses) |
| 17 | [17. Set Boss(#17-set-boss) |
| 18 | [18. Check Subordinate(#18-check-subordinate) |
| 19 | [19. Audit Organizational Reporting Lines(#19-audit-organizational-reporting-lines) |
| 20 | [Removed Endpoints (Old Evidence Cleanup)(#removed-endpoints-old-evidence-cleanup) |

---

## Overview
This document describes expected **200 OK** response schemas for **19 endpoints** in the C10 cluster.

**Source of Truth:** Screenshots `Screenshot_2026-10-06_at_23.39.11` through `23.42.02`.

---

## 1. List SGOD Enterprises

**Endpoint:** `GET /sgod-auth/v1/sgod/enterprises`
**Response Type:** `IBeApiEnvelope<IPaginatedResponse<ITenant>>`
**Success HTTP Code:** 200

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "tenant-uuid-A",
        "name": "Acme Corp",
        "status": "active",
        "subscriptionEnd": "2027-10-06T10:00:00.000Z",
        "features": [
          "audit_logging",
          "mfa_required"
        ]
      }
    ],
    "total": 42,
    "page": 1,
    "limit": 20,
    "nextCursor": "eyJpZCI6InRlbmFudC11dWlkLUIifQ=="
  },
  "message": "OK",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## 2. Statistics Overview

**Endpoint:** `GET /sgod-auth/v1/sgod/enterprises/statistics/overview`
**Response Type:** Custom envelope
**Success HTTP Code:** 200

```json
{
  "success": true,
  "data": {
    "totalEnterprises": 42,
    "totalActive": 30,
    "totalPending": 8,
    "totalVerified": 28,
    "totalBlocked": 4
  },
  "message": "OK",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## 3. Assign Enterprises to User

**Endpoint:** `POST /sgod-auth/v1/sgod/enterprises/assign`
**Success HTTP Code:** 200

```json
{
  "success": true,
  "data": {
    "userId": "user-uuid",
    "assignedTenantIds": [
      "tenant-uuid-B"
    ]
  },
  "message": "Tenants assigned successfully",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## 4. Unassign Enterprise from User

**Endpoint:** `POST /sgod-auth/v1/sgod/enterprises/unassign`
**Success HTTP Code:** 200

```json
{
  "success": true,
  "data": {
    "userId": "user-uuid",
    "remainingTenantIds": [
      "tenant-uuid-A",
      "tenant-uuid-C"
    ]
  },
  "message": "Tenant unassigned successfully",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## 5. Set Assigned Enterprises

**Endpoint:** `POST /sgod-auth/v1/sgod/enterprises/set-assigned`
**Success HTTP Code:** 200

```json
{
  "success": true,
  "data": {
    "userId": "user-uuid",
    "assignedTenantIds": [
      "tenant-uuid-A",
      "tenant-uuid-C"
    ]
  },
  "message": "Tenants set-assigned successfully",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## 6. List Deleted Enterprises

**Endpoint:** `GET /sgod-auth/v1/sgod/enterprises/deleted`
**Response Type:** Same as #1 but filtered to deleted
**Success HTTP Code:** 200

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "tenant-deleted-uuid",
        "name": "Deleted Corp",
        "status": "deleted",
        "deletedAt": "2026-09-15T10:00:00.000Z"
      }
    ],
    "total": 5,
    "page": 1,
    "limit": 20
  },
  "message": "OK",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## 7. Get Enterprise by ID

**Endpoint:** `GET /sgod-auth/v1/sgod/enterprises/{tenantId}`
**Success HTTP Code:** 200

```json
{
  "success": true,
  "data": {
    "id": "tenant-uuid-A",
    "name": "Acme Corp",
    "status": "active",
    "subscriptionEnd": "2027-10-06T10:00:00.000Z",
    "features": [
      "audit_logging",
      "mfa_required"
    ],
    "createdAt": "2025-10-06T10:00:00.000Z",
    "updatedAt": "2026-10-06T10:00:00.000Z"
  },
  "message": "OK",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## 8. Block Enterprise

**Endpoint:** `POST /sgod-auth/v1/sgod/enterprises/{tenantId}/block`
**Success HTTP Code:** 200

```json
{
  "success": true,
  "data": {
    "id": "tenant-uuid-B",
    "status": "blocked",
    "blockedAt": "2026-10-06T10:00:00.000Z",
    "blockedReason": "Policy violation - manual review"
  },
  "message": "Tenant blocked",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## 9. Unblock Enterprise

**Endpoint:** `POST /sgod-auth/v1/sgod/enterprises/{tenantId}/unblock`
**Success HTTP Code:** 200

```json
{
  "success": true,
  "data": {
    "id": "tenant-uuid-B",
    "status": "active",
    "unblockedAt": "2026-10-06T10:00:00.000Z",
    "unblockedReason": "Audit complete - unblock"
  },
  "message": "Tenant unblocked",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## 10. Restore Deleted Enterprise

**Endpoint:** `POST /sgod-auth/v1/sgod/enterprises/{tenantId}/restore`
**Success HTTP Code:** 200

```json
{
  "success": true,
  "data": {
    "id": "tenant-uuid-deleted",
    "status": "active",
    "restoredAt": "2026-10-06T10:00:00.000Z"
  },
  "message": "Tenant restored",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## 11. Update Enterprise Subscription

**Endpoint:** `PATCH /sgod-auth/v1/sgod/enterprises/{tenantId}/subscription`
**Success HTTP Code:** 200

```json
{
  "success": true,
  "data": {
    "id": "tenant-uuid-A",
    "subscriptionEnd": "2028-10-06T10:00:00.000Z",
    "durationDaysAdded": 365
  },
  "message": "Subscription updated",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## 12. Update Enterprise Features

**Endpoint:** `PATCH /sgod-auth/v1/sgod/enterprises/{tenantId}/features`
**Success HTTP Code:** 200

```json
{
  "success": true,
  "data": {
    "id": "tenant-uuid-A",
    "features": [
      "audit_logging",
      "sso",
      "mfa_required"
    ]
  },
  "message": "Features updated",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## 13. Get Enterprise Statistics by ID

**Endpoint:** `GET /sgod-auth/v1/sgod/enterprises/{tenantId}/statistics`
**Success HTTP Code:** 200

```json
{
  "success": true,
  "data": {
    "tenantId": "tenant-uuid-A",
    "totalUsers": 120,
    "totalActiveUsers": 95,
    "totalDocuments": 1500,
    "totalStorageBytes": 5368709120
  },
  "message": "OK",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## 14. Assign Organizational

**Endpoint:** `POST /sgod-auth/v1/users/{userId}/organizational/assign`
**Response Type:** `IAssignUserDeptPositionResponse`
**Success HTTP Code:** 200

```json
{
  "success": true,
  "data": {
    "userId": "user-uuid-B",
    "departmentId": "dept-uuid",
    "positionId": "pos-uuid",
    "primaryRoleId": "role-uuid",
    "bossId": "boss-uuid"
  },
  "message": "User assigned to organizational position",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## 15. Remove User from Organizational Position

**Endpoint:** `POST /sgod-auth/v1/users/{userId}/organizational/remove?userType=EnterpriseUser`
**Response Type:** `IRemoveUserOrganizationalResponse`
**Success HTTP Code:** 200

```json
{
  "success": true,
  "data": {
    "message": "User removed from organizational structure successfully"
  },
  "message": "Position membership removed",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## 16. Get Available Bosses

**Endpoint:** `GET /sgod-auth/v1/users/{userId}/organizational/bosses/available?userType=EnterpriseUser`
**Response Type:** `IAvailableBossesResponse`
**Success HTTP Code:** 200

```json
{
  "success": true,
  "data": {
    "bosses": [
      {
        "id": "user-manager-uuid",
        "fullName": {
          "firstName": "Alice",
          "lastName": "Manager"
        },
        "email": "alice.manager@enterprise.test",
        "positionId": "pos-manager-uuid",
        "departmentId": "dept-mgmt-uuid"
      }
    ]
  },
  "message": "OK",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## 17. Set Boss

**Endpoint:** `POST /sgod-auth/v1/users/{userId}/organizational/bosses/set`
**Success HTTP Code:** 200

```json
{
  "success": true,
  "data": {
    "userId": "user-uuid-B",
    "bossId": "user-manager-uuid"
  },
  "message": "Boss set successfully",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## 18. Check Subordinate

**Endpoint:** `GET /sgod-auth/v1/users/{userId}/organizational/check-subordinate?subordinateId={subordinateId}`
**Response Type:** `ICheckSubordinateResponse`
**Success HTTP Code:** 200

```json
{
  "success": true,
  "data": {
    "isSubordinate": true,
    "message": "User is a direct subordinate"
  },
  "message": "OK",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

### Response Field Descriptions
| Field | Type | Description |
|-------|------|-------------|
| data.isSubordinate | boolean | Whether subordinateId reports up to userId |
| data.message | string | Optional human-readable status |

**Note:** Old evidence had a `depth` field, but actual `ICheckSubordinateData` only has `isSubordinate: boolean` and optional `message?: string`. The `depth` field does NOT exist in current DTO.

---

## 19. Audit Organizational Reporting Lines

**Endpoint:** `GET /sgod-auth/v1/organizations/audit?tenantId={tenantId}`
**Success HTTP Code:** 200

```json
{
  "success": true,
  "data": {
    "tenantId": "tenant-uuid-A",
    "reportingLines": [
      {
        "userId": "user-uuid-B",
        "bossId": "user-manager-uuid",
        "departmentId": "dept-uuid",
        "positionId": "pos-uuid"
      }
    ],
    "inconsistencies": [],
    "auditedAt": "2026-10-06T10:00:00.000Z"
  },
  "message": "OK",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Removed Endpoints (Old Evidence Cleanup)

The following success responses have been **REMOVED** from this document because the corresponding endpoints are not present in the current Swagger:
- ❌ `POST /users/{id}/organizational/bosses/add` — NOT in Swagger
- ❌ `GET /users/{id}/organizational/bosses` — NOT in Swagger
- ❌ `GET /users/{id}/organizational/subordinates` — NOT in Swagger