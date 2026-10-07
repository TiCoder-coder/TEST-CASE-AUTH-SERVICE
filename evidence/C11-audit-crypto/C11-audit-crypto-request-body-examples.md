# C11 — Audit Logs / Crypto — Request Body Examples

<div align="center">

![Cluster](https://img.shields.io/badge/C11-Audit+Logs+++Crypto+PoC-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Evidence Type](https://img.shields.io/badge/Evidence-Request+Body+Examples-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)

</div>

- [Error Responses](./C11-audit-crypto-error-responses.md)
- [Success Responses](./C11-audit-crypto-success-responses.md)

---

## 🧭 Mục Lục (Table of Contents)

| # | Endpoint |
|---|---|
| 01 | [Audit Logs — List](#audit-logs--list) |
| 02 | [Audit Logs — Get by ID](#audit-logs--get-by-id) |
| 03 | [Audit Logs — Export](#audit-logs--export) |
| 04 | [Test Crypto — Encrypt String](#test-crypto--encrypt-string) |
| 05 | [Test Crypto — Decrypt String](#test-crypto--decrypt-string) |

---

## Overview
This document provides representative request body examples for **audit log** and **test crypto helper** endpoints.

---

## Audit Logs — List

**Endpoint:** `GET /sgod-auth/v1/sgod/audit-logs`
**DTO Source:** Query string
**Actor:** ROOT_ADMIN (or SGOD admin)

### Sample Request Body
```json
{}
```

### Query Parameters
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| page | number | ❌ | Page index |
| pageSize | number | ❌ | Page size |
| actorId | string | ❌ | Filter by actor ID |
| action | string | ❌ | Filter by action key |
| fromDate | string | ❌ | ISO8601 start date |
| toDate | string | ❌ | ISO8601 end date |

---

## Audit Logs — Get by ID

**Endpoint:** `GET /sgod-auth/v1/sgod/audit-logs/{id}`
**DTO Source:** None
**Actor:** ROOT_ADMIN

### Sample Request Body
```json
{}
```

---

## Audit Logs — Export

**Endpoint:** `GET /sgod-auth/v1/sgod/audit-logs/export`
**DTO Source:** Query string
**Actor:** ROOT_ADMIN

### Sample Request Body
```json
{}
```

---

## Test Crypto — Encrypt String

**Endpoint:** `POST /sgod-auth/v1/test-crypto/encrypt-string-helper`
**DTO Source:** `ParamEncryptStringDto` from `types.ts`
**Actor:** ROOT_ADMIN (test-only helper)

### Sample Request Body
```json
{
  "plaintext": "Hello World",
  "context": "test"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| plaintext | string | required | Plain text to encrypt |
| context | string | required | Encryption context (e.g., `test`) |

---

## Test Crypto — Decrypt String

**Endpoint:** `POST /sgod-auth/v1/test-crypto/decrypt-string-helper`
**DTO Source:** `ParamDecryptStringDto` from `types.ts`
**Actor:** ROOT_ADMIN

### Sample Request Body
```json
{
  "ciphertext": "base64-or-armored-ciphertext",
  "context": "test"
}
```

### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| ciphertext | string | required | Ciphertext produced by encrypt |
| context | string | required | Same context used during encryption |