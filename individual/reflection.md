# Individual Reflection

**Người viết:** [Tên của bạn]  
**Vai trò:** [Vai trò của bạn trong team]

---

Qua quá trình làm demo Hackathon này, tôi đã thay đổi một mindset rất lớn về việc thiết kế sản phẩm AI (AI Product Design).

Trước đây, khi nghĩ đến việc áp dụng AI vào ứng dụng thực tế, tôi thường rơi vào cái bẫy kỳ vọng tạo ra một "Super Flow" (Happy Path) - nơi AI có thể tự động hóa và giải quyết mọi thứ 100%. Tuy nhiên, khi mapping vào bài toán giao đồ ăn thực tế, tôi nhận ra việc "cố đấm ăn xôi" bắt AI tự quyết định trong mọi trường hợp sẽ dẫn đến hệ lụy UX tồi tệ. Ví dụ: AI tự động đổi món mặn cho một người đang ăn chay chỉ vì hai món có giá tiền bằng nhau. Điều này sẽ phá hủy hoàn toàn niềm tin của người dùng vào hệ thống.

---

## Bài học cốt lõi

Giá trị thực sự của một hệ thống AI tốt không nằm ở việc nó luôn luôn đúng, mà nằm ở việc nó biết tính toán độ không chắc chắn (Low-confidence / Failure) để trả lại quyền quyết định (Augment) cho con người ở đúng thời điểm.

---

## Key Takeaways từ thiết kế 4 paths

Cơ cấu 4 paths (Happy, Low-confidence, Failure, Correction) đã giúp team tôi xây dựng một prototype tuy nhỏ (chỉ cắt một Slice), nhưng chứng minh được một tư duy thiết kế trọn vẹn:

- Dám cho AI tự động hóa khi rủi ro thấp.
- Biết thiết kế UX để hỏi lại khách hàng khi rủi ro ở mức trung bình.
- Và quan trọng nhất, biết "giơ tay xin hàng" để con người can thiệp khi rủi ro cao.

---

## Correction Loop (Điểm quan trọng nhất)

Cuối cùng, tư duy "Correction" (lưu lại log khi user từ chối gợi ý của AI) là một điểm sáng giúp hệ thống không chỉ giải quyết sự cố hiện tại mà còn tự cải thiện trong tương lai.

Đây chính là cách thiết kế AI lấy con người làm trung tâm (Human-Centered AI) mà tôi sẽ áp dụng vào các dự án sau này.
