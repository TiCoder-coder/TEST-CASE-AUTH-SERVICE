# SGOD AUTH SERVICE — TEST CASE DOCUMENTATION

> **End-to-End Postman Testing Guide · Environment Configuration · API Execution · Evidence · Verification · Security**
>
> Technical documentation for executing, validating, debugging, and maintaining the SGOD Auth Service positive-path test suite across local, development, and staging-oriented workflows.

<div align="center">

![Postman](https://img.shields.io/badge/Postman-API%20Testing-0b0f19?style=for-the-badge&logo=postman&logoColor=FF6C37&labelColor=0b0f19&color=FF6C37)
![Python](https://img.shields.io/badge/Python-Verification-0b0f19?style=for-the-badge&logo=python&logoColor=FFD43B&labelColor=0b0f19&color=3776AB)
![JSON](https://img.shields.io/badge/JSON-Collection%20%26%20Environment-0b0f19?style=for-the-badge&logo=json&logoColor=FFFFFF&labelColor=0b0f19&color=7A8B99)
![OpenAPI](https://img.shields.io/badge/OpenAPI-176%20Endpoints-0b0f19?style=for-the-badge&logo=swagger&logoColor=85EA2D&labelColor=0b0f19&color=85EA2D)
![Security](https://img.shields.io/badge/Security-Secret%20Aware-0b0f19?style=for-the-badge&logo=owasp&logoColor=FF728F&labelColor=0b0f19&color=FF728F)

</div>

<div align="center">

| **176** API Endpoints | **180** Positive Test Cases | **181** Postman Items | **11** Functional Clusters |
|:---:|:---:|:---:|:---:|
| **17** Swagger Tags | **40** Markdown Files | **21** Python Files | **33** Evidence Markdown Files |

</div>

---

## 🧭 MỤC LỤC (TABLE OF CONTENTS)

| # | Mục | Mô tả |
|---|---|---|
| [01](#01-tổng-quan-overview) | **Tổng quan** | Overview · Scope · Audience |
| [02](#02-cấu-trúc-thư-mục-folder-structure) | **Cấu trúc thư mục** | Folder Structure |
| [03](#03-tải--cài-đặt-postman-download--install) | **Tải & cài đặt Postman** | Download & Install |
| [04](#04-khởi-động-postman-lần-đầu-first-time-setup) | **Khởi động lần đầu** | First-time Setup |
| [05](#05-cấu-hình-environment-environment-configuration) | **Cấu hình Environment** | Environment Configuration |
| [06](#06-import-collection--environment-vào-postman) | **Import Collection & Environment** | Import Artifacts |
| [07](#07-cấu-hình-test-actor-accounts) | **Test Actor Accounts** | Cấu hình Actors |
| [08](#08-chạy-test-trong-postman-collection-runner) | **Collection Runner** | Chạy Test |
| [09](#09-đọc--phân-tích-kết-quả) | **Đọc & phân tích kết quả** | Result Analysis |
| [10](#10-verify-scripts-tự-động-c09-c10) | **Verify Scripts tự động** | C09/C10 Verification |
| [11](#11-quy-trình-nghiệp-vụ-test-workflow) | **Quy trình nghiệp vụ** | Workflow · Execution Order · Success Criteria · Reporting · Regression |
| [12](#12-security-rules--best-practices) | **Security Rules** | Best Practices |
| [13](#13-limitations--known-gaps) | **Limitations & Known Gaps** | Known Gaps |
| [14](#14-references) | **References** | Tài liệu tham chiếu |

---

## 01. TỔNG QUAN (OVERVIEW)

Đây là bộ **test case documentation đầy đủ** cho **SGOD Auth Service** — backend authentication service của hệ thống SGOD. Tài liệu được thiết kế để phục vụ đồng thời bốn nhóm người dùng chính:

- **Manual Tester**: mở Postman, import artifacts, cấu hình environment và chạy từng test case hoặc từng cluster.
- **Automation Engineer**: sử dụng Postman, Newman và Python verification scripts để tích hợp vào quy trình kiểm thử tự động / CI-CD.
- **Developer**: đọc API contract, request/response evidence và execution flow của **176 endpoints**.
- **QA Lead**: theo dõi coverage, execution evidence, defects, known gaps và reporting.

### 1.1 Test Suite at a Glance

| **176** API Endpoints | **180** Positive Test Cases | **181** Postman Items | **11** Functional Clusters |
|:---:|:---:|:---:|:---:|
| **17** Swagger Tags | **40** Markdown Files | **21** Python Files | **33** Evidence Markdown Files |

### 1.2 Phạm vi (Scope)

#### 1.2.1 Cluster scope

| Cluster | Mô tả | Endpoints | Test Cases |
|---|---|---:|---:|
| **C01** | Core Auth (Login, Session, MFA, Password, Activation) | 28 | 28 |
| **C02** | Enterprise Registration, Permissions, Email Verification | 20 | 20 |
| **C03** | Roles CRUD + Tree + IAM | 8 | 8 |
| **C04** | Departments CRUD + Tree + IAM | 8 | 8 |
| **C05** | Positions CRUD + Tree + IAM | 8 | 8 |
| **C06** | Enterprise Users (CRUD + Profile + IAM + Wallet) | 28 | 28 |
| **C07** | SGOD Users (CRUD + Profile + IAM + Permanent Delete) | 26 | 26 |
| **C08** | IAM Step-up MFA + SGOD Admins + Step-up Auth | 14 | 14 |
| **C09** | Sub-Enterprises (CRUD + Organizational + Bosses + Block) | 20 | 19 |
| **C10** | Tenant Management (CRUD + Subscription + Organizational) | 19 | 19 |
| **C11** | Audit Logs + Crypto (PoC) | 5 | 5 |

#### 1.2.2 Trong phạm vi (In-Scope)

- Toàn bộ **176 endpoint** từ 12 Swagger screenshots
- **180 positive test cases** (C09 có 20, các cluster khác 12–28) trong **11 clusters**
- **Authentication flows**: login 5 principal types, MFA, password, activation, session
- **IAM flows**: step-up, roles, departments, positions
- **Principal lifecycle**: CRUD, delete/restore, block/unblock
- **Organizational**: boss, department/position assignment
- **Tenant management**: assign/unassign, subscription, features
- **Audit logs** và **Crypto PoC**

#### 1.2.3 Ngoài phạm vi (Out-of-Scope, milestone này)

- Negative cases (invalid input, missing required, wrong type) — đã có skeleton ở `evidence/C09-*/negative-test-cases.csv` và `evidence/C10-*/negative-test-cases.csv`
- Security abuse cases (brute force, enumeration, replay)
- Cross-tenant denial
- Expired/revoked token
- Performance/load testing
- Contract của endpoint chưa freeze (`CONTRACT_PENDING`)

#### 1.2.4 Definition of Done (DoD)

| Trạng thái | Ý nghĩa |
|---|---|
| `POSITIVE-DESIGNED` | Contract reviewed, positive path designed, fixtures identified |
| `POSITIVE-TESTED` | Executed, actual recorded, all assertions PASS, evidence captured |
| `FAIL` | Actual không khớp expected; defect logged |
| `BLOCKED` | Contract pending, environment unavailable, hoặc dependency unmet |
| `NOT_RUN` | Planned but not executed yet |

#### 1.2.5 Verification Status (End-to-End scripts)

| Cluster | Script | Status |
|---|---|---|
| C09 | `scripts/verify/verify_c09_end_to_end.py` | ✅ ALL CHECKS PASSED |
| C10 | `scripts/verify/verify_c10_end_to_end.py` | ✅ ALL CHECKS PASSED |

Các cluster khác (C01–C08, C11) hiện tại chưa có end-to-end script; verify thủ công qua Postman.

### 1.3 Đối tượng & quyền đọc

| Audience | Section bắt đầu nên đọc |
|---|---|
| Manual tester mới | [03](#03-tải--cài-đặt-postman-download--install) → [08](#08-chạy-test-trong-postman-collection-runner) |
| Automation engineer | [09](#09-đọc--phân-tích-kết-quả) → [10](#10-verify-scripts-tự-động-c09-c10) |
| Developer đọc contract | [01](#01-tổng-quan-overview) → [`specifications/`](./specifications/) |
| QA Lead review | [11](#11-quy-trình-nghiệp-vụ-test-workflow) → [13](#13-limitations--known-gaps) |

> [!IMPORTANT]
> **Đây là positive-path test suite.** Các test case chỉ verify luồng thành công. Negative test, security abuse, performance và contract chi tiết hiện nằm trong `evidence/C09-*` và `evidence/C10-*` skeletons. Xem chi tiết tại [§ 13 Limitations](#13-limitations--known-gaps).

### 1.4 FE Mapping Status (S / T / G)

| Status | Ý nghĩa | Count |
|---|---|---:|
| **S** | Service/transport seen, runtime path proven | 142 |
| **T** | Refresh at transport layer only | 1 |
| **G** | No FE caller found (GAP) | 33 |
| **Tổng** | — | **176** |

**Implications:**

- **S (142)** — Verify cả API behavior + FE hook integration.
- **T (1)** — Verify API behavior only (transport layer refresh tự động).
- **G (33)** — Verify API behavior only; FE cần phát triển sau.

> [!TIP]
> Endpoint nào có status `G` thì chỉ cần assert ở API layer; FE caller chưa tồn tại nên không cần verify hook integration. Chi tiết gap cụ thể xem [§ 13.2 Known Gaps](#132-known-gaps-từ-fe-survey).

---

## 02. CẤU TRÚC THƯ MỤC (FOLDER STRUCTURE)

```text
docs/test-case/
├── README.md                              ← File này (entry point) — chứa test plan, execution order, success criteria
├── auth_test_cases.csv                    ← Master CSV — 180 test cases × 27 columns
│
├── specifications/                        ← Đặc tả kỹ thuật (5 files)
│   ├── endpoint_inventory.md              ← 176 endpoints × 11 clusters
│   ├── authentication_rules.md            ← Auth/MFA/session rules
│   ├── authorization_matrix.md            ← Permission/role/tenant isolation matrix
│   ├── test_data_strategy.md              ← 17 actors + fixtures + naming convention
│   └── contract_decisions.md              ← Contract freeze decisions & rationale
│
├── postman/                               ← Postman artifacts
│   ├── collections/
│   │   └── SGOD_Auth_Service.postman_collection.json
│   ├── environments/
│   │   ├── local.postman_environment.json
│   │   ├── dev.postman_environment.json
│   │   └── staging.postman_environment.json
│   └── scripts/                           ← Python refactor + verify scripts
│       ├── _paths.py                      ← Path resolver helper
│       ├── run.py                         ← Wrapper chạy tất cả scripts
│       ├── csv/                           ← CSV processing scripts
│       ├── postman/                       ← Postman JSON refactor scripts
│       └── verify/                        ← Verify C09/C10 end-to-end
│
└── evidence/                              ← Evidence per cluster (33 files)
    ├── C01-core-auth/
    │   ├── C01-core-auth-request-body-examples.md
    │   ├── C01-core-auth-success-responses.md
    │   ├── C01-core-auth-error-responses.md
    │   └── C01-core-auth-negative-test-cases.csv
    ├── C02-enterprise-email/
    ├── C03-roles/
    ├── C04-departments/
    ├── C05-positions/
    ├── C06-enterprise-users/
    ├── C07-sgod-users/
    ├── C08-admin-step-up/
    ├── C09-sub-enterprises/
    │   ├── C09-sub-enterprises-request-body-examples.md
    │   ├── C09-sub-enterprises-success-responses.md
    │   ├── C09-sub-enterprises-error-responses.md
    │   └── C09-sub-enterprises-negative-test-cases.csv
    ├── C10-enterprise-organizational/
    │   ├── C10-enterprise-organizational-request-body-examples.md
    │   ├── C10-enterprise-organizational-success-responses.md
    │   ├── C10-enterprise-organizational-error-responses.md
    │   └── C10-enterprise-organizational-negative-test-cases.csv
    └── C11-audit-crypto/
```

### 2.1 Vai trò của từng nhóm file

| Nhóm | File | Vai trò |
|---|---|---|
| **Master artifacts** | `auth_test_cases.csv` | Source of truth — 180 test cases × 27 columns |
| **Spec** | `specifications/*.md` | Đặc tả chi tiết endpoints, rules, fixtures |
| **Postman collection** | `postman/collections/*.json` | Collection v2.1.1 — 181 items, 11 folders |
| **Environment** | `postman/environments/*.json` | 3 environments: local, dev, staging |
| **Evidence** | `evidence/C<NN>-*/*.md` | Request bodies + Success responses + Error responses |
| **Scripts** | `postman/scripts/*.py` | Refactor + verify scripts (dùng `_paths.py`) |

### 2.2 Thống kê artifact

| Metric | Count |
|---|---:|
| Tổng file `.md` | 40 |
| Tổng file `.py` | 21 (20 scripts + 1 helper) |
| Tổng file `.json` (Postman) | 4 (1 collection + 3 environments) |
| Tổng file `.csv` | 3 (1 master + 2 negative skeletons của C09/C10) |
| Tổng evidence folders | 11 |
| Tổng lines (tất cả `.md`) | ~9,000 |

### 2.3 Data flow giữa các artifacts

```text
         ┌──────────────────────────────┐
         │      auth_test_cases.csv     │  180 rows × 27 cols
         │      (Source of truth)       │
         └──────────────────────────────┘
                      │
            ┌─────────┼─────────┐
            ▼         ▼         ▼
   ┌────────────┐ ┌────────┐ ┌────────────┐
   │ Spec .md   │ │ Build  │ │ Postman    │
   │ files      │ │ scripts│ │ Collection │
   └────────────┘ └────────┘ └────────────┘
            │         │         │
            └─────────┼─────────┘
                      ▼
         ┌──────────────────────────────┐
         │       Evidence files         │  Request / Success / Error
         └──────────────────────────────┘
```

| **CSV** Rows + Columns | → | **Postman** Items + Method + Path | → | **Evidence** Files + Coverage |
|:---:|:---:|:---:|:---:|:---:|

> [!IMPORTANT]
> `auth_test_cases.csv` là **source of truth** cho danh sách test case; collection là executable artifact; evidence dùng để đối chiếu request/response/error contract. Khi một artifact thay đổi, cần kiểm tra alignment với các artifact còn lại.

---

## 03. TẢI & CÀI ĐẶT POSTMAN (DOWNLOAD & INSTALL)

> **Nguồn chính thức:** [Postman Downloads](https://www.postman.com/downloads/) · [Postman Installation Guide](https://learning.postman.com/docs/getting-started/installation/install-app/) · [System Requirements](https://learning.postman.com/docs/getting-started/installation/system-requirements/)

### 3.1 Chọn phương thức sử dụng

| Phương thức | Khi nên dùng | Khuyến nghị cho suite này |
|---|---|---|
| **Postman Desktop App** | Test local/DEV, chạy collection lớn, export run results | **Khuyến nghị chính** |
| **Postman Web App** | Test nhanh trên browser, làm việc cloud/team | Dùng được, nên cài **Desktop Agent** |
| **Newman / Postman CLI** | Automation, CI/CD, headless execution | Dùng cho automation/reporting |

### 3.2 Chọn hệ điều hành và kiến trúc

Postman Desktop hiện hỗ trợ **Windows, macOS và Linux** trên các kiến trúc phổ biến.

| OS | Kiến trúc | Cách xác định nhanh | Link chính thức |
|---|---|---|---|
| **macOS** | Apple silicon (M-series) |  → **About This Mac** → Chip | [Download Postman](https://www.postman.com/downloads/) |
| **macOS** | Intel |  → **About This Mac** → Processor | [Download Postman](https://www.postman.com/downloads/) |
| **Windows** | x64 / ARM64 | Settings → System → About → System type | [Download Postman](https://www.postman.com/downloads/) |
| **Linux** | x64 / ARM64 | `uname -m` | [Download Postman](https://www.postman.com/downloads/) |

```bash
# Linux architecture check
uname -m
# x86_64  -> x64
# aarch64 -> ARM64
```

### 3.3 Cài đặt trên macOS

#### Cách A — Download trực tiếp

1. Truy cập **[Postman Downloads](https://www.postman.com/downloads/?utm_source=chatgpt.com)**.
2. Chọn đúng bản **Apple silicon** hoặc **Intel** theo chip máy.
3. Nếu trình duyệt tải file `.zip`, giải nén trong thư mục **Downloads**.
4. Mở Postman và khi được hỏi, chuyển `Postman.app` vào **Applications**.
5. Mở **Applications → Postman**.

#### Cách B — Homebrew

```bash
brew install --cask postman
```

> [!NOTE]
> Postman hiện hỗ trợ **macOS 11 (Big Sur) trở lên**. Nếu macOS chặn ứng dụng, kiểm tra **System Settings → Privacy & Security** và chỉ cho phép mở khi file được tải từ nguồn Postman chính thức.

### 3.4 Cài đặt trên Windows

1. Tải installer từ **[Postman Downloads](https://www.postman.com/downloads/?utm_source=chatgpt.com)**.
2. Chọn đúng kiến trúc **Intel 64-bit (x64)** hoặc **ARM 64-bit**.
3. Chạy file `.exe` và hoàn tất cài đặt.
4. Mở Postman từ **Start Menu**.

> [!NOTE]
> Postman hỗ trợ **Windows 10 trở lên**.

### 3.5 Cài đặt trên Linux

#### Cách A — Snap (khuyến nghị bởi Postman)

```bash
sudo snap install postman
```

#### Cách B — Tarball

```bash
# Ví dụ x64. Luôn ưu tiên lấy link mới nhất từ Postman Downloads.
wget https://dl.pstmn.io/download/latest/linux_64 -O postman.tar.gz
sudo tar -xzf postman.tar.gz -C /opt/
sudo ln -s /opt/Postman/Postman /usr/local/bin/postman
postman
```

> [!WARNING]
> Không khởi chạy Postman bằng `sudo`. Trên Linux cần bảo đảm user có quyền đọc/ghi với `~/.config` và hệ thống có `openssl`.

### 3.6 Sử dụng Postman Web App

Nếu không muốn cài Desktop App, có thể sử dụng [Postman Web App](https://web.postman.co/).

Đối với request tới backend local/localhost, nên cài **Postman Desktop Agent** để vượt qua các giới hạn CORS của browser và cho phép Web App gửi request thông qua agent chạy trên máy.

**Luồng:**

| **Browser** Postman Web App | → | **Desktop Agent** Local request bridge | → | **SGOD Auth BE** `localhost / DEV` |
|:---:|:---:|:---:|:---:|:---:|

### 3.7 Yêu cầu hệ thống và khuyến nghị project

| Hạng mục | Yêu cầu / khuyến nghị |
|---|---|
| **Windows** | Windows 10+ |
| **macOS** | macOS 11 (Big Sur)+ |
| **Linux** | Ubuntu 18.04+, Fedora 32+, Debian 10+ |
| **Browser** | Chrome 80+, Firefox 76+, Edge 79+, Safari 13.1.1+ |
| **RAM** | Project recommendation: ≥ 4 GB, khuyến nghị 8 GB+ cho collection lớn |
| **Disk** | Project recommendation: duy trì đủ dung lượng trống để persist response/logs |
| **Network** | Cần internet nếu dùng sync/team/cloud; local-only flow có thể hoạt động không cần sync |

### 3.8 Tài khoản Postman: bắt buộc hay tùy chọn?

- **Desktop App**: có thể **Skip sign-in** và dùng app ở chế độ local cho nhiều tác vụ API cơ bản.
- **Tài khoản Postman**: nên dùng khi cần sync, team workspace, collaboration hoặc cloud features.
- **Web App**: sử dụng theo luồng đăng nhập Postman.

> [!TIP]
> Với SGOD Auth Service, nếu chỉ chạy local test cá nhân, Desktop App + local environment là luồng đơn giản nhất. Nếu team cần chia sẻ collection/environment, đăng nhập và dùng workspace chung sẽ thuận tiện hơn.

### 3.9 Checklist sau khi cài

- [ ] Postman mở được bình thường.
- [ ] Có thể truy cập **Collections** và **Environments**.
- [ ] Nếu dùng Web App để test local: Desktop Agent đã chạy.
- [ ] Đã xác định đúng workspace sẽ import SGOD artifacts.
- [ ] Chưa nhập bất kỳ production credential nào.

---

## 04. KHỞI ĐỘNG POSTMAN LẦN ĐẦU (FIRST-TIME SETUP)

### 4.1 Mở Postman

- **macOS**: Applications / Launchpad → **Postman**.
- **Windows**: Start → tìm **Postman**.
- **Linux**: mở launcher hoặc chạy `postman` trong Terminal.

### 4.2 Nhận diện các khu vực chính

| Khu vực | Vai trò trong SGOD test suite |
|---|---|
| **Sidebar / Items** | Mở Collections, Environments, History và các resource liên quan. |
| **Workbench** | Chỉnh request, headers, body, authorization, scripts và đọc response. |
| **Environment selector** | Chọn `SGOD - Local`, `SGOD - Dev` hoặc `SGOD - Staging`. |
| **Console** | Debug URL, headers, scripts, variables và runtime errors. |
| **Runner** | Chạy folder/collection theo thứ tự và xem pass/fail. |

### 4.3 Tạo hoặc chọn Workspace

Workspace dùng để nhóm collection, environment và lịch sử làm việc theo project/team.

1. Mở workspace selector trong Postman.
2. Dùng **My Workspace** nếu test cá nhân, hoặc tạo workspace mới cho team.
3. Nếu tạo mới, đặt tên gợi ý: `SGOD Auth Service`.
4. Chọn đúng workspace **trước khi import** để tránh collection/environment nằm sai nơi.

### 4.4 Chọn chiến lược cấu hình

Có hai cách hợp lệ:

| Chiến lược | Cách làm | Khi dùng |
|---|---|---|
| **Import-first** | Import collection + file environment có sẵn trong repo | **Khuyến nghị** |
| **Manual setup** | Tạo environment mới rồi nhập từng variable | Khi file environment chưa có hoặc cần debug |

### 4.5 Preflight trước khi import

- [ ] Đã clone/open đúng repository chứa `docs/test-case/`.
- [ ] Đã xác định target environment: **Local / Dev / Staging**.
- [ ] Đã biết `baseUrlAuth` tương ứng.
- [ ] Có `authApiKey` từ BE/team secret store nếu endpoint yêu cầu.
- [ ] Không sử dụng production credentials.

---

## 05. CẤU HÌNH ENVIRONMENT (ENVIRONMENT CONFIGURATION)

Environment là tập biến được Postman resolve vào request tại runtime. Với SGOD Auth Service, environment giữ **base URL, API key, session tokens, actor credentials, IDs sinh động trong quá trình chạy và MFA data**.

### 5.1 Variable scope và precedence

Khi nhiều scope có cùng tên biến, scope hẹp hơn có precedence cao hơn. Theo Postman hiện tại, thứ tự từ **cao → thấp** là:

| Priority | Scope | Phạm vi |
|---:|---|---|
| **1** | **Local** | Giá trị tạm thời trong request/collection run |
| **2** | **Data** | Dữ liệu iteration từ CSV/JSON/dataset trong Runner |
| **3** | **Environment** | Environment đang active |
| **4** | **Collection** | Toàn collection |
| **5** | **Global** | Toàn workspace |

> [!NOTE]
> **Postman Vault** là cơ chế riêng cho secret, không nên xem như một dòng trong precedence table ở trên. Dynamic variables (`{{$random...}}`) cũng là nhóm riêng.

### 5.2 Local Value, Shared Value và Secure Variable

Postman hiện dùng mô hình:

- **Local value**: mặc định chỉ tồn tại trên instance Postman của người dùng, không tự động sync lên cloud.
- **Shared value**: chỉ được đồng bộ khi người dùng chủ động share; một số cloud features sử dụng shared value.
- **Secure variable**: dùng cho dữ liệu nhạy cảm; UI sẽ bảo vệ/mask giá trị.
- **Postman Vault**: lựa chọn mạnh hơn cho secret cần tách khỏi environment/collection thông thường.

> [!CAUTION]
> Không share `authApiKey`, password, access token, refresh token, TOTP secret hoặc recovery code lên workspace nếu không có quy trình quản lý secret được team phê duyệt.

### 5.3 Cách khuyến nghị — Import Environment có sẵn

Repository đã có ba file:

```text
docs/test-case/postman/environments/
├── local.postman_environment.json
├── dev.postman_environment.json
└── staging.postman_environment.json
```

Quy trình:

1. Mở **Import** trong workspace.
2. Chọn đúng file environment cần dùng.
3. Sau import, mở **Environments** và chọn environment vừa import.
4. Điền **local values** còn thiếu như `authApiKey`, actor credentials và MFA secret.
5. Chọn environment đó bằng selector ở góc trên của workbench.
6. Mở Variables pane để kiểm tra không còn variable bắt buộc nào unresolved.

### 5.4 Cách thay thế — Tạo Environment thủ công

1. Mở **Environments**.
2. Tạo environment mới.
3. Đặt tên: `SGOD - Local`, `SGOD - Dev` hoặc `SGOD - Staging`.
4. Thêm các biến bên dưới.

| Variable | Suggested Local Value | Sensitive | Nguồn / thời điểm điền |
|---|---|:---:|---|
| `baseUrlAuth` | `http://localhost:3000` | No | Theo target BE |
| `authApiKey` | `<your-api-key-here>` | **Yes** | BE team / secret store |
| `lang` | `vi` | No | Static |
| `runId` | *(empty)* | No | Pre-request script |
| `deviceId` | *(empty)* | No | Pre-request script |
| `accessToken` | *(empty)* | **Yes** | Login response |
| `refreshToken` | *(empty)* | **Yes** | Login response |
| `interimToken` | *(empty)* | **Yes** | MFA flow |
| `tenantId` | *(empty)* | No | API response |
| `actorEmail` | `<actor-email>` | **Yes** | Seed/test data |
| `actorPassword` | `<actor-password>` | **Yes** | Seed/test data |
| `currentTotp` | *(empty)* | **Yes** | Generate per operation |
| `mfa_secret_key` | `<MFA_TARGET_secret>` | **Yes** | MFA enrollment |
| `user_id` | *(empty)* | No | Create response |
| `target_user_id` | *(empty)* | No | Create response |
| `role_parent_id` | *(empty)* | No | IAM flow |
| `role_child_id` | *(empty)* | No | IAM flow |
| `dept_parent_id` | *(empty)* | No | IAM flow |
| `dept_child_id` | *(empty)* | No | IAM flow |
| `pos_parent_id` | *(empty)* | No | IAM flow |
| `pos_child_id` | *(empty)* | No | IAM flow |

> [!TIP]
> Đánh dấu các biến nhạy cảm là **Secure** hoặc chuyển secret quan trọng sang **Postman Vault**. Không đặt giá trị thật vào file environment được commit vào Git.

### 5.5 Chọn Environment đang active

1. Dùng **environment selector** ở góc trên của workbench.
2. Chọn `SGOD - Local`, `SGOD - Dev` hoặc `SGOD - Staging`.
3. Hover hoặc mở **Variables pane** để xác nhận Postman resolve đúng giá trị.

Ví dụ set biến bằng script:

```javascript
pm.environment.set("runId", "tc-run-20261007-001");
```

### 5.6 Dùng biến trong request

**URL**

```text
{{baseUrlAuth}}/sgod-auth/v1/enterprise-users/sessions
```

**Headers**

```text
x-api-key: {{authApiKey}}
x-device-id: {{deviceId}}
Authorization: Bearer {{accessToken}}
```

**Body**

```json
{
  "credential": "{{actorEmail}}",
  "password": "{{actorPassword}}"
}
```

### 5.7 Auto-generate `runId` và `deviceId`

Mở collection → **Scripts → Pre-request** và dùng:

```javascript
if (!pm.environment.get("runId")) {
  const now = new Date();
  const dateStr = now.toISOString().slice(0, 10).replace(/-/g, "");
  const random = Math.random().toString(36).substring(2, 8);
  pm.environment.set("runId", `tc-run-${dateStr}-${random}`);
}

if (!pm.environment.get("deviceId")) {
  pm.environment.set(
    "deviceId",
    `dev-${Math.random().toString(36).substring(2, 14)}`
  );
}
```

Generate thủ công khi cần:

```bash
# macOS / Linux
uuidgen | tr 'A-Z' 'a-z'

# Python
python3 -c "import uuid; print(f'tc-run-{uuid.uuid4().hex[:12]}')"
```

### 5.8 Environment preflight checklist

Trước khi chạy request đầu tiên:

- [ ] Đúng environment đang active.
- [ ] `baseUrlAuth` trỏ đúng Local/DEV/Staging.
- [ ] `authApiKey` có local value hợp lệ nếu required.
- [ ] `actorEmail` và `actorPassword` đúng actor cần test.
- [ ] `runId` và `deviceId` đã có giá trị.
- [ ] Không có placeholder bắt buộc dạng `<...>` còn sót.
- [ ] Không có secret thật được share/commit ngoài quy trình cho phép.

---

## 06. IMPORT COLLECTION & ENVIRONMENT VÀO POSTMAN

### 6.1 Artifact cần import

**Collection**

```text
docs/test-case/postman/collections/
└── SGOD_Auth_Service.postman_collection.json
```

**Environment**

```text
docs/test-case/postman/environments/
├── local.postman_environment.json
├── dev.postman_environment.json
└── staging.postman_environment.json
```

> [!IMPORTANT]
> Chỉ cần import **environment phù hợp với target đang test**. Không cần active đồng thời cả ba environment.

### 6.2 Mở Import

Trong workspace, chọn **Import** / **Use resources or import**, sau đó có thể:

- chọn file/folder;
- kéo thả file vào cửa sổ import;
- paste raw text hoặc URL khi phù hợp.

### 6.3 Import Collection

1. Chọn `SGOD_Auth_Service.postman_collection.json`.
2. Xác nhận import vào đúng workspace.
3. Sau khi hoàn tất, kiểm tra collection xuất hiện trong **Collections**.
4. Expand collection và xác nhận đủ **11 folders**.

```text
📁 SGOD_Auth_Service
├── 📁 C01 — Core Auth
├── 📁 C02 — Enterprise / Permission / Email
├── 📁 C03 — Roles
├── 📁 C04 — Departments
├── 📁 C05 — Positions
├── 📁 C06 — Enterprise Users
├── 📁 C07 — SGOD Users
├── 📁 C08 — IAM Step-up + SGOD Admins
├── 📁 C09 — Sub-Enterprises
├── 📁 C10 — Tenant Management / Organizational
└── 📁 C11 — Audit Logs / Crypto
```

Collection artifact hiện có **181 items** trên **11 folders**; master positive-test CSV có **180 test cases**.

### 6.4 Import Environment

1. Mở **Import** lần nữa.
2. Chọn một trong các file `local`, `dev`, `staging`.
3. Mở **Environments** và kiểm tra variable names.
4. Điền local secret values còn trống.
5. Chọn environment vừa import làm **active environment**.

### 6.5 Mở request đầu tiên

1. Expand `C01 — Core Auth`.
2. Mở request **``1. LOGIN — Enterprise Sessions``**.
3. Kiểm tra:
   - **Method**: `POST`
   - **URL**: `{{baseUrlAuth}}/sgod-auth/v1/enterprises/sessions`
   - **Headers**: `x-api-key`, `Content-Type`
   - **Body**: JSON có `credential` và `password`
4. Hover các `{{variables}}` để bảo đảm chúng resolve đúng giá trị.

### 6.6 Collection-level configuration

Ở collection level, kiểm tra các nhóm cấu hình sau:

| Khu vực | Mục đích |
|---|---|
| **Authorization** | Auth mặc định nếu collection sử dụng inheritance |
| **Variables** | Biến dùng chung trong collection |
| **Scripts → Pre-request** | Khởi tạo `runId`, `deviceId` hoặc data động |
| **Scripts → Post-response** | Assertions, lưu token/ID, chaining |
| **Documentation** | Mô tả collection/request |

### 6.7 Post-import verification

- [ ] Collection xuất hiện đúng workspace.
- [ ] Có **11 cluster folders**.
- [ ] Environment target đã import và active.
- [ ] `{{baseUrlAuth}}` resolve đúng.
- [ ] Không có unresolved variable quan trọng.
- [ ] Request đầu tiên có method/path/body đúng.
- [ ] Secret values chỉ tồn tại local/secure/vault theo chính sách team.

---

## 07. CẤU HÌNH TEST ACTOR ACCOUNTS

Để chạy test, bạn cần **17 test actors** (tài khoản test) trong database. Chi tiết xem: [`specifications/test_data_strategy.md`](./specifications/test_data_strategy.md).

### 7.1 Tạo actors

#### A. Trên **DEV environment**

DEV thường có sẵn script seed data. Liên hệ BE team để:

1. **Tạo tài khoản** cho 17 actors trong bảng `users` (hoặc tương đương).
2. **MFA enrollment** cho actors có MFA.
3. **Tenant setup**: Tạo ENTERPRISE_A, ENTERPRISE_B.
4. **Role/Department/Position fixtures**: Seed theo `test_data_strategy.md`.
5. **Boss relationship**: MANAGER → EMPLOYEE.

#### B. Trên **Local environment**

Nếu chạy BE local, bạn cần:

1. **Chạy migration scripts** để tạo tables.
2. **Chạy seed scripts** để tạo actors.
3. **Manual MFA enrollment** qua UI hoặc API.

### 7.2 Lấy credentials thật

Sau khi actors đã tồn tại trong DB, lấy credentials thật:

1. **Email**: `{{runId}}-actor@sgod.test` (theo convention).
2. **Password**: Lấy từ DB owner (hoặc dùng password mặc định).
3. **MFA secret key**: Từ enrollment response, lưu vào `mfa_secret_key` variable.

### 7.3 Inject credentials vào Environment

Mở environment `SGOD - Local` và update các biến:

| Variable | Giá trị | Lưu ý |
|---|---|---|
| `actorEmail` | `ENT_USER_A_email_thật` | Từ DB |
| `actorPassword` | `password_thật` | Từ DB |
| `mfa_secret_key` | `JBSWY3DPEHPK3PXP...` | Từ MFA enrollment |
| `authApiKey` | `x-api-key_thật` | Từ BE team |

> [!CAUTION]
> **KHÔNG commit credential thật vào Git.** Ưu tiên local value + Secure variable hoặc Postman Vault. Chỉ share secret khi team có quy trình quản lý secret được phê duyệt.

### 7.4 Generate `actorEmail` động (nếu cần)

Nếu BE tạo actor mới mỗi lần chạy, dùng pattern:

```javascript
// Trong pre-request script
const runId = pm.environment.get("runId");
pm.environment.set("actorEmail", `${runId}-actor@sgod.test`);
pm.environment.set("targetEmail", `${runId}-target@sgod.test`);
```

### 7.5 Actor readiness checklist

- [ ] Đủ **17 test actors** theo `test_data_strategy.md`.
- [ ] ENTERPRISE_A / ENTERPRISE_B và tenant relationship đã seed đúng.
- [ ] Role / Department / Position fixtures đã tồn tại.
- [ ] Boss relationship MANAGER → EMPLOYEE đã sẵn sàng.
- [ ] Actor có MFA đã enrollment và có secret tương ứng.
- [ ] Credential local trong Postman khớp seed data.
- [ ] Không actor nào vô tình trỏ tới production identity.

---

## 08. CHẠY TEST TRONG POSTMAN (COLLECTION RUNNER)

### 8.1 Chạy một request

1. Mở request cần test, ví dụ `1. LOGIN — Enterprise Sessions`.
2. Kiểm tra environment đang active.
3. Kiểm tra URL/headers/body đã resolve variables.
4. Click **Send**.
5. Đọc response và **Test Results** / post-response assertions.

Response viewer thường cho phép kiểm tra:

- status code;
- response time;
- response size;
- body;
- headers;
- cookies;
- test/assertion results;
- visualization nếu request có `pm.visualizer`.

### 8.2 Chạy một folder

1. Trong **Collections**, chọn folder, ví dụ `C01 — Core Auth`.
2. Click **Run**.
3. Chọn **Functional → Local** khi chạy local Collection Runner.
4. Chọn đúng environment ở environment selector.
5. Cấu hình Runner rồi click **Start run**.

> [!TIP]
> Đối với suite này, chạy **theo folder/cluster** giúp cô lập lỗi tốt hơn chạy toàn bộ 181 items ngay từ đầu.

### 8.3 Cấu hình Collection Runner

| Option | Giá trị khuyến nghị | Ý nghĩa |
|---|---|---|
| **Environment** | `SGOD - Local` / `Dev` / `Staging` | Environment cho toàn run |
| **Iterations** | `1` | Số vòng chạy suite |
| **Delay** | `0 ms` mặc định | Delay trước mỗi request; tăng nếu cần giảm áp lực/rate-limit |
| **Iteration data** | Empty | Chỉ dùng khi chạy CSV/JSON/dataset |
| **Persist responses for a session** | **On** khi debug | Giữ request/response để review trong session |
| **Turn off logs during run** | Off khi debug | Bật chỉ khi cần tối ưu large run |
| **Stop run if an error occurs** | Tùy mục tiêu | Dừng khi script/request gặp error |
| **Keep variable values** | **On** nếu flow cần giữ token/ID sau run | Persist local variable changes sau run |
| **Run without stored cookies** | Off mặc định | Dùng khi muốn vô hiệu cookie store |
| **Save cookies after collection run** | Theo flow | Giữ cookie changes trong Cookie Manager |

### 8.4 Recommended execution mode cho SGOD

| **SMOKE** C01 | → | **FOUNDATION** C02 + C08 + C03–C05 | → | **LIFECYCLE** C06–C09 | → | **TENANT / AUDIT** C10–C11 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|

### 8.5 Chạy full collection

Sau khi các cluster riêng lẻ chạy ổn định:

1. Chọn collection root `SGOD_Auth_Service`.
2. Click **Run**.
3. Giữ execution order theo dependency của Section 11.
4. Chạy **1 iteration** trước.
5. Nếu collection lớn gây memory pressure, tắt **Persist responses** hoặc **Turn off logs during run**, hoặc chia thành các run nhỏ hơn.

### 8.6 Dừng / hủy Runner

Nếu phát hiện environment sai, credential sai hoặc side effect không mong muốn:

1. Stop run ngay.
2. Kiểm tra request cuối cùng đã chạy.
3. Kiểm tra variables/cookies đã bị thay đổi hay chưa.
4. Cleanup state nếu cần.
5. Chỉ rerun sau khi root cause được xác định.

---

## 09. ĐỌC & PHÂN TÍCH KẾT QUẢ

### 9.1 Response Viewer

| Khu vực | Mô tả | Khi dùng |
|---|---|---|
| **Body / Pretty** | JSON/XML/HTML formatted | Đọc payload chính |
| **Raw** | Plain response | Debug encoding/raw content |
| **Preview** | Render HTML khi phù hợp | Response dạng HTML |
| **Headers** | Response headers | Debug CORS, cache, content type |
| **Cookies** | Cookie state | Verify cookie/session flow |
| **Test Results** | Assertions pass/fail | Kiểm tra contract logic |
| **Visualize** | Custom view từ `pm.visualizer` | Khi request có visualization script |

### 9.2 Status codes thường gặp

| Code | Ý nghĩa | Expected trong test |
|---:|---|---|
| **200** | OK | Success thông thường |
| **201** | Created | Tạo resource mới |
| **204** | No Content | Delete/action thành công không có body |
| **400** | Bad Request | Validation error trong negative test |
| **401** | Unauthorized | Missing/invalid/expired auth |
| **403** | Forbidden | Không đủ quyền |
| **404** | Not Found | Resource/path không tồn tại |
| **409** | Conflict | Duplicate/state conflict |
| **429** | Too Many Requests | Rate limit |
| **500** | Internal Server Error | Backend error/defect cần điều tra |

### 9.3 Đọc JSON Response

Ví dụ response 200 OK từ `POST /enterprise-users/sessions`:

```json
{
  "success": true,
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "interimToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "mfaRequired": false,
    "expiresIn": 3600,
    "user": {
      "id": "uuid-abc-123",
      "email": "user@example.com",
      "userName": "username",
      "fullName": {
        "firstName": "First",
        "lastName": "Last"
      },
      "tenantId": "tenant-uuid-456",
      "userType": "enterprise_user"
    }
  },
  "message": "Login successful",
  "timestamp": "2026-10-07T10:00:00.000Z"
}
```

**Các field cần assert:**

- `success`: `true`.
- `data.accessToken`: present, string, non-empty.
- `data.refreshToken`: present, string, non-empty.
- `data.mfaRequired`: đúng với actor/flow.
- `data.user.id`: đúng format contract.
- `data.user.email`: match input.

### 9.4 Lưu giá trị từ response — Scripts → Post-response

Postman hiện đặt test/assertion scripts ở **Scripts → Post-response**.

```javascript
const json = pm.response.json();

pm.environment.set("accessToken", json.data.accessToken);
pm.environment.set("refreshToken", json.data.refreshToken);
pm.environment.set("user_id", json.data.user.id);
pm.environment.set("tenantId", json.data.user.tenantId);

pm.test("Login successful", function () {
  pm.response.to.have.status(200);
  pm.expect(json.success).to.eql(true);
  pm.expect(json.data.accessToken).to.be.a("string");
  pm.expect(json.data.accessToken.length).to.be.greaterThan(0);
});

pm.test("User has tenant", function () {
  pm.expect(json.data.user.tenantId).to.be.a("string");
  pm.expect(json.data.user.userType).to.eql("enterprise_user");
});
```

### 9.5 Đọc Collection Runner Results

Sau run, tập trung vào:

- test count và failed assertions;
- request errors;
- total duration;
- average response time;
- environment đã dùng;
- iteration number;
- request/response details nếu bật **Persist responses for a session**;
- **Console log** nếu cần debug script.

**Ví dụ logic đọc kết quả:**

```text
C01 — Core Auth
├── Request 01  POST /enterprise-users/sessions   ✅ 200
├── Request 02  GET  /users/myself                ✅ 200
├── ...
└── Request 28  GET  /dev/emails                  ❌ 500
```

Khi một request fail, click request đó để đối chiếu **request → response → test assertion → runtime variables**.

### 9.6 Export Results

#### A. Postman Desktop App

Collection Runner cho phép **Export run results** từ menu của run. Tính năng export run results khả dụng trên Desktop App; Web App không có cùng export flow.

#### B. JSON / JUnit cho automation

Nếu cần machine-readable report cho CI/CD, dùng Newman reporters:

```bash
# JSON + CLI
newman run SGOD_Auth_Service.postman_collection.json \
  -e local.postman_environment.json \
  -r cli,json \
  --reporter-json-export artifacts/sgod-auth-run.json

# JUnit + CLI
newman run SGOD_Auth_Service.postman_collection.json \
  -e local.postman_environment.json \
  -r cli,junit \
  --reporter-junit-export artifacts/sgod-auth-junit.xml
```

> [!NOTE]
> Không commit environment file chứa secret thật vào repository chỉ để chạy Newman. Trong CI/CD, inject secrets bằng cơ chế secret management của pipeline.

### 9.7 Debug khi gặp lỗi

Kiểm tra theo thứ tự:

1. **Environment**: đúng target chưa?
2. **Variable resolution**: có `{{...}}` nào unresolved không?
3. **Status code**: 4xx hay 5xx?
4. **Response body**: backend trả error contract gì?
5. **Postman Console**: URL thực tế, headers, script error.
6. **Authorization**: API key/token/cookie có đúng context không?
7. **Dependency**: request trước đó có tạo token/ID/resource cần cho request hiện tại không?
8. **Assertion**: lỗi do backend hay do expected value trong script?

| Symptom | Kiểm tra đầu tiên |
|---|---|
| `401 Unauthorized` | token/API key/session context |
| `403 Forbidden` | role/permission/tenant |
| `404 Not Found` | `baseUrlAuth`, path, resource ID |
| `409 Conflict` | duplicate resource / lifecycle state |
| `429 Too Many Requests` | rate limit / delay |
| `500 Internal Server Error` | backend log + request evidence + defect report |

---

## 10. VERIFY SCRIPTS TỰ ĐỘNG (C09, C10)

Ngoài chạy trên Postman UI, có 2 **Python scripts** verify end-to-end CSV ↔ Postman ↔ Evidence alignment.

### 10.1 Verify C09

```bash
# Từ repo root (SAM-V2/)
python3 docs/test-case/postman/scripts/run.py verify/verify_c09_end_to_end.py
```

**Output mong đợi:**

```text
[OK] CSV total rows: 180, C09 rows: 20
[OK] Postman C09 items: 20
[OK] CSV ↔ Postman name alignment (20 items)
[OK] Evidence file: C09-sub-enterprises-request-body-examples.md (9215 bytes)
[OK] Evidence file: C09-sub-enterprises-success-responses.md (11581 bytes)
[OK] Evidence file: C09-sub-enterprises-error-responses.md (2229 bytes)
[OK] Evidence file: C09-sub-enterprises-negative-test-cases.csv (4283 bytes)

============================================================
✅ ALL CHECKS PASSED
```

### 10.2 Verify C10

```bash
python3 docs/test-case/postman/scripts/run.py verify/verify_c10_end_to_end.py
```

**Output mong đợi:**

```text
✅ CSV: 19 C10 rows found
✅ CSV: all 19 rows have aligned columns
✅ Postman: 19 C10 items found
✅ CSV ↔ Postman: 19 endpoints match (method + path structure)
✅ Evidence request-body: 19 endpoints documented
✅ Evidence success-responses: 19 endpoints documented
✅ Evidence: removed endpoints (bosses/add, bosses, subordinates) purged
✅ Negative CSV: 20 rows × 20 cols

✅ ALL C10 VERIFICATIONS PASSED
```

### 10.3 Ý nghĩa

Verify scripts check:

- **CSV có đúng số rows** cho cluster.
- **CSV columns aligned** (không bị shift).
- **Postman có đúng số items** cho cluster.
- **CSV `Postman Request Name` match** Postman `item.name`.
- **Evidence files tồn tại** + size &gt; 500 bytes.

**KHÔNG check:**

- Body content match (cần chạy Postman Runner).
- Response schema (cần execute thật).
- Side effects (cần test integration).

### 10.4 Troubleshooting scripts

| Lỗi | Nguyên nhân | Cách fix |
|---|---|---|
| `ModuleNotFoundError: No module named '_paths'` | Python không tìm thấy `_paths.py` | Luôn dùng `run.py` wrapper |
| `FileNotFoundError: ...auth_test_cases.csv` | Path sai | Kiểm tra `_paths.py` |
| `KeyError: 'AUTH-C09-...'` | CSV column shift | Chạy `repair_c09_column_shifts.py` |
| `JSON decode error` | Postman collection bị corrupt | Re-import collection |

### 10.5 Verification gate

| **CSV** Rows + Columns | → | **POSTMAN** Items + Method + Path | → | **EVIDENCE** Files + Coverage | → | **PASS** Alignment Gate |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|

> [!IMPORTANT]
> `ALL CHECKS PASSED` xác nhận **artifact alignment** cho phạm vi script kiểm tra; nó không thay thế execution thật của API, response-schema validation hoặc integration side-effect verification.

---

## 11. QUY TRÌNH NGHIỆP VỤ TEST (WORKFLOW)

### 11.1 End-to-End Workflow

| | | | | |
|:---:|:---:|:---:|:---:|:---:|
| **STEP 1** 🧰 PREPARE<br/>Install Postman · Choose workspace | → | **STEP 2** ⚙️ ENVIRONMENT<br/>Import env · URL · secrets | → | **STEP 3** 📦 COLLECTION<br/>Import · verify 11 folders |
| **STEP 6** 📊 EVIDENCE<br/>Results · logs · defects | ← | **STEP 5** ▶️ EXECUTE<br/>C01 → C11 by dependency | ← | **STEP 4** 👥 ACTORS<br/>17 actors · MFA · fixtures |
| | | ↓ | | |
| | | **STEP 7** ✅ VERIFY<br/>C09/C10 scripts · confirm alignment | | |

#### Step 1 — Chuẩn bị

- Cài Postman Desktop hoặc chuẩn bị Web App + Desktop Agent.
- Chọn/tạo workspace `SGOD Auth Service`.
- Xác định Local / Dev / Staging target.

#### Step 2 — Cấu hình Environment

- Import environment file hoặc tạo thủ công.
- Set `baseUrlAuth`, `authApiKey`, actor credentials.
- Generate `runId`, `deviceId`.
- Chọn environment active.

#### Step 3 — Import Collection

- Import `SGOD_Auth_Service.postman_collection.json`.
- Xác nhận 11 folders và collection structure.
- Kiểm tra request đầu tiên resolve đúng variable.

#### Step 4 — Setup Actors

- Seed 17 test actors.
- Setup tenant/role/department/position fixtures.
- MFA enrollment cho actor cần MFA.
- Inject credentials vào local environment.

#### Step 5 — Chạy Test

- C01 trước để xác nhận authentication foundation.
- Chạy các phase còn lại theo execution order bên dưới.
- Chỉ chạy full suite sau khi các dependency chính ổn định.

#### Step 6 — Ghi nhận Kết quả

- Review pass/fail và failed assertions.
- Persist/export run results khi cần.
- Lưu request/response evidence theo chính sách redact.
- Log defect nếu backend behavior lệch contract.

#### Step 7 — Verify Post-execution

```bash
python3 docs/test-case/postman/scripts/run.py verify/verify_c09_end_to_end.py
python3 docs/test-case/postman/scripts/run.py verify/verify_c10_end_to_end.py
```

### 11.2 Execution Order (chi tiết)

Suite được tổ chức thành **6 phases theo dependency** — phase sau chỉ chạy khi phase trước ổn định.

**Phase 1 — Authentication Foundation (C01):**

1. Login cho 5 principal types.
2. Session: refresh, context, myself, logout.
3. Device: trust, untrust, logout one/all.
4. MFA: enable → verify → disable.
5. Password: change, forgot, reset.
6. Activation: resend, activate.

**Phase 2 — Enterprise & Email (C02):**

1. Register → verify email → login.
2. Permissions catalog.
3. Email verification OTP.

**Phase 3 — IAM Foundation:**

1. Step-up MFA (C08).
2. Roles CRUD + tree + move + delete/restore (C03).
3. Departments CRUD + tree + move + delete/restore (C04).
4. Positions CRUD + tree + available + preview + delete/restore (C05).

**Phase 4 — Principal Lifecycle:**

- C06: Enterprise Users (CRUD, profile aliases, role/dept/pos assignment, boss, block/unblock, wallet).
- C07: SGOD Users (CRUD, profile aliases, role/dept/pos, permanent delete).
- C08: SGOD Admins (CRUD, block, permanent delete).
- C09: Sub-Enterprises (CRUD, organizational, bosses, block).

**Phase 5 — Tenant Management (C10):**

- List/overview/statistics.
- Assign/unassign/set-assigned.
- Block/unblock/restore.
- Subscription/features update.
- Organizational: assign/remove/boss/check-subordinate.
- Organization audit.

**Phase 6 — Audit & Crypto (C11):**

- Audit logs (dùng events từ Phase 1-5).
- Crypto string round-trip.
- Crypto file round-trip.

### 11.3 Khi nào chạy lại từ đầu?

- Sau khi BE deploy version mới → chạy lại toàn bộ.
- Sau khi sửa test data → chạy từ cluster bị ảnh hưởng trở đi.
- Sau khi sửa collection/environment → chạy từ cluster liên quan.

### 11.4 Khi nào chạy từng phần?

- Debug 1 cluster cụ thể → chạy folder Runner.
- Smoke test sau deploy → chạy C01 trước (foundation).
- Regression test → chạy toàn bộ theo execution order.

### 11.5 Success Criteria

#### Per Case

Một test case được tính PASS khi:

- ✅ Status code khớp expected.
- ✅ Response body structure khớp schema trong evidence.
- ✅ Post-response assertions pass.
- ✅ Evidence được lưu trong `evidence/C<NN>-<name>/`.

#### Per Cluster

Một cluster PASS khi:

- ✅ 100% test cases PASS hoặc BLOCKED có lý do rõ ràng.
- ✅ Verify script (nếu có) chạy `ALL CHECKS PASSED`.
- ✅ Coverage không giảm so với revisions trước.

#### Per Phase

- ✅ Phase N depends on Phase N-1 passing ≥ 90%.
- ✅ All fixtures from Phase N-1 are still valid (no premature cleanup).
- ✅ `runId` remains consistent across all phases.

### 11.6 Reporting

Sau khi chạy xong, báo cáo phải ghi các metric sau:

| Metric | Count |
|---|---:|
| Total designed | 180 |
| Total executed | X |
| Passed | X |
| Failed | X |
| Blocked | X |
| Not run | X |

**Rules:**

- Mỗi `FAIL` có Bug ID + root cause.
- Mỗi `BLOCKED` có lý do cụ thể.
- Evidence lưu ở `evidence/C<NN>-<name>/`.
- Test data IDs thực (từ BE response) phải map với `runId`.

### 11.7 Regression Procedure (sau khi BE fix defect)

1. Retest case FAIL → PASS.
2. Re-run dependency chain (ví dụ: nếu C03 roles fail, C06/C07/C08/C09 phụ thuộc cũng cần re-run).
3. Update execution log.
4. Commit evidence mới.
5. Re-run end-to-end verify scripts (nếu có):

```bash
python3 docs/test-case/postman/scripts/run.py verify/verify_c09_end_to_end.py
python3 docs/test-case/postman/scripts/run.py verify/verify_c10_end_to_end.py
```

---

## 12. SECURITY RULES & BEST PRACTICES

### 12.1 Nguyên tắc vàng (Golden Rules)

> [!CAUTION]
> **CRITICAL:** Không ghi password, token, OTP/TOTP, recovery code, MFA secret hoặc API key thật vào bất kỳ artifact nào được commit/chia sẻ: workbook, collection, environment export, evidence, console log hoặc screenshot.

### 12.2 Checklist bảo mật

| Rule | What to Assert | What NOT to Assert |
|---|---|---|
| **Token** | presence, type, non-empty | exact value |
| **Password** | NEVER in response | NEVER in response |
| **Hash/Salt** | NEVER in response | NEVER in response |
| **Recovery codes** | redact in evidence | Never commit to artifact |
| **TOTP/OTP** | New per operation | Never reuse code |
| **Cookie HttpOnly** | Set đúng | Not readable by JS |
| **API key** | Inject qua env, không hardcode | — |

### 12.3 Best Practices

#### ✅ DO

1. **Dùng Environment variables** cho mọi giá trị nhạy cảm.
2. **Generate `runId` mới** mỗi lần chạy.
3. **Tạo OTP/TOTP mới** mỗi thao tác.
4. **Redact evidence** trước khi commit.
5. **Đánh dấu Secure** cho variables nhạy cảm hoặc dùng **Postman Vault**.
6. **Dùng pre-request scripts** để auto-generate runId, deviceId.
7. **Save responses** thay vì copy-paste thủ công.
8. **Export Runner results** để có bằng chứng.

#### ❌ DON'T

1. **ĐỪNG commit** giá trị thật vào git.
2. **ĐỪNG share** environment file `.json` chứa credentials qua Slack/Email.
3. **ĐỪNG dùng production** credentials cho test.
4. **ĐỪNG reuse** OTP/TOTP qua nhiều lần chạy.
5. **ĐỪNG hardcode** URL/credentials trong collection.
6. **ĐỪNG log** sensitive data vào Postman Console.
7. **ĐỪNG share Postman account** với team (mỗi người 1 account riêng).

### 12.4 Cleanup

Sau khi test xong:

- **Logout** tất cả sessions (`POST /sessions/current`).
- **Unblock** actors đã block.
- **Restore** actors đã delete.
- **Disable MFA** enrollment (nếu cần).
- **Xóa** test fixtures có `runId` prefix (nếu có API delete).

### 12.5 Nếu lỡ commit secrets

1. **Rotate ngay** credentials bị lộ.
2. **Loại bỏ secret khỏi history** bằng công cụ phù hợp (ví dụ `git filter-repo`/BFG) nếu secret đã đi vào Git history; `git revert` đơn thuần không xóa secret khỏi commit cũ.
3. **Notify team** về sự cố.
4. **Update secrets** trong environment.
5. **Document incident** trong execution log.

### 12.6 Secret-handling decision

| Loại dữ liệu | Nơi lưu khuyến nghị | Không nên lưu |
|---|---|---|
| Base URL / non-sensitive ID | Environment local value | Hardcode lặp lại trong từng request |
| API key / Password / Token | Secure local variable hoặc Vault | README, committed JSON, screenshot |
| CI/CD secret | Pipeline secret manager | Repository source code |
| Evidence | Redacted artifact | Raw secret-bearing payload |

---

## 13. LIMITATIONS & KNOWN GAPS

### 13.1 Hiện tại (Scope của test suite này)

- ❌ **Negative cases**: Chỉ có skeleton ở C09/C10 negative CSVs; chưa cover đầy đủ invalid input, missing required, wrong type.
- ❌ **Security abuse cases**: brute force, enumeration, replay — chưa cover.
- ❌ **Cross-tenant denial**: Chưa cover (C10 có hint nhưng chưa full).
- ❌ **Expired/revoked token**: Chưa cover.
- ❌ **Performance/load testing**: Chưa cover.
- ❌ **Contract freeze**: Nhiều endpoint vẫn `CONTRACT_PENDING` — cần BE team confirm trước khi assert chi tiết.

### 13.2 Known Gaps từ FE survey

| Gap | Description | Impact |
|---|---|---|
| **GAP-01** | Axios unwrap → profile double-unwrap | FE defect possible |
| **GAP-03** | `handleGetRoleTree` reads `res.data.tree/res.data/res` | FE hook inconsistency |
| **GAP-04** | `responseData.data.isSubordinate` reads nested path | FE unwrap issue |
| **GAP-06** | SGOD hooks fallback token rỗng | Cookie mode may succeed but profile nil |

### 13.3 Contract Issues

| ID | Endpoint(s) | Issue | Priority |
|---|---|---|---|
| **CI-01** | All | Envelope: `result` vs `data` | HIGH |
| **CI-02** | `/sgod-admins/*` | Path `/sgod/admins` vs `/sgod-admins/*` | MEDIUM |
| **CI-03** | `/test-crypto/*` | DEV/PoC endpoints | MEDIUM |
| **CI-04** | `getEnterpriseUsersDeleted` | FE gọi base với status=Deleted | MEDIUM |
| **CI-05** | All PATCH | snake_case vs camelCase | HIGH |

### 13.4 Cảnh báo

> **C11 Crypto** là PoC — không phải production business API. Kết quả test chỉ mang tính tham khảo.
>
> **DEV-only endpoints** (`/dev/emails`, `/test-crypto/*`) chỉ chạy ở DEV environment. KHÔNG chạy ở staging/production.

### 13.5 Cách đọc các limitation

Các mục trong section này là **known scope boundaries**, không phải mặc định là defect của backend. Khi phát hiện failure mới, cần phân loại rõ:

1. **Test gap** — chưa có test case.
2. **Contract gap** — API contract chưa freeze hoặc chưa thống nhất.
3. **Frontend integration gap** — caller/unwrap/path không đồng nhất.
4. **Backend defect** — behavior thực tế sai contract đã xác nhận.
5. **Environment/data issue** — seed, secret hoặc dependency chưa đúng.

---

## 14. REFERENCES

### 14.1 Tài liệu trong repository

| Tài liệu | Mô tả |
|---|---|
| [`README.md`](./README.md) | Entry point của test-case documentation (chứa test plan, execution order, success criteria, reporting, regression) |
| [`auth_test_cases.csv`](./auth_test_cases.csv) | Master CSV — 180 rows × 27 columns |
| [`specifications/endpoint_inventory.md`](./specifications/endpoint_inventory.md) | 176 endpoints × 11 clusters |
| [`specifications/authentication_rules.md`](./specifications/authentication_rules.md) | Auth/MFA/session rules |
| [`specifications/authorization_matrix.md`](./specifications/authorization_matrix.md) | Permission/role/tenant isolation matrix |
| [`specifications/test_data_strategy.md`](./specifications/test_data_strategy.md) | Actors + fixtures + naming convention |
| [`postman/scripts/README.md`](./postman/scripts/README.md) | Hướng dẫn Python scripts |
| `evidence/C<NN>-*/*.md` | Request / success / error evidence per cluster |

### 14.2 Postman official references

- [Postman Downloads](https://www.postman.com/downloads/)
- [Install Postman](https://learning.postman.com/docs/getting-started/installation/install-app/)
- [Postman System Requirements](https://learning.postman.com/docs/getting-started/installation/system-requirements/)
- [Import Data into Postman](https://learning.postman.com/docs/getting-started/importing-and-exporting/importing-data/)
- [Store and Reuse Values Using Variables](https://learning.postman.com/latest-v-12/docs/use/send-requests/variables/variables)
- [Manage Environments](https://learning.postman.com/latest-v-12/docs/use/send-requests/variables/managing-environments)
- [Use Scripts in Postman](https://learning.postman.com/latest-v-12/docs/tests-and-scripts/write-scripts/intro-to-scripts)
- [Collection Runner](https://learning.postman.com/latest-v-12/docs/tests-and-scripts/running-collections/intro-to-collection-runs)
- [Newman Built-in Reporters](https://learning.postman.com/docs/reference/newman-cli/newman-built-in-reporters)

### 14.3 Nguồn gốc plan

- **Plan**: `docs/plan_to_process_FE/auth/plan_write_test_case/2026-10-06-plan-positive-test-cases-auth-service.md`
- **Guide**: `.codex/attachments/a81b4180-552d-433a-a91b-a635af4cb0c3/Pasted text.txt`
- **Auth v3 flow**: `docs/description_from_BE/auth/auth-flow-guide_v3.md`

---

<div align="center">

**SGOD AUTH SERVICE · TEST CASE DOCUMENTATION**

<sub>Postman · API Testing · Automation · Verification · Evidence · Security</sub>

[⬆ Back to top](#sgod-auth-service--test-case-documentation)

</div>