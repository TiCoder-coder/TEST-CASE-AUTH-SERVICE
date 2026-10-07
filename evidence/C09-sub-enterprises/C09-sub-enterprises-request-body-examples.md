# C09 — Sub-Enterprises — Request Body Examples

<div align="center">

![Cluster](https://img.shields.io/badge/C09-Sub-Enterprises-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Evidence Type](https://img.shields.io/badge/Evidence-Request+Body+Examples-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)

</div>

- [Error Responses](./C09-sub-enterprises-error-responses.md)
- [Success Responses](./C09-sub-enterprises-success-responses.md)

---

## 🧭 Mục Lục (Table of Contents)

| # | Endpoint |
|---|---|
| 01 | [Sub-Enterprise Create(#sub-enterprise-create) |
| 02 | [Sub-Enterprise Update (Partial PATCH)(#sub-enterprise-update-partial-patch) |
| 03 | [Sub-Enterprise Update My-Profile (3 aliases)(#sub-enterprise-update-my-profile-3-aliases) |
| 04 | [Sub-Enterprise List(#sub-enterprise-list) |
| 05 | [Sub-Enterprise Statistics(#sub-enterprise-statistics) |
| 06 | [Sub-Enterprise Deleted List(#sub-enterprise-deleted-list) |
| 07 | [Sub-Enterprise Get by ID(#sub-enterprise-get-by-id) |
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
This document provides representative request body examples for the **Sub-Enterprises** cluster. Sub-enterprise users are members of an external sub-company (branch) attached to a parent SGOD tenant.

> **Important DTO notes:**
> - `ParamCreateSubEnterpriseUser` requires `userType: "EnterpriseUser"` (PascalCase, NOT `sub_enterprise`).
> - `ParamUpdateSubEnterpriseUser` is a partial-patch DTO with fields: `fullName`, `email`, `phone`, `gender`, `avatarUrl`.
> - `ParamAssignDepartmentPositionSubEnterpriseUser` does NOT include `primaryRoleId` (no primary role concept in sub-enterprise).
> - `ParamSetBossSubEnterpriseUser` requires `userType: "EnterpriseUser"` alongside `bossId`.
> - Roles endpoint method is **PATCH** (not POST) per Swagger.
> - Organizational endpoint method is **PATCH** (not POST) per Swagger.
> - Path for set-boss is **/bosses** (plural, not /boss).

---

## Sub-Enterprise Create

**Endpoint:** `POST /sgod-auth/v1/sub-enterprises`
**DTO Source:** `ParamCreateSubEnterpriseUser` from `types.ts`
**Actor:** Enterprise user (with create permission in parent tenant)

### Sample Request Body
```json
{
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
  "userType": "EnterpriseUser"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | required | Sub-enterprise user email |
| userName | string | required | Username |
| fullName.firstName | string | required | First name |
| fullName.lastName | string | required | Last name |
| phone | string | required | Phone |
| gender | enum | required | `Male` / `Female` / `Other` (PascalCase) |
| departmentId | string | required | Department ID |
| positionId | string | required | Position ID |
| roleIds | string[] | required | Role IDs |
| userType | enum | required | `EnterpriseUser` (PascalCase) |

---

## Sub-Enterprise Update (Partial PATCH)

**Endpoint:** `PATCH /sgod-auth/v1/sub-enterprises/{userId}`
**DTO Source:** `ParamUpdateSubEnterpriseUser` from `types.ts`
**Actor:** Enterprise user (with update permission)

### Sample Request Body
```json
{
  "fullName": {
    "firstName": "Robert",
    "lastName": "Marley"
  },
  "email": "voanhnhatTicoder+subent@sgod.test",
  "phone": "0904446666",
  "gender": "MALE",
  "avatarUrl": "https://cdn.sgod.test/avatars/subent-a-001.png"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| fullName.firstName | string | optional | New first name |
| fullName.lastName | string | optional | New last name |
| email | string | optional | New email |
| phone | string | optional | New phone |
| gender | enum | optional | Gender (`MALE` / `FEMALE` / `OTHER`) |
| avatarUrl | string | optional | New avatar URL |

---

## Sub-Enterprise Update My-Profile (3 aliases)

**Endpoints:** `PATCH /sgod-auth/v1/sub-enterprises/me` | `my-profile` | `profile`
**DTO Source:** `ParamUpdateMySubEnterpriseProfile` from `types.ts`
**Actor:** Sub-enterprise user (themselves)

### Sample Request Body
```json
{
  "fullName": {
    "firstName": "Robert",
    "lastName": "Marley"
  },
  "email": "voanhnhatTicoder@gmail.com",
  "phone": "0904446666",
  "gender": "MALE",
  "avatarUrl": "https://cdn.sgod.test/avatars/me.png"
}
```

---

## Sub-Enterprise List

**Endpoint:** `GET /sgod-auth/v1/sub-enterprises`
**Query Params:** `page`, `limit`, `search`, `departmentId`, `positionId`, `roleId`, `status`
**Actor:** Enterprise user

No request body (parameter list only).

---

## Sub-Enterprise Statistics

**Endpoint:** `GET /sgod-auth/v1/sub-enterprises/stats`
**Actor:** Enterprise user

No request body.

> Note: Swagger uses `/stats` (not `/statistics`).

---

## Sub-Enterprise Deleted List

**Endpoint:** `GET /sgod-auth/v1/sub-enterprises/deleted`
**Query Params:** `page`, `limit`, `search`, `departmentId`, `positionId`, `roleId`, `status`
**Actor:** Enterprise user

No request body.

---

## Sub-Enterprise Get by ID

**Endpoint:** `GET /sgod-auth/v1/sub-enterprises/{userId}`
**Actor:** Enterprise user

No request body.

---

## Sub-Enterprise Delete (Soft)

**Endpoint:** `DELETE /sgod-auth/v1/sub-enterprises/{userId}`
**Actor:** Enterprise user (with delete permission)

No request body.

---

## Sub-Enterprise Permanent Delete

**Endpoint:** `DELETE /sgod-auth/v1/sub-enterprises/{userId}/permanent`
**Actor:** Enterprise user (with permanent-delete permission)

No request body.

---

## Sub-Enterprise Restore

**Endpoint:** `POST /sgod-auth/v1/sub-enterprises/{userId}/restore`
**Actor:** Enterprise user (with restore permission)

No request body.

---

## Sub-Enterprise Set Organizational (PATCH)

**Endpoint:** `PATCH /sgod-auth/v1/sub-enterprises/{userId}/organizational`
**DTO Source:** `ParamAssignDepartmentPositionSubEnterpriseUser` from `types.ts`
**Actor:** Enterprise user (with org permission)

### Sample Request Body
```json
{
  "departmentId": "dept-parent-001",
  "positionId": "pos-parent-001",
  "bossId": "boss-user-001",
  "userType": "EnterpriseUser"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| departmentId | string | optional | New department ID |
| positionId | string | optional | New position ID |
| userType | enum | optional | `EnterpriseUser` (required per Swagger) |
| primaryRoleId | string | NOT USED | DTO has this field, but create-org path does not use it |
| bossId | string | optional | New boss ID |

> Swagger method is **PATCH** (not POST). Body does NOT include `primaryRoleId` for sub-enterprise organizational assignment.

---

## Sub-Enterprise Get Organizational

**Endpoint:** `GET /sgod-auth/v1/sub-enterprises/{userId}/organizational`
**Actor:** Enterprise user

No request body.

---

## Sub-Enterprise Set Roles (PATCH)

**Endpoint:** `PATCH /sgod-auth/v1/sub-enterprises/{userId}/roles`
**DTO Source:** `ParamAssignRolesSubEnterpriseUser` from `types.ts`
**Actor:** Enterprise user (with role-assignment permission)

### Sample Request Body
```json
{
  "roleIds": [
    "role-custom-001",
    "role-custom-002"
  ]
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| roleIds | string[] | required | New role IDs (replaces existing list) |

> Swagger method is **PATCH** (not POST).

---

## Sub-Enterprise Get Roles

**Endpoint:** `GET /sgod-auth/v1/sub-enterprises/{userId}/roles`
**Actor:** Enterprise user

No request body.

---

## Sub-Enterprise List Available Bosses

**Endpoint:** `GET /sgod-auth/v1/sub-enterprises/{userId}/bosses`
**Actor:** Enterprise user

No request body.

> Swagger path uses `bosses` (plural, not `available-bosses`).

---

## Sub-Enterprise Set Boss

**Endpoint:** `PATCH /sgod-auth/v1/sub-enterprises/{userId}/bosses`
**DTO Source:** `ParamSetBossSubEnterpriseUser` from `types.ts`
**Actor:** Enterprise user (with boss-assignment permission)

### Sample Request Body
```json
{
  "bossId": "boss-user-001",
  "userType": "EnterpriseUser"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| bossId | string | required | New boss user ID |
| userType | enum | required | `EnterpriseUser` (required per Swagger) |

> Swagger path is **/bosses** (plural), NOT `/boss`.

---

## Sub-Enterprise Block

**Endpoint:** `POST /sgod-auth/v1/sub-enterprises/{userId}/block`
**Actor:** Enterprise user (with block permission; MFA step-up may be required)

No request body.

---

## Sub-Enterprise Unblock

**Endpoint:** `POST /sgod-auth/v1/sub-enterprises/{userId}/unblock`
**Actor:** Enterprise user (with unblock permission)

No request body.