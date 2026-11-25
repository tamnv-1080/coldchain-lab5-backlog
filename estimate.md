# Estimate — SWP và giờ cho backlog LAB-5

Số liệu trong file này sinh bằng [`scripts/compute-estimates.py`](scripts/compute-estimates.py) từ báo cáo skill và [`backlog/swp-overrides.yaml`](backlog/swp-overrides.yaml), kết quả ở [`backlog/estimates.json`](backlog/estimates.json). Field "SWP" và "Giờ ước lượng" trên GitHub Project được ghi từ đúng file này và đã đọc lại để đối chiếu (174/174 mục khớp).

## 1. Báo cáo HTML của skill

[`reports/estimate-swp-coldchain-lab5-backlog-20261123-070414.html`](reports/estimate-swp-coldchain-lab5-backlog-20261123-070414.html) — mở trực tiếp bằng trình duyệt, không cần mạng.

| Mục | Giá trị |
|---|---|
| Skill | `tkm:estimate-swp`, mức `medium`, nguồn là GitHub Project #2, `--no-push-kpi` (không đẩy sang KPI Insight) |
| Phạm vi chấm | 151 mục lá (issue không có sub-issue + sub-issue). 7 issue cha và 12 epic (báo cáo HTML gọi chung là 19 mục cha) không chấm, lấy tổng của con |
| Kết quả | 600 SWP · độ tin cậy 11 cao / 140 trung bình · khoảng dao động 457–754 SWP |
| Hiệu chỉnh | 5 issue mẫu, người review chấp nhận cả 5 nên không lan hiệu chỉnh sang issue khác (trạng thái `accepted`) |
| Sau báo cáo | 2 mục 10 SWP được tách thành 4 sub-issue, giữ nguyên tổng (§2). Báo cáo HTML giữ nguyên, phần tách ghi ở `swp-overrides.yaml` |

## 2. Issue mẫu skill chọn

Skill chọn mẫu theo luật cố định (nhỏ nhất, trung vị dưới, lớn nhất, ngoại lệ, độ tin cậy thấp nhất). Người review chọn mức độ khó trước, rồi chọn điểm cụ thể trong khoảng của mức đó.

| Issue | Skill chấm (Scope × Complexity → SWP) | Bạn chốt | Lý do |
|---|---|---|---|
| [#33](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/33) E02-10 Làm rõ IdP của khách (nhỏ nhất) | 1 × 0 → 1 | Mức "rất dễ", **1 SWP** | Chỉ soạn và gửi bộ câu hỏi, không có code. Ước trực tiếp 3 giờ, khớp hệ số 3 giờ/SWP |
| [#164](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/164) E12-05 Spec luồng đề xuất/duyệt chính sách (trung vị dưới) | 2 × 2 → 3 | Mức "dễ", **giữ 3** | Một tài liệu spec, nhưng luồng có 3 trạng thái và ràng buộc người đề xuất ≠ người duyệt, nên không phải mức rất dễ |
| [#63](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/63) E05-05 RPC import nhiệt độ (lớn nhất) | 5 × 3 → 10 | **Giữ 10**, sau đó tách 6 + 4 | Điểm phản ánh đúng khối lượng: một transaction ghi 4 loại dữ liệu, chống trùng 2 tầng. Nhưng vượt trần 8 SWP của nguyên tắc chia task (`task-breakdown.md` §1.1), nên tách thành E05-05a (ghi + rollback, 3×3=6) và E05-05b (chống trùng, 2×3=4) |
| [#62](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/62) E05-13 Migration alarm theo đợt (ngoại lệ) | 5 × 3 → 10 | **Giữ 10**, sau đó tách 6 + 4 | Như trên: E05-13a (đổi cấu trúc alarm + chuyển dữ liệu cũ, 6) và E05-13b (cột/bảng mới, 4) |
| [#14](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/14) E01-02 CI + migration theo môi trường + backup (độ tin cậy thấp nhất) | 5 × 2 → 8 | **Giữ 8** | 4 môi trường, cổng duyệt tay cho UAT/prod, diễn tập restore. Đúng trần, không cần tách |

Mẫu 3–5 được chấp nhận chung một lượt sau khi xem bảng điểm, không hỏi lại từng mức. Hai điểm review thấy nhưng **không sửa điểm**:

- **Sub-issue quy tắc giờ lái bị chấm thấp.** 7 quy tắc nhiều ngày chỉ được 1–3 SWP mỗi quy tắc, tổng 15 SWP, vì mỗi body ngắn. Quyết định: giữ điểm để thống nhất với báo cáo skill. Đây là rủi ro ước thấp, theo dõi ở `progress-report.md`.
- **Màn hình FE bị chấm thấp so với khối lượng thật.** Ví dụ màn R002 入荷検品 (handy) được 3 SWP. Không sửa SWP mà xử lý bằng hệ số giờ riêng cho FE (§3).

## 3. Cách quy ra giờ

**Quy tắc:** giờ của mục lá = SWP × hệ số theo lớp. Giờ của issue cha và epic = tổng giờ các con.

| Lớp (tag đầu tiêu đề) | Giờ/SWP | Căn cứ |
|---|---|---|
| `[FE]`, `[FE+BE]` | **5,5** | Trung vị của 5 màn ước trực tiếp |
| Các lớp khác (`[DB]`, `[BE]`, `[DB+BE]`, `[QA]`, `[INFRA]`, `[BrSE]`, `[DOC]`) | **3,0** | Trung vị của 6 issue ước trực tiếp |

Giờ ở đây gồm code, unit test, sửa sau review và các điểm của DoD. **Không** gồm buffer, họp và quản lý.

Các mẫu ước trực tiếp (AI ước giờ trực tiếp từ phạm vi và điều kiện nghiệm thu của issue, rồi mới chia cho SWP; người duyệt chọn hệ số):

| Issue | Lớp | SWP | Giờ ước trực tiếp | Giờ/SWP |
|---|---|---|---|---|
| E02-10 Làm rõ IdP | BrSE | 1 | 3 | 3,0 |
| E09-04a Quy tắc TB lái 2 ngày + 4 ca biên | BE | 2 | 6 | 3,0 |
| E09-03b Lái liên tục 4 giờ + 8 ca biên | BE | 3 | 10 | 3,3 |
| E09-06b RPC công bố tuyến | DB | 6 | 16 | 2,7 |
| E09-20 Test tích hợp giờ lái | QA | 8 | 28 | 3,5 |
| E05-05 RPC import nhiệt độ (trước khi tách) | DB | 10 | 30 | 3,0 |
| E03-05 M001 マスタ (chỉ xem) | FE | 4 | 14 | 3,5 |
| E04-05 R002 入荷検品 (handy) | FE | 3 | 18 | 6,0 |
| E07-10 D002 配送完了・POD (online) | FE | 5 | 26 | 5,2 |
| E09-16 D001 màn tài xế (điện thoại) | FE | 4 | 22 | 5,5 |
| E08-06 S001 ルート計画 | FE | 8 | 44 | 5,5 |

**Vì sao tách hệ số theo lớp:** lần đầu chỉ dùng 6 mẫu đầu và một hệ số 3,0. Đối chiếu với LAB-1 (§5) cho thấy phần FE chỉ bằng 0,22 lần LAB-1, trong khi BE/DB bằng 0,59 lần. Nguyên nhân là cả 6 mẫu đều không phải màn hình. Thêm 5 mẫu FE thì tổng tăng từ 1.800 lên 2.000 giờ.

**Buffer đặt ở capacity, không cộng vào từng issue.** Mỗi người có 6 giờ làm hiệu quả/ngày, sprint 10 ngày, giữ lại 15% dự phòng, còn **51 giờ/người/sprint** (PREMISE A5). Cộng buffer vào từng issue thì burndown không còn so được với ước lượng.

**Kiểm capacity theo vai (chỉ R1, phân công lúc ước lượng — trước PREMISE H7):**

| Vai giả định | Giờ R1 | Số sprint nếu chỉ 1 người làm |
|---|---|---|
| BE-1 | 513 | 10,1 |
| BE-2 | 699 | 13,7 |
| FE-1 | 236 | 4,6 |
| FE-2 | 204 | 4,0 |
| QA-1 | 210 | 4,1 |
| BrSE | 42 (+96 giờ viết spec R1.1) | 2,7 |
| **Cả đội** | **1.904** | **6,2 sprint** nếu chia đều được |

Từ Sprint 1, 60 giờ engine chuyển sang FE (PREMISE H7): BE-1 còn 453, FE-1 269, FE-2 231.

Không chia đều được: 1.212 giờ BE/DB dồn cho 2 người BE, cần khoảng 12 sprint. FE và QA rảnh từ sprint 5. Đây là rủi ro tiến độ lớn nhất, được đưa vào `progress-report.md`. Muốn xong R1 trong khoảng 6–7 sprint thì phải thêm 2 BE, hoặc chuyển bớt route API (`[BE]` mỏng) sang FE-2. Kế hoạch nguồn lực ở LAB-1 cũng đặt BE lớn hơn FE (giai đoạn 構築: BE 5,1–8,5 người-tháng/tháng, FE 3,2–5,4).

## 4. Tổng theo epic

| Epic | Số issue | Tổng SWP | Tổng giờ | Ghi chú |
|---|---|---|---|---|
| [#1](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/1) E01 Nền tảng, hạ tầng và khoá đường ghi | 12 | 52 | 156 | Phải xong trước mọi epic ghi dữ liệu (E01-05, E01-06) |
| [#2](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/2) E02 Phân quyền 12 role và đăng nhập | 12 (15 lá) | 51 | 168 | E02-05 SSO chờ khách trả lời IdP (E02-10) |
| [#3](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/3) E03 Master và chính sách có version | 5 | 23 | 79 | Master nạp bằng seed, M001 chỉ xem |
| [#4](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/4) E04 Nhập hàng và chất lượng lô | 12 | 45 | 162 | Lệch LAB-1 nhiều nhất (0,35), xem §5 |
| [#5](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/5) E05 Nhiệt độ, alarm và SLA 15 phút | 13 (15 lá) | 62 | 208 | Đã tách E05-05, E05-13 |
| [#6](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/6) E06 Đơn hàng và phân bổ lô | 13 (17 lá) | 76 | 258 | Engine phân bổ 5 quy tắc + 34 ca biên |
| [#7](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/7) E07 Xuất hàng và POD (online) | 12 | 47 | 171 | POD offline và ảnh POD ở R1.1 |
| [#8](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/8) E08 Lập tuyến | 9 (10 lá) | 38 | 144 | Cờ giờ lái 2024: 17 SWP / 61 giờ |
| [#9](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/9) E09 ★ Giờ lái xe tải từ 2024 | 23 (36 lá) | 134 | 430 | Toàn bộ epic chịu ràng buộc. Rủi ro ước thấp ở 7 quy tắc nhiều ngày (§2) |
| [#10](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/10) E10 Truy xuất | 2 | 6 | 26 | L001 rút gọn |
| [#11](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/11) E11 Kiểm thử hệ thống, chuẩn bị phát hành R1 | 6 | 34 | 102 | Cờ giờ lái 2024: 5 SWP (E2E tuyến) |
| [#12](https://github.com/tamnv-1080/coldchain-lab5-backlog/issues/12) E12 Release 1.1 — viết spec | 11 | 32 | 96 | Chỉ giờ viết spec. Cờ giờ lái 2024: 3 SWP (spec sự cố tuyến) |
| **Tổng** | **130 (153 lá)** | **600** | **2.000** | R1: 568 SWP / 1.904 giờ. Chịu ràng buộc giờ lái 2024: **159 SWP / 514 giờ (26%)** |

**Phát triển R1.1 (ước thô, chưa thành issue — PREMISE A6).** Các mục R1.1★ của E12 — ★ ở đây nghĩa là chặn go-live, không phải giờ lái (POD offline, ảnh POD, 受取拒否, hồ sơ 逸脱, duyệt chính sách) chặn go-live. Lấy giờ LAB-1 của các feature tương ứng: khoảng **660 giờ**. Nhân tỉ lệ LAB-5/LAB-1 ở §5 (0,59) thì còn khoảng **390 giờ**. Khoảng 390–660 giờ là con số dùng để lập kế hoạch tới khi spec R1.1 xong và được break thành issue.

## 5. So với LAB-1

Giờ LAB-1 = man-day implement (BE + FE) của LAB-1 quy ra giờ theo hệ số trong bản LAB-1, **chưa cộng buffer**. Cột LAB-1 chỉ tính các feature mà R1 của LAB-5 cũng làm; phần đã loại ghi ở cột "Vì sao".

| Phần | LAB-1 (giờ) | LAB-5 (giờ) | Chênh | Vì sao |
|---|---|---|---|---|
| E01 ↔ F02 + F30 | 238 | 156 | −82 (0,66) | Đã loại màn 監査ログ照会 (F02-03, thuộc F27 phase sau) và 可用性レポート. LAB-1 tính "基盤" theo khối; LAB-5 chia nhỏ khoá đường ghi và bất biến sự kiện, mỗi mục nhỏ được điểm thấp |
| E02 ↔ F01 | 200 | 168 | −32 (0,84) | Gần nhau. LAB-1 có màn quản lý role (F01-04), LAB-5 thay bằng script (PREMISE S7) nhưng thêm RLS cho 4 nhóm bảng |
| E03 ↔ F05-07 | 42 | 79 | +37 (1,88) | R1 không có màn CRUD master (F05-01…06) và màn chính sách (F06), vì master nạp bằng seed và duyệt chính sách sang R1.1 (E12-05). LAB-5 cao hơn vì thêm cột vòng đời, hàm chọn version dùng chung và màn M001 |
| E04 ↔ F08 + F10 | 468 | 162 | −306 (0,35) | Đã loại 入荷予定 (F07-01), 一時温度帯申請, ロットラベル. Phần còn lại lệch nhiều nhất: 2 màn handy (R002, Q001) chỉ 7 SWP, 2 engine kiểm nhập hàng mỗi engine 9 giờ trong khi LAB-1 tính 42 giờ. **Chưa giải thích hết, coi là rủi ro ước thấp** |
| E05 ↔ F21 + F22-01 | 283 | 208 | −75 (0,74) | Đã loại hồ sơ 逸脱 (F22-02, sang R1.1). LAB-4 thiết kế chi tiết import và đợt alarm nên issue rõ, ít lệch |
| E06 ↔ F12–F14 | 587 | 258 | −329 (0,44) | LAB-1 nhân thêm hệ số độ khó nghiệp vụ (theo hệ số trong bản LAB-1) cho engine. LAB-5 chia engine thành 5 quy tắc + 34 ca biên; mỗi quy tắc nhỏ được điểm thấp. Rủi ro ước thấp. LAB-5 gồm script nạp lịch sử giao 18 giờ do PREMISE S4 thêm |
| E07 ↔ F15–F17 | 525 | 171 | −354 (0,33) | Đã loại POD offline (F17-03), ảnh POD, POD照会, 出庫票 (sang R1.1/phase sau). Phần còn lại: màn handy O005/O006 và D002 chỉ 10 SWP FE. Rủi ro ước thấp |
| E08 + E09 ↔ F19 + F20 | 608 | 574 | −34 (0,94) | Gần khớp, nhưng vì 2 lý do ngược chiều: LAB-4 thấy quy tắc nhiều ngày, giờ làm thực tế và số dư đầu kỳ phức tạp hơn LAB-1; trong khi từng quy tắc ở LAB-5 bị chấm thấp (§2). LAB-5 gồm phần PREMISE thêm: adapter bản đồ + spike (S5), kiểm khi lưu (S8), script số dư đầu kỳ (S3, S6) |
| E10 ↔ F24-01 | 123 | 26 | −97 (0,21) | L001 ở LAB-4 rút gọn (chỉ tra theo lô); LAB-1 tính màn cỡ L và nhân hệ số độ khó nghiệp vụ |
| **Tổng phần so được** | **3.074** | **1.802** | **−1.272 (0,59)** | |
| Phần LAB-1 có nhưng R1 không làm (21 feature ở trên) | 1.103 | 0 | — | Theo phạm vi LAB-4 §4: sang R1.1 hoặc phase sau. R1.1 hiện chỉ có 96 giờ viết spec |
| Chức năng LAB-4 không thiết kế (F03, F04, F09, F11, F18, F23, F25–F29) | 1.834 | 0 | — | 2 script nạp dữ liệu thuộc F29 (E06-11, E09-19, 36 giờ) đã tính ở dòng E06 và E08 + E09. Phần còn lại ngoài phạm vi backlog |
| QA kiểm thử hệ thống | ~1.183 (QA 8,45 người-tháng trong resource plan) | 210 (test tự động của QA-1, đã gồm E2E E11-01…04) | — | Không so được: LAB-5 chỉ tính test tự động gắn với issue. Thiết kế và chạy test case thủ công/UAT chưa thành issue (`task-breakdown.md` §4) |
| Buffer | Theo hệ số trong bản LAB-1 | 0 trong issue | — | LAB-5 giữ 15% ở capacity sprint (§3) |

**Kết luận.** Với cùng phạm vi, LAB-5 bằng khoảng 0,6 lần LAB-1. Không ép cho khớp, vì không bên nào chắc đúng hơn:

- LAB-1 là ước lượng rất thô (Super Rough), dùng các hệ số trong bản LAB-1.
- LAB-5 ước từ dưới lên. Tuy vậy, hệ số giờ do chính người lập backlog ước, và skill có xu hướng chấm thấp mục nhỏ.

Chỗ lệch tập trung ở màn hình handy và engine nghiệp vụ (E04, E06, E07). Tiêu chí đặt trước: nếu Sprint 1 chỉ đạt khoảng 60% số giờ kế hoạch thì LAB-1 đúng hơn. **Sprint 1 giả lập đạt 56%** (120/216 giờ) và giờ thực tế bằng 1,15 lần ước lượng, nên số liệu nghiêng về LAB-1. Một phần của 56% là do chờ khách và chờ phụ thuộc, không chỉ do ước thấp. Vì vậy chưa đổi hệ số: lập kế hoạch tổng thể theo khoảng LAB-5 → LAB-1, và tính lại hệ số cuối Sprint 2 (`progress-report.md` R5).
