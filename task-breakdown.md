# Task breakdown — từ bộ thiết kế LAB-4 tới backlog trên GitHub Project

Nguồn duy nhất của backlog: [`backlog/backlog.yaml`](backlog/backlog.yaml). Issue trên Project được sinh từ file này bằng [`scripts/push-backlog-to-github-project.py`](scripts/push-backlog-to-github-project.py); tiêu đề mỗi issue bắt đầu bằng mã backlog (`E09-04b · …`) để tra ngược.

## 1. Nguyên tắc chia task

### 1.1 Độ hạt — chia tới đâu thì dừng

| Quy tắc | Nội dung |
|---|---|
| Một issue = một phần giao được | Review được trong một PR, có điều kiện nghiệm thu kiểm được (test, wireframe, hợp đồng BM-52). Không có issue kiểu "làm màn X" chung chung |
| Tách theo lớp khi lớp đó có người làm riêng | `[DB]` migration/RPC (BE-2) · `[BE]` engine TS + route API (BE-1) · `[FE]` màn hình · `[QA]` test tự động. Gộp `[DB+BE]` khi RPC và route nhỏ, một người làm liền mạch tốt hơn |
| Trần kích thước | Mục lá ≤ 8 SWP (≈ ≤ 3 ngày công). Lớn hơn thì tách |
| Dừng tách | Khi tách thêm sẽ ra phần không test riêng được, hoặc nhỏ hơn ~2 giờ |
| Việc không phải code vẫn là issue | Câu hỏi cho khách (`clarification`), spike có time-box (`spike`), viết spec R1.1 (`[DOC]`) — vì chúng chặn issue khác và tốn giờ thật |

### 1.2 Khi nào tách sub-issue

Tách sub-issue khi một issue chứa **nhiều quy tắc nghiệp vụ độc lập, mỗi quy tắc có bảng ca biên riêng** trong BM-53. Mỗi quy tắc thành một sub-issue để chấm SWP, giao việc và báo tiến độ riêng. Issue cha khi đó chỉ là vỏ gom: không ước lượng, SWP/giờ của cha = tổng các con.

Áp dụng ở hai chỗ có nhiều biến nhất:
- `E06-03` engine phân bổ: 消費期限, dải nhiệt, hạn giao theo hợp đồng, 日付逆転, FEFO.
- `E09-03` / `E09-04` kiểm giờ lái: 4 nhóm quy tắc trong ngày, 7 quy tắc nhiều ngày (ràng buộc 2024).

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

<!-- §2–§4 viết sau khi backlog qua review độc lập -->
