# C09 — Sub-Enterprises — Success Response Schemas

<div align="center">

![Cluster](https://img.shields.io/badge/C09-Sub-Enterprises-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Evidence Type](https://img.shields.io/badge/Evidence-Success+Responses-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)

</div>

- [Error Responses](./C09-sub-enterprises-error-responses.md)
- [Request Body Examples](./C09-sub-enterprises-request-body-examples.md)

---

## 🧭 Mục Lục (Table of Contents)

| # | Endpoint |
|---|---|
| 01 | [Sub-Enterprise Create(#sub-enterprise-create) |
| 02 | [Sub-Enterprise Update(#sub-enterprise-update) |
| 03 | [Sub-Enterprise Update My-Profile (me / my-profile / profile)(#sub-enterprise-update-my-profile-me--my-profile--profile) |
| 04 | [Sub-Enterprise Get by ID(#sub-enterprise-get-by-id) |
| 05 | [Sub-Enterprise List(#sub-enterprise-list) |
| 06 | [Sub-Enterprise Statistics(#sub-enterprise-statistics) |
| 07 | [Sub-Enterprise Deleted List(#sub-enterprise-deleted-list) |
| 08 | [Sub-Enterprise Delete (Soft)(#sub-enterprise-delete-soft) |
| 09 | [Sub-Enterprise Permanent Delete(#sub-enterprise-permanent-delete) |
| 10 | [Sub-Enterprise Restore(#sub-enterprise-restore) |
| 11 | [Sub-Enterprise Set Organizational (PATCH)(#sub-enterprise-set-organizational-patch) |
| 12 | [Sub-Enterprise Get Organizational(#sub-enterprise-get-organizational) |
| 13 | [Sub-Enterprise Set Roles (PATCH)(#sub-enterprise-set-roles-patch) |
| 14 | [Sub-Enterprise Get Roles(#sub-enterprise-get-roles) |
| 15 | [Sub-Enterprise List Available Bosses(#sub-enterprise-list-available-bosses) |
| 16 | [Sub-Enterprise Set Boss(#sub-enterprise-set-boss) |
| 17 | [Sub-Enterprise Block(#sub-enterprise-block) |
| 18 | [Sub-Enterprise Unblock(#sub-enterprise-unblock) |

---

## Overview
This document describes expected 200 OK response schemas for each endpoint in the Sub-Enterprises cluster. All responses follow the `IBeApiEnvelope<T>` envelope pattern.

---

## Sub-Enterprise Create

**Endpoint:** `POST /sgod-auth/v1/sub-enterprises`
**Response Type:** `IBeApiEnvelope<ISubEnterpriseUser>`
**Success HTTP Code:** 201 or 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "id": "subent-uuid-001",
    "email": "voanhnhatTicoder+subent@sgod.test",
    "userName": "subent_owner",
    "fullName": {
      "firstName": "Bob",
      "lastName": "Marley"
    },
    "phone": "0904445555",
    "gender": "Male",
    "departmentId": "dept-parent-001",
    "positionId": "pos-parent-001",
    "roleIds": [
      "role-custom-001"
    ],
    "userType": "EnterpriseUser",
    "bossId": null,
    "status": "active",
    "tenantId": "tenant-a-001",
    "createdAt": "2026-10-06T10:00:00.000Z"
  },
  "message": "Sub-enterprise user created",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

### Response Field Descriptions
| Field | Type | Description |
|-------|------|-------------|
| data.id | string | Sub-enterprise user ID |
| data.email | string | User email |
| data.userType | string | Always `EnterpriseUser` |
| data.bossId | string\|null | Current boss user ID (nullable) |
| data.status | string | `active` / `blocked` |
| data.tenantId | string | Parent tenant ID |

---

## Sub-Enterprise Update

**Endpoint:** `PATCH /sgod-auth/v1/sub-enterprises/{userId}`
**Response Type:** `IBeApiEnvelope<ISubEnterpriseUser>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "id": "subent-uuid-001",
    "fullName": {
      "firstName": "Robert",
      "lastName": "Marley"
    },
    "email": "voanhnhatTicoder+subent@sgod.test",
    "phone": "0904446666",
    "gender": "MALE",
    "avatarUrl": "https://cdn.sgod.test/avatars/subent-a-001.png"
  },
  "message": "Sub-enterprise user updated",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Sub-Enterprise Update My-Profile (me / my-profile / profile)

**Endpoint:** `PATCH /sgod-auth/v1/sub-enterprises/me` (and aliases)
**Response Type:** `IBeApiEnvelope<ISubEnterpriseUser>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "id": "subent-uuid-001",
    "fullName": {
      "firstName": "Robert",
      "lastName": "Marley"
    },
    "email": "voanhnhatTicoder@gmail.com",
    "phone": "0904446666",
    "gender": "MALE",
    "avatarUrl": "https://cdn.sgod.test/avatars/me.png"
  },
  "message": "Profile updated",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Sub-Enterprise Get by ID

**Endpoint:** `GET /sgod-auth/v1/sub-enterprises/{userId}`
**Response Type:** `IBeApiEnvelope<ISubEnterpriseUser>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "id": "subent-uuid-001",
    "email": "voanhnhatTicoder+subent@sgod.test",
    "userName": "subent_owner",
    "fullName": {
      "firstName": "Bob",
      "lastName": "Marley"
    },
    "phone": "0904445555",
    "gender": "Male",
    "departmentId": "dept-parent-001",
    "positionId": "pos-parent-001",
    "roleIds": [
      "role-custom-001"
    ],
    "userType": "EnterpriseUser",
    "bossId": "boss-user-001",
    "status": "active",
    "tenantId": "tenant-a-001",
    "createdAt": "2026-10-06T10:00:00.000Z"
  },
  "message": "OK",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Sub-Enterprise List

**Endpoint:** `GET /sgod-auth/v1/sub-enterprises`
**Response Type:** `IBeApiEnvelope<IGetSubEnterpriseUserListResponseData>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "users": [
      {
        "id": "subent-uuid-001",
        "email": "voanhnhatTicoder+subent@sgod.test",
        "userType": "EnterpriseUser",
        "status": "active"
      },
      {
        "id": "subent-uuid-002",
        "email": "voanhnhatTicoder+subent-b@sgod.test",
        "userType": "EnterpriseUser",
        "status": "blocked"
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

## Sub-Enterprise Statistics

**Endpoint:** `GET /sgod-auth/v1/sub-enterprises/stats`
**Response Type:** `IBeApiEnvelope<IGetSubEnterpriseUserStatisticsResponseData>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "total": 25,
    "active": 22,
    "blocked": 1,
    "deleted": 2
  },
  "message": "OK",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Sub-Enterprise Deleted List

**Endpoint:** `GET /sgod-auth/v1/sub-enterprises/deleted`
**Response Type:** `IBeApiEnvelope<IGetSubEnterpriseUserListResponseData>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "users": [
      {
        "id": "subent-deleted-001",
        "email": "voanhnhatTicoder+deleted@sgod.test",
        "userType": "EnterpriseUser",
        "status": "deleted"
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

## Sub-Enterprise Delete (Soft)

**Endpoint:** `DELETE /sgod-auth/v1/sub-enterprises/{userId}`
**Response Type:** `IBeApiEnvelope<{ deleted: boolean; id: string }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "deleted": true,
    "id": "subent-uuid-001"
  },
  "message": "Sub-enterprise user soft-deleted",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Sub-Enterprise Permanent Delete

**Endpoint:** `DELETE /sgod-auth/v1/sub-enterprises/{userId}/permanent`
**Response Type:** `IBeApiEnvelope<{ deleted: boolean; permanent: boolean; id: string }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "deleted": true,
    "permanent": true,
    "id": "subent-permanent-001"
  },
  "message": "Sub-enterprise user permanently deleted",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Sub-Enterprise Restore

**Endpoint:** `POST /sgod-auth/v1/sub-enterprises/{userId}/restore`
**Response Type:** `IBeApiEnvelope<{ restored: boolean; id: string }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "restored": true,
    "id": "subent-deleted-001"
  },
  "message": "Sub-enterprise user restored",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Sub-Enterprise Set Organizational (PATCH)

**Endpoint:** `PATCH /sgod-auth/v1/sub-enterprises/{userId}/organizational`
**Response Type:** `IBeApiEnvelope<IAssignUserDeptPositionResponse>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "departmentId": "dept-parent-001",
    "positionId": "pos-parent-001",
    "bossId": "boss-user-001",
    "userType": "EnterpriseUser"
  },
  "message": "Organizational assignment updated",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Sub-Enterprise Get Organizational

**Endpoint:** `GET /sgod-auth/v1/sub-enterprises/{userId}/organizational`
**Response Type:** `IBeApiEnvelope<IAssignUserDeptPositionResponse>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "departmentId": "dept-parent-001",
    "positionId": "pos-parent-001",
    "bossId": "boss-user-001",
    "userType": "EnterpriseUser"
  },
  "message": "OK",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Sub-Enterprise Set Roles (PATCH)

**Endpoint:** `PATCH /sgod-auth/v1/sub-enterprises/{userId}/roles`
**Response Type:** `IBeApiEnvelope<IRoleAssignmentResponse>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "userId": "subent-uuid-001",
    "roleIds": [
      "role-custom-001",
      "role-custom-002"
    ]
  },
  "message": "Roles assigned",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Sub-Enterprise Get Roles

**Endpoint:** `GET /sgod-auth/v1/sub-enterprises/{userId}/roles`
**Response Type:** `IBeApiEnvelope<IRoleAssignmentResponse>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "userId": "subent-uuid-001",
    "roleIds": [
      "role-custom-001",
      "role-custom-002"
    ]
  },
  "message": "OK",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Sub-Enterprise List Available Bosses

**Endpoint:** `GET /sgod-auth/v1/sub-enterprises/{userId}/bosses`
**Response Type:** `IBeApiEnvelope<IAvailableBossesResponse>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "candidates": [
      {
        "id": "boss-user-001",
        "fullName": {
          "firstName": "Manager",
          "lastName": "One"
        },
        "positionId": "pos-parent-001"
      }
    ]
  },
  "message": "OK",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Sub-Enterprise Set Boss

**Endpoint:** `PATCH /sgod-auth/v1/sub-enterprises/{userId}/bosses`
**Response Type:** `IBeApiEnvelope<ISetBossResponse>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "userId": "subent-uuid-001",
    "bossId": "boss-user-001",
    "userType": "EnterpriseUser"
  },
  "message": "Boss updated",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Sub-Enterprise Block

**Endpoint:** `POST /sgod-auth/v1/sub-enterprises/{userId}/block`
**Response Type:** `IBeApiEnvelope<{ blocked: boolean; id: string }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "blocked": true,
    "id": "subent-block-001"
  },
  "message": "Sub-enterprise user blocked",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

---

## Sub-Enterprise Unblock

**Endpoint:** `POST /sgod-auth/v1/sub-enterprises/{userId}/unblock`
**Response Type:** `IBeApiEnvelope<{ unblocked: boolean; id: string }>`
**Success HTTP Code:** 200

### Sample Success Response
```json
{
  "success": true,
  "data": {
    "unblocked": true,
    "id": "subent-block-001"
  },
  "message": "Sub-enterprise user unblocked",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```