# Backlog LAB-5 — hệ thống nghiệp vụ chuỗi kho lạnh thực phẩm

**Dự án:** coldchain-lab5-backlog · **Mã học viên:** tamnv-1080 · **Đề:** Product B

## 1. Tổng quan

- **Nguồn:** backlog break từ bộ thiết kế LAB-4 nộp ngày 2026-11-21. Bộ spec LAB-4 không nộp lại.
- **PREMISE.md: có thay đổi.**
  - 9 dòng thêm/sửa spec (S1–S9).
  - 9 giả định bổ sung (A1–A9).
  - 7 hướng đã chốt (H1–H7).
- **Quy mô:** 12 epic · 130 issue · 32 sub-issue · 153 mục lá có ước lượng · **600 SWP · 2.000 giờ** (Release 1: 1.904 giờ).
- **Ràng buộc giờ lái xe tải từ 2024:** 44 mục, 159 SWP, 514 giờ, tách riêng bằng cờ và field (`task-breakdown.md` §3).
- **Sprint giả lập đã chạy:** Sprint 1, từ 2026-12-01 đến 2026-12-14. Kết quả: 23 mục, xong 56%. Báo cáo gửi khách viết bằng tiếng Nhật.

## 2. Link

| | Link |
|---|---|
| Repo | https://github.com/tamnv-1080/coldchain-lab5-backlog |
| GitHub Project | https://github.com/users/tamnv-1080/projects/2 |
| Project, lọc Sprint 1 | https://github.com/users/tamnv-1080/projects/2?filterQuery=iteration%3A%22Sprint+1%22 |
| Báo cáo HTML của skill chấm SWP | [`reports/estimate-swp-coldchain-lab5-backlog-20261123-070414.html`](reports/estimate-swp-coldchain-lab5-backlog-20261123-070414.html). Tải về rồi mở bằng trình duyệt; không cần mạng |

Đã mở thử cả 4 link bằng cửa sổ ẩn danh (không đăng nhập GitHub): _(chờ xác nhận)_

Field trên Project:
- Status
- Iteration
- Phụ trách (giả định)
- SWP (giá trị đã review)
- Giờ ước lượng
- Release
- Ràng buộc đặc thù
- Loại (Epic / Issue / Sub-issue)

## 3. Cấu trúc repo

| File / thư mục | Nội dung |
|---|---|
| `README.md` | File này |
| [`PREMISE.md`](PREMISE.md) | Tiền đề: backlog khác bộ LAB-4 ở đâu (spec thêm/bỏ/sửa, giả định, hướng đã chốt) |
| [`task-breakdown.md`](task-breakdown.md) | Nguyên tắc chia task, spec → issue, hạng mục ràng buộc giờ lái 2024, chỗ hở của LAB-4 |
| [`estimate.md`](estimate.md) | SWP đã review, cách quy giờ, tổng theo epic, so với estimate LAB-1 |
| [`progress-report.md`](progress-report.md) | Báo cáo tiến độ Sprint 1 (giả lập), tiếng Nhật, gửi khách được |
| [`AI-report.md`](AI-report.md) | Skill, prompt, agent đã dùng; cách review output AI; nhận xét |
| [`backlog/`](backlog/) | `backlog.yaml`: nguồn duy nhất của backlog · `swp-overrides.yaml`: tách mục sau khi chấm · `estimates.json`: SWP và giờ từng mục · `github-issue-map.json`: mã backlog ↔ số issue, id field |
| [`scripts/`](scripts/) | `validate-and-summarize-backlog.py`: kiểm backlog · `push-backlog-to-github-project.py`: tạo issue, field, ghi SWP/giờ · `compute-estimates.py`: SWP → giờ · `simulate-sprint.py`: Iteration, trạng thái sprint, burndown |
| [`sprints/`](sprints/) | `sprint-1-simulation.yaml`: kịch bản Sprint 1 giả lập |
| [`reports/`](reports/) | Báo cáo HTML của skill chấm SWP · `sprint-1-burndown.svg` |
| `.gitignore` | Bỏ qua file tạm và file biến môi trường |

## 4. Spec → epic

| Spec (mã/file LAB-4 hoặc dòng PREMISE) | Epic trên Project | Ghi chú |
|---|---|---|
| Architecture `YCL_SYSTEM_DESIGN`, ADR-001/002/003/005, `YCL_OVERVIEW_DB`, `error-codes.md` | [#1 — E01 Nền tảng, hạ tầng và khoá đường ghi](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/1) | Làm trước mọi nghiệp vụ |
| ADR-009, `role-permission-matrix.md`, `A001_SPEC`, `A002_SPEC`; PREMISE S7, H6 | [#2 — E02 Phân quyền 12 role và đăng nhập](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/2) | |
| ADR-006, `M001_SPEC`, `AUTH_MASTER_DB` (master) | [#3 — E03 Master và chính sách có version](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/3) | |
| `R002_SPEC`, `Q001_SPEC`, `I001_SPEC`, `INBOUND_RECEIVE_TECH`, `LOT_STATUS_DECISION_TECH` | [#4 — E04 Nhập hàng và chất lượng lô](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/4) | |
| `Q004_SPEC`, `TEMPERATURE_IMPORT_TECH`, ADR-008, `TEMPERATURE_DB` | [#5 — E05 Nhiệt độ, alarm và SLA 15 phút](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/5) | |
| `O001_SPEC`, `O002_SPEC`, `ALLOCATION_ENGINE_TECH`, ADR-004; PREMISE S4, H3, H4 | [#6 — E06 Đơn hàng và phân bổ lô](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/6) | |
| `O006_SPEC`, `D002_SPEC`, `POD_COMPLETE_TECH`, `OUTBOUND_DELIVERY_DB`; PREMISE S9 | [#7 — E07 Xuất hàng và POD (online)](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/7) | POD offline ở R1.1 (#12) |
| `S001_SPEC` (soạn tuyến), API-RTE-005/006, `ROUTE_PLANNING_DB`; PREMISE S5, S8, A1 | [#8 — E08 Lập tuyến](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/8) | **6 issue mang cờ giờ lái 2024** (adapter bản đồ, huỷ tuyến, màn công bố…) |
| ADR-007, `DRIVING_TIME_CHECK_TECH`, `WORK_EVENT_RECORD_TECH`, `D001_SPEC`, `S001_SPEC` (panel kiểm); PREMISE S2, S3, S6, H1, H5 | [#9 — E09 ★ Giờ lái xe tải từ 2024](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/9) | **Ràng buộc giờ lái 2024**: cả epic. Mỗi quy tắc một sub-issue |
| `L001_SPEC` | [#10 — E10 Truy xuất](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/10) | |
| `YCL_SYSTEM_DESIGN` (NFR, phát hành); PREMISE A7 | [#11 — E11 Kiểm thử hệ thống và chuẩn bị phát hành](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/11) | 1 issue mang cờ giờ lái 2024 (E2E lập tuyến) |
| PREMISE (LAB-4) §4.1 Release 1.1, ADR-010; PREMISE S1, A6 | [#12 — E12 Release 1.1: viết spec trước khi break](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/12) | 1 issue mang cờ giờ lái 2024 (spec sự cố tuyến) |

Bảng chi tiết tới từng issue và phần spec chưa thành issue: `task-breakdown.md` §2.
