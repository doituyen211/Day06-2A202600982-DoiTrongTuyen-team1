# Lịch sử Test Prompt & Failure Log (Auto-Substitute Engine)

## 1. Mục tiêu Prompt

Nhận thông tin `out_of_stock_item` (món bị hết), đối chiếu với `available_menu` và `user_preferences`. Output phải trả về JSON chuẩn xác định được `Confidence_Score` (0-100) và path tương ứng.

## 2. Test Cases dựa trên 4 Paths

### [TEST 01] Happy Path (Điểm > 90%)

- **Input:**
  - Hết: Trà sữa Trân châu đen (size L)
  - Còn: Trà sữa Trân châu trắng (size L)
  - User Pref: Không có kén ăn.
- **Expected:** `score > 90`, `action_path: "auto_swap"`.
- **Actual / Kết quả:** AI trả về `score: 95`. Lý do: Cùng nhóm thức uống, chênh lệch giá bằng 0.
- **Đánh giá:** PASS.

### [TEST 02] Low-confidence (Điểm 50-89%)

- **Input:**
  - Hết: Pizza Hải Sản
  - Còn: Pizza Gà Nấm, Mỳ Ý Hải Sản.
  - User Pref: Thích đồ biển.
- **Expected:** `score ~ 70-80`, `action_path: "user_choice"`. Trả về 2 option.
- **Actual / Kết quả:** AI trả về `score: 75`. Đưa ra 2 option vì Mỳ Ý (trùng vị biển nhưng khác loại), Pizza Gà (khác vị nhưng cùng bánh).
- **Đánh giá:** PASS.

### [TEST 03] Failure Path (Điểm < 50%)

- **Input:**
  - Hết: Salad chay (Vegan)
  - Còn: Cơm gà, Phở bò.
- **Expected:** `score < 50`, `action_path: "manual_fallback"`.
- **Actual / Kết quả:** Ban đầu AI gợi ý Phở Bò vì giá gần bằng (Fail).
- **Sửa lỗi (Correction):** Bổ sung rule vào System Prompt: _"Trừ 100 điểm (Veto) ngay lập tức nếu vi phạm nguyên tắc ăn kiêng (vd: Khách ăn chay nhưng gợi ý đồ mặn)."_
- **Re-test:** AI trả về `score: 0`, `action_path: "manual_fallback"`. Yêu cầu tài xế gọi điện. Đánh giá: PASS.

## 3. Failure Log Schema

Mọi path `Failure` hoặc user bấm `Hủy/Undo` ở Happy Path sẽ được log lại theo JSON sau để đưa về DB:

````json
{
  "timestamp": "2026-06-03T15:00:00Z",
  "order_id": "ORD-8912",
  "ai_suggestion": "Pepsi",
  "user_correction": "Cancel Item",
  "failure_reason": "User hates Pepsi even if Coke is unavailable",
  "action": "Update User_Preferences: dislikes_pepsi"
}

### 2. `group/prototype-readme.md`
```markdown
# Prototype README - Smart Auto-Substitute Engine

## Tổng quan Demo
Demo giải quyết bài toán: Tài xế giao đồ ăn gặp cảnh quán báo hết món. AI sẽ thay mặt tài xế giải quyết với khách dựa trên độ tự tin (Confidence).

## Kiến trúc (Tech Stack)
- **Backend:** Python + FastAPI (Giao tiếp với OpenAI/Gemini API để tính Confidence Score).
- **Frontend:** Next.js + TailwindCSS (Giả lập màn hình Tài xế và Màn hình App khách).

## Các Path cần chạy khi Demo Live
Khi trình bày, hãy làm theo đúng 3 kịch bản sau để show rõ năng lực rẽ nhánh của AI:
1. **Bấm hết món "Coca Cola":** Show ra UI màn hình khách tự động đổi sang Pepsi (Path: `Happy`).
2. **Bấm hết món "Pizza Bò":** Show ra UI popup hỏi khách chọn Pizza Gà hay Mỳ Ý (Path: `Low-confidence`).
3. **Bấm hết món "Salad Chay":** Show UI màn hình báo lỗi, app nhảy cảnh báo "Vui lòng gọi khách" bên máy tài xế (Path: `Failure` - minh chứng AI biết giới hạn).

## Hướng dẫn Run Local
1. Clone repo.
2. Tại thư mục backend:
   ```bash
   pip install -r requirements.txt
   uvicorn main:app --reload
   3. Tại thư mục frontend:
   ```bash
   npm install
   npm run dev
   4. Truy cập `http://localhost:3000` để bắt đầu dry-run.

### 3. `group/spec-final.md`
```markdown
# FINAL SPEC: Smart Auto-Substitute Engine

## 01. Evidence (Pain Point)
- **Vấn đề:** Đơn hàng Food Delivery (ShopeeFood/Grab) bị thiếu món khi tài xế tới quán.
- **Evidence:** Review thật của user bị hủy đơn oan vì không nghe máy; Tài xế than phiền mất 3-5 phút chờ đợi tại quán để gọi điện.

## 02. Slice (Phạm vi giải quyết)
- **User:** Tài xế (báo lỗi) và Khách hàng (nhận resolution).
- **Task:** Xử lý sự cố hết món tự động.
- **AI Decision:** JSON Output tính toán `Confidence_Score` từ 0 - 100 để quyết định rẽ nhánh.
- **Output:** Push Notification / Popup in-app cho khách (Tự đổi, bắt chọn, hoặc báo tài xế gọi).

## 03. Decision (Augment vs Automate)
Flow áp dụng cơ chế hybrid, con người không bao giờ mất hoàn toàn quyền kiểm soát:
- **Automate:** Tự đổi khi cực kỳ tự tin (Điểm > 90). Human có quyền Undo trong 30s.
- **Augment:** Chọn lọc từ 50 món xuống 2 món (Điểm 50-89). Human là người click chọn cuối cùng.

## 04. Failure (4 Paths để test)
1. **Happy:** AI tự động đổi món và bù tiền.
2. **Low-confidence:** AI show ra 2 lựa chọn thay thế tốt nhất, user chọn 1.
3. **Failure:** AI từ chối đưa ra quyết định (vì khách ăn chay nhưng chỉ còn đồ mặn). Yêu cầu tài xế gọi trực tiếp.
4. **Correction:** User bấm Undo/Hủy sau khi AI auto-swap -> Ghi log vào rule cá nhân của user.

## 05. Owner
- **Dev Backend:** Setup prompt tính điểm, API FastAPI.
- **Dev Frontend:** Dựng 2 màn giả lập (Tài xế bấm nút + Màn khách nhận thông báo).
- **PM/Presenter:** Chuẩn bị Slide (HTML), narrative dry-run 3 path.

### 4. `individual/reflection.md`
```markdown
# Individual Reflection

**Người viết:** [Tên của bạn]

Qua quá trình làm demo Hackathon này, tôi đã thay đổi một mindset rất lớn về việc thiết kế AI Product.

Trước đây, khi nghĩ đến AI, tôi luôn kỳ vọng tạo ra một "super flow" (Happy Path) giải quyết mọi thứ 100% tự động. Nhưng khi mapping vào bài toán giao đồ ăn thực tế, tôi nhận ra việc "cố quá" sẽ dẫn đến hệ lụy tồi tệ: AI tự động đổi món mặn cho người ăn chay, gây mất niềm tin khủng khiếp cho người dùng.

Bài học cốt lõi tôi rút ra: **Giá trị thực sự của AI không nằm ở việc nó luôn đúng, mà nằm ở việc nó biết tính toán độ không chắc chắn (Low-confidence / Failure) để trả lại quyền quyết định (Augment) cho con người ở đúng thời điểm.**

Cơ chế 4 paths (Happy, Low-confidence, Failure, Correction) đã giúp team tôi xây dựng một prototype tuy nhỏ (Slice) nhưng chứng minh được một luồng tư duy UX Product hoàn chỉnh. Log Correction ở chặng cuối cũng là key quan trọng để AI học và "bớt sai" đi trong các cuốc xe tương lai.

Tất cả đã sẵn sàng. Chúc nhóm bạn có một buổi sáng mai ghép code build demo thật trơn tru và pitch thành công!
````
