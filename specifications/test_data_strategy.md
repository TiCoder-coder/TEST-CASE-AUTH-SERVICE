# SGOD Auth Service — Test Data Strategy

> **Plan reference**: `docs/plan_to_process_FE/auth/plan_write_test_case/2026-10-06-plan-positive-test-cases-auth-service.md`
> **Guide reference**: `docs/testing/auth-service/specifications/test_data_strategy.md`
> **Last updated**: 2026-10-07
> **Scope**: Test actors, fixtures, naming convention, cleanup

<div align="center">

![Actors](https://img.shields.io/badge/Test_Actors-17-0b0f19?style=for-the-badge&logo=users&logoColor=FFD43B&labelColor=0b0f19&color=FF6C37)
![Fixtures](https://img.shields.io/badge/Fixtures-Role%2FDept%2FPos%2FDevice%2FWallet-0b0f19?style=for-the-badge&logo=database&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)
![runId](https://img.shields.io/badge/runId-UUID_v4-0b0f19?style=for-the-badge&logo=key&logoColor=FFD43B&labelColor=0b0f19&color=55E6AA)

</div>

---

## 🧭 Mục Lục (Table of Contents)

| # | Mục | Mô tả |
|---|---|---|
| [01](#01-test-actor-registry) | **Test Actor Registry** | 17 actors |
| [02](#02-fixture-registry) | **Fixture Registry** | Roles/Depts/Pos/Devices |
| [03](#03-test-data-naming-convention) | **Naming Convention** | runId-based |
| [04](#04-environment-variables-template) | **Environment Variables** | Template |
| [05](#05-runid-và-isolation) | **runId & Isolation** | UUID v4 strategy |
| [06](#06-test-data-dependencies) | **Test Data Dependencies** | Dependency graph |
| [07](#07-cleanup-strategy) | **Cleanup Strategy** | Per-case + order |
| [08](#08-otptotp-handling) | **OTP/TOTP Handling** | Generation rules |
| [09](#09-seed-data-requirements) | **Seed Data Requirements** | Pre-run checklist |
| [10](#10-security-rules) | **Security Rules** | Redaction + isolation |

---

## 01. Test Actor Registry

Mỗi actor là **identity riêng**, không dùng chung session/token giữa các actor.

### 1.1 SGOD Admin Tier (Cookie session)

| Actor Alias | Type | State | MFA | Notes |
|---|---|---|---|---|
| `ROOT_ADMIN` | SGOD Admin | Active, verified | Yes | Disposable root test identity. **Never use production root** |
| `SGOD_ADMIN_A` | SGOD Admin | Active, verified | Yes | Full permissions for Tenant A management |
| `SGOD_ADMIN_B` | SGOD Admin | Active, verified | Yes | Full permissions for Tenant B management |

### 1.2 Enterprise Tier (JSON token)

| Actor Alias | Type | State | MFA | Notes |
|---|---|---|---|---|
| `ENTERPRISE_A` | Enterprise | Active, verified, subscription valid | N/A | Tenant-level login principal |
| `ENTERPRISE_B` | Enterprise | Active, verified, subscription valid | N/A | Tenant-level login principal |

### 1.3 Enterprise User Tier (JSON token)

| Actor Alias | Type | State | MFA | Notes |
|---|---|---|---|---|
| `ENT_USER_A` | Enterprise User | Active, activated | Yes | Primary login for C01/C06 |
| `ENT_USER_B` | Enterprise User | Active, activated | Yes | Secondary login for C06 |
| `ENT_USER_BLOCKED` | Enterprise User | Blocked | No | For block/unblock state cases |
| `ENT_USER_DELETED` | Enterprise User | Soft-deleted | No | For delete/restore cases |
| `MFA_TARGET` | Enterprise User | Active | Yes | For MFA enroll/disable tests |
| `PASSWORD_TARGET` | Enterprise User | Active | No | For password change tests |
| `ACTIVATION_TARGET` | Enterprise User | Pending | No | For activation flow tests |

### 1.4 Sub-Enterprise User Tier (JSON token)

| Actor Alias | Type | State | MFA | Notes |
|---|---|---|---|---|
| `SUBENT_A` | Sub-Enterprise User | Active, activated | Yes | Belongs to ENTERPRISE_A |
| `SUBENT_B` | Sub-Enterprise User | Active, activated | Yes | Belongs to ENTERPRISE_A |

### 1.5 SGOD User Tier (Cookie session)

| Actor Alias | Type | State | MFA | Notes |
|---|---|---|---|---|
| `SGOD_USER_A` | SGOD User | Active | Yes | Primary login for C07 |
| `SGOD_USER_DELETED` | SGOD User | Soft-deleted | No | For delete/restore |
| `SGOD_USER_BLOCKED` | SGOD User | Blocked | No | For block/unblock |

**Tổng**: 17 actors (3 SGOD Admin + 2 Enterprise + 7 Enterprise User + 2 Sub-Enterprise + 3 SGOD User).

---

## 02. Fixture Registry

### 2.1 Roles (C03)

| Fixture Alias | Type | Parent | Tenant |
|---|---|---|---|
| `ROLE_ROOT` | SYSTEM | None | ROOT |
| `ROLE_PARENT` | CUSTOM | ROLE_ROOT | ENTERPRISE_A |
| `ROLE_CHILD` | CUSTOM | ROLE_PARENT | ENTERPRISE_A |
| `ROLE_DELETED` | CUSTOM | ROLE_PARENT | ENTERPRISE_A |

### 2.2 Departments (C04)

| Fixture Alias | Parent | Tenant |
|---|---|---|
| `DEPT_ROOT` | None | ENTERPRISE_A |
| `DEPT_PARENT` | DEPT_ROOT | ENTERPRISE_A |
| `DEPT_CHILD` | DEPT_PARENT | ENTERPRISE_A |
| `DEPT_MOVE_PARENT` | None | ENTERPRISE_A |
| `DEPT_DELETED` | DEPT_PARENT | ENTERPRISE_A |

### 2.3 Positions (C05)

| Fixture Alias | Department | Layer | Role | Parent |
|---|---|---:|---|---|
| `POS_ROOT` | DEPT_ROOT | 1 | ROLE_ROOT | None |
| `POS_PARENT` | DEPT_PARENT | 2 | ROLE_PARENT | POS_ROOT |
| `POS_CHILD` | DEPT_CHILD | 3 | ROLE_CHILD | POS_PARENT |
| `POS_VACANT` | DEPT_CHILD | 3 | ROLE_CHILD | POS_PARENT |
| `POS_DELETED` | DEPT_CHILD | 3 | ROLE_CHILD | POS_PARENT |

### 2.4 Organizational Relations (C10)

| Fixture Alias | Position | Boss | Members |
|---|---|---|---|
| `MANAGER` | POS_PARENT | None | 2 employees |
| `EMPLOYEE` | POS_CHILD | MANAGER | 0 |

### 2.5 Devices (C01)

| Fixture Alias | Owner | Trusted | Notes |
|---|---|---|---|
| `DEVICE_A` | ENT_USER_A | Yes | Current test device |
| `DEVICE_B` | ENT_USER_A | Yes | Secondary device |
| `DEVICE_UNTRUSTED` | ENT_USER_A | No | For trust/untrust cases |

### 2.6 Wallets (C06)

| Fixture Alias | Owner | State |
|---|---|---|
| `WALLET_TARGET` | ENT_USER_A | Active, provisioned |

### 2.7 Crypto Fixtures (C11)

| Fixture Alias | Type | Content |
|---|---|---|
| `CRYPTO_STRING` | Unicode string | `"Xin chào SGOD 测试 🔐"` |
| `CRYPTO_FILE` | Binary file | 1MB PNG fixture |

### 2.8 Deleted Targets (Restore Flow)

| Fixture Alias | Type | Belongs To |
|---|---|---|
| `DELETED_USER_ENT` | Enterprise User | ENTERPRISE_A |
| `DELETED_USER_SGOD` | SGOD User | SGOD_ADMIN_A |
| `DELETED_ROLE` | Role CUSTOM | ENTERPRISE_A |
| `DELETED_DEPT` | Department | ENTERPRISE_A |
| `DELETED_POS` | Position | ENTERPRISE_A |

---

## 03. Test Data Naming Convention

Tất cả test data dùng suffix theo `runId` để isolation:

### 3.1 runId Format

```text
{{runId}} = UUID v4, ví dụ: "tc-run-20261007-001"
```

Generate bằng:

```bash
uuidgen
# Hoặc
python3 -c "import uuid; print(f'tc-run-{uuid.uuid4().hex[:12]}')"
```

### 3.2 Naming Patterns

```text
{{actorEmail}}    = "{{runId}}-actor@sgod.test"
{{actorUserName}} = "{{runId}}_actor"
{{targetEmail}}   = "{{runId}}-target@sgod.test"
{{targetUserName}} = "{{runId}}_target"
{{roleName}}      = "{{runId}}_role_{{feature}}"     # e.g., tc-run-20261007-001_role_parent
{{deptName}}      = "{{runId}}_dept_{{feature}}"
{{posName}}       = "{{runId}}_pos_{{feature}}"
```

### 3.3 Examples

```text
# Roles
"tc-run-20261007-001_role_parent"
"tc-run-20261007-001_role_child"
"tc-run-20261007-001_role_deleted"

# Users
"tc-run-20261007-001-actor@sgod.test"
"tc-run-20261007-001_target_user"
```

---

## 04. Environment Variables (Template)

Template Postman environment (no secrets):

```json
{
  "baseUrlAuth": "{{baseUrlAuth}}",
  "authApiKey": "{{authApiKey}}",
  "lang": "vi",
  "runId": "{{runId}}",
  "deviceId": "{{deviceId}}",
  "accessToken": "{{accessToken}}",
  "refreshToken": "{{refreshToken}}",
  "interimToken": "{{interimToken}}",
  "tenantId": "{{tenantId}}",
  "actorEmail": "{{actorEmail}}",
  "actorPassword": "{{actorPassword}}",
  "currentTotp": "{{currentTotp}}",
  "mfa_recovery_codes": "{{mfa_recovery_codes}}",
  "role_parent_id": "{{role_parent_id}}",
  "role_child_id": "{{role_child_id}}",
  "dept_parent_id": "{{dept_parent_id}}",
  "dept_child_id": "{{dept_child_id}}",
  "pos_parent_id": "{{pos_parent_id}}",
  "pos_child_id": "{{pos_child_id}}",
  "user_id": "{{user_id}}",
  "target_user_id": "{{target_user_id}}",
  "subent_user_id": "{{subent_user_id}}"
}
```

> **SECURITY RULE**: Không ghi giá trị thật của password, token, OTP, recovery code vào bất kỳ artifact nào (workbook, Postman, evidence). Chỉ dùng biến.

### Variable Categories

| Category | Variables | Lifecycle |
|---|---|---|
| **Infrastructure** | `baseUrlAuth`, `authApiKey`, `lang` | Static (per env) |
| **Session** | `runId`, `deviceId` | Per run |
| **Tokens** | `accessToken`, `refreshToken`, `interimToken` | Per login |
| **Credentials** | `actorEmail`, `actorPassword`, `currentTotp` | Per run |
| **Test Data IDs** | `role_*_id`, `dept_*_id`, `pos_*_id`, `user_id` | Per test case |
| **Misc** | `tenantId`, `mfa_recovery_codes` | Per session |

---

## 05. runId và Isolation

Mỗi lần chạy test:

1. **Generate `runId` mới** (UUID v4)
2. **Prefix tất cả seed data** với `runId`
3. **Tạo fixture mới trong environment** thay vì reuse
4. **Record fixture IDs thực** trả từ BE vào execution log
5. **Không dùng ID từ tài liệu hoặc ảnh** — luôn capture từ response

### Isolation Benefits

- Multiple test runs có thể chạy song song không conflict
- Cleanup chỉ cần xóa data có `runId` prefix
- Reproduction: chạy lại với cùng `runId` để reproduce state

### When to Reuse `runId`

- Debug một lần chạy cụ thể
- Re-test sau khi BE fix
- Nếu phải re-run toàn bộ phase

---

## 06. Test Data Dependencies

### 6.1 Authentication Foundation (C01/C02)

```text
ROOT_ADMIN
  └── SGOD_ADMIN_A
  └── SGOD_ADMIN_B
        └── ENTERPRISE_A
        │     ├── ENT_USER_A
        │     ├── ENT_USER_B
        │     ├── ENT_USER_BLOCKED
        │     └── ENT_USER_DELETED
        │           └── SUBENT_A
        │           └── SUBENT_B
        └── ENTERPRISE_B
              └── (similar structure)
```

### 6.2 Role/Department/Position Foundation (C03/C04/C05)

```text
ENTERPRISE_A
  ├── ROLE_PARENT
  │     └── ROLE_CHILD
  ├── DEPT_PARENT
  │     └── DEPT_CHILD
  └── POS_PARENT
        └── POS_CHILD
```

### 6.3 Principal Lifecycle (C06/C07/C08/C09)

```text
ENTERPRISE_A
  ├── ENT_USER_A
  │     ├── assigned: ROLE_DEPT
  │     ├── assigned: DEPT_POS
  │     └── assigned: BOSS (MANAGER)
  ├── SUBENT_A
  │     ├── assigned: ROLE_DEPT
  │     └── assigned: DEPT_POS
  └── (negative cases: BLOCKED, DELETED)

SGOD_ADMIN_A
  └── SGOD_USER_A
        ├── assigned: ROLE_DEPT
        └── assigned: DEPT_POS
```

### 6.4 Organizational Graph (C10)

```text
ENTERPRISE_A
  ├── DEPT_PARENT
  │     └── POS_PARENT (MANAGER)
  │           └── POS_CHILD (EMPLOYEE)
  └── DEPT_MOVE_PARENT
        └── POS_VACANT
```

---

## 07. Cleanup Strategy

### 7.1 Per-Case Cleanup

Mỗi case có cleanup riêng được định nghĩa trong postcondition:

| Case Type | Cleanup Action |
|---|---|
| **Login session** | Logout session riêng (DELETE /sessions/current) |
| **MFA enrollment** | Disable → Unenroll (nếu enrollment mới) |
| **Password change** | Reset về fixture password (POST /passwords/change) |
| **Create role/dept/pos** | Delete fixture (DELETE /{type}/{id}) |
| **Delete/restore** | Restore nếu cần (POST /{type}/{id}/restore) |
| **Block/unblock** | Unblock (POST /{type}/{id}/unblock) |
| **Wallet revoke** | Re-provision (nếu có API) |
| **Boss assignment** | Remove boss (PATCH /{type}/{id}/boss với null) |
| **Role assignment** | Unassign (PATCH với roleIds rỗng) |

### 7.2 Destructive Test Rule

> **CRITICAL**: Hard delete, revoke, logout-all và các thao tác destructive **CHỈ** chạy trên disposable fixture có prefix `runId`. Không bao giờ chạy trên tài khoản shared developer hoặc record mà tests khác phụ thuộc.

### 7.3 No DB Cleanup

Không tự viết SQL hoặc direct DB cleanup. Chỉ dùng API endpoints đã được duyệt để cleanup. Nếu không có delete API cho loại record nào, dùng seed/reset fixture procedure do BE owner xác nhận.

### 7.4 Cleanup Order (Reverse of Creation)

```text
1. Logout sessions
2. Unassign roles
3. Unassign positions
4. Remove boss
5. Delete/restore user
6. Delete/restore role
7. Delete/restore department
8. Delete/restore position
```

### 7.5 Cleanup Failure Handling

- Nếu cleanup fail: log vào execution log, không fail test
- Document leftover state trong execution report
- Có thể chạy manual cleanup script sau khi test xong

---

## 08. OTP/TOTP Handling

| Step | Source | Rule |
|---|---|---|
| **OTP từ email inbox** | DEV inbox endpoint (`GET /dev/emails`) | Lấy mới mỗi thao tác, **không reuse** |
| **TOTP code** | Tạo mới từ `MFA_TARGET` enrollment | Lấy mới mỗi thao tác, **không reuse** |
| **Recovery code** | Từ enrollment mới | Lưu vào environment variable, dùng khi TOTP fail |
| **Selector/token reset** | Từ `POST /passwords/forgot` response | Dùng ngay, có expiry (thường 1h) |

### TOTP Generation (Test Side)

```python
import pyotp
totp = pyotp.TOTP("{{mfa_secret_key}}")
current_code = totp.now()  # 6-digit code, valid 30s
```

Hoặc trong Postman pre-request script:

```javascript
const totp = require('otpauth');
const secret = pm.environment.get("mfa_secret_key");
const totpInstance = new totp.TOTP({ secret: secret, digits: 6, period: 30 });
const code = totpInstance.generate();
pm.environment.set("currentTotp", code);
```

### OTP Extraction (DEV Inbox)

```bash
# Sau khi trigger forgot password, lấy OTP từ DEV inbox
curl -H "x-api-key: $API_KEY" "$BASE_URL/dev/emails?limit=10" | \
  jq '.data[] | select(.to == "{{actorEmail}}") | .body' | \
  grep -oE '[0-9]{6}' | head -1
```

---

## 09. Seed Data Requirements

| Type | Requirement | Used by Cluster |
|---|---|---|
| **Role tree** | Ít nhất 3 levels (ROOT → PARENT → CHILD) | C03 |
| **Department tree** | Ít nhất 2 levels | C04 |
| **Position tree** | Ít nhất 2 levels, có vacant position | C05 |
| **User with position** | MANAGER + EMPLOYEE relationship | C05, C09, C10 |
| **Statistics** | Pre-seeded data với count xác định | All (statistics endpoints) |
| **Device trust** | Ít nhất 1 trusted + 1 untrusted device | C01 |
| **Wallet** | Ít nhất 1 user có wallet provisioned | C06 |
| **Crypto fixtures** | 1 unicode string + 1 binary file | C11 |

### Validation Before Test Run

- [ ] All actors exist in DB
- [ ] All actors active (not blocked/deleted)
- [ ] Role tree has 3 levels
- [ ] Department tree has 2+ levels
- [ ] Position tree has 2+ levels with 1 vacant
- [ ] MANAGER → EMPLOYEE boss relationship set
- [ ] DEVICE_A trusted, DEVICE_UNTRUSTED untrusted
- [ ] WALLET_TARGET has active wallet
- [ ] CRYPTO_STRING and CRYPTO_FILE ready

---

## 10. Security Rules

> **CRITICAL**: All artifacts (Postman collection, evidence, screenshots) MUST NOT contain real secrets.

### 10.1 What NOT to Commit

| Type | Example | Why |
|---|---|---|
| **Passwords** | `MySecretP@ss123` | Reusable credential |
| **Tokens** | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` | Session hijack risk |
| **OTP/TOTP** | `123456` | Replay attack |
| **Recovery codes** | `abcd-efgh-ijkl` | Account takeover |
| **API keys** | `sk_live_abc123` | Backend compromise |
| **Cookie values** | `session=abc123` | Session hijack |

### 10.2 What to Use Instead

| Real value | Placeholder |
|---|---|
| Real password | `{{actorPassword}}` |
| Real token | `{{accessToken}}` |
| Real TOTP | `{{currentTotp}}` |
| Real recovery code | `{{mfa_recovery_codes}}` |
| Real API key | `{{authApiKey}}` |

### 10.3 Evidence Redaction

Trước khi commit evidence `.md` files:

- Replace token values with `<REDACTED>`
- Replace password values with `<REDACTED>`
- Replace OTP/TOTP with `<REDACTED>`
- Replace recovery codes with `<REDACTED>`
- Replace email/username with `<REDACTED-{timestamp}>`

### 10.4 runId Scope

- `runId` KHÔNG phải secret (chỉ là test isolation marker)
- Nhưng vẫn nên treat như identifier — không leak ra ngoài test env
- Khi debug, share `runId` cụ thể qua internal channel only