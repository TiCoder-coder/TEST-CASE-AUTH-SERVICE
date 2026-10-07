# C03 — Roles — Error Response Schemas

<div align="center">

![Cluster](https://img.shields.io/badge/C03-Roles-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Evidence Type](https://img.shields.io/badge/Evidence-Error+Responses-0b0f19?style=for-the-badge&logo=checkmarx&logoColor=FFFFFF&labelColor=0b0f19&color=48E7FF)

</div>

- [Request Body Examples](./C03-roles-request-body-examples.md)
- [Success Responses](./C03-roles-success-responses.md)

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
| 404 | Resource not found | "Role not found" |
| 409 | Conflict (duplicate) | "Role name already exists" |
| 500 | Internal server error | "Internal server error" |

## Cluster-Specific Error Codes

### Validation Errors
- **ROLE_NAME_REQUIRED** (400): "name is required"
- **ROLE_LAYER_REQUIRED** (400): "layer is required"
- **ROLE_TYPE_REQUIRED** (400): "role_type is required"
- **ROLE_INVALID_LAYER** (400): "Invalid layer"

### Conflict Errors
- **ROLE_NAME_EXISTS** (400 or 409): "Role name already exists" (uniqueness per layer+tenant)

### Permission Errors
- **ROLE_PERMISSION_NOT_FOUND** (400): "Permission not found"
- **ROLE_PARENT_NOT_FOUND** (400): "Invalid parent role"

### System Role Errors
- **ROLE_SYSTEM_PROTECTED** (403): "System role cannot be deleted"
- **ROLE_SYSTEM_IMMUTABLE** (403): "System role cannot be modified"

### Hierarchy Errors
- **ROLE_CYCLE_DETECTED** (400): "Cannot create cycle"
- **ROLE_HAS_CHILDREN** (400): "Cannot delete role with assigned children"

### Tenant Errors
- **ROLE_TENANT_MISMATCH** (403): "Access denied"
- **ROLE_TENANT_NOT_FOUND** (404): "Tenant not found"

### Not Found Errors
- **ROLE_NOT_FOUND** (404): "Role not found"