# C11 — Audit Logs / Crypto — Error Response Schemas

<div align="center">

![Cluster](https://img.shields.io/badge/C11-Audit+Logs+++Crypto+PoC-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Evidence Type](https://img.shields.io/badge/Evidence-Error+Responses-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)

</div>

- [Request Body Examples](./C11-audit-crypto-request-body-examples.md)
- [Success Responses](./C11-audit-crypto-success-responses.md)

---

## 🧭 Mục Lục (Table of Contents)

| # | Endpoint |
|---|---|
| 01 | [Standard Error Envelope(#standard-error-envelope) |
| 02 | [HTTP Status Code Mapping(#http-status-code-mapping) |
| 03 | [Cluster-Specific Error Codes(#cluster-specific-error-codes) |

---

## Overview
All auth-service endpoints return consistent error envelopes following the `IBeApiEnvelope` pattern. Error responses always include `success: false`.

## Standard Error Envelope
```json
{
  "success": false,
  "message": "Human-readable error message",
  "timestamp": "2026-10-06T10:00:00.000Z"
}
```

## HTTP Status Code Mapping
| HTTP Code | Trigger | Example Message |
|-----------|---------|----------------|
| 400 | Validation error / Bad request | "plaintext is required" |
| 401 | Missing or invalid token | "Unauthorized" |
| 403 | Insufficient permissions | "Access denied" |
| 404 | Resource not found | "Audit log not found" |
| 500 | Internal server error | "Internal server error" |

## Cluster-Specific Error Codes

### Crypto Errors
- **CRYPTO_PLAINTEXT_REQUIRED** (400): "plaintext is required"
- **CRYPTO_DECRYPT_FAILED** (400): "Decryption failed"
- **CRYPTO_CONTEXT_MISMATCH** (400): "Decryption failed" (also covers wrong context)
- **CRYPTO_INVALID_CIPHERTEXT** (400): "Invalid ciphertext"
- **CRYPTO_NOT_FOUND** (404): "Ciphertext record not found"

### Audit Log Errors
- **AUDIT_UNAUTHORIZED** (401): "Unauthorized"
- **AUDIT_FORBIDDEN** (403): "Access denied"
- **AUDIT_NOT_FOUND** (404): "Audit log not found"
- **AUDIT_EXPORT_FAILED** (500): "Failed to export audit logs"