# C05 — Positions — Error Response Schemas

<div align="center">

![Cluster](https://img.shields.io/badge/C05-Positions-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Evidence Type](https://img.shields.io/badge/Evidence-Error+Responses-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)

</div>

- [Request Body Examples](./C05-positions-request-body-examples.md)
- [Success Responses](./C05-positions-success-responses.md)

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
| 400 | Validation error / Bad request | "name and code are required" |
| 401 | Missing or invalid token | "Unauthorized" |
| 403 | Insufficient permissions | "Access denied" |
| 404 | Resource not found | "Position not found" |
| 409 | Conflict (duplicate) | "Position code already exists" |
| 500 | Internal server error | "Internal server error" |

## Cluster-Specific Error Codes

### Validation Errors
- **POS_NAME_REQUIRED** (400): "name is required"
- **POS_CODE_REQUIRED** (400): "code is required"
- **POS_DEPT_REQUIRED** (400): "department_id is required"
- **POS_MISSING_FIELDS** (400): "name and code are required"

### Conflict Errors
- **POS_CODE_EXISTS** (409): "Position code already exists"

### Dependency Errors
- **POS_HAS_USERS** (400): "Cannot delete position with users"

### Hierarchy Errors
- **POS_CYCLE_DETECTED** (400): "Cannot create cycle"

### Not Found Errors
- **POS_NOT_FOUND** (404): "Position not found"
- **POS_DEPT_NOT_FOUND** (400): "Department not found"
- **POS_PARENT_NOT_FOUND** (400): "Parent position not found"