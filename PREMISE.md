# PREMISE — Backlog LAB-5 khác bộ thiết kế LAB-4 ở đâu

Backlog break từ bộ thiết kế LAB-4 (nộp 2026-11-21). Không sửa lại bộ spec LAB-4. Những gì đổi, thêm hoặc chốt trong lúc break được ghi ở đây, và issue liên quan trỏ về mã dòng (S1, A2, H1…). Mã spec trong bảng là mã tài liệu LAB-4 (ví dụ `DRIVING_TIME_CHECK_TECH §4.5`, `DIV-14`, `PREMISE D04` là PREMISE của LAB-4).

## 1. Spec thêm / bỏ / sửa so với LAB-4

| # | Spec (mã/file LAB-4) | Thêm/Bỏ/Sửa | Trước → sau | Vì sao | Issue bị ảnh hưởng |
|---|---|---|---|---|---|
| S1 | PREMISE (LAB-4) §4.1 kế hoạch Release 1.1; `DIV-14` | Thêm | R1.1 có 10 mục → thêm mục 11 "ghi sự cố tuyến S003/D003" | Phát hiện khi break E09: `DIV-14` ghi "phase sau" cho bảng sự cố tuyến, nhưng §4.1 chỉ liệt kê mục P0, nên yêu cầu sự cố tuyến (FR-SCH-05, P1) không có mốc nào. Không có mốc thì không lập kế hoạch được (cùng lý do review độc lập LAB-4 đã nêu cho §4.1) | E12-11 |
| S2 | `WORK_EVENT_RECORD_TECH §4.7` dòng 2 | Sửa | `[TBD]` pg_cron hay Vercel Cron → **Vercel Cron gọi route nội bộ** | Phải chốt mới break được E09-14. Lý do chọn ở H1 | E09-14 |
| S3 | PREMISE (LAB-4) D04 ("luỹ kế năm nhập làm số dư đầu kỳ khi chuyển dữ liệu") | Sửa | Không nói nạp bằng gì → **script CSV do vận hành chạy**, không có màn hình ở R1 | Phát hiện khi break E09-04e/f: quy tắc năm (3.300 giờ, 960 giờ) thiếu số dư thì trả `BASELINE_MISSING` và chặn công bố. Chuyển dữ liệu (F29) không được thiết kế ở LAB-4, nên nếu không có đường nạp thì ngày go-live **không tài xế nào công bố được tuyến** | E09-19, E09-04e, E09-04f |
| S4 | `OUTBOUND_DELIVERY_DB §4.3` (`source = MIGRATION`), PREMISE (LAB-4) D07 | Thêm | Mô hình có dòng lịch sử `MIGRATION` nhưng không có đường nạp → **thêm script nạp lịch sử giao** | Phát hiện khi break E06-03d: không có lịch sử từ hệ thống cũ thì lần giao đầu tiên của mỗi khách × SKU sau go-live không được kiểm 日付逆転. Đây là đường "lọt" ở vùng lỗi nghiêm trọng, giống loại lỗi review LAB-4 đã bắt (D18) | E06-11, E06-03d |
| S5 | `S001_SPEC` J-14, IF-MAP-01 (LAB-4 để ở mức "điểm tích hợp") | Sửa | Không có thiết kế adapter → **thêm adapter bản đồ + spike + câu hỏi cho khách** | Phát hiện khi break E09-07: phút tham chiếu từ bản đồ là căn cứ chống "nhập tay để che vi phạm" (D16). Không có nguồn tham chiếu thì mọi đoạn lái thành nhập tay và R10 phải duyệt toàn bộ, luồng công bố gần như đứng | E08-03, E08-08, E08-09, E09-07 |
| S6 | `DRIVING_TIME_CHECK_TECH §4.3` dòng 6 (ngày không dữ liệu = REST), §4.5 quy tắc 5 (`BASELINE_GAP`) | Sửa | Chỉ nạp số dư năm (S3) → **nạp thêm giờ làm từng ngày của 13 ngày trước go-live, go-live vào ngày 1 của tháng** | Review độc lập LAB-5: chỉ có số dư năm thì nếu ngày chốt rơi giữa tháng, quy tắc tháng trả `BASELINE_GAP` và chặn công bố cả tháng go-live; còn các ngày trước go-live bị coi là nghỉ, nên TB 2 tuần, TB 2 ngày và nghỉ giữa 2 ngày bị **tính thiếu** (mềm hơn luật) | E09-19 |
| S7 | `role-permission-matrix` P-19 ("phase sau, gán bằng migration/seed"), ADR-009 (không suy role từ IdP) | Thêm | Không có cách gán role khi vận hành → **script gán/thu hồi role do R11 chạy, có ghi người gán** | Review độc lập LAB-5: user mới không có quyền gì (E02-01) và role không lấy từ IdP, nên sau go-live không ai cấp quyền được nếu không có công cụ. Màn quản lý role vẫn để phase sau | E02-12 |
| S8 | `API-RTE-005_API §5` bước 7–8 | Sửa (cách chia) | Một API → **tách**: phần soạn tuyến (E08-02a/b) và phần chạy kiểm 拘束時間 khi lưu (E09-23) | Review độc lập LAB-5 (BLOCKER): bước 8 của PUT segments chạy engine giờ lái, để chung trong E08 là gộp việc của ràng buộc 2024 vào issue không mang cờ | E08-02a, E08-02b, E09-23 |
| S9 | `O006_SPEC` T-02, DIV-22 | Thêm | Trạng thái PICKED/LOADED có trong thiết kế DB nhưng R1 không có RPC ghi → **issue làm rõ** | Review độc lập LAB-5: điều kiện nghiệm thu cũ ("nhảy cóc bị từ chối") làm `dispatch_order` (ALLOCATED → DISPATCHED) không chạy được | E07-01, E07-12 |

## 2. Giả định bổ sung

| # | Giả định | Chỗ spec/RFP để ngỏ | Ảnh hưởng tới issue/estimate |
|---|---|---|---|
| A1 | Dùng dịch vụ bản đồ khách đang có (LAB-1 đã giả định trong bảng phí). Adapter ước lượng cho **1 dịch vụ REST**, đổi dịch vụ thì chỉ đổi phần cài đặt | IF-MAP-01 chỉ nêu có tích hợp, không nêu dịch vụ nào | E08-03 ước cho 1 dịch vụ; E08-09 time-box 1 ngày. Khách chưa trả lời trước Sprint 3 thì PL chọn dịch vụ thay thế |
| A2 | CSV số dư đầu kỳ: mã tài xế, năm tài chính, 拘束 luỹ kế (phút), 超勤 luỹ kế (phút), ngày chốt. Một dòng/tài xế/năm | D04 không nêu định dạng | E09-19: chỉ là script + kiểm hợp lệ, không màn hình |
| A3 | CSV lịch sử giao: khách, SKU, hạn, ngày giao, số lượng, điều kiện giao; nạp **12 tháng gần nhất**. Dòng không rõ hạn để NULL, đơn liên quan vào BUSINESS_REVIEW (theo `DIV-27`) | Chuyển dữ liệu (F29) không thiết kế ở LAB-4 | E06-11 |
| A4 | IdP doanh nghiệp tích hợp được qua Supabase Auth (SAML hoặc OIDC), **1 IdP** | QA#24 chỉ chốt "SSO", chưa biết IdP nào | E02-05 bị chặn bởi E02-10. IdP ngoài khả năng Supabase thì tách issue mới |
| A5 | Đội giả định 6 người: BE-1, BE-2, FE-1, FE-2, QA-1, BrSE. **6 giờ làm hiệu quả/ngày**, sprint 2 tuần = 10 ngày làm | Đề LAB-5 và LAB-1 không quy định đội phát triển | Capacity sprint (progress-report.md), cách quy giờ (estimate.md) |
| A6 | Release 1.1 ở LAB-5 chỉ có issue **viết spec**. Effort phát triển R1.1 chỉ ước thô ở `estimate.md`, chưa thành issue | PREMISE (LAB-4) §4.1: phải có spec trước khi break | E12-01…11; tổng giờ R1 không gồm dev R1.1 |
| A7 | Go-live vào **ngày 1 của tháng**; khách cung cấp giờ bắt đầu/kết thúc làm việc từng ngày của 13 ngày trước go-live (từ bảng chấm công hiện có) | D04 chỉ nói "luỹ kế năm"; RFP không nêu ngày go-live | E09-19; kế hoạch phát hành E11-06 |
| A8 | Danh sách bảng sự kiện chỉ ghi thêm = danh sách ở quy ước 2 mục 4 của `YCL_OVERVIEW_DB` (DIV-03 ghi lẫn "11 bảng" và "12 bảng") | Mâu thuẫn số lượng trong chính spec LAB-4 | E01-06: dev đối chiếu danh sách khi làm, không đổi estimate |

## 3. Hướng đã chốt

| # | Vấn đề | Các phương án ở LAB-4 | Phương án chốt | Vì sao |
|---|---|---|---|---|
| H1 | Cơ chế lịch cho job EV6 03:00 (dựng lại giờ làm D-1 + kiểm lại tuyến) | Supabase pg_cron · Vercel Cron (`WORK_EVENT_RECORD_TECH §4.7`, `[TBD]`) | **Vercel Cron** gọi route nội bộ, xác thực bằng secret | Bước kiểm lại chạy engine TypeScript ở API server (ADR-004), pg_cron không chạy được. Cho pg_cron gọi HTTP thì phải thêm pg_net và để secret trong DB |
| H2 | Môi trường test RPC | LAB-2 dùng pglite để kiểm cú pháp SQL; LAB-4 không chọn | **Supabase CLI local** (Postgres thật) chạy trong CI | Test khoá đường ghi (E01-10) và RBAC (E02-11) cần role `authenticated`/`service_role`, RLS và `auth.uid()` thật, pglite không có |
| H3 | Quyết định business-review (`O002_SPEC` T-01, YCL §11 Q10) | Áp quy tắc hạn giao cho riêng đơn · bắt buộc sửa hợp đồng trước | **Áp cho riêng đơn** (giữ G-02 của O002) | Sửa hợp đồng cần luồng duyệt master (P-18), đã đẩy sang R1.1 (E12-05). Chọn "sửa hợp đồng trước" thì R1 không xử lý được đơn nào rơi vào business-review |
| H4 | Đơn phân bổ một phần có được phân bổ bổ sung không (`O002_SPEC` T-02) | Có · Không | **Không** ở R1 (giữ G-03) | Theo QA#19 phương án A; thêm phân bổ bổ sung thì phải đổi máy trạng thái đơn và O006 |
| H5 | Cách tách hạng mục chịu ràng buộc giờ lái 2024 | (LAB-4 để chung ở feature route-planning) | Logic quy tắc, kiểm khi lưu, công bố, giờ làm thực tế ở **epic E09**. Việc ở epic khác mà ràng buộc làm đổi phạm vi/effort (adapter bản đồ, huỷ tuyến dựng lại kế hoạch, màn công bố, E2E tuyến, spec sự cố tuyến) **giữ ở epic của nó nhưng mang cờ** `constraint:driving-2024` | Bản nháp đầu viết "toàn bộ effort nằm trong E09", review độc lập chỉ ra là sai (S8). Gom hết vào E09 thì epic lập tuyến không còn nghĩa; cờ ở cấp issue cho phép lọc đủ 44 mục và cộng effort riêng |
| H6 | Điểm áp MFA cho role đặc quyền | Theo thao tác (bản nháp backlog) · lúc đăng nhập (A001) | **Lúc đăng nhập**, do IdP/Supabase thực hiện; server kiểm mức xác thực của phiên | Theo `A001_SPEC` §3 và scenario MFA; bản nháp backlog lệch thiết kế, review độc lập chỉ ra |
