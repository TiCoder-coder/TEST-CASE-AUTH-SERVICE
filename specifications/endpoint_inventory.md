# SGOD Auth Service — Endpoint Inventory

> **Source**: 12 Swagger screenshots provided by sếp.
> **Plan reference**: `docs/plan_to_process_FE/auth/plan_write_test_case/2026-10-06-plan-positive-test-cases-auth-service.md`
> **Guide reference**: `docs/testing/auth-service/specifications/endpoint_inventory.md`
> **Last updated**: 2026-10-07
> **Total**: 177 rows displayed, 176 unique operations (duplicate `GET /sgod-auth/v1/dev/emails` counted once).

<div align="center">

![Swagger](https://img.shields.io/badge/Source-12_Swagger_Screenshots-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Endpoints](https://img.shields.io/badge/Endpoints-176_Unique-0b0f19?style=for-the-badge&logo=openapiinitiative&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)
![Test Cases](https://img.shields.io/badge/Test_Cases-180-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFD43B&labelColor=0b0f19&color=55E6AA)

</div>

---

## 🧭 Mục Lục (Table of Contents)

| # | Mục | Mô tả |
|---|---|---|
| [01](#01-conventions) | **Conventions** | Auth columns · Status · FE mapping |
| [02](#02-c01--core-auth-28-endpoints) | **C01 — Core Auth** | 28 endpoints (Sessions, MFA, Password, Activation) |
| [03](#03-c02--enterprise--permission--email-12-endpoints) | **C02 — Enterprise / Permission / Email** | 12 endpoints |
| [04](#04-c03--roles-15-endpoints) | **C03 — Roles** | 15 endpoints |
| [05](#05-c04--departments-12-endpoints) | **C04 — Departments** | 12 endpoints |
| [06](#06-c05--positions-12-endpoints) | **C05 — Positions** | 12 endpoints |
| [07](#07-c06--enterprise-users-19-endpoints) | **C06 — Enterprise Users** | 19 endpoints |
| [08](#08-c07--sgod-users-18-endpoints) | **C07 — SGOD Users** | 18 endpoints |
| [09](#09-c08--iam-step-up--sgod-admins-19-endpoints) | **C08 — IAM Step-up / SGOD Admins** | 19 endpoints |
| [10](#10-c09--sub-enterprises-17-endpoints) | **C09 — Sub-Enterprises** | 17 endpoints |
| [11](#11-c10--tenant-management-19-endpoints) | **C10 — Tenant Management** | 19 endpoints |
| [12](#12-c11--audit-logs--crypto-poc-5-endpoints) | **C11 — Audit Logs / Crypto PoC** | 5 endpoints |
| [13](#13-summary) | **Summary** | Cluster summary table |
| [14](#14-contract-issues-log) | **Contract Issues Log** | CI-01 → CI-05 |

---

## 01. Conventions

- All endpoints prefixed with `/sgod-auth/v1`
- `{{baseUrlAuth}}` = base URL of auth service (e.g. `https://api.sgod.com`)
- `{{authApiKey}}` = `x-api-key` header value injected per environment
- `{{lang}}` = language header (`vi` | `en`)
- `{{accessToken}}` / `{{refreshToken}}` = JSON token for enterprise/sub-enterprise principals
- `{{cookieJar}}` = cookie jar for SGOD user/admin principals
- `{{deviceId}}` = device identifier per session

### 1.1 Status Codes

- **`CONTRACT_READY`** = status/schema confirmed from implementation
- **`CONTRACT_PENDING`** = contract not yet frozen; assert what BE returns, not what it "should" return

### 1.2 FE Mapping Codes

- **S** = Service/transport seen, runtime path proven (142)
- **T** = Refresh at transport layer only (1)
- **G** = No FE caller found (GAP) (33)

### 1.3 Auth Columns

- **API Key** = `x-api-key` header required
- **Bearer** = `Authorization: Bearer {{accessToken}}` required
- **Cookie** = HttpOnly cookie session required
- **Step-up** = must have valid step-up grant in current session
- **SGOD Staff** = SGOD admin permissions required
- **DEV** = DEV environment only

---

## 02. C01 — Core Auth (28 endpoints)

| # | Method | Endpoint | Auth | Contract | FE |
|---|--------|----------|------|----------|----|
| 1 | GET | `/users/myself/profile-with-assets` | Bearer | CONTRACT_PENDING | G |
| 2 | PATCH | `/users/myself/profile-with-assets` | Bearer | CONTRACT_PENDING | G |
| 3 | POST | `/enterprises/sessions` | API Key + Device | CONTRACT_PENDING | S |
| 4 | POST | `/enterprise-users/sessions` | API Key + Device | CONTRACT_PENDING | S |
| 5 | POST | `/sgod-users/sessions` | API Key + Device + Cookie | CONTRACT_PENDING | S |
| 6 | POST | `/sgod-admins/sessions` | API Key + Device + Cookie | CONTRACT_PENDING | S |
| 7 | POST | `/sub-enterprises/sessions` | API Key + Device | CONTRACT_PENDING | S |
| 8 | POST | `/sessions/refresh` | Bearer / Cookie | CONTRACT_PENDING | T |
| 9 | POST | `/sessions/current` | Bearer / Cookie | CONTRACT_PENDING | S |
| 10 | DELETE | `/sessions/devices/{deviceId}` | Bearer | CONTRACT_PENDING | S |
| 11 | DELETE | `/sessions` | Bearer / Cookie | CONTRACT_PENDING | S |
| 12 | GET | `/session/context` | Bearer / Cookie | CONTRACT_PENDING | S |
| 13 | GET | `/users/myself` | Bearer / Cookie | CONTRACT_PENDING | S |
| 14 | GET | `/sessions/devices` | Bearer | CONTRACT_PENDING | G |
| 15 | POST | `/devices/{deviceId}/trust` | Bearer | CONTRACT_PENDING | G |
| 16 | POST | `/devices/{deviceId}/untrust` | Bearer | CONTRACT_PENDING | G |
| 17 | POST | `/mfa/enable` | Bearer | CONTRACT_PENDING | S |
| 18 | POST | `/mfa/disable` | Bearer | CONTRACT_PENDING | S |
| 19 | POST | `/mfa/unenroll` | Bearer | CONTRACT_PENDING | G |
| 20 | POST | `/mfa/verification` | Bearer | CONTRACT_PENDING | S |
| 21 | POST | `/mfa/verify` | Interim Token | CONTRACT_PENDING | S |
| 22 | POST | `/passwords/change` | Bearer | CONTRACT_PENDING | S |
| 23 | POST | `/passwords/forgot` | None | CONTRACT_PENDING | S |
| 24 | POST | `/passwords/reset` | None | CONTRACT_PENDING | S |
| 25 | POST | `/users/{userId}/actions/initiate-reset-password` | Bearer + Step-up | CONTRACT_PENDING | S |
| 26 | POST | `/users/{userId}/actions/resend-activation` | Bearer | CONTRACT_PENDING | G |
| 27 | POST | `/activate-account` | Interim Token | CONTRACT_PENDING | S |
| 28 | GET | `/dev/emails` | API Key + DEV | CONTRACT_PENDING | G |

**Cluster summary**: 28 endpoints, 28 test cases

**FE mapping notes:**

- `useAuthEnterprise.ts` → C01 LOGIN-002/003 (Enterprise login)
- `useAuthSession.ts` → C01 SESSION (refresh, logout, context)
- `useAuthMfa.ts` → C01 MFA (enable, verify, disable)
- `useLogoutHandler.ts` → C01 SESSION (logout flow)
- `/dev/emails` → DEV only; not used in production

**Evidence**: [`evidence/C01-core-auth/`](../evidence/C01-core-auth/)

---

## 03. C02 — Enterprise / Permission / Email (12 endpoints)

| # | Method | Endpoint | Auth | Contract | FE | Notes |
|---|--------|----------|------|----------|-----|-------|
| 29 | POST | `/enterprises/register` | API Key | CONTRACT_PENDING | S | Public registration |
| 30 | GET | `/enterprises/profile` | Bearer | CONTRACT_PENDING | G | Own tenant |
| 31 | POST | `/enterprises/verifications/resend-otp` | Bearer | CONTRACT_PENDING | S | Resend verification OTP |
| 32 | GET | `/permissions` | Bearer | CONTRACT_PENDING | S | Permission catalog |
| 33 | GET | `/emails/check` | Bearer | CONTRACT_PENDING | G | Check email availability |
| 34 | POST | `/emails/check-exists` | Bearer | CONTRACT_PENDING | G | Email exists check |
| 35 | POST | `/emails/send` | Bearer | CONTRACT_PENDING | G | Send email |
| 36 | POST | `/emails/verifications/code` | Bearer | CONTRACT_PENDING | S | Generate verification code |
| 37 | POST | `/emails/verify` | Bearer | CONTRACT_PENDING | G | Verify code |
| 38 | POST | `/emails/payment-code` | Bearer | CONTRACT_PENDING | G | Payment code request |
| 39 | POST | `/emails/payment-code/verify` | Bearer | CONTRACT_PENDING | G | Payment code verify |
| 40 | GET | `/emails/token` | API Key + DEV | CONTRACT_PENDING | G | DEV only |

> **Note**: `GET /dev/emails` appears in both C01 (row 28) and C02. Primary case belongs to C01; traceability kept in both tags.

**Cluster summary**: 12 endpoints, 12 test cases

**FE mapping notes:**

- `authPermissions.ts` → C02 PERMISSION (catalog)
- `authPermissions.service.ts` → C02 PERMISSION
- `otp.service.ts` / `useOTP.ts` → C02 EMAIL verification

**Evidence**: [`evidence/C02-enterprise-email/`](../evidence/C02-enterprise-email/)

---

## 04. C03 — Roles (15 endpoints)

| # | Method | Endpoint | Auth | Contract | FE |
|---|--------|----------|------|----------|-----|
| 41 | POST | `/roles` | Bearer | CONTRACT_PENDING | S |
| 42 | GET | `/roles` | Bearer | CONTRACT_PENDING | S |
| 43 | GET | `/roles/tree` | Bearer | CONTRACT_PENDING | S |
| 44 | GET | `/roles/tree/{rootRoleId}` | Bearer | CONTRACT_PENDING | S |
| 45 | GET | `/roles/tenant/{tenantId}` | Bearer | CONTRACT_PENDING | S |
| 46 | GET | `/roles/creatable-layers` | Bearer | CONTRACT_PENDING | G |
| 47 | GET | `/roles/statistics` | Bearer | CONTRACT_PENDING | S |
| 48 | GET | `/roles/deleted` | Bearer | CONTRACT_PENDING | S |
| 49 | GET | `/roles/{id}` | Bearer | CONTRACT_PENDING | S |
| 50 | PATCH | `/roles/{id}` | Bearer | CONTRACT_PENDING | S |
| 51 | DELETE | `/roles/{id}` | Bearer | CONTRACT_PENDING | S |
| 52 | POST | `/roles/{id}/restore` | Bearer | CONTRACT_PENDING | S |
| 53 | PATCH | `/roles/{id}/move` | Bearer | CONTRACT_PENDING | S |
| 54 | GET | `/roles/{id}/users` | Bearer | CONTRACT_PENDING | S |
| 55 | GET | `/roles/{id}/available-parents` | Bearer | CONTRACT_PENDING | S |

**Cluster summary**: 15 endpoints, 15 test cases

**FE mapping notes:**

- `auth-role.service.ts` → all C03
- `useAuthRole.ts` → C03 ROLE CRUD + tree
- `useIamStepUpGuard.ts` → C03 role-based guard

**Evidence**: [`evidence/C03-roles/`](../evidence/C03-roles/)

---

## 05. C04 — Departments (12 endpoints)

| # | Method | Endpoint | Auth | Contract | FE |
|---|--------|----------|------|----------|-----|
| 56 | POST | `/departments` | Bearer | CONTRACT_PENDING | S |
| 57 | GET | `/departments` | Bearer | CONTRACT_PENDING | S |
| 58 | GET | `/departments/tree` | Bearer | CONTRACT_PENDING | S |
| 59 | GET | `/departments/statistics` | Bearer | CONTRACT_PENDING | S |
| 60 | GET | `/departments/deleted` | Bearer | CONTRACT_PENDING | S |
| 61 | GET | `/departments/{id}` | Bearer | CONTRACT_PENDING | S |
| 62 | PATCH | `/departments/{id}` | Bearer | CONTRACT_PENDING | S |
| 63 | DELETE | `/departments/{id}` | Bearer | CONTRACT_PENDING | S |
| 64 | POST | `/departments/{id}/restore` | Bearer | CONTRACT_PENDING | S |
| 65 | GET | `/departments/{departmentId}/users` | Bearer | CONTRACT_PENDING | S |
| 66 | GET | `/departments/{departmentId}/statistics` | Bearer | CONTRACT_PENDING | S |
| 67 | POST | `/departments/{departmentId}/move` | Bearer | CONTRACT_PENDING | S |

**Cluster summary**: 12 endpoints, 12 test cases

**FE mapping notes:**

- `auth-departments.service.ts` → all C04
- `authDepartment.ts` → C04 DEPARTMENT CRUD + tree

**Evidence**: [`evidence/C04-departments/`](../evidence/C04-departments/)

---

## 06. C05 — Positions (12 endpoints)

| # | Method | Endpoint | Auth | Contract | FE |
|---|--------|----------|------|----------|-----|
| 68 | POST | `/positions` | Bearer | CONTRACT_PENDING | S |
| 69 | GET | `/positions` | Bearer | CONTRACT_PENDING | S |
| 70 | GET | `/positions/tree` | Bearer | CONTRACT_PENDING | S |
| 71 | GET | `/positions/statistics` | Bearer | CONTRACT_PENDING | S |
| 72 | GET | `/positions/available` | Bearer | CONTRACT_PENDING | S |
| 73 | GET | `/positions/deleted` | Bearer | CONTRACT_PENDING | S |
| 74 | GET | `/positions/{id}` | Bearer | CONTRACT_PENDING | S |
| 75 | PATCH | `/positions/{id}` | Bearer | CONTRACT_PENDING | S |
| 76 | DELETE | `/positions/{id}` | Bearer | CONTRACT_PENDING | S |
| 77 | POST | `/positions/{id}/restore` | Bearer | CONTRACT_PENDING | S |
| 78 | GET | `/positions/{positionId}/users` | Bearer | CONTRACT_PENDING | S |
| 79 | POST | `/positions/preview-change` | Bearer | CONTRACT_PENDING | S |

**Cluster summary**: 12 endpoints, 12 test cases

**FE mapping notes:**

- `auth-positions.service.ts` → all C05
- `authPoisition.ts` → C05 POSITION CRUD + tree + available + preview

**Evidence**: [`evidence/C05-positions/`](../evidence/C05-positions/)

---

## 07. C06 — Enterprise Users (19 endpoints)

| # | Method | Endpoint | Auth | Contract | FE |
|---|--------|----------|------|----------|-----|
| 80 | POST | `/enterprise-users` | Bearer | CONTRACT_PENDING | S |
| 81 | GET | `/enterprise-users` | Bearer | CONTRACT_PENDING | S |
| 82 | GET | `/enterprise-users/statistics` | Bearer | CONTRACT_PENDING | S |
| 83 | GET | `/enterprise-users/deleted` | Bearer | CONTRACT_PENDING | S |
| 84 | GET | `/enterprise-users/{userId}` | Bearer | CONTRACT_PENDING | S |
| 85 | PATCH | `/enterprise-users/{userId}` | Bearer | CONTRACT_PENDING | S |
| 86 | DELETE | `/enterprise-users/{userId}` | Bearer | CONTRACT_PENDING | S |
| 87 | POST | `/enterprise-users/{userId}/restore` | Bearer | CONTRACT_PENDING | S |
| 88 | PATCH | `/enterprise-users/my-profile` | Bearer | CONTRACT_PENDING | S |
| 89 | PATCH | `/enterprise-users/profile` | Bearer | CONTRACT_PENDING | S |
| 90 | PATCH | `/enterprise-users/me` | Bearer | CONTRACT_PENDING | S |
| 91 | POST | `/enterprise-users/{userId}/block` | Bearer + Step-up | CONTRACT_PENDING | S |
| 92 | POST | `/enterprise-users/{userId}/unblock` | Bearer | CONTRACT_PENDING | S |
| 93 | PATCH | `/enterprise-users/{userId}/roles` | Bearer | CONTRACT_PENDING | S |
| 94 | PATCH | `/enterprise-users/{userId}/department-position` | Bearer | CONTRACT_PENDING | S |
| 95 | GET | `/enterprise-users/{userId}/available-bosses` | Bearer | CONTRACT_PENDING | S |
| 96 | PATCH | `/enterprise-users/{userId}/boss` | Bearer | CONTRACT_PENDING | S |
| 97 | DELETE | `/enterprise-users/{userId}/position` | Bearer | CONTRACT_PENDING | S |
| 98 | POST | `/enterprise-users/{userId}/revoke-wallet-key` | Bearer + SGOD Staff | CONTRACT_PENDING | S |

**Cluster summary**: 19 endpoints, 19 test cases

**FE mapping notes:**

- `auth-enterprise-user.service.ts` → all C06
- `useAuthEnterpriseUser.ts` → C06 ENTERPRISE-USER lifecycle

**Evidence**: [`evidence/C06-enterprise-users/`](../evidence/C06-enterprise-users/)

---

## 08. C07 — SGOD Users (18 endpoints)

| # | Method | Endpoint | Auth | Contract | FE |
|---|--------|----------|------|----------|-----|
| 99 | POST | `/sgod-users` | Bearer + SGOD Admin | CONTRACT_PENDING | S |
| 100 | GET | `/sgod-users` | Bearer | CONTRACT_PENDING | S |
| 101 | GET | `/sgod-users/deleted` | Bearer | CONTRACT_PENDING | S |
| 102 | PATCH | `/sgod-users/my-profile` | Bearer | CONTRACT_PENDING | S |
| 103 | PATCH | `/sgod-users/profile` | Bearer | CONTRACT_PENDING | S |
| 104 | PATCH | `/sgod-users/me` | Bearer | CONTRACT_PENDING | S |
| 105 | GET | `/sgod-users/statistics` | Bearer | CONTRACT_PENDING | S |
| 106 | GET | `/sgod-users/{userId}` | Bearer | CONTRACT_PENDING | S |
| 107 | PATCH | `/sgod-users/{userId}` | Bearer | CONTRACT_PENDING | S |
| 108 | DELETE | `/sgod-users/{userId}` | Bearer | CONTRACT_PENDING | S |
| 109 | POST | `/sgod-users/{userId}/restore` | Bearer | CONTRACT_PENDING | S |
| 110 | DELETE | `/sgod-users/{userId}/permanent` | Bearer + Root | CONTRACT_PENDING | G |
| 111 | POST | `/sgod-users/{userId}/block` | Bearer + Step-up | CONTRACT_PENDING | S |
| 112 | POST | `/sgod-users/{userId}/unblock` | Bearer | CONTRACT_PENDING | S |
| 113 | PATCH | `/sgod-users/{userId}/roles` | Bearer | CONTRACT_PENDING | S |
| 114 | PATCH | `/sgod-users/{userId}/department-position` | Bearer | CONTRACT_PENDING | S |
| 115 | GET | `/sgod-users/{userId}/available-bosses` | Bearer | CONTRACT_PENDING | S |
| 116 | PATCH | `/sgod-users/{userId}/boss` | Bearer | CONTRACT_PENDING | S |

**Cluster summary**: 18 endpoints, 19 test cases (extra test for profile aliases)

**FE mapping notes:**

- `auth-sgod-users.service.ts` → all C07
- `useAuthSgodUser.ts` → C07 SGOD-USER lifecycle

**Evidence**: [`evidence/C07-sgod-users/`](../evidence/C07-sgod-users/)

---

## 09. C08 — IAM Step-up / SGOD Admins (19 endpoints)

| # | Method | Endpoint | Auth | Contract | FE | Notes |
|---|--------|----------|------|----------|-----|-------|
| 117 | POST | `/iam/step-up` | Bearer + MFA | CONTRACT_PENDING | S | IAM Step-up |
| 118 | POST | `/sgod/admins` | Bearer + SGOD Admin | CONTRACT_PENDING | S | |
| 119 | GET | `/sgod/admins` | Bearer | CONTRACT_PENDING | S | |
| 120 | GET | `/sgod/admins/statistics` | Bearer | CONTRACT_PENDING | S | |
| 121 | GET | `/sgod/admins/deleted` | Bearer | CONTRACT_PENDING | S | |
| 122 | GET | `/sgod/admins/{adminId}` | Bearer | CONTRACT_PENDING | S | |
| 123 | PATCH | `/sgod/admins/{adminId}` | Bearer | CONTRACT_PENDING | S | |
| 124 | DELETE | `/sgod/admins/{adminId}` | Bearer | CONTRACT_PENDING | S | |
| 125 | PATCH | `/sgod/admins/my-profile` | Bearer | CONTRACT_PENDING | S | |
| 126 | PATCH | `/sgod/admins/profile` | Bearer | CONTRACT_PENDING | S | |
| 127 | PATCH | `/sgod/admins/me` | Bearer | CONTRACT_PENDING | S | |
| 128 | POST | `/sgod/admins/{adminId}/restore` | Bearer | CONTRACT_PENDING | G | |
| 129 | DELETE | `/sgod/admins/{adminId}/permanent` | Bearer + Root | CONTRACT_PENDING | G | |
| 130 | POST | `/sgod/admins/{adminId}/block` | Bearer + Step-up | CONTRACT_PENDING | S | |
| 131 | POST | `/sgod/admins/{adminId}/unblock` | Bearer | CONTRACT_PENDING | S | |
| 132 | PATCH | `/sgod/admins/{userId}/roles` | Bearer | CONTRACT_PENDING | S | |
| 133 | PATCH | `/sgod/admins/{userId}/department-position` | Bearer | CONTRACT_PENDING | S | |
| 134 | GET | `/sgod/admins/{userId}/available-bosses` | Bearer | CONTRACT_PENDING | S | |
| 135 | PATCH | `/sgod/admins/{userId}/boss` | Bearer | CONTRACT_PENDING | S | |

**Cluster summary**: 19 endpoints, 19 test cases

**FE mapping notes:**

- `auth-iam-stepup.service.ts` → C08 STEPUP
- `auth-sgod-admin.service.ts` → C08 ADMIN lifecycle
- `useAuthIamStepUp.ts` → C08 STEPUP
- `useAuthSgodAdmin.ts` → C08 ADMIN

**Evidence**: [`evidence/C08-admin-step-up/`](../evidence/C08-admin-step-up/)

---

## 10. C09 — Sub-Enterprises (17 endpoints)

| # | Method | Endpoint | Auth | Contract | FE |
|---|--------|----------|------|----------|-----|
| 136 | POST | `/sub-enterprises` | Bearer | CONTRACT_PENDING | S |
| 137 | GET | `/sub-enterprises` | Bearer | CONTRACT_PENDING | S |
| 138 | GET | `/sub-enterprises/statistics` | Bearer | CONTRACT_PENDING | S |
| 139 | GET | `/sub-enterprises/deleted` | Bearer | CONTRACT_PENDING | S |
| 140 | GET | `/sub-enterprises/{userId}` | Bearer | CONTRACT_PENDING | S |
| 141 | PATCH | `/sub-enterprises/{userId}` | Bearer | CONTRACT_PENDING | S |
| 142 | DELETE | `/sub-enterprises/{userId}` | Bearer | CONTRACT_PENDING | G |
| 143 | PATCH | `/sub-enterprises/my-profile` | Bearer | CONTRACT_PENDING | S |
| 144 | PATCH | `/sub-enterprises/profile` | Bearer | CONTRACT_PENDING | S |
| 145 | PATCH | `/sub-enterprises/me` | Bearer | CONTRACT_PENDING | S |
| 146 | POST | `/sub-enterprises/{userId}/restore` | Bearer | CONTRACT_PENDING | G |
| 147 | POST | `/sub-enterprises/{userId}/block` | Bearer + Step-up | CONTRACT_PENDING | S |
| 148 | POST | `/sub-enterprises/{userId}/unblock` | Bearer | CONTRACT_PENDING | S |
| 149 | POST | `/sub-enterprises/{userId}/roles` | Bearer | CONTRACT_PENDING | S |
| 150 | POST | `/sub-enterprises/{userId}/organizational` | Bearer | CONTRACT_PENDING | S |
| 151 | GET | `/sub-enterprises/{userId}/bosses` | Bearer | CONTRACT_PENDING | S |
| 152 | PATCH | `/sub-enterprises/{userId}/boss` | Bearer | CONTRACT_PENDING | S |

**Cluster summary**: 17 endpoints, **20 test cases** (extra tests for permanent delete + GET-ORG + GET-ROLES)

**FE mapping notes:**

- `auth-sub-enterprise-user.service.ts` → C09 SUB-ENTERPRISE lifecycle
- `useAuthSubEnterpriseUser.ts` → C09 SUB-ENTERPRISE CRUD + organizational
- `useAuthSgodSubEnterprise.ts` → C09 SUB-ENTERPRISE

**Evidence**: [`evidence/C09-sub-enterprises/`](../evidence/C09-sub-enterprises/)

**Verify script**: [`../postman/scripts/verify/verify_c09_end_to_end.py`](../postman/scripts/verify/verify_c09_end_to_end.py) — ✅ ALL CHECKS PASSED

---

## 11. C10 — Tenant Management (19 endpoints)

| # | Method | Endpoint | Auth | Contract | FE |
|---|--------|----------|------|----------|-----|
| 153 | GET | `/sgod/enterprises` | Bearer + SGOD Staff | CONTRACT_PENDING | S |
| 154 | GET | `/sgod/enterprises/statistics/overview` | Bearer + SGOD Staff | CONTRACT_PENDING | S |
| 155 | POST | `/sgod/enterprises/assign` | Bearer + SGOD Staff | CONTRACT_PENDING | S |
| 156 | POST | `/sgod/enterprises/unassign` | Bearer + SGOD Staff | CONTRACT_PENDING | S |
| 157 | POST | `/sgod/enterprises/set-assigned` | Bearer + SGOD Staff | CONTRACT_PENDING | S |
| 158 | GET | `/sgod/enterprises/deleted` | Bearer + SGOD Staff | CONTRACT_PENDING | S |
| 159 | GET | `/sgod/enterprises/{tenantId}` | Bearer | CONTRACT_PENDING | S |
| 160 | POST | `/sgod/enterprises/{tenantId}/block` | Bearer + SGOD Staff | CONTRACT_PENDING | S |
| 161 | POST | `/sgod/enterprises/{tenantId}/unblock` | Bearer | CONTRACT_PENDING | S |
| 162 | POST | `/sgod/enterprises/{tenantId}/restore` | Bearer + SGOD Staff | CONTRACT_PENDING | G |
| 163 | PATCH | `/sgod/enterprises/{tenantId}/subscription` | Bearer + SGOD Staff | CONTRACT_PENDING | S |
| 164 | PATCH | `/sgod/enterprises/{tenantId}/features` | Bearer + SGOD Staff | CONTRACT_PENDING | S |
| 165 | GET | `/sgod/enterprises/{tenantId}/statistics` | Bearer + SGOD Staff | CONTRACT_PENDING | S |
| 166 | POST | `/users/{userId}/organizational/assign` | Bearer | CONTRACT_PENDING | G |
| 167 | POST | `/users/{userId}/organizational/remove` | Bearer | CONTRACT_PENDING | S |
| 168 | GET | `/users/{userId}/organizational/bosses/available` | Bearer | CONTRACT_PENDING | G |
| 169 | POST | `/users/{userId}/organizational/bosses/set` | Bearer | CONTRACT_PENDING | G |
| 170 | GET | `/users/{userId}/organizational/check-subordinate` | Bearer | CONTRACT_PENDING | S |
| 171 | GET | `/organizations/audit` | Bearer + SGOD Staff | CONTRACT_PENDING | G |

**Cluster summary**: 19 endpoints, 19 test cases

**FE mapping notes:**

- `auth-sgod-enterprise.service.ts` → C10 TENANT lifecycle + assignment
- `auth-users-organizational.service.ts` → C10 ORGANIZATIONAL
- `useAuthSgodEnteprise.ts` → C10 TENANT
- `useAuthUserOrganizational.ts` / `useAuthUsersOrganizational.ts` → C10 ORGANIZATIONAL

**Evidence**: [`evidence/C10-enterprise-organizational/`](../evidence/C10-enterprise-organizational/)

**Verify script**: [`../postman/scripts/verify/verify_c10_end_to_end.py`](../postman/scripts/verify/verify_c10_end_to_end.py) — ✅ ALL CHECKS PASSED

---

## 12. C11 — Audit Logs / Crypto PoC (5 endpoints)

| # | Method | Endpoint | Auth | Contract | FE |
|---|--------|----------|------|----------|-----|
| 172 | GET | `/sgod/audit-logs` | Bearer + SGOD Staff | CONTRACT_PENDING | G |
| 173 | GET | `/sgod/audit-logs/{id}` | Bearer + SGOD Staff | CONTRACT_PENDING | G |
| 174 | GET | `/sgod/audit-logs/export` | Bearer + SGOD Staff | CONTRACT_PENDING | G |
| 175 | POST | `/test-crypto/encrypt-string-helper` | Bearer | CONTRACT_PENDING | G |
| 176 | POST | `/test-crypto/decrypt-string-helper` | Bearer | CONTRACT_PENDING | G |

> **Note**: C11 evidence also documents 2 file-helper endpoints (encrypt/decrypt file) in some Swagger screenshots but only 5 are counted in the final test plan. See `evidence/C11-audit-crypto/` for full schema details.

**Cluster summary**: 5 endpoints, 5 test cases

**FE mapping notes:**

- C11: No FE service/hook caller found in current source survey (all marked G — GAP)

**Evidence**: [`evidence/C11-audit-crypto/`](../evidence/C11-audit-crypto/)

---

## 13. Summary

| Cluster | Tag | Endpoints | Test Cases | Evidence | Verify Script |
|---|---|---:|---:|---|---|
| **C01** | sgod-auth | 28 | 28 | ✅ | — |
| **C02** | sgod-auth-enterprise / permissions / email-verification | 12 | 12 | ✅ | — |
| **C03** | sgod-auth-roles | 15 | 15 | ✅ | — |
| **C04** | sgod-auth-departments | 12 | 12 | ✅ | — |
| **C05** | sgod-auth-positions | 12 | 12 | ✅ | — |
| **C06** | sgod-auth-enterprise-users | 19 | 19 | ✅ | — |
| **C07** | sgod-auth-sgod-users | 18 | 19 | ✅ | — |
| **C08** | sgod-auth-iam-step-up / sgod-admins | 19 | 19 | ✅ | — |
| **C09** | sgod-auth-sub-enterprises | 17 | 20 | ✅ | ✅ PASS |
| **C10** | sgod-auth-sgod-enterprises / users-organizational / organizations | 19 | 19 | ✅ | ✅ PASS |
| **C11** | sgod-auth-audit-logs / test-crypto | 5 | 5 | ✅ | — |
| **Total** | **17 Swagger tags** | **176** | **180** | — | — |

**FE coverage**: S = 142, T = 1, G = 33 (service/transport seen but UI execution not proven)

---

## 14. Contract Issues Log

| Issue ID | Endpoint(s) | Issue | Status |
|---|---|---|---|
| **CI-01** | All | Response envelope: Auth v3 overview uses `result`, MFA/step-up section uses `data` | CONTRACT_PENDING |
| **CI-02** | `/sgod-admins/*` | Admin management uses `/sgod/admins` path per Swagger | CONTRACT_PENDING |
| **CI-03** | `/test-crypto/*` | DEV/PoC endpoints; environment exposure must be confirmed | CONTRACT_PENDING |
| **CI-04** | `getEnterpriseUsersDeleted` | FE calls base `enterprise-users` with status=Deleted; Swagger has `/enterprise-users/deleted` | CONTRACT_PENDING |
| **CI-05** | All PATCH endpoints | snake_case vs camelCase field mapping needs freeze per DTO | CONTRACT_PENDING |