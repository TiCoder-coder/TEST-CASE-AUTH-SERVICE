# SGOD Auth Service — Authentication Rules

> **Plan reference**: `docs/plan_to_process_FE/auth/plan_write_test_case/2026-10-06-plan-positive-test-cases-auth-service.md`
> **Guide reference**: `docs/testing/auth-service/specifications/authentication_rules.md`
> **Last updated**: 2026-10-07
> **Scope**: C01 cluster (Core Auth) + cross-cutting auth behaviors for all 11 clusters

<div align="center">

![Auth Methods](https://img.shields.io/badge/Principal_Types-5-0b0f19?style=for-the-badge&logo=shield&logoColor=FFD43B&labelColor=0b0f19&color=FF6C37)
![MFA](https://img.shields.io/badge/MFA-Step--Up_OTP-0b0f19?style=for-the-badge&logo=googletotp&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)
![Tokens](https://img.shields.io/badge/Tokens-JSON_+_Cookie-0b0f19?style=for-the-badge&logo=jsonwebtokens&logoColor=FFD43B&labelColor=0b0f19&color=55E6AA)

</div>

---

## 🧭 Mục Lục (Table of Contents)

| # | Mục | Mô tả |
|---|---|---|
| [01](#01-authentication-methods-by-principal-type) | **Authentication Methods** | 5 principal types |
| [02](#02-mfa-flows) | **MFA Flows** | Enable / Verify / Disable / Unenroll |
| [03](#03-session-management) | **Session Management** | Devices · Tokens · Context |
| [04](#04-token-delivery-modes) | **Token Delivery Modes** | JSON vs Cookie |
| [05](#05-interim-token-handling) | **Interim Token Handling** | MFA challenge token |
| [06](#06-step-up-authentication) | **Step-Up Authentication** | Sensitive action grant |
| [07](#07-login-response-states) | **Login Response States** | nextStep chain |
| [08](#08-password-flows) | **Password Flows** | Change / Forgot / Reset |
| [09](#09-account-activation) | **Account Activation** | Resend / Activate |
| [10](#10-envelope-contract-issues) | **Envelope Contract Issues** | `result` vs `data` |
| [11](#11-security-assertions) | **Security Assertions** | Critical security rules |

---

## 01. Authentication Methods by Principal Type

Auth Service hỗ trợ **5 principal types**, mỗi loại có authentication flow riêng:

### 1.1 Enterprise Principal

| Method | Endpoint | Response |
|---|---|---|
| Login | `POST /enterprises/sessions` | JSON: `accessToken` + `refreshToken` |
| Refresh | `POST /sessions/refresh` | JSON: new `accessToken` + `refreshToken` |
| Logout | `POST /sessions/current` | Tokens cleared |

**Required Headers:**

- `x-api-key`: API key của application
- `x-device-id`: Device identifier
- `Content-Type`: `application/json`
- `Authorization`: `Bearer {{accessToken}}` (for protected endpoints)

**Response example:**

```json
{
  "success": true,
  "data": {
    "accessToken": "eyJ...",
    "refreshToken": "eyJ...",
    "userType": "enterprise"
  }
}
```

### 1.2 Enterprise User Principal

| Method | Endpoint | Response |
|---|---|---|
| Login | `POST /enterprise-users/sessions` | JSON: `accessToken` + `refreshToken` + `userType` |

Cùng headers như Enterprise Principal; token dùng cho tất cả endpoints user-scoped (enterprise-users, roles, departments, positions, etc.).

### 1.3 Sub-Enterprise Principal

| Method | Endpoint | Response |
|---|---|---|
| Login | `POST /sub-enterprises/sessions` | JSON: `accessToken` + `refreshToken` |

Sub-enterprise là user thuộc branch (công ty con) gắn vào parent SGOD tenant. Token scope giới hạn trong sub-tenant.

### 1.4 SGOD User Principal

| Method | Endpoint | Response |
|---|---|---|
| Login | `POST /sgod-users/sessions` | HttpOnly cookie + minimal body |

**Token delivery**: HttpOnly cookie — không trả JSON `accessToken` trong body.

### 1.5 SGOD Admin Principal

| Method | Endpoint | Response |
|---|---|---|
| Login | `POST /sgod-admins/sessions` | HttpOnly cookie + minimal body |

Có quyền cao nhất, có thể thao tác trên tenant management và audit logs.

---

## 02. MFA Flows

### 2.1 Enable MFA

```text
POST /mfa/enable
Headers: Authorization: "Bearer {{accessToken}}"
Body: {}   // empty body, server generates secret
→ Response: { secret: "JBSWY3DPEHPK3PXP", otpauthUrl: "otpauth://totp/..." }
```

**Test rules:**

- Response chứa TOTP secret và otpauthUrl
- Lưu secret vào environment variable `mfa_secret_key`
- Sau enable, verify bằng `POST /mfa/verification`

### 2.2 Verification (Initial Setup)

```text
POST /mfa/verification
Headers: Authorization: "Bearer {{accessToken}}"
Body: { "code": "{{currentTotp}}" }
→ Response: { verified: true }
```

**Test rules:**

- Tính OTP mới mỗi lần chạy từ `mfa_secret_key`
- Sau verify, user chính thức có MFA active

### 2.3 MFA Verify (Login Challenge)

```text
POST /mfa/verify
Headers: Authorization: "Bearer {{interimToken}}"   // KHÔNG phải accessToken
Body: { "code": "{{currentTotp}}" }
→ Response: { accessToken, refreshToken, mfaRequired: false }
```

**Test rules:**

- interimToken chỉ dùng cho endpoint này, một lần duy nhất
- Sau verify, interimToken bị revoke

### 2.4 Disable MFA

```text
POST /mfa/disable
Headers: Authorization: "Bearer {{accessToken}}"
Body: { "code": "{{currentTotp}}" }   // current OTP required
→ Response: { mfaDisabled: true }
```

### 2.5 MFA Unenroll (Full Removal)

```text
POST /mfa/unenroll
Headers: Authorization: "Bearer {{accessToken}}"
Body: { ... }   // DTO riêng, chưa freeze — CONTRACT_PENDING
→ Response: { enrollment removed }
```

**Test notes:**

- Endpoint này ở `CONTRACT_PENDING` — chỉ assert what BE returns
- Sau unenroll, user không thể MFA verify nữa

---

## 03. Session Management

### 3.1 Device Trust

```text
POST /devices/{deviceId}/trust
Headers: Authorization: "Bearer {{accessToken}}"
Body: { ... }  // password hoặc 2FA proof theo DTO
→ Response: { device marked as trusted }

POST /devices/{deviceId}/untrust
Body: { ... }  // fresh proof required
→ Response: { device marked as untrusted }
```

**Test rules:**

- Trust yêu cầu proof (password hoặc 2FA) — không được trust without proof
- Untrust có thể không cần proof (tùy implementation)
- Verify trong `GET /sessions/devices` sau khi trust/untrust

### 3.2 Device Logout

```text
DELETE /sessions/devices/{deviceId}
Headers: Authorization: "Bearer {{accessToken}}"
→ Response: { target device session revoked; other devices unchanged }

DELETE /sessions
Headers: Authorization: "Bearer {{accessToken}}"  // hoặc cookie
→ Response: { all sessions for actor revoked; tokens cleared }
```

**Test notes:**

- Logout-all (DELETE /sessions): phải re-login để tiếp tục
- Logout-one: session khác vẫn hoạt động

### 3.3 Session Context

```text
GET /session/context
Headers: Authorization: "Bearer {{accessToken}}"
→ Response: {
    "identity": {
      "id": "uuid",
      "email": "user@example.com",
      "type": "enterprise_user",
      ...
    },
    "tenantId": "tenant-uuid",
    "claims": [...],
    "is2FAVerifiedInSession": true,
    "isUse2FA": true,
    "deviceId": "device-uuid",
    "roles": [...],
    "permissions": [...]
  }
```

**Anonymous context** (khi không có session):

```text
GET /session/context
→ Response: {
    "identity": { "id": "" },
    "roles": [],
    "permissions": [],
    "is2FAVerifiedInSession": false
  }
HTTP 200 vẫn được trả về (không phải 401)
```

**Test rules:**

- Có session: assert `identity.id` non-empty, có roles/permissions
- Không có session: assert `identity.id === ""`, arrays rỗng
- `is2FAVerifiedInSession` phải khớp với state hiện tại

---

## 04. Token Delivery Modes

| Principal | Token Type | Delivery | Notes |
|---|---|---|---|
| **Enterprise** | JSON | `accessToken` + `refreshToken` in body | — |
| **Enterprise User** | JSON | `accessToken` + `refreshToken` in body | — |
| **Sub-Enterprise** | JSON | `accessToken` + `refreshToken` in body | — |
| **SGOD User** | Cookie | HttpOnly cookie + optional body | No JSON token assertion |
| **SGOD Admin** | Cookie | HttpOnly cookie + optional body | No JSON token assertion |

**Test rules:**

- JSON principals: assert `accessToken` + `refreshToken` presence, type, non-empty
- Cookie principals: assert cookie set đúng (Cookie header), không assert body có token
- KHÔNG assert exact token value (chỉ presence + format)

---

## 05. Interim Token Handling

`interimToken` được trả khi login yêu cầu MFA challenge:

- **Storage**: Environment variable (test) / Keychain (FE) / Cookie (BE)
- **Lifetime**: Ngắn, expire sau khi verify hoặc timeout (~5 minutes)
- **Usage**: Authorization header `Bearer {{interimToken}}` cho MFA verify
- **Not for**: Không dùng interimToken cho các request khác ngoài MFA verify

**Test rules:**

- interimToken chỉ dùng cho `POST /mfa/verify`
- Dùng interimToken cho endpoint khác → expect 401
- Sau khi dùng interimToken, nó bị revoked (một lần duy nhất)

---

## 06. Step-Up Authentication

Step-up dùng cho các action nhạy cảm (block, delete, etc.) — cần MFA proof mới trong TTL ngắn:

```text
POST /iam/step-up
Headers: Authorization: "Bearer {{accessToken}}"
Body: { "code": "{{currentTotp}}" }
→ Response: {
    "verified": true,
    "ttlSeconds": 300,
    "expiresAt": "2026-10-07T10:05:00.000Z"
  }
```

**Rules:**

- Session phải đã verify MFA (`is2FAVerifiedInSession: true`)
- `verified: true` + `ttlSeconds` positive → step-up thành công
- Sau khi step-up, mutation cần grant có thể thực hiện trong TTL
- TTL: 5 minutes (300s) — sau khi hết, phải step-up lại

**Test cases cần step-up:**

- Block user (C06/C08/C09)
- Initiate password reset (admin)
- Hard delete (C07, C08)

---

## 07. Login Response States

| State | `nextStep` | Tokens Returned | Next Action |
|---|---|---|---|
| **Success (no MFA)** | absent/null | `accessToken` + `refreshToken` | Proceed with normal flow |
| **MFA Required** | `REQUIRE_2FA` | `interimToken` | POST `/mfa/verify` |
| **Account Verification** | `REQUIRE_ACCOUNT_VERIFICATION` | `interimToken` | POST `/activate-account` |
| **Password Change** | `AM_FORCE_CHANGE_PASSWORD` | — | POST `/passwords/change` |

> Chỉ coi login hoàn tất khi đã vượt qua bước cần thiết và profile/session context dùng được.

**Test rules:**

- Sau mỗi state, follow `Next Action` chain cho đến khi có full session
- Verify session context (`GET /session/context`) trả về identity đúng

---

## 08. Password Flows

### 8.1 Change Password (User self-service)

```text
POST /passwords/change
Headers: Authorization: "Bearer {{accessToken}}"
Body: {
  "oldPassword": "{{oldPassword}}",
  "newPassword": "{{newPassword}}",
  "otp": "{{currentTotp}}"  // nếu MFA bật
}
→ Response: { success: true }
```

**Test rules:**

- Verify login bằng password mới thành công
- Verify password cũ không còn dùng được
- MFA optional: nếu user có MFA bật, phải cung cấp OTP

### 8.2 Forgot Password (Public)

```text
POST /passwords/forgot
Body: { "email": "{{actorEmail}}" }
→ Response: {
    "success": true,
    "message": "If email exists, reset link sent"
  }
```

**Test rules:**

- Response LUÔN generic success (không tiết lộ email có tồn tại hay không)
- Reset material gửi qua email inbox (DEV: `GET /dev/emails`)
- Material có expiry (thường 1 hour)

### 8.3 Reset Password (Public)

```text
POST /passwords/reset
Body: {
  "selector": "{{selector}}",      // từ email link
  "token": "{{resetToken}}",       // từ email link
  "newPassword": "{{newPassword}}",
  "otp": "{{currentTotp}}"          // nếu MFA bật
}
→ Response: { success: true }
```

---

## 09. Account Activation

### 9.1 Resend Activation

```text
POST /users/{userId}/actions/resend-activation
Headers: Authorization: "Bearer {{accessToken}}"
Body: {}   // empty
→ Response: { activationEmailSent: true }
```

### 9.2 Activate Account

```text
POST /activate-account
Headers: Authorization: "Bearer {{interimToken}}"
Body: {
  "selector": "{{selector}}",    // từ email link
  "token": "{{activationToken}}" // từ email link
}
→ Response: { success: true, accountActivated: true }
```

**Test rules:**

- Sau activate, login với cùng credentials phải trả `nextStep: null` (Success no MFA)
- Account pending → MFA verify → activation chain đầy đủ

---

## 10. Envelope Contract Issues

| Endpoint | Envelope | Status |
|---|---|---|
| Auth v3 overview (login, session, etc.) | `result` | CONTRACT_PENDING — một số endpoint đang dùng `result.data` thay vì `data` |
| MFA / Step-up (C01) | `data` | CONTRACT_READY |
| C02-C11 endpoints | `data` | CONTRACT_READY |

> **Implication**: Test scripts nên check cả `data` và `result.data` cho đến khi CI-01 được giải quyết. Xem [README § 13.3 Contract Issues](../README.md#133-contract-issues).

---

## 11. Security Assertions

| Field | What to Assert | What NOT to Assert |
|---|---|---|
| **Token** | presence, type (string), non-empty | exact value |
| **Password** | NEVER in response | NEVER in response |
| **Hash/Salt** | NEVER in response | NEVER in response |
| **Recovery codes** | redact in evidence | Never commit to artifact |
| **TOTP/OTP** | New per operation | Never reuse code |
| **Cookie HttpOnly** | Cookie set correctly | Not readable by JS |

### Critical Security Rules

1. **No secrets in artifacts**: Không ghi password, token, OTP, recovery code, API key thật vào bất kỳ artifact nào (workbook, collection, evidence, screenshot).

2. **Variable placeholders**: Mọi giá trị nhạy cảm dùng `{{variable}}` placeholder. Giá trị thật inject qua environment variables.

3. **Evidence redaction**: Trước khi commit evidence, redact:
   - Replace token values with `<REDACTED>`
   - Replace password values with `<REDACTED>`
   - Replace OTP/TOTP with `<REDACTED>`
   - Replace recovery codes with `<REDACTED>`

4. **Fresh OTPs**: Mỗi thao tác tạo OTP/TOTP MỚI. Không reuse từ lần chạy trước.

5. **HttpOnly cookies**: KHÔNG đọc HttpOnly cookie bằng JavaScript. Chỉ assert cookie set đúng qua response headers.

6. **runId isolation**: Prefix tất cả test data với `runId` để tránh collision giữa các lần chạy.

### Test Data Cleanup

- Sau khi test xong, restore state (unblock user, restore deleted, etc.)
- Không để lại test artifacts trong production data
- Nếu không thể cleanup, document lại trong execution log