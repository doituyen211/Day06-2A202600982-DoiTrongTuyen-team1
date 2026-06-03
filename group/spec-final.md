# FINAL SPEC: Smart Auto-Substitute Engine

## 01. Evidence (Pain Point Thực Tế)

**Vấn đề:** Trong mảng Food & Local Delivery (ShopeeFood, Grab), sự cố "hết món" khi tài xế tới nơi là một điểm nghẽn lớn.

**Evidence:**

- **Tài xế:** Mất trung bình 3-5 phút đứng chờ tại quán để gọi điện đổi món, làm giảm năng suất chạy cuốc trong giờ cao điểm.
- **Khách hàng:** Không phải lúc nào cũng cầm điện thoại. Lỡ cuộc gọi dẫn đến đơn bị hủy oan uổng hoặc giao thiếu đồ, gây ức chế (dựa trên nhiều review thực tế trên app).

---

## 02. Slice (Phạm Vi Giải Quyết)

Cắt một flow cực nhỏ gọn để build trong Hackathon:

- **Task:** Tự động hóa quá trình xử lý sự cố "Hết món".
- **User:** Tài xế (người trigger sự cố) và Khách hàng (người nhận resolution).
- **AI Decision:** AI phân tích menu khả dụng, lịch sử mua hàng, chênh lệch giá -> Tính toán Confidence_Score (0-100).
- **Output:** Giao diện tương tác trên màn hình App Khách hàng.

---

## 03. Decision (Augment vs Automate)

Flow này áp dụng thiết kế hybrid, con người không bao giờ mất hoàn toàn quyền kiểm soát:

- **Automate (Tự làm):** Áp dụng khi AI cực kỳ tự tin (Confidence > 90).  
  → AI tự đổi món, bù trừ tiền.  
  → Human rights: Khách có quyền Undo/Hủy trong 30 giây đầu tiên.

- **Augment (Gợi ý):** Áp dụng khi AI phân vân (Confidence 50–89).  
  → AI lọc từ một menu dài xuống còn 2 lựa chọn tối ưu nhất.  
  → Human rights: Khách hàng là người click chọn quyết định cuối cùng.

---

## 04. Failure (Các Path Phải Test)

Dự án không chỉ demo "Happy Path" mà user story trải dài qua 4 nhánh UX:

- **Happy (Confidence > 90%):**  
  AI đúng và tự tin -> Tự động đổi (Auto-swap).

- **Low-confidence (Confidence 50–89%):**  
  AI không chắc -> Thu hẹp lựa chọn, hỏi ý kiến khách hàng.

- **Failure (Confidence < 50%):**  
  AI sai hoặc thiếu dữ kiện an toàn (vd: rủi ro đổi đồ mặn cho người ăn chay) -> Hệ thống nhường quyền, chuyển người thật (tài xế gọi điện).

- **Correction (Vòng lặp học tập):**  
  Khi user sửa, từ chối, hoặc bấm Hủy sau auto-swap -> Ghi nhận log sự kiện để cập nhật rule vào database hồ sơ cá nhân.

---

## 05. Owner (Kế Hoạch Thực Thi Sáng Mai)

- **Dev Backend:** Viết cấu trúc Prompt JSON, tích hợp API, tinh chỉnh logic cộng/trừ điểm Confidence.
- **Dev Frontend:** Code mockup UI Next.js cho 2 màn hình (Tài xế trigger & Khách hàng nhận push).
- **PM/Presenter:** Thiết kế Slide (HTML), ghép nối flow, chạy dry-run kịch bản thuyết trình đảm bảo rẽ đủ các path.
