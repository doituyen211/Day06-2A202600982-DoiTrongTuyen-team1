# Prototype README - Smart Auto-Substitute Engine

## Tổng quan Demo

Prototype này giải quyết một bài toán (pain point) rất cụ thể trong quá trình giao nhận đồ ăn (Food Delivery): Tài xế đến quán thì phát hiện hết món.  
Thay vì bắt tài xế đứng chờ và gọi điện cho khách hàng (gây mất thời gian, giảm tỷ lệ hoàn thành cuốc), AI sẽ thay mặt tài xế giải quyết dựa trên độ tự tin (Confidence Score).

## Kiến trúc (Tech Stack)

**Backend:** Python + FastAPI. Đóng vai trò nhận API từ Frontend, ghép với System Prompt và gọi LLM (OpenAI/Gemini). Xử lý logic tính điểm Confidence_Score và trả về kết quả JSON.

**Frontend:** Next.js + TailwindCSS. Dựng nhanh 2 màn hình giả lập để phục vụ demo live:

- Màn hình của Tài xế/Quán ăn: Chỉ có nút `[Báo hết món X]`.
- Màn hình App Khách hàng: Hiển thị Push Notification hoặc Popup tương tác xử lý sự cố.

## Các Path cần chạy khi Demo Live (Dry Run)

Để chứng minh với Ban giám khảo rằng AI của chúng ta biết giới hạn của chính mình, người thuyết trình (Presenter) cần demo đúng 3 kịch bản sau:

### Path 1 - Happy Path (AI Tự tin > 90%):

Action: Bấm hết món "Coca Cola" (trong khi quán còn Pepsi).

Result: Show UI màn hình khách nhận thông báo tự động đổi sang Pepsi (Kèm nút Undo đếm ngược 30s).

---

### Path 2 - Low-confidence (AI Phân vân 50% - 89%):

Action: Bấm hết món "Pizza Bò" (trong khi quán còn Pizza Gà, Mỳ Ý).

Result: Show UI popup hỏi khách chọn 1 trong 2 món thay thế tốt nhất do AI đề xuất. Khách bấm chốt.

---

### Path 3 - Failure Path (AI Không chắc chắn < 50%):

Action: Bấm hết món "Salad Chay" (trong khi quán chỉ còn đồ mặn).

Result: Show UI màn hình app khách nhảy cảnh báo: "Món của bạn đã hết, tài xế đang gọi điện hỗ trợ". Đồng thời màn hình tài xế nhận lệnh yêu cầu gọi điện trực tiếp. Minh chứng rõ ràng nhất cho việc AI biết "giơ tay xin hàng".

## Hướng dẫn Run Local (Dành cho Dev)

Clone repo về máy.

### Setup Backend:

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
