# SGOD Auth Service — Authorization Matrix

> **Plan reference**: `docs/plan_to_process_FE/auth/plan_write_test_case/2026-10-06-plan-positive-test-cases-auth-service.md`
> **Guide reference**: `docs/testing/auth-service/specifications/authorization_matrix.md`
> **Last updated**: 2026-10-07
> **Scope**: 5 principal types × 11 clusters — permissions, tenant isolation, step-up rules

<div align="center">

![Principal Types](https://img.shields.io/badge/Principal_Types-5-0b0f19?style=for-the-badge&logo=users&logoColor=FFD43B&labelColor=0b0f19&color=FF6C37)
![Tenant Rules](https://img.shields.io/badge/Tenant_Isolation-6_Rules-0b0f19?style=for-the-badge&logo=building&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)
![Step-Up](https://img.shields.io/badge/Step--Up--TTL-300s-0b0f19?style=for-the-badge&logo=shield&logoColor=FF728F&labelColor=0b0f19&color=55E6AA)

</div>

---

## 🧭 Mục Lục (Table of Contents)

| # | Mục | Mô tả |
|---|---|---|
| [01](#01-actor--permission-mapping) | **Actor → Permission** | 5 actor tiers |
| [02](#02-authorization-by-endpoint-cluster) | **Authorization by Cluster** | 11 clusters |
| [03](#03-tenant-isolation-rules) | **Tenant Isolation** | R01–R06 |
| [04](#04-step-up-requirements) | **Step-Up Requirements** | Sensitive actions |
| [05](#05-profile-alias-authorization) | **Profile Alias** | my-profile / me / profile |
| [06](#06-roledepartmentposition-ceiling-rules) | **Ceiling Rules** | Role/Dept/Pos |
| [07](#07-boss-assignment-rules) | **Boss Assignment** | B01–B05 |
| [08](#08-test-cases-coverage) | **Test Cases Coverage** | Summary |

---

## 01. Actor → Permission Mapping

### 1.1 SGOD Admin Tier (ROOT_ADMIN / SGOD_ADMIN_A / SGOD_ADMIN_B)

| Permission | ROOT_ADMIN | SGOD_ADMIN_A | SGOD_ADMIN_B |
|---|:---:|:---:|:---:|
| **Manage all tenants** | ✅ | ❌ | ❌ |
| **Manage tenant A** | ❌ | ✅ | ❌ |
| **Manage tenant B** | ❌ | ❌ | ✅ |
| **Create SGOD users** | ✅ | ❌ | ❌ |
| **Create SGOD admins** | ✅ | ❌ | ❌ |
| **Hard delete SGOD users** | ✅ | ❌ | ❌ |
| **Hard delete SGOD admins** | ✅ | ❌ | ❌ |
| **Manage enterprise subscription** | ✅ | ❌ | ❌ |
| **Assign enterprises to users** | ✅ | ❌ | ❌ |
| **View audit logs** | ✅ | ✅ | ✅ |
| **Manage all roles** | ✅ | ❌ | ❌ |
| **Manage department/position** | ✅ | ❌ | ❌ |
| **Tenant management (C10)** | ✅ | ❌ | ❌ |
| **Permanent delete** | ✅ | ❌ | ❌ |

**Notes:**

- `ROOT_ADMIN` có quyền global, dùng để setup test fixtures
- `SGOD_ADMIN_A` chỉ quản lý Tenant A
- `SGOD_ADMIN_B` chỉ quản lý Tenant B
- SGOD Admin tier dùng **cookie session** (không có JSON token)

### 1.2 Enterprise Admin (ENTERPRISE_A / ENTERPRISE_B)

| Permission | ENTERPRISE_A | ENTERPRISE_B |
|---|:---:|:---:|
| **Manage own tenant users** | ✅ | ✅ |
| **Manage own tenant roles** | ✅ | ✅ |
| **Manage own tenant depts/positions** | ✅ | ✅ |
| **View own tenant audit** | ✅ | ✅ |
| **Manage other tenant** | ❌ | ❌ |
| **Manage SGOD users** | ❌ | ❌ |
| **Manage subscription** | ❌ | ❌ |
| **Manage SGOD admins** | ❌ | ❌ |
| **Hard delete users** | ❌ | ❌ |

**Notes:**

- Enterprise Admin dùng JSON token (`accessToken` + `refreshToken`)
- Có quyền trên parent tenant và tất cả sub-enterprises thuộc tenant đó

### 1.3 Enterprise User (ENT_USER_A / ENT_USER_B / ENT_USER_BLOCKED / ENT_USER_DELETED)

| Permission | ACTIVE | BLOCKED | DELETED |
|---|:---:|:---:|:---:|
| **Login** | ✅ | ✅ (returns Blocked state) | ❌ |
| **Self profile** | ✅ | ✅ | ❌ |
| **Own roles assignment (read)** | ✅ | ✅ | ❌ |
| **Mutation trong tenant** | ✅ | ❌ | ❌ |
| **Tenant isolation** | ✅ | ❌ | ❌ |
| **Restore deleted** | ❌ | ❌ | ✅ (after restore) |

### 1.4 Sub-Enterprise (SUBENT_A / SUBENT_B)

| Permission | Status |
|---|---|
| **Login** | ✅ |
| **Manage sub-enterprise users** | ✅ (trong sub-tenant scope) |
| **Manage parent tenant** | ❌ |
| **Manage other sub-tenant** | ❌ |
| **Roles/depts/positions** | ✅ (sub-tenant scoped) |

### 1.5 MFA_TARGET / PASSWORD_TARGET / ACTIVATION_TARGET

| Actor | Purpose | Special |
|---|---|---|
| **MFA_TARGET** | MFA enable/verify/disable flow | MFA secret stored in `mfa_secret_key` env |
| **PASSWORD_TARGET** | Password change/forgot/reset | No MFA |
| **ACTIVATION_TARGET** | Account activation flow | Account pending |

---

## 02. Authorization by Endpoint Cluster

### 2.1 C01 — Core Auth (28 endpoints)

| Endpoint | Auth Required | Notes |
|---|---|---|
| `POST /{type}/sessions` | API Key + Device | Public login |
| `POST /sessions/refresh` | Bearer / Cookie | Refresh token |
| `POST /sessions/current` | Bearer / Cookie | Logout current device |
| `DELETE /sessions` | Bearer / Cookie | Logout all |
| `GET /session/context` | Bearer / Cookie | Identity + claims |
| `POST /mfa/enable` | Bearer | Returns secret |
| `POST /mfa/verify` | Interim Token | MFA challenge |
| `POST /passwords/*` | None / Bearer | Public reset / User change |
| `POST /activate-account` | Interim Token | Activation flow |

### 2.2 C02 — Enterprise / Permission / Email (12 endpoints)

| Endpoint | Auth Required | Permission |
|---|---|---|
| `POST /enterprises/register` | API Key | Public |
| `GET /enterprises/profile` | Bearer | ReadOwnTenant |
| `GET /permissions` | Bearer | ReadPermission |
| `POST /emails/*` | Bearer | ManageEmail |
| `POST /emails/verifications/code` | Bearer | EmailVerification |

### 2.3 C03 — Roles (15 endpoints)

| Endpoint | Auth Required | Permission |
|---|---|---|
| `POST /roles` | Bearer | CreateRole |
| `GET /roles` | Bearer | ReadRole |
| `GET /roles/tree` | Bearer | ReadRole |
| `GET /roles/{id}` | Bearer | ReadRole |
| `PATCH /roles/{id}` | Bearer | UpdateRole |
| `DELETE /roles/{id}` | Bearer | DeleteRole |
| `POST /roles/{id}/restore` | Bearer | DeleteRole |
| `PATCH /roles/{id}/move` | Bearer | UpdateRole |
| `GET /roles/{id}/users` | Bearer | ReadRole |
| `GET /roles/{id}/available-parents` | Bearer | ReadRole |

### 2.4 C04 — Departments (12 endpoints)

| Endpoint | Auth Required | Permission |
|---|---|---|
| `POST /departments` | Bearer | CreateDepartment |
| `GET /departments` | Bearer | ReadDepartment |
| `GET /departments/tree` | Bearer | ReadDepartment |
| `GET /departments/statistics` | Bearer | ReadDepartment |
| `GET /departments/deleted` | Bearer | ReadDepartment |
| `GET /departments/{id}` | Bearer | ReadDepartment |
| `PATCH /departments/{id}` | Bearer | UpdateDepartment |
| `DELETE /departments/{id}` | Bearer | DeleteDepartment |
| `POST /departments/{id}/restore` | Bearer | DeleteDepartment |
| `GET /departments/{departmentId}/users` | Bearer | ReadDepartment |
| `GET /departments/{departmentId}/statistics` | Bearer | ReadDepartment |
| `POST /departments/{departmentId}/move` | Bearer | UpdateDepartment |

### 2.5 C05 — Positions (12 endpoints)

| Endpoint | Auth Required | Permission |
|---|---|---|
| `POST /positions` | Bearer | CreatePosition |
| `GET /positions` | Bearer | ReadPosition |
| `GET /positions/tree` | Bearer | ReadPosition |
| `GET /positions/statistics` | Bearer | ReadPosition |
| `GET /positions/available` | Bearer | ReadPosition |
| `GET /positions/deleted` | Bearer | ReadPosition |
| `GET /positions/{id}` | Bearer | ReadPosition |
| `PATCH /positions/{id}` | Bearer | UpdatePosition |
| `DELETE /positions/{id}` | Bearer | DeletePosition |
| `POST /positions/{id}/restore` | Bearer | DeletePosition |
| `GET /positions/{positionId}/users` | Bearer | ReadPosition |
| `POST /positions/preview-change` | Bearer | ReadPosition |

### 2.6 C06/C07/C08 — User/Admin Principal (56 endpoints)

| Endpoint Pattern | Auth Required | Step-up |
|---|---|---|
| `POST /enterprise-users` | Bearer | No |
| `POST /sgod-users` | Bearer + SGOD Admin | No |
| `POST /sgod/admins` | Bearer + SGOD Admin | No |
| `POST /sub-enterprises` | Bearer | No |
| `POST /{type}/{id}/block` | Bearer | **Yes** (C06/C08/C09) |
| `POST /{type}/{id}/unblock` | Bearer | No |
| `DELETE /{type}/{id}/permanent` | Bearer + Root | No (chỉ cần ROOT_ADMIN) |
| `POST /{type}/{id}/revoke-wallet-key` | Bearer + SGOD Staff | No |
| Profile aliases | Bearer | No |

**Pattern types:**

- `{type}` = `enterprise-users` | `sgod-users` | `sub-enterprises` | `sgod/admins`

### 2.7 C09 — Sub-Enterprises (17 endpoints)

| Endpoint | Auth Required | Notes |
|---|---|---|
| `POST /sub-enterprises` | Bearer | Enterprise Admin |
| `GET /sub-enterprises` | Bearer | — |
| `GET /sub-enterprises/statistics` | Bearer | — |
| `GET /sub-enterprises/deleted` | Bearer | — |
| `GET /sub-enterprises/{userId}` | Bearer | Tenant isolation |
| `PATCH /sub-enterprises/{userId}` | Bearer | — |
| `DELETE /sub-enterprises/{userId}` | Bearer | — |
| `PATCH /sub-enterprises/my-profile` | Bearer | Self |
| `PATCH /sub-enterprises/me` | Bearer | Self |
| `PATCH /sub-enterprises/profile` | Bearer | Self |
| `POST /sub-enterprises/{userId}/restore` | Bearer | — |
| `POST /sub-enterprises/{userId}/block` | Bearer + Step-up | — |
| `POST /sub-enterprises/{userId}/unblock` | Bearer | — |
| `POST /sub-enterprises/{userId}/roles` | Bearer | — |
| `POST /sub-enterprises/{userId}/organizational` | Bearer | — |
| `GET /sub-enterprises/{userId}/bosses` | Bearer | — |
| `PATCH /sub-enterprises/{userId}/boss` | Bearer | — |

### 2.8 C10 — Organizational / Enterprise Management (19 endpoints)

| Endpoint | Auth Required | Notes |
|---|---|---|
| `POST /sgod/enterprises/assign` | Bearer + SGOD Staff | No step-up |
| `POST /sgod/enterprises/unassign` | Bearer + SGOD Staff | No step-up |
| `POST /sgod/enterprises/set-assigned` | Bearer + SGOD Staff | No step-up |
| `GET /sgod/enterprises` | Bearer + SGOD Staff | — |
| `GET /sgod/enterprises/statistics/overview` | Bearer + SGOD Staff | — |
| `GET /sgod/enterprises/deleted` | Bearer + SGOD Staff | — |
| `GET /sgod/enterprises/{tenantId}` | Bearer | — |
| `POST /sgod/enterprises/{tenantId}/block` | Bearer + SGOD Staff | **Step-up** |
| `POST /sgod/enterprises/{tenantId}/unblock` | Bearer | No step-up |
| `POST /sgod/enterprises/{tenantId}/restore` | Bearer + SGOD Staff | — |
| `PATCH /sgod/enterprises/{tenantId}/subscription` | Bearer + SGOD Staff | — |
| `PATCH /sgod/enterprises/{tenantId}/features` | Bearer + SGOD Staff | — |
| `GET /sgod/enterprises/{tenantId}/statistics` | Bearer + SGOD Staff | — |
| `POST /users/{userId}/organizational/assign` | Bearer | No step-up |
| `POST /users/{userId}/organizational/remove` | Bearer | No step-up |
| `GET /users/{userId}/organizational/bosses/available` | Bearer | — |
| `POST /users/{userId}/organizational/bosses/set` | Bearer | — |
| `GET /users/{userId}/organizational/check-subordinate` | Bearer | — |
| `GET /organizations/audit` | Bearer + SGOD Staff | — |

### 2.9 C11 — Audit / Crypto (5 endpoints)

| Endpoint | Auth Required | Notes |
|---|---|---|
| `GET /sgod/audit-logs` | Bearer + SGOD Staff | — |
| `POST /test-crypto/encrypt-string-helper` | Bearer | PoC, DEV |
| `POST /test-crypto/decrypt-string-helper` | Bearer | PoC, DEV |
| `POST /test-crypto/encrypt-file-helper` | Bearer | PoC, DEV |
| `POST /test-crypto/decrypt-file-helper` | Bearer | PoC, DEV |

---

## 03. Tenant Isolation Rules

| Rule | Description |
|---|---|
| **R01** | Enterprise A không thể đọc/mutate resource của Enterprise B |
| **R02** | SGOD Admin chỉ quản lý tenants được phân quyền (SGOD_ADMIN_A → Tenant A only) |
| **R03** | Role/Department/Position chỉ thuộc 1 tenant (single-tenant scoping) |
| **R04** | Cross-tenant reference trong mutation phải bị reject (e.g., assign role của tenant A cho user của tenant B) |
| **R05** | `/roles/tenant/{tenantId}` chỉ SGOD Admin được gọi (cross-tenant listing) |
| **R06** | Sub-Enterprise chỉ thấy resource của parent Enterprise |

**Test cases cần verify R01:**

- ENTERPRISE_A login → không GET được user của ENTERPRISE_B
- ENTERPRISE_A PATCH user của ENTERPRISE_B → 403/404
- ENTERPRISE_A không assign role của mình cho user của ENTERPRISE_B

**Test cases cần verify R02:**

- SGOD_ADMIN_A không thấy Tenant B trong `/sgod/enterprises`
- SGOD_ADMIN_A không block được Tenant B

---

## 04. Step-Up Requirements

| Action | Requires Step-up | Cluster |
|---|:---:|---|
| **Block user** | ✅ Yes | C06, C08, C09 |
| **Initiate password reset (admin)** | ✅ Yes | C01 |
| **Unblock user** | ❌ No | C06, C08, C09 |
| **Create user** | ❌ No | C06, C07, C08, C09 |
| **Update profile** | ❌ No | All |
| **Assign roles** | ❌ No | C06, C07, C08, C09 |
| **Block enterprise** | ✅ Yes | C10 |
| **Unblock enterprise** | ❌ No | C10 |
| **Restore deleted** | ❌ No | All |
| **Permanent delete** | ❌ No (cần ROOT_ADMIN) | C07, C08 |

**Step-up flow:**

1. POST `/iam/step-up` với `twoFactorCode` mới
2. Nhận `verified: true` + `ttlSeconds: 300`
3. Trong TTL, có thể thực hiện mutation cần step-up
4. Sau TTL, phải step-up lại

**Test rules:**

- Mutation cần step-up mà không có grant → 403
- Step-up với TOTP sai → 401
- Step-up grant chỉ valid trong TTL

---

## 05. Profile Alias Authorization

`/my-profile`, `/me`, `/profile` aliases cho phép user update chính mình mà không cần biết userId:

| Alias | Authorization | Persistence |
|---|---|---|
| `PATCH /enterprise-users/my-profile` | Caller = principal | Same as `/{id}` |
| `PATCH /enterprise-users/me` | Caller = principal | Same as `/{id}` |
| `PATCH /enterprise-users/profile` | Caller = principal | Same as `/{id}` |
| `PATCH /sgod-users/my-profile` | Caller = principal | Same as `/{id}` |
| `PATCH /sgod-users/me` | Caller = principal | Same as `/{id}` |
| `PATCH /sgod-users/profile` | Caller = principal | Same as `/{id}` |
| `PATCH /sgod/admins/my-profile` | Caller = principal | Same as `/{id}` |
| `PATCH /sgod/admins/me` | Caller = principal | Same as `/{id}` |
| `PATCH /sgod/admins/profile` | Caller = principal | Same as `/{id}` |
| `PATCH /sub-enterprises/my-profile` | Caller = principal | Same as `/{id}` |
| `PATCH /sub-enterprises/me` | Caller = principal | Same as `/{id}` |
| `PATCH /sub-enterprises/profile` | Caller = principal | Same as `/{id}` |

**Test rules:**

- `my-profile`, `me`, `profile` 3 aliases phải có cùng behavior
- Caller KHÔNG thể dùng alias để update user khác (chỉ update chính mình)
- Updates qua alias phải persist giống như update qua `/{id}`

---

## 06. Role/Department/Position Ceiling Rules

| Entity | Ceiling Field | Rule |
|---|---|---|
| **Role** | `source_type` | CUSTOM roles không gán cho actor ngoài creator tenant |
| **Department** | `role_id` | Ceiling theo nhánh role; children inherit ceiling |
| **Position** | `role_id` | Phải bằng `primaryRoleId` của user được assign |

**Test rules:**

- CUSTOM role của Tenant A không assign được cho user của Tenant B
- Department ceiling = max role tier trong nhánh đó
- Position role_id phải khớp với user primaryRoleId khi assign

---

## 07. Boss Assignment Rules

| Rule | Description |
|---|---|
| **B01** | Boss phải thuộc candidate list hợp lệ (available-bosses endpoint) |
| **B02** | Boss phải thuộc position parent chain (không cùng layer) |
| **B03** | Không tự lấy caller id làm boss (caller ≠ boss) |
| **B04** | Vacate position không tự chọn replacement boss |
| **B05** | Boss thuộc cùng department hoặc parent department |

**Test cases:**

- Set boss = candidate from `/available-bosses` → OK
- Set boss = user ngoài `/available-bosses` → 400/403
- Set boss = self → 400
- Set boss for vacant position without specifying → use default OR fail

---

## 08. Test Cases Coverage

| Cluster | Endpoints | Test Cases | Auth-related Special |
|---|---:|---:|---|
| C01 | 28 | 28 | MFA flows, password reset, activation |
| C02 | 12 | 12 | Public register, email verification |
| C03 | 15 | 15 | Role tree, tenant isolation |
| C04 | 12 | 12 | Department tree |
| C05 | 12 | 12 | Position tree, preview change |
| C06 | 19 | 19 | Block step-up, wallet revoke |
| C07 | 18 | 19 | Profile aliases, permanent delete (Root) |
| C08 | 19 | 19 | Step-up, admin tier permissions |
| C09 | 17 | 20 | Boss assignment, organizational |
| C10 | 19 | 19 | Tenant management, block step-up |
| C11 | 5 | 5 | Audit log, crypto PoC |
| **Total** | **176** | **180** | — |