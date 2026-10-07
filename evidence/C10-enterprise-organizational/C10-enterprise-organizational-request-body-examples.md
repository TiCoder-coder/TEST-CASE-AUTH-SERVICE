# C10 — SGOD Enterprises / Organizational — Request Body Examples

<div align="center">

![Cluster](https://img.shields.io/badge/C10-Tenant+Management-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Evidence Type](https://img.shields.io/badge/Evidence-Request+Body+Examples-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)

</div>

- [Error Responses](./C10-enterprise-organizational-error-responses.md)
- [Success Responses](./C10-enterprise-organizational-success-responses.md)

---

## 🧭 Mục Lục (Table of Contents)

| # | Endpoint |
|---|---|
| 01 | [1. List SGOD Enterprises(#1-list-sgod-enterprises) |
| 02 | [2. Statistics Overview(#2-statistics-overview) |
| 03 | [3. Assign Enterprises to User(#3-assign-enterprises-to-user) |
| 04 | [4. Unassign Enterprise from User(#4-unassign-enterprise-from-user) |
| 05 | [5. Set Assigned Enterprises (Replace All)(#5-set-assigned-enterprises-replace-all) |
| 06 | [6. List Deleted Enterprises(#6-list-deleted-enterprises) |
| 07 | [7. Get Enterprise by ID(#7-get-enterprise-by-id) |
| 08 | [8. Block Enterprise(#8-block-enterprise) |
| 09 | [9. Unblock Enterprise(#9-unblock-enterprise) |
| 10 | [10. Restore Deleted Enterprise(#10-restore-deleted-enterprise) |
| 11 | [11. Update Enterprise Subscription(#11-update-enterprise-subscription) |
| 12 | [12. Update Enterprise Features(#12-update-enterprise-features) |
| 13 | [13. Get Enterprise Statistics by ID(#13-get-enterprise-statistics-by-id) |
| 14 | [14. Assign Organizational (Department / Position / Boss)(#14-assign-organizational-department--position--boss) |
| 15 | [15. Remove User from Organizational Position(#15-remove-user-from-organizational-position) |
| 16 | [16. Get Available Bosses(#16-get-available-bosses) |
| 17 | [17. Set Boss(#17-set-boss) |
| 18 | [18. Check Subordinate(#18-check-subordinate) |
| 19 | [19. Audit Organizational Reporting Lines(#19-audit-organizational-reporting-lines) |
| 20 | [Summary of Removed/Incorrect Endpoints (from previous evidence)(#summary-of-removedincorrect-endpoints-from-previous-evidence) |
| 21 | [Summary of DTO Corrections(#summary-of-dto-corrections) |
| 22 | [Summary of Body Corrections(#summary-of-body-corrections) |

---

## Overview
This document provides representative request body examples for **19 endpoints** in the C10 cluster, covering SGOD-side tenant management and organizational hierarchy operations.

**Source of Truth:** Screenshots `Screenshot_2026-10-06_at_23.39.11` through `23.42.02`.
**FE Service:** `apps/sgod-sam-v2/src/services/auth/auth-sgod-enterprise.service.ts` + `auth-users-organizational.service.ts`
**DTO Source:** `apps/sgod-sam-v2/src/services/types.ts`

---

## 1. List SGOD Enterprises

**Endpoint:** `GET /sgod-auth/v1/sgod/enterprises`
**DTO Source:** `ParamGetSgodEnterprises` (query string only)
**Actor:** SGOD_ADMIN

### Sample Request Body
```json
{}
```

### Query Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| page | integer | optional | Page number (default 1) |
| cursor | string | optional | Cursor for keyset pagination |
| limit | integer | optional | Items per page |
| search | string | optional | Full-text search |
| departmentId | uuid | optional | Filter by department |
| positionId | uuid | optional | Filter by position |
| roleId | uuid | optional | Filter by role |
| status | enum | optional | Tenant status filter |

---

## 2. Statistics Overview

**Endpoint:** `GET /sgod-auth/v1/sgod/enterprises/statistics/overview`
**DTO Source:** None
**Actor:** SGOD_ADMIN

### Sample Request Body
```json
{}
```

### Response Schema (Success — 200)
```json
{
  "success": true,
  "code": 200,
  "data": {
    "totalEnterprises": 42,
    "totalActive": 30,
    "totalPending": 8,
    "totalVerified": 28,
    "totalBlocked": 4
  }
}
```

---

## 3. Assign Enterprises to User

**Endpoint:** `POST /sgod-auth/v1/sgod/enterprises/assign`
**DTO Source:** `ParamAssignSgodEnterprises` from `types.ts`
**Actor:** SGOD_ADMIN

### Sample Request Body
```json
{
  "userId": "{{userId}}",
  "tenantIds": [
    "{{tenantIdB}}"
  ]
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| userId | uuid | required | User to assign tenants to |
| tenantIds | uuid[] | required | Tenant IDs to add to user's assignment |

---

## 4. Unassign Enterprise from User

**Endpoint:** `POST /sgod-auth/v1/sgod/enterprises/unassign`
**DTO Source:** `ParamUnassignSgodEnterprise` from `types.ts`
**Actor:** SGOD_ADMIN

### Sample Request Body
```json
{
  "userId": "{{userId}}",
  "tenantId": "{{tenantIdB}}"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| userId | uuid | required | User to unassign tenant from |
| tenantId | uuid | required | Single tenant ID to remove |

---

## 5. Set Assigned Enterprises (Replace All)

**Endpoint:** `POST /sgod-auth/v1/sgod/enterprises/set-assigned`
**DTO Source:** `ParamSetAssignedSgodEnterprises` from `types.ts`
**Actor:** SGOD_ADMIN

### Sample Request Body
```json
{
  "userId": "{{userId}}",
  "tenantIds": [
    "{{tenantIdA}}",
    "{{tenantIdC}}"
  ]
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| userId | uuid | required | Target user |
| tenantIds | uuid[] | required | **Complete replacement set** — existing tenants not in this list are removed |

---

## 6. List Deleted Enterprises

**Endpoint:** `GET /sgod-auth/v1/sgod/enterprises/deleted`
**DTO Source:** `ParamGetSgodEnterprises` (query string only)
**Actor:** SGOD_ADMIN

### Sample Request Body
```json
{}
```

---

## 7. Get Enterprise by ID

**Endpoint:** `GET /sgod-auth/v1/sgod/enterprises/{tenantId}`
**DTO Source:** None
**Actor:** SGOD_ADMIN

### Sample Request Body
```json
{}
```

---

## 8. Block Enterprise

**Endpoint:** `POST /sgod-auth/v1/sgod/enterprises/{tenantId}/block`
**DTO Source:** `ParamBlockSgodEnterprise` from `types.ts` (reason is optional in DTO, but Swagger shows as REQUIRED for compliance audit)
**Actor:** SGOD_ADMIN

### Sample Request Body
```json
{
  "reason": "Policy violation - manual review"
}
```

### Field Descriptions
| Field | Type | Required (Swagger) | Required (DTO) | Description |
|-------|------|--------------------|--------------|-------------|
| reason | string | REQUIRED | optional | Reason for blocking tenant |

---

## 9. Unblock Enterprise

**Endpoint:** `POST /sgod-auth/v1/sgod/enterprises/{tenantId}/unblock`
**DTO Source:** `ParamUnblockSgodEnterprise` from `types.ts` (reason is optional in DTO, but Swagger shows as REQUIRED for compliance audit)
**Actor:** SGOD_ADMIN

### Sample Request Body
```json
{
  "reason": "Audit complete - unblock"
}
```

---

## 10. Restore Deleted Enterprise

**Endpoint:** `POST /sgod-auth/v1/sgod/enterprises/{tenantId}/restore`
**DTO Source:** None (no body)
**Actor:** SGOD_ADMIN

### Sample Request Body
```json
{}
```

---

## 11. Update Enterprise Subscription

**Endpoint:** `PATCH /sgod-auth/v1/sgod/enterprises/{tenantId}/subscription`
**DTO Source:** `ParamUpdateSgodEnterpriseSubscription` from `types.ts`
**Actor:** SGOD_ADMIN

### Sample Request Body
```json
{
  "durationDays": 365
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| durationDays | integer | required | Number of days to extend subscription |

---

## 12. Update Enterprise Features

**Endpoint:** `PATCH /sgod-auth/v1/sgod/enterprises/{tenantId}/features`
**DTO Source:** `ParamUpdateSgodEnterpriseFeatures` from `types.ts`
**Actor:** SGOD_ADMIN

### Sample Request Body
```json
{
  "features": [
    "audit_logging",
    "sso",
    "mfa_required"
  ]
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| features | string[] | required | Feature keys to enable (replace full set) |

---

## 13. Get Enterprise Statistics by ID

**Endpoint:** `GET /sgod-auth/v1/sgod/enterprises/{tenantId}/statistics`
**DTO Source:** None
**Actor:** SGOD_ADMIN

### Sample Request Body
```json
{}
```

---

## 14. Assign Organizational (Department / Position / Boss)

**Endpoint:** `POST /sgod-auth/v1/users/{userId}/organizational/assign`
**DTO Source:** `ParamAssignUserOrganizational` (GAP: not yet defined in types.ts)
**Actor:** ENT_USER_ADMIN

### Sample Request Body
```json
{
  "departmentId": "{{deptId}}",
  "positionId": "{{posId}}",
  "primaryRoleId": "{{primaryRoleId}}",
  "bossId": "{{bossId}}",
  "userType": "EnterpriseUser"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| departmentId | uuid | required | Department to assign user to |
| positionId | uuid | required | Position within department |
| primaryRoleId | uuid | optional | Primary role binding |
| bossId | uuid | optional | Reporting manager user ID |
| userType | enum | required | `EnterpriseUser` / `SubEnterpriseUser` / `SgodUser` / `SgodAdmin` (PascalCase per Swagger) |

### GAP-07 Note
`useAuthUserOrganizational` hook currently only wraps `removeUserOrganizational` and `checkSubordinate`. The `assign` method is **NOT** yet implemented in service/hook.

---

## 15. Remove User from Organizational Position

**Endpoint:** `POST /sgod-auth/v1/users/{userId}/organizational/remove?userType=enterprise_user`
**DTO Source:** `ParamRemoveUserOrganizational` from `types.ts`
**Actor:** ENT_USER_ADMIN

### Query Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| userType | enum | **REQUIRED** | `EnterpriseUser` / `SubEnterpriseUser` / `SgodUser` / `SgodAdmin` |

### Sample Request Body
```json
{}
```

---

## 16. Get Available Bosses

**Endpoint:** `GET /sgod-auth/v1/users/{userId}/organizational/bosses/available?userType=enterprise_user`
**DTO Source:** None
**Actor:** ENT_USER_ADMIN

### Query Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| userType | enum | **REQUIRED** | `EnterpriseUser` / `SubEnterpriseUser` / `SgodUser` / `SgodAdmin` |

### Sample Request Body
```json
{}
```

### Response Schema
```json
{
  "success": true,
  "code": 200,
  "data": {
    "bosses": [
      {
        "id": "user-uuid",
        "fullName": {
          "firstName": "John",
          "lastName": "Doe"
        },
        "positionId": "...",
        "departmentId": "..."
      }
    ]
  }
}
```

### GAP-07 Note
`getAvailableBosses` method is **NOT** yet implemented in `useAuthUserOrganizational`.

---

## 17. Set Boss

**Endpoint:** `POST /sgod-auth/v1/users/{userId}/organizational/bosses/set`
**DTO Source:** `ISetBossRequest` from `types.ts`
**Actor:** ENT_USER_ADMIN

### Sample Request Body
```json
{
  "bossId": "{{bossId}}",
  "userType": "EnterpriseUser"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| bossId | uuid | required | Boss user ID |
| userType | enum | required | `EnterpriseUser` / `SubEnterpriseUser` / `SgodUser` / `SgodAdmin` (PascalCase per Swagger) |

### GAP-07 Note
`setBoss` method is **NOT** yet implemented in `useAuthUserOrganizational`.

---

## 18. Check Subordinate

**Endpoint:** `GET /sgod-auth/v1/users/{userId}/organizational/check-subordinate?subordinateId={subordinateId}`
**DTO Source:** `ParamCheckSubordinate` from `types.ts`
**Actor:** ENT_USER_ADMIN

### Query Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| subordinateId | uuid | **REQUIRED** | User ID to check if subordinate to {userId} |

### Sample Request Body
```json
{}
```

### Response Schema
```json
{
  "success": true,
  "code": 200,
  "data": {
    "isSubordinate": true,
    "message": "User is a direct subordinate"
  }
}
```

---

## 19. Audit Organizational Reporting Lines

**Endpoint:** `GET /sgod-auth/v1/organizations/audit`
**DTO Source:** None
**Actor:** SGOD_ADMIN

### Query Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tenantId | uuid | optional | Filter audit by specific tenant |

### Sample Request Body
```json
{}
```

### GAP-07 Note
`auditOrganization` method is **NOT** yet implemented in `useAuthUserOrganizational`.

---

## Summary of Removed/Incorrect Endpoints (from previous evidence)

The following endpoints appeared in the old evidence but are **NOT** in the current Swagger:
- ❌ `POST /users/{id}/organizational/bosses/add` (not in Swagger ảnh 14-19)
- ❌ `GET /users/{id}/organizational/bosses` (not in Swagger)
- ❌ `GET /users/{id}/organizational/subordinates` (not in Swagger)

## Summary of DTO Corrections

The following DTO names in old evidence were incorrect and have been corrected:
- ❌ `ParamBlockTenantDto` → ✅ `ParamBlockSgodEnterprise`
- ❌ `ParamUpdateSubscriptionDto` → ✅ `ParamUpdateSgodEnterpriseSubscription`
- ❌ `ParamSetFeaturesDto` → ✅ `ParamUpdateSgodEnterpriseFeatures`
- ❌ `ParamSetUserBossesDto` → ✅ `ISetBossRequest` (interface) / `ParamAssignUserOrganizational` (for assign)

## Summary of Body Corrections

- ❌ Subscription old body had `{"durationDays":365,"plan":"premium"}` (extra `plan` field) → ✅ `{"durationDays":365}`
- ❌ Bosses set body had `"userType":"enterprise_user"` (lowercase) → ✅ `"userType":"EnterpriseUser"` (PascalCase per Swagger enum)