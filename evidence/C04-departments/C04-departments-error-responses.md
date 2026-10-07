# C04 — Departments — Error Response Schemas

<div align="center">

![Cluster](https://img.shields.io/badge/C04-Departments-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Evidence Type](https://img.shields.io/badge/Evidence-Error+Responses-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)

</div>

- [Request Body Examples](./C04-departments-request-body-examples.md)
- [Success Responses](./C04-departments-success-responses.md)

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
| 400 | Validation error / Bad request | "name is required" |
| 401 | Missing or invalid token | "Unauthorized" |
| 403 | Insufficient permissions | "Access denied" |
| 404 | Resource not found | "Department not found" |
| 409 | Conflict (duplicate) | "Department code already exists" |
| 500 | Internal server error | "Internal server error" |

## Cluster-Specific Error Codes

### Validation Errors
- **DEPT_NAME_REQUIRED** (400): "name is required"
- **DEPT_CODE_REQUIRED** (400): "code is required"

### Conflict Errors
- **DEPT_CODE_EXISTS** (409): "Department code already exists"

### Dependency Errors
- **DEPT_HAS_USERS** (400): "Cannot delete department with users"
- **DEPT_HAS_CHILDREN** (400): "Cannot delete department with children"

### Hierarchy Errors
- **DEPT_CYCLE_DETECTED** (400): "Cannot create cycle"

### Not Found Errors
- **DEPT_NOT_FOUND** (404): "Department not found"
- **DEPT_PARENT_NOT_FOUND** (400): "Parent department not found"