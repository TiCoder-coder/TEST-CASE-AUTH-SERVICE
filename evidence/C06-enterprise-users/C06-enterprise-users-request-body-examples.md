# C06 — Enterprise Users — Request Body Examples

<div align="center">

![Cluster](https://img.shields.io/badge/C06-Enterprise+Users-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Evidence Type](https://img.shields.io/badge/Evidence-Request+Body+Examples-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)

</div>

- [Error Responses](./C06-enterprise-users-error-responses.md)
- [Success Responses](./C06-enterprise-users-success-responses.md)

---

## 🧭 Mục Lục (Table of Contents)

| # | Endpoint |
|---|---|
| 01 | [Enterprise User Create(#enterprise-user-create) |
| 02 | [Enterprise User Update(#enterprise-user-update) |
| 03 | [Enterprise User Get by ID(#enterprise-user-get-by-id) |
| 04 | [Enterprise User Delete(#enterprise-user-delete) |
| 05 | [Enterprise User List(#enterprise-user-list) |
| 06 | [Enterprise User Assign Roles(#enterprise-user-assign-roles) |
| 07 | [Enterprise User Set Department/Position(#enterprise-user-set-departmentposition) |
| 08 | [Enterprise User Block(#enterprise-user-block) |
| 09 | [Enterprise User Unblock(#enterprise-user-unblock) |
| 10 | [Enterprise User Change Password (Admin)(#enterprise-user-change-password-admin) |

---

## Overview
This document provides representative request body examples for each operation in the **Enterprise Users** cluster.

---

## Enterprise User Create

**Endpoint:** `POST /sgod-auth/v1/enterprise-users`
**DTO Source:** `ParamCreateEnterpriseUserDto` from `types.ts`
**Actor:** SGOD admin (or tenant admin)

### Sample Request Body
```json
{
  "email": "member@enterprise.test",
  "userName": "member01",
  "fullName": {
    "firstName": "Jane",
    "lastName": "Smith"
  },
  "phone": "0909876543",
  "gender": "female",
  "departmentId": "dept-uuid",
  "positionId": "pos-uuid",
  "roleIds": [
    "role-uuid-1"
  ],
  "userType": "enterprise_user"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | ✅ | User email (unique within tenant) |
| userName | string | ✅ | Username |
| fullName.firstName | string | ✅ | First name |
| fullName.lastName | string | ✅ | Last name |
| phone | string | ✅ | Phone number |
| gender | enum | string | `male` / `female` / `other` |
| departmentId | string | ✅ | Department ID |
| positionId | string | ✅ | Position ID |
| roleIds | string[] | ✅ | Role IDs to assign |
| userType | enum | string | `enterprise_user` |

---

## Enterprise User Update

**Endpoint:** `PATCH /sgod-auth/v1/enterprise-users/{id}`
**DTO Source:** `ParamUpdateEnterpriseUserDto` from `types.ts`
**Actor:** SGOD admin

### Sample Request Body
```json
{
  "fullName": {
    "firstName": "Janet",
    "lastName": "Doe"
  },
  "phone": "0901112222",
  "gender": "female"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| fullName.firstName | string | ❌ | New first name |
| fullName.lastName | string | ❌ | New last name |
| phone | string | ❌ | New phone |
| gender | enum | string | ❌ | New gender |

---

## Enterprise User Get by ID

**Endpoint:** `GET /sgod-auth/v1/enterprise-users/{id}`
**DTO Source:** None
**Actor:** SGOD admin

### Sample Request Body
```json
{}
```

---

## Enterprise User Delete

**Endpoint:** `DELETE /sgod-auth/v1/enterprise-users/{id}`
**DTO Source:** None
**Actor:** SGOD admin

### Sample Request Body
```json
{}
```

---

## Enterprise User List

**Endpoint:** `GET /sgod-auth/v1/enterprise-users?tenantId=...`
**DTO Source:** Query string
**Actor:** SGOD admin

### Sample Request Body
```json
{}
```

---

## Enterprise User Assign Roles

**Endpoint:** `PATCH /sgod-auth/v1/enterprise-users/{id}/roles`
**DTO Source:** `ParamAssignUserRolesDto` from `types.ts`
**Actor:** SGOD admin

### Sample Request Body
```json
{
  "roleIds": [
    "role-uuid-1",
    "role-uuid-2"
  ]
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| roleIds | string[] | ✅ | Full replacement list of role IDs |

---

## Enterprise User Set Department/Position

**Endpoint:** `PATCH /sgod-auth/v1/enterprise-users/{id}/department-position`
**DTO Source:** `ParamSetDeptPositionDto` from `types.ts`
**Actor:** SGOD admin

### Sample Request Body
```json
{
  "departmentId": "new-dept-uuid",
  "positionId": "new-pos-uuid"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| departmentId | string | ✅ | New department ID |
| positionId | string | ✅ | New position ID |

---

## Enterprise User Block

**Endpoint:** `POST /sgod-auth/v1/enterprise-users/{id}/block`
**DTO Source:** None (optional reason in query/body)
**Actor:** SGOD admin

### Sample Request Body
```json
{
  "reason": "Violation of policy"
}
```

---

## Enterprise User Unblock

**Endpoint:** `POST /sgod-auth/v1/enterprise-users/{id}/unblock`
**DTO Source:** None
**Actor:** SGOD admin

### Sample Request Body
```json
{}
```

---

## Enterprise User Change Password (Admin)

**Endpoint:** `POST /sgod-auth/v1/enterprise-users/{id}/password`
**DTO Source:** `ParamAdminChangePasswordDto` from `types.ts`
**Actor:** SGOD admin

### Sample Request Body
```json
{
  "newPassword": "NewP@ssw0rd!"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| newPassword | string | ✅ | New password (must meet policy) |