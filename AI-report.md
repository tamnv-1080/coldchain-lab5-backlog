# AI-report — Cách dùng AI trong LAB-5

| Mục | Giá trị |
|---|---|
| Người thực hiện | tamnv-1080 (PL/BrSE) |
| Công cụ | Claude Code (model Opus) + Takumi kit, chạy trong VS Code; `gh` CLI + GitHub GraphQL |
| Ngày | 2026-11-23 → 2026-11-25 |
| Sản phẩm | Backlog 12 epic · 130 issue · 32 sub-issue (153 mục lá) trên [GitHub Project](https://github.com/users/tamnv-1080/projects/2); 4 script; báo cáo SWP HTML; 6 file nộp |

Mô hình làm việc giống LAB-4: **1 AI chính điều phối + agent cho việc lặp + reviewer độc lập chỉ đọc + người duyệt ở 3 cổng**. Trước mỗi bước, AI trình chiến lược và các điểm cần chốt, người duyệt xong mới làm.

## 1. Skill, prompt và agent đã dùng

| Việc | Cách làm | Đầu vào → đầu ra |
|---|---|---|
| **Chia task** | AI chính, không dùng skill riêng. Đọc spec LAB-4 theo thứ tự README feature → spec màn (BM-51) / API (BM-52) / logic (BM-53) → DB (BM-50), mục "task gợi ý cho LAB-5" trong 10 ADR, bảng DIV-01…39. Quy tắc chia ghi ở `task-breakdown.md` §1 | Spec LAB-4 → [`backlog/backlog.yaml`](backlog/backlog.yaml) (nguồn duy nhất). Script [`validate-and-summarize-backlog.py`](scripts/validate-and-summarize-backlog.py) kiểm key trùng, phụ thuộc hỏng, mục lá thiếu phạm vi/nghiệm thu |
| **Review backlog** | 1 agent `read-only-reviewer` (không có quyền ghi). Prompt chỉ đưa đường dẫn spec + backlog và các tiêu chí: độ phủ spec, ràng buộc giờ lái 2024, câu chép từ RFP. **Không đưa kết luận của AI chính** để reviewer không bị dẫn | Backlog nháp → 27 phát hiện |
| **Đẩy lên GitHub Project** | Script [`push-backlog-to-github-project.py`](scripts/push-backlog-to-github-project.py) do AI viết, chạy được nhiều lần không tạo trùng (lưu trạng thái ở `backlog/github-issue-map.json`) | YAML → 174 issue, sub-issue, quan hệ blocked-by, field, label |
| **Chấm SWP** | Skill `tkm:estimate-swp`. Lệnh: `/tkm:estimate-swp https://github.com/users/tamnv-1080/projects/2 --no-push-kpi --level medium`. Skill tự gọi `tkm:confidence`, chia 5 worker chấm song song, tự chọn 5 mẫu đại diện cho người duyệt | Issue trên Project → [báo cáo HTML](reports/estimate-swp-coldchain-lab5-backlog-20261123-070414.html), 600 SWP |
| **Ghi SWP và giờ lên Project** | [`compute-estimates.py`](scripts/compute-estimates.py) đọc payload nhúng trong báo cáo HTML (+ file tách mục sau chấm) → `estimates.json`. Agent ghi là AI chính (Claude Code) chạy lệnh `set-estimates` của script đẩy, không dùng subagent riêng; chỉ chạy sau khi người duyệt SWP (Cổng 2). Ghi field SWP và "Giờ ước lượng"; cha = tổng con. Sau đó đọc lại Project để so | 174/174 mục khớp |
| **Quy giờ** | AI chọn 11 mẫu, ước giờ trực tiếp → hệ số theo lớp (FE 5,5 giờ/SWP, lớp khác 3,0). So với ước lượng LAB-1 cùng phạm vi | [`estimate.md`](estimate.md) |
| **Sprint giả lập** | Kịch bản ở [`sprints/sprint-1-simulation.yaml`](sprints/sprint-1-simulation.yaml). Script [`simulate-sprint.py`](scripts/simulate-sprint.py) tạo field Iteration (GraphQL, vì `gh` CLI không tạo được kiểu ITERATION), ghi Status/Iteration, đóng issue Done, vẽ burndown SVG, đọc lại Project | 23 mục Sprint 1, 0 lệch khi đọc lại |
| **Báo cáo tiến độ** | AI chính soạn. Bảng trạng thái, giờ theo người, burndown lấy từ số `simulate-sprint.py report` in ra. Dự báo (BE còn ~1.090 giờ, M1 còn 255 giờ) do AI tính thêm bằng một lệnh Python trên `estimates.json`, không nằm trong script. 1 reviewer chỉ đọc soát số liệu và tìm chỗ "tô hồng", prompt không chứa kết luận của AI chính | [`progress-report.md`](progress-report.md) (tiếng Nhật) |

**Prompt chính theo việc** (tóm tắt, không phải nguyên văn; từng lần duyệt ghi ở nhật ký làm bài):

| Việc | Prompt / chỉ dẫn |
|---|---|
| Chia task | Dán nguyên đề + "Hãy nêu chiến lược làm bài này trước rồi cùng tiến hành". Người duyệt 7 quyết định AI đề xuất: chỉ break chi tiết R1, R1.1 chỉ là issue viết spec; mục lá ≤ 8 SWP; mỗi quy tắc giờ lái 1 sub-issue; người phụ trách giả định bằng field; giờ = SWP × hệ số từ mẫu ước trực tiếp; sprint 2 tuần |
| Review backlog | "Đối chiếu backlog với spec LAB-4: độ phủ API/DIV/RPC, việc chịu ràng buộc giờ lái 2024 có bị gộp hoặc thiếu cờ không, có câu chép từ RFP không; trả phát hiện theo mức BLOCKER/MAJOR/MINOR kèm dòng dẫn chứng" |
| Chấm SWP | Lệnh skill ở bảng trên. Người trả lời các câu hỏi của skill cho từng mẫu (mức khó, điểm) |
| Quy giờ | Người chọn giữa 2 phương án AI đưa: một hệ số chung 3,0 hay hệ số theo lớp; chọn theo lớp, "không ép theo LAB-1" |
| Báo cáo tiến độ | Người chốt: viết tiếng Nhật, gửi khách được. Prompt reviewer: "Soát mọi con số với nguồn; tìm chỗ tô hồng: tin xấu bị làm nhẹ, bỏ sót hoặc chôn vùi; phụ thuộc được nêu có đúng backlog không; nội dung nội bộ không nên gửi khách" |

## 2. Cách review output của AI

### 2.1 Các lớp kiểm

| Lớp | Kiểm gì |
|---|---|
| **Máy** | Validator backlog; đếm độ phủ (mọi API ghi, DIV, RPC đều có issue); đọc lại Project sau mỗi lần ghi (issue = item, blocked-by, cha–con, SWP, giờ, trạng thái sprint); assert "tách issue giữ tổng SWP" trong script |
| **Reviewer độc lập** | 2 lần: backlog trước khi publish (~6 phút, ~180k token) và báo cáo tiến độ trước khi đưa người kiểm (~4 phút, ~90k token). Reviewer chỉ đọc, không biết kết luận của AI chính |
| **AI chính tự kiểm** | Mỗi phát hiện của reviewer được kiểm lại bằng spec/số liệu trước khi sửa, không sửa theo phản xạ |
| **Người** | Cổng 1: duyệt backlog + yêu cầu review độc lập trước khi publish. Cổng 2: duyệt 5 mẫu SWP (2 mẫu đầu qua 2 vòng: chọn mức khó → chọn điểm; 3 mẫu còn lại chấp nhận chung một lượt), quyết tách mục quá trần, quyết hệ số giờ theo lớp. Cổng 3: kiểm báo cáo tiến độ, **đang chờ người kiểm bản đã sửa** |

### 2.2 Vấn đề phát hiện và cách xử lý

| Vấn đề | Ai phát hiện | Xử lý |
|---|---|---|
| Việc của ràng buộc giờ lái 2024 nằm lẫn trong epic lập tuyến mà không mang cờ; câu "toàn bộ effort ràng buộc nằm trong E09" của AI là sai (BLOCKER) | Reviewer backlog | Cờ ở cấp issue (44 mục, 8 mục ngoài E09); tách API lưu đoạn tuyến (PREMISE S8); viết lại H5 |
| 11 lỗi lớn khác: số ca biên phân bổ ghi 23 (đúng là 34), không có RPC ghi PICKED/LOADED nên điều kiện nghiệm thu làm xuất hàng không chạy, không có cách gán role khi vận hành, biên ghi trễ, MFA đặt sai chỗ… | Reviewer backlog | AI kiểm lại 7 phát hiện then chốt bằng spec (đúng cả 7) rồi sửa; thêm 7 issue, sửa phụ thuộc, thêm PREMISE S6–S9, A7–A8, H6 |
| YAML viết dạng `[a, b]` cho câu có dấu phẩy → câu bị cắt | Validator | Chuyển sang danh sách khối |
| GraphQL từ chối số thực ("16.5") vì `gh -F` gửi dạng chuỗi; lỗi "already linked" làm script dừng; mạng reset | Khi chạy script | Đưa số thẳng vào mutation; bỏ qua lỗi "đã liên kết"; retry lỗi mạng. Script chạy tiếp không tạo trùng |
| 2 mục 10 SWP vượt trần 8 SWP | AI tự soát sau khi chấm | Người quyết tách, giữ tổng (#171–#174) |
| Sub-issue quy tắc giờ lái bị chấm rất thấp (1 SWP): chia càng nhỏ, body càng ngắn, AI chấm càng thấp | AI tự soát | Người quyết giữ điểm, ghi là rủi ro ước thấp |
| **Hệ số giờ 3,0 lấy từ 6 mẫu không có màn hình nào → FE chỉ bằng 0,22 lần LAB-1** | AI tự phát hiện khi so với LAB-1 | Dừng lại đưa người quyết, không tự sửa số đã chốt. Người chọn hệ số theo lớp (FE 5,5) |
| Sprint 1 không có màn hình nào làm được vì mọi issue FE đều chờ API | AI khi chọn phạm vi sprint | Chuyển 2 FE sang engine TS không phụ thuộc (PREMISE H7); thêm spec R1.1 cho BrSE |
| **Báo cáo tiến độ "tô hồng"**: số đúng nhưng không nói mốc M1 đã mất; dự báo M3 dùng tốc độ cả đội thay vì nút thắt BE; "trong 15% dự phòng" bị chính báo cáo phản bác; **AI bịa việc FE/QA làm trong giờ trống**; khẳng định một phụ thuộc không có trong backlog; đưa phương án đăng nhập email/password như thể tự quyết; link tài liệu nội bộ trong báo cáo gửi khách | Reviewer báo cáo (2 BLOCKER, 9 cần sửa) | AI tính lại theo BE (còn ~1.090 giờ; M1 còn 255 giờ, BE-2 150 giờ) rồi viết lại: kết luận ngay đầu báo cáo, M1 tách 2 bước, M3 thành khoảng cho 2 phương án, nêu thẳng 90 giờ không có việc, phương án đăng nhập thành đề xuất chờ khách duyệt |

## 3. Nhận xét

**Điểm đặc biệt**
- **Một nguồn, nhiều đầu ra.** Backlog, SWP, giờ và sprint đều sinh từ file dữ liệu bằng script, nên Project, báo cáo và burndown không lệch nhau; mọi lần ghi đều có bước đọc lại.
- **Ràng buộc giờ lái 2024 lọc được và cộng riêng được:** cờ ở cấp issue + field trên Project. 44 mục, 159 SWP, 514 giờ (26%).
- **Chỗ hở của LAB-4 thành dữ liệu có địa chỉ:** mỗi chỗ hở trỏ về một dòng PREMISE hoặc một issue làm rõ (`task-breakdown.md` §4).

**Làm được**
- Review độc lập bắt được lỗi mà AI chính không tự thấy, ở cả 2 lần: lần 1 về phạm vi ràng buộc, lần 2 về cách diễn giải. Điều kiện là prompt không chứa kết luận của AI chính.
- AI tự dừng ở các điểm phải do người quyết (hệ số giờ, tách mục, điểm thấp), không tự sửa số đã chốt.
- So với LAB-1 bằng số cùng phạm vi, nên chỉ ra được chỗ ước thấp cụ thể (E04, E06, E07) và nút thắt BE, thay vì chỉ có một con số tổng.

**Cần cải thiện**
- **Skill chấm SWP chấm thấp màn hình và các mảnh nhỏ.** Phải bù bằng hệ số theo lớp. Lần sau nên đưa mẫu màn hình vào bước hiệu chỉnh của skill ngay từ đầu.
- **AI có xu hướng chọn cách nói dễ nghe** khi viết báo cáo cho khách. Số đúng chưa đủ; báo cáo tiến độ phải luôn qua reviewer độc lập và người kiểm.
- **Backlog thiếu việc FE làm được sớm:** mọi màn hình đều chờ API. Nên tách sẵn issue dựng màn theo hợp đồng API (BM-52) ngay lúc break.
- **Thiết kế test thủ công và UAT chưa thành issue**, nên kế hoạch không thể hiện việc của QA.
- **Dữ liệu sprint là giả lập:** hệ số giờ chỉ được kiểm thật khi có velocity thật.
- **Chưa ghi giờ người đọc và duyệt**, nên chưa tính được AI tiết kiệm bao nhiêu công.
