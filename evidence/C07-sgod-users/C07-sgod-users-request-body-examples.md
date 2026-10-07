# C07 — SGOD Users — Request Body Examples

<div align="center">

![Cluster](https://img.shields.io/badge/C07-SGOD+Users-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Evidence Type](https://img.shields.io/badge/Evidence-Request+Body+Examples-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)

</div>

- [Error Responses](./C07-sgod-users-error-responses.md)
- [Success Responses](./C07-sgod-users-success-responses.md)

---

## 🧭 Mục Lục (Table of Contents)

| # | Endpoint |
|---|---|
| 01 | [SGOD User Create(#sgod-user-create) |
| 02 | [SGOD User Update(#sgod-user-update) |
| 03 | [SGOD User Get by ID(#sgod-user-get-by-id) |
| 04 | [SGOD User List(#sgod-user-list) |
| 05 | [SGOD User Delete(#sgod-user-delete) |
| 06 | [SGOD User Permanent Delete(#sgod-user-permanent-delete) |
| 07 | [SGOD User Assign Roles(#sgod-user-assign-roles) |
| 08 | [SGOD User Set Department/Position(#sgod-user-set-departmentposition) |
| 09 | [SGOD User Block(#sgod-user-block) |
| 10 | [SGOD User Unblock(#sgod-user-unblock) |

---

## Overview
This document provides representative request body examples for each operation in the **SGOD Users** cluster. SGOD users are staff of the SGOD organization itself (not bound to a tenant).

---

## SGOD User Create

**Endpoint:** `POST /sgod-auth/v1/sgod-users`
**DTO Source:** `ParamCreateSgodUserDto` from `types.ts`
**Actor:** ROOT_ADMIN (SGOD root)

### Sample Request Body
```json
{
  "email": "sgod@sgod.test",
  "userName": "sgodstaff",
  "fullName": {
    "firstName": "Alice",
    "lastName": "Wong"
  },
  "phone": "0905556666",
  "gender": "female",
  "departmentId": "sgod-dept-uuid",
  "positionId": "sgod-pos-uuid",
  "roleIds": [
    "sgod-role-uuid"
  ],
  "userType": "sgodUser"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | ✅ | SGOD user email |
| userName | string | ✅ | Unique username |
| fullName.firstName | string | ✅ | First name |
| fullName.lastName | string | ✅ | Last name |
| phone | string | required | Phone |
| gender | enum | string | `male` / `female` / `other` |
| departmentId | string | required | SGOD department ID |
| positionId | string | required | SGOD position ID |
| roleIds | string[] | required | SGOD role IDs |
| userType | enum | string | `sgodUser` |

---

## SGOD User Update

**Endpoint:** `PATCH /sgod-auth/v1/sgod-users/{id}`
**DTO Source:** `ParamPatchSgodUser` from `types.ts` (all fields optional nested)
**Actor:** SGOD_ADMIN_A

### Sample Request Body
```json
{
  "fullName": {
    "firstName": "Alicia",
    "lastName": "Wong"
  },
  "email": "alicia.wong@sgod.test",
  "phone": "0905557777",
  "gender": "female",
  "avatarUrl": "https://cdn.sgod.test/avatars/sgod-alicia.png"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| fullName.firstName | string | ❌ | New first name |
| fullName.lastName | string | ❌ | New last name |
| email | string | ❌ | New email |
| phone | string | ❌ | New phone |
| gender | enum | string | New gender |
| avatarUrl | string | ❌ | New avatar URL |

---

## SGOD User Get by ID

**Endpoint:** `GET /sgod-auth/v1/sgod-users/{id}`
**DTO Source:** None
**Actor:** ROOT_ADMIN

### Sample Request Body
```json
{}
```

---

## SGOD User List

**Endpoint:** `GET /sgod-auth/v1/sgod-users`
**DTO Source:** Query string
**Actor:** ROOT_ADMIN

### Sample Request Body
```json
{}
```

---

## SGOD User Delete

**Endpoint:** `DELETE /sgod-auth/v1/sgod-users/{id}`
**DTO Source:** None
**Actor:** ROOT_ADMIN

### Sample Request Body
```json
{}
```

---

## SGOD User Permanent Delete

**Endpoint:** `DELETE /sgod-auth/v1/sgod-users/{id}/permanent`
**DTO Source:** None
**Actor:** ROOT_ADMIN

### Sample Request Body
```json
{}
```

---

## SGOD User Assign Roles

**Endpoint:** `PATCH /sgod-auth/v1/sgod-users/{id}/roles`
**DTO Source:** `ParamAssignUserRolesDto` from `types.ts`
**Actor:** ROOT_ADMIN

### Sample Request Body
```json
{
  "roleIds": [
    "sgod-role-uuid"
  ]
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| roleIds | string[] | required | Full replacement list of role IDs |

---

## SGOD User Set Department/Position

**Endpoint:** `PATCH /sgod-auth/v1/sgod-users/{id}/department-position`
**DTO Source:** `ParamAssignDeptPositionSgodUser` from `types.ts` (all fields optional)
**Actor:** SGOD_ADMIN_A

### Sample Request Body
```json
{
  "departmentId": "new-sgod-dept-uuid",
  "positionId": "new-sgod-pos-uuid",
  "bossId": "manager-sgod-uuid",
  "userType": "sgodUser"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| departmentId | string | ❌ | New SGOD department ID |
| positionId | string | ❌ | New SGOD position ID |
| bossId | string | ❌ | New boss ID |
| userType | string | ❌ | User type discriminator (`sgodUser`) |

---

## SGOD User Block

**Endpoint:** `POST /sgod-auth/v1/sgod-users/{id}/block`
**DTO Source:** `ParamBlockSgodUser` (userId only) — no body required
**Actor:** SGOD_ADMIN_A with step-up MFA

### Sample Request Body
```json
{}
```

---

## SGOD User Unblock

**Endpoint:** `POST /sgod-auth/v1/sgod-users/{id}/unblock`
**DTO Source:** None
**Actor:** ROOT_ADMIN

### Sample Request Body
```json
{}
```