# C08 — IAM Step-up / SGOD Admins — Request Body Examples

<div align="center">

![Cluster](https://img.shields.io/badge/C08-IAM+Step-up+++SGOD+Admins-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Evidence Type](https://img.shields.io/badge/Evidence-Request+Body+Examples-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)

</div>

- [Error Responses](./C08-admin-step-up-error-responses.md)
- [Success Responses](./C08-admin-step-up-success-responses.md)

---

## 🧭 Mục Lục (Table of Contents)

| # | Endpoint |
|---|---|
| 01 | [IAM Step-up(#iam-step-up) |
| 02 | [SGOD Admin List(#sgod-admin-list) |
| 03 | [SGOD Admin Get(#sgod-admin-get) |
| 04 | [SGOD Admin Create(#sgod-admin-create) |
| 05 | [SGOD Admin Update(#sgod-admin-update) |
| 06 | [SGOD Admin Block(#sgod-admin-block) |
| 07 | [SGOD Admin Unblock(#sgod-admin-unblock) |
| 08 | [SGOD Admin Delete(#sgod-admin-delete) |
| 09 | [SGOD Admin Assign Roles(#sgod-admin-assign-roles) |

---

## Overview
This document provides representative request body examples for IAM step-up authentication and SGOD admin management.

---

## IAM Step-up

**Endpoint:** `POST /sgod-auth/v1/iam/step-up`
**DTO Source:** `ParamIamStepUpDto` from `types.ts`
**Actor:** Authenticated user with MFA enrolled

### Sample Request Body
```json
{
  "twoFactorCode": "654321"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| twoFactorCode | string | required | 6-digit TOTP code |

---

## SGOD Admin List

**Endpoint:** `GET /sgod-auth/v1/sgod/admins`
**DTO Source:** Query string
**Actor:** ROOT_ADMIN

### Sample Request Body
```json
{}
```

---

## SGOD Admin Get

**Endpoint:** `GET /sgod-auth/v1/sgod/admins/{adminId}`
**DTO Source:** None
**Actor:** SGOD_ADMIN_A / ROOT_ADMIN

### Sample Request Body
```json
{}
```

---

## SGOD Admin Create

**Endpoint:** `POST /sgod-auth/v1/sgod/admins`
**DTO Source:** `ParamCreateSgodAdmin` from `types.ts`
**Actor:** ROOT_ADMIN

### Sample Request Body
```json
{
  "email": "root@sgod.test",
  "userName": "rootadmin",
  "fullName": {
    "firstName": "Root",
    "lastName": "Admin"
  },
  "phone": "0900000001",
  "gender": "male",
  "departmentId": "sgod-dept-uuid",
  "positionId": "sgod-pos-uuid",
  "roleIds": [
    "root-role-uuid"
  ],
  "userType": "sgodAdmin"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | ✅ | Admin email |
| userName | string | ✅ | Unique username |
| fullName.firstName | string | ✅ | First name |
| fullName.lastName | string | ✅ | Last name |
| phone | string | ✅ | Phone |
| gender | enum | string | Gender (`male` / `female` / `other`) |
| departmentId | string | ✅ | Department ID |
| positionId | string | ✅ | Position ID |
| roleIds | string[] | ✅ | Role IDs |
| userType | enum | string | `sgodAdmin` (literal) |

---

## SGOD Admin Update

**Endpoint:** `PATCH /sgod-auth/v1/sgod/admins/{adminId}`
**DTO Source:** `ParamPatchSgodAdmin` from `types.ts` (all fields optional nested)
**Actor:** SGOD_ADMIN_A / ROOT_ADMIN

### Sample Request Body
```json
{
  "fullName": {
    "firstName": "Root2",
    "lastName": "Admin"
  },
  "email": "root2@sgod.test",
  "phone": "0900009999",
  "gender": "male",
  "avatarUrl": "https://cdn.sgod.test/avatars/sgod-root2.png"
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

## SGOD Admin Block

**Endpoint:** `POST /sgod-auth/v1/sgod/admins/{adminId}/block`
**DTO Source:** `ParamBlockSgodAdmin` (adminId only) — no body required
**Actor:** SGOD_ADMIN_A (with step-up MFA)

### Sample Request Body
```json
{}
```

---

## SGOD Admin Unblock

**Endpoint:** `POST /sgod-auth/v1/sgod/admins/{adminId}/unblock`
**DTO Source:** `ParamUnblockSgodAdmin` (adminId only) — no body required
**Actor:** SGOD_ADMIN_A

### Sample Request Body
```json
{}
```

---

## SGOD Admin Delete

**Endpoint:** `DELETE /sgod-auth/v1/sgod/admins/{adminId}`
**DTO Source:** None
**Actor:** ROOT_ADMIN

### Sample Request Body
```json
{}
```

---

## SGOD Admin Assign Roles

**Endpoint:** `PATCH /sgod-auth/v1/sgod/admins/{adminId}/roles`
**DTO Source:** `ParamAssignRolesSgodAdmin` from `types.ts`
**Actor:** ROOT_ADMIN

### Sample Request Body
```json
{
  "roleIds": [
    "root-role-uuid"
  ]
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| roleIds | string[] | required | Full replacement list of role IDs |