# Task breakdown — từ bộ thiết kế LAB-4 tới backlog trên GitHub Project

Nguồn duy nhất của backlog: [`backlog/backlog.yaml`](backlog/backlog.yaml). Issue trên Project được sinh từ file này bằng [`scripts/push-backlog-to-github-project.py`](scripts/push-backlog-to-github-project.py); tiêu đề mỗi issue bắt đầu bằng mã backlog (`E09-04b · …`) để tra ngược.

## 1. Nguyên tắc chia task

### 1.1 Độ hạt — chia tới đâu thì dừng

| Quy tắc | Nội dung |
|---|---|
| Một issue = một phần giao được | Review được trong một PR, có điều kiện nghiệm thu kiểm được (test, wireframe, hợp đồng BM-52). Không có issue kiểu "làm màn X" chung chung |
| Tách theo lớp khi lớp đó có người làm riêng | `[DB]` migration/RPC (BE-2) · `[BE]` engine TS + route API (BE-1) · `[FE]` màn hình · `[QA]` test tự động. Gộp `[DB+BE]` khi RPC và route nhỏ, một người làm liền mạch tốt hơn |
| Trần kích thước | Mục lá ≤ 8 SWP (≈ 24 giờ BE/DB, 44 giờ FE — `estimate.md` §3). Lớn hơn thì tách. Kiểm lại sau khi chấm: 2 mục 10 SWP (E05-05, E05-13) đã tách, giữ tổng |
| Dừng tách | Khi tách thêm sẽ ra phần không test riêng được, hoặc nhỏ hơn ~2 giờ |
| Việc không phải code vẫn là issue | Câu hỏi cho khách (`clarification`), spike có time-box (`spike`), viết spec R1.1 (`[DOC]`) — vì chúng chặn issue khác và tốn giờ thật |

### 1.2 Khi nào tách sub-issue

Tách sub-issue khi một issue chứa **nhiều quy tắc nghiệp vụ độc lập, mỗi quy tắc có bảng ca biên riêng** trong BM-53. Mỗi quy tắc thành một sub-issue để chấm SWP, giao việc và báo tiến độ riêng. Issue cha khi đó chỉ là vỏ gom: không ước lượng, SWP/giờ của cha = tổng các con.

Áp dụng ở hai chỗ có nhiều biến nhất:
- `E06-03` engine phân bổ: 消費期限, dải nhiệt, hạn giao theo hợp đồng, 日付逆転, FEFO.
- `E09-03` / `E09-04` kiểm giờ lái: 4 nhóm quy tắc trong ngày, 7 quy tắc nhiều ngày (ràng buộc 2024).

Ngoài ra tách sub-issue khi một issue vượt trần kích thước (§1.1) hoặc gồm các phần do lớp/người khác nhau làm: `E02-02` (RLS theo nhóm bảng), `E05-05` / `E05-13` (tách sau khi chấm SWP), `E06-03`, `E08-02`, `E09-06`, `E09-11`.

### 1.3 Định nghĩa xong (DoD) — áp cho mọi issue

1. Code đã merge vào nhánh chính qua PR có ít nhất 1 người review (không phải người viết).
2. Điều kiện nghiệm thu trong issue đều tích; ca biên nêu trong issue có test tự động và chạy trong CI.
3. Quyền được kiểm ở cả API và DB (RPC `has_role` / RLS) nếu issue có thao tác ghi; không route ghi nào nhận kết quả tính sẵn từ client.
4. Thông báo lỗi tiếng Nhật đúng mã trong bảng mã lỗi; màn hình khớp wireframe LAB-4.
5. Deploy được lên môi trường test; migration chạy được trên dữ liệu seed.
6. Thay đổi so với spec LAB-4 (nếu có) đã ghi vào `PREMISE.md` của repo này.

Issue `[DOC]` / `clarification`: xong khi tài liệu/câu trả lời được PL duyệt và issue dev tiếp theo đã được tạo.

### 1.4 Dùng epic → issue → sub-issue trên Project

| Cấp | Trên GitHub | Field "Loại" | Ước lượng |
|---|---|---|---|
| Epic | Issue có label `epic`, các issue con gắn bằng **sub-issue** của GitHub | Epic | Không (tổng hợp từ con) |
| Issue | Sub-issue của epic | Issue | SWP + giờ (trừ khi có sub-issue) |
| Sub-issue | Sub-issue của issue | Sub-issue | SWP + giờ |

- Phụ thuộc giữa issue dùng quan hệ **blocked by** của GitHub, đồng thời liệt kê trong body.
- Field của Project: Status · Iteration · Phụ trách (giả định) · SWP · Giờ ước lượng · Release · Ràng buộc đặc thù · Loại.
- Người phụ trách là vai trò giả định (BE-1, BE-2, FE-1, FE-2, QA-1, BrSE), không gán tài khoản thật.
- Hạng mục chịu ràng buộc giờ lái 2024 có label `constraint:driving-2024` và field "Ràng buộc đặc thù = Giờ lái 2024", lọc được thành một view riêng.
- Ký hiệu ★: ở epic E09 và §3 nghĩa là ràng buộc giờ lái 2024; "R1.1★" nghĩa là mục Release 1.1 chặn go-live (PREMISE LAB-4 §4.1).

## 2. Spec LAB-4 → issue

Mã tài liệu là mã trong bộ spec LAB-4. Body mỗi issue liệt kê tài liệu nguồn ở mục "Tài liệu thiết kế LAB-4". Bảng dưới gom theo nhóm tài liệu. Số issue là số trên repo [coldchain-lab5-backlog](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues).

| Spec | Epic | Issue / sub-issue | Phần spec chưa thành issue và vì sao |
|---|---|---|---|
| `YCL_SYSTEM_DESIGN` (architecture), ADR-001/002/003/005, `YCL_OVERVIEW_DB` §5, `error-codes.md` | [E01](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/1) | #13–#24 | Không có |
| ADR-009, `role-permission-matrix.md`, `A001_SPEC`, `A002_SPEC`, `AUTH_MASTER_DB` (role) | [E02](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/2) | #25–#40 (RLS tách sub #27–#30) | Màn quản lý role (P-19): matrix để "phase sau". R1 thay bằng script gán role #40 (PREMISE S7) |
| ADR-006, `M001_SPEC` (gộp M002, M007), `AUTH_MASTER_DB` (master), `TEMPERATURE_DB` (devices) | [E03](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/3) | #41–#45 | Màn CRUD master và luồng đề xuất/duyệt chính sách: LAB-4 để R1.1. Mới có issue viết spec #164 |
| `R002_SPEC`, `Q001_SPEC`, `I001_SPEC`, `INBOUND_RECEIVE_TECH`, `LOT_STATUS_DECISION_TECH`, API-INB-002, API-QLT-001/003 | [E04](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/4) | #46–#57 | Upload ảnh nhập kho lên Storage (ADR-010): R1.1★, chưa có spec → mới có issue viết spec #161. Di chuyển lô (F09/F11): R1.1 → issue viết spec #167 |
| `Q004_SPEC` (gồm Q002), `TEMPERATURE_IMPORT_TECH`, ADR-008, API-TMP-002/003/004, `TEMPERATURE_DB` | [E05](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/5) | #58–#70; sub #171–#174 (tách sau khi chấm SWP) | Hồ sơ 逸脱 + màn điều tra (F22-02): R1.1★ → issue viết spec #163. Mail cảnh báo ngoài giờ (IF-MAIL-01, EV4): LAB-4 chỉ thiết kế tới "điểm tích hợp", alarm vẫn nằm đầu hàng đợi Q002 → phase sau, rủi ro ở §4. Báo cáo alarm quá hạn (F26) → issue viết spec #169 |
| `O001_SPEC`, `O002_SPEC`, `ALLOCATION_ENGINE_TECH`, ADR-004, API-ORD-002/004/005, `ORDER_ALLOCATION_DB` | [E06](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/6) | #71–#88; sub #74–#78 (mỗi quy tắc 1 sub) | Nhận đơn từ ERP qua SFTP (IF-ERP-01, EV2): LAB-4 chỉ là điểm tích hợp, đơn nhập tay vẫn tạo được ở O001 (#72) → phase sau |
| `O006_SPEC`, `D002_SPEC`, `POD_COMPLETE_TECH`, API-OUT-002, API-DLV-002, `OUTBOUND_DELIVERY_DB` | [E07](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/7) | #89–#100 | POD offline 8 giờ, ảnh POD, 受取拒否 + đảo lịch sử giao (ADR-010, LAB-4 §4.1): R1.1★, LAB-4 chỉ có ADR, chưa có spec màn/API → chỉ có issue viết spec #160–#162. Effort ước thô 390–660 giờ (`estimate.md` §4) |
| `S001_SPEC` (soạn tuyến), API-RTE-005/006, `ROUTE_PLANNING_DB` | [E08](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/8) ★ một phần | #101–#108, #111, #112, #117; sub #103, #107 | Không có. Thêm adapter bản đồ + spike (#105, #106, PREMISE S5) mà LAB-4 chỉ ghi là điểm tích hợp |
| ADR-007, `DRIVING_TIME_CHECK_TECH`, `WORK_EVENT_RECORD_TECH`, `D001_SPEC`, `S001_SPEC` (panel kiểm, S002 công bố), API-RTE-003/007, API-DRV-002/004 | [E09](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/9) ★ | #109, #110, #113–#116, #118–#151; sub #120–#130, #132–#134, #139–#141 | Ghi sự cố tuyến S003/D003 (FR-SCH-05): LAB-4 không thiết kế và không có mốc → issue viết spec #170 (PREMISE S1). Chi tiết ràng buộc: §3 |
| `L001_SPEC` | [E10](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/10) | #152, #153 | Thu hồi (F25) và khoá tra cứu SKU / nhà cung cấp / 産地: R1.1 → issue viết spec #165, #168 |
| `YCL_SYSTEM_DESIGN` (NFR, phát hành) | [E11](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/11) | #154–#159 | Thiết kế và chạy test case thủ công, UAT: backlog mới có test tự động gắn với issue → rủi ro R8 trong `progress-report.md`, tạo issue ở Sprint 2 |
| PREMISE (LAB-4) §4.1 kế hoạch Release 1.1, ADR-010 | [E12](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/12) | #160–#170 (chỉ là issue viết spec) | Phát triển R1.1: chỉ break khi spec được duyệt, nếu không thì ước lượng không có căn cứ. LAB-4 §4.1 ghi R1 **không go-live** khi các mục ★ chưa xong |
| PREMISE (LAB-4) §4 "phase sau": báo cáo/KPI (F26), audit (F27), sổ HACCP (F23), thu hồi (F25), kiểm kê và di chuyển (F09/F11), trả hàng/khiếu nại (F18), chuyển dữ liệu (F29) | — | Một phần thành issue viết spec R1.1: #165 (F25), #166 (F27), #167 (F09/F11), #169 (F26 alarm). Chuyển dữ liệu: chỉ 2 script mà thiếu thì R1 không chạy được, #87 (lịch sử giao) và #148 (số dư giờ lái) | F23, F18, KPI chung, kiểm kê: ngoài phạm vi thiết kế LAB-4 và ngoài kế hoạch R1.1, chưa có mốc. Chuyển master và tồn kho đầu kỳ: chưa thiết kế, ghi ở §4 |
| Option X01–X10 (logger online, VRP, kế toán, デジタコ…) | — | — | Ngoài phạm vi từ LAB-1 |

## 3. Hạng mục chịu ràng buộc giờ lái xe tải từ 2024

44 mục lá, 159 SWP, 514 giờ (26% tổng giờ). Trên Project lọc bằng field "Ràng buộc đặc thù = Giờ lái 2024" hoặc label `constraint:driving-2024`. Cách tách: PREMISE H5.

| Ràng buộc | Issue | Vì sao tách riêng |
|---|---|---|
| Quy tắc trong ngày: 拘束 13/15 giờ, 連続運転 4 giờ, giờ làm và 超勤 ngày, nhiều tuyến/ngày | #119, #120–#123 (cha #113) | Mỗi quy tắc có bảng ca biên riêng (SD-1…SD-17). Tách để chấm SWP, giao việc, test và báo tiến độ theo từng quy tắc. Sai một quy tắc là cho công bố tuyến vi phạm luật |
| Quy tắc nhiều ngày: TB lái 2 ngày, TB 2 tuần, nghỉ giữa 2 ngày, 拘束 tháng 284 giờ, 拘束 năm 3.300 giờ, 超勤 năm 960 giờ, thiếu dữ liệu → chặn | #124–#130 (cha #114) | Như trên (MD-1…MD-21). Quy tắc năm cần số dư đầu kỳ (#148). Chỗ này prototype và LAB-1 chưa có |
| Ghép kết quả, kiểm khi lưu và khi công bố: chạy 2 tầng lúc lưu đoạn, gắn version quy tắc, đóng băng kết quả, chặn công bố | #115, #131, #132–#134 (cha #116), #118 | Đây là điểm chặn cứng. Tách khỏi E08 vì review độc lập chỉ ra bước 8 của API lưu đoạn chạy engine giờ lái (PREMISE S8) |
| Phút lái nhập tay phải được R10 duyệt | #135 | Chống "sửa giờ kế hoạch để che vi phạm" (LAB-4 D16) |
| Giờ làm thực tế: bảng sự kiện, ghi/sửa/duyệt giờ, dựng lại ngày, job 03:00, kiểm lại tuyến tương lai | #109, #110, #136, #137, #139–#143 (cha #138) | Nguồn số liệu thật cho quy tắc nhiều ngày. Sai ở đây thì kiểm nhiều ngày sai theo |
| Màn hình: tài xế ghi giờ, R10 duyệt, panel kiểm ở S001, API luỹ kế | #144–#147 | Cùng ràng buộc. FE ước theo hệ số FE |
| Dữ liệu đầu kỳ | #148 | Thiếu thì ngày go-live không công bố được tuyến nào (PREMISE S3, S6) |
| Kiểm thử | #149, #150, #157 (E11) | Test tích hợp kịch bản 2024, hiệu năng với 1 năm dữ liệu, E2E lập tuyến → ghi giờ → kiểm lại |
| Làm rõ với khách | #151 | Bản tóm tắt quy tắc và giả định gửi khách (QA#27). Thay đổi sau khi khách trả lời thành issue mới |
| Việc ở epic lập tuyến mà ràng buộc làm đổi phạm vi: vòng đời tuyến, adapter bản đồ, huỷ tuyến, màn công bố, câu hỏi và spike bản đồ | #101, #104, #105, #106, #111, #117 (E08) | **Giữ ở E08 nhưng mang cờ.** Phút tham chiếu từ bản đồ là căn cứ chống nhập tay che vi phạm. Huỷ tuyến phải dựng lại kế hoạch giờ làm. Gom hết vào E09 thì epic lập tuyến không còn nghĩa (PREMISE H5) |
| Spec ghi sự cố tuyến S003/D003 (FR-SCH-05) | #170 (E12) | Sự cố trên đường làm đổi giờ thực tế. LAB-4 không có mốc cho yêu cầu này (PREMISE S1) |

## 4. Chỗ hở và mâu thuẫn của LAB-4 phát hiện khi break

Cách xử lý là một trong bốn loại: **đã sửa thiết kế** (trỏ PREMISE), **giả định** (trỏ PREMISE), **tạo issue làm rõ** (#số), hoặc **để mở** kèm lý do.

| Spec LAB-4 | Chỗ hở / mâu thuẫn | Xử lý |
|---|---|---|
| PREMISE (LAB-4) §4.1, `DIV-14` | Bảng sự cố tuyến (FR-SCH-05) ghi "phase sau" nhưng không có trong kế hoạch R1.1, nên không có mốc nào | Đã sửa thiết kế: PREMISE S1, issue #170 |
| `WORK_EVENT_RECORD_TECH §4.7` | `[TBD]` dùng pg_cron hay Vercel Cron cho job 03:00 | Đã sửa thiết kế: PREMISE S2, H1 (Vercel Cron) |
| PREMISE (LAB-4) D04, `DRIVING_TIME_CHECK_TECH` §4.3, §4.5 | Số dư giờ lái đầu kỳ không có đường nạp. Chỉ nạp số dư năm thì quy tắc tháng và 2 tuần tính thiếu | Đã sửa thiết kế: PREMISE S3, S6, issue #148 |
| PREMISE (LAB-4) D04 | Không nêu định dạng file số dư | Giả định: PREMISE A2 |
| `OUTBOUND_DELIVERY_DB §4.3`, D07 | Có dòng lịch sử `MIGRATION` nhưng không có đường nạp → lần giao đầu sau go-live không kiểm được 日付逆転 | Đã sửa thiết kế: PREMISE S4, issue #87. Định dạng: giả định A3 |
| `S001_SPEC` J-14, IF-MAP-01 | Không có thiết kế adapter bản đồ, không biết dịch vụ nào | Đã sửa thiết kế: PREMISE S5, giả định A1. Tạo issue làm rõ #104 (đã trả lời trong Sprint 1 giả lập), spike #105 |
| `role-permission-matrix` P-19 | Không có cách gán role khi vận hành, role không suy từ IdP | Đã sửa thiết kế: PREMISE S7, issue #40 |
| `API-RTE-005_API §5` bước 7–8 | Một API chứa cả soạn tuyến và kiểm giờ lái | Đã sửa thiết kế: PREMISE S8 (cách chia API) (#107, #131) |
| `O006_SPEC` T-02, `DIV-22` | DB có trạng thái PICKED/LOADED nhưng R1 không có RPC ghi | Tạo issue làm rõ #100 (PREMISE S9). Sprint 1 giả lập chốt: R1 không ghi |
| `YCL_OVERVIEW_DB` `DIV-03` | Ghi lẫn "11 bảng" và "12 bảng" sự kiện chỉ ghi thêm | Giả định: PREMISE A8 |
| `YCL_SYSTEM_DESIGN` §11 Q2, QA#12 | Khách chưa chấp nhận hạ tầng Supabase + Vercel Tokyo | Tạo issue làm rõ #23 |
| QA#24, IF-IDP-01 | Chỉ chốt "SSO", chưa biết IdP nào, giao thức nào | Giả định PREMISE A4 + tạo issue làm rõ #33 (đang Blocked) |
| `YCL_SYSTEM_DESIGN` §11 Q3, Q12, Q13 (QA#27) | Cách tính 超勤, các giả định giờ lái nhiều ngày, nghĩa của "ước tính > 24 giờ" | Tạo issue làm rõ #151 |
| `YCL_SYSTEM_DESIGN` §11 Q10, `O002_SPEC` T-01 | Business-review: áp quy tắc riêng cho đơn hay phải sửa hợp đồng trước | Đã sửa thiết kế: PREMISE H3 (áp riêng cho đơn) |
| `O002_SPEC` T-02 | Đơn phân bổ một phần có được phân bổ bổ sung không | Đã sửa thiết kế: PREMISE H4 (không, ở R1) |
| `A001_SPEC` §3 và bản nháp backlog | Điểm áp MFA: theo thao tác hay lúc đăng nhập | Đã sửa thiết kế: PREMISE H6 (lúc đăng nhập) |
| LAB-4 không chọn môi trường test RPC | pglite không có RLS, role và `auth.uid()` thật | Đã sửa thiết kế: PREMISE H2 (Supabase CLI local) |
| LAB-4 không có lịch phát triển | Không có mốc thì báo cáo tiến độ không nói được trễ mốc nào | Giả định: PREMISE A7 (go-live ngày 1 của tháng), A9 (lịch sprint, M1/M2/M3) |
| `YCL_SYSTEM_DESIGN` §11 Q1 (LAB-4 A01) | Nhiệt độ đúng biên tính là trong ngưỡng hay ngoài | **Để mở:** giữ giả định của LAB-4. Khách trả lời khác thì chỉ đổi dữ liệu chính sách nhiệt, không đổi code (#59 test cả 2 phía biên) |
| `YCL_SYSTEM_DESIGN` §11 Q7, Q8 | RFP mâu thuẫn: nhập ngoài ngưỡng là chặn hay cách ly; thiếu trường truy xuất gạo/bò là chặn hay cách ly | **Để mở:** giữ lựa chọn của LAB-4 (Q7 cách ly, Q8 chặn), chờ QA đợt 2. Nếu đổi thì chỉ sửa engine: #47 (Q7), #46 (Q8), không đổi mô hình dữ liệu |
| `YCL_SYSTEM_DESIGN` §11 Q9 | Trường 「参照」 của đơn không có trong từ điển dữ liệu | **Để mở:** giữ giả định `order_ref` của LAB-4 (#71). Bỏ trường này thì chỉ bỏ ràng buộc UNIQUE |
| `YCL_SYSTEM_DESIGN` §11 Q4 | Thời gian phiên và tự khoá trên máy dùng chung | **Để mở:** là giá trị cấu hình, không đổi phạm vi issue. Chốt trước UAT |
| `YCL_SYSTEM_DESIGN` §11 Q5 | Ca đêm có đủ 2 người R04 để release lô 2 bước không | **Để mở**, đây là rủi ro vận hành: không đủ thì lô chờ tới ca sáng. Thêm luồng ngoại lệ thì phải đổi `LOT_STATUS_DECISION_TECH`. Chưa tạo issue vì đây là câu hỏi về cách vận hành của khách |
| `YCL_SYSTEM_DESIGN` §11 Q6, Q11 (QA#22) | Ma trận mức sai lệch × người duyệt; tạo 逸脱 khi xếp xe hoặc nhập kho ngoài ngưỡng | **Để mở** ở R1: R1 chỉ chặn; ma trận chờ phòng chất lượng của khách định nghĩa, nên đưa vào spec R1.1 (#163) |
| IF-MAIL-01 (EV4) | Mail cảnh báo alarm ngoài giờ chỉ ở mức điểm tích hợp | **Để mở:** ngoài phạm vi R1 theo LAB-4. Rủi ro SLA 15 phút ngoài giờ, cần PL chốt có đưa vào R1.1 hay không |
| F29 chuyển dữ liệu | Master và tồn kho đầu kỳ từ hệ thống cũ chưa được thiết kế | **Để mở:** LAB-4 để phase sau. Master tạm nạp bằng seed. Cần chốt trước khi lập kế hoạch UAT (mốc M3) |
