# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: HỨA QUANG LINH
- **Student ID**: 2A202600466
- **Date**: 06/04/2026

---

## I. Technical Contribution (15 Points)

- **Modules Implementated**:
  - `src/agent/agent.py`
  - `src/tools/find_common_free_slots.py`
  - `src/tools/book_meeting.py`
  - `src/tools/send_invitation_email.py`
  - `run_prompts.py`

- **Code Highlights**:
  - Xây dựng vòng lặp `Thought -> Action -> Observation` trong `src/agent/agent.py`, cho phép agent gọi tool theo từng bước thay vì cố trả lời ngay như chatbot baseline.
  - Thiết kế prompt hệ thống có ràng buộc rõ ràng: chỉ được sinh một `Action` mỗi lượt, phải chờ `Observation` thật, không được tự bịa `booking_id`, và ngày phải dùng định dạng `YYYY-MM-DD`.
  - Cài đặt parser cho action bằng `ast`, giúp đọc keyword arguments an toàn hơn so với tách chuỗi thủ công.
  - Hoàn thiện bộ tool cho workflow đặt lịch họp thực tế: tìm lịch rảnh chung, tạo booking, gửi email mời và ghi lại kết quả vào `bookings.json` và `sent_emails.json`.
  - Tổ chức script `run_prompts.py` để so sánh trực tiếp giữa chatbot baseline và agent trên cùng một bộ prompt dùng chung.

- **Documentation**:
  - `ReActAgent` nhận câu hỏi từ người dùng, gửi prompt vào provider LLM, parse `Action`, gọi tool tương ứng trong `src/tools/registry.py`, rồi đưa `Observation` quay lại prompt cho bước tiếp theo.
  - Bộ công cụ trong `src/tools/` đóng vai trò như môi trường bên ngoài của agent. Chính các observation từ tool giúp agent chuyển từ suy luận thuần ngôn ngữ sang hành động có kiểm chứng.
  - Dữ liệu đầu ra trong `src/tools/bookings.json` và `src/tools/sent_emails.json` là bằng chứng cho thấy agent không chỉ “nói” mà đã thực hiện đúng pipeline nhiều bước.

---

## II. Debugging Case Study (10 Points)

- **Problem Description**:
  - Lỗi nổi bật của Agent v1 là hiện tượng `chain hallucination`: mô hình tự sinh liên tiếp nhiều bước trong cùng một lần phản hồi, bao gồm cả `Observation` giả và `booking_id` giả, thay vì dừng sau một tool call để chờ kết quả thật từ hệ thống.

- **Diagnosis**:
  - Nguyên nhân gốc không nằm ở tool mà nằm ở cách điều khiển mô hình. Nếu system prompt không ràng buộc chặt, LLM có xu hướng “giải luôn cả chuỗi” trong một forward pass: tự tưởng tượng booking đã được tạo xong, tự gán `booking_id=12345`, rồi tiếp tục gọi `send_invitation_email`.
  - Đây là lỗi nguy hiểm vì kết quả nhìn bề ngoài có vẻ hợp lý, nhưng dữ liệu lại không đồng bộ với hệ thống thật. Nếu parser chỉ lấy tool call đầu tiên, bug có thể bị che khuất chứ chưa được xử lý tận gốc.
  - Một lỗi phụ được ghi nhận trong báo cáo nhóm là mô hình từng sinh sai năm ở tham số ngày họp (`2025` thay vì `2026`), cho thấy agent cần guardrail rõ ràng hơn ở bước chuẩn hóa input.

- **Solution**:
  - Bổ sung rule trong system prompt: `Generate ONLY ONE Action per response. Do NOT simulate or predict future Observations.`
  - Ép agent chỉ được sử dụng `booking_id` lấy từ observation thật của tool `book_meeting`.
  - Thêm ràng buộc ngày họp phải theo định dạng `YYYY-MM-DD` và không được nhỏ hơn ngày hiện tại.
  - Dùng parser dựa trên `ast` để xử lý arguments chắc chắn hơn, giảm lỗi khi LLM sinh tham số có kiểu dữ liệu khác nhau.
  - Sau khi siết prompt và guardrail, agent chuyển sang hành vi đúng: tìm lịch rảnh -> đặt lịch -> gửi email, mỗi bước đều dựa trên dữ liệu thật từ tool trước đó.

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

1. **Reasoning**: `Thought` block giúp agent tách bài toán lớn thành các quyết định nhỏ, ví dụ phải tìm khung giờ rảnh trước khi đặt lịch và chỉ gửi email sau khi có `booking_id` thật. Chatbot baseline không có cơ chế này nên thường chỉ trả lời bằng hướng dẫn ngôn ngữ tự nhiên thay vì hoàn thành tác vụ.

2. **Reliability**: Agent không phải lúc nào cũng tốt hơn chatbot. Với câu hỏi đơn giản, chatbot nhanh hơn, rẻ hơn và ít vòng lặp hơn. Agent lại dễ mắc lỗi parser, gọi sai tool, hoặc kéo dài context gây tăng latency và chi phí. Điều này thể hiện rõ trong bảng so sánh của báo cáo nhóm: agent thắng ở multi-step task nhưng thua chatbot về cost và thời gian phản hồi cho tác vụ đơn giản.

3. **Observation**: Observation là yếu tố quyết định sự khác biệt giữa chatbot và agent. Khi `find_common_free_slots` trả về khung giờ thật, agent có căn cứ để chọn thời điểm đặt họp. Khi `book_meeting` trả về `booking_id`, agent mới có dữ liệu hợp lệ để gửi email. Nói cách khác, observation biến quá trình suy luận từ “đoán” thành “ra quyết định dựa trên trạng thái môi trường”.

Từ lab này, em rút ra rằng chatbot phù hợp cho tác vụ hỏi đáp hoặc tóm tắt, còn agent phù hợp cho tác vụ có nhiều bước phụ thuộc lẫn nhau. Tuy nhiên, agent chỉ thực sự đáng tin khi tool spec rõ ràng, parser chắc chắn và telemetry đủ tốt để phát hiện sai lệch hành vi của mô hình.

---

## IV. Future Improvements (5 Points)

- **Scalability**: Chuyển dữ liệu `schedule`, `bookings` và `sent_emails` từ file JSON sang database như PostgreSQL để hỗ trợ nhiều phiên chạy đồng thời, truy vấn tốt hơn và dễ audit hơn.
- **Safety**: Thêm lớp validation schema cho từng tool, kiểm tra email organizer theo whitelist domain, từ chối booking trong quá khứ, và thêm cơ chế chặn khi LLM sinh nhiều hơn một `Action` trong một lượt.
- **Performance**: Giảm chi phí bằng cách rút gọn prompt, cắt bớt history không cần thiết, dùng caching cho những lần kiểm tra lịch lặp lại, và bổ sung provider fallback để tránh timeout khi model chính phản hồi chậm.

---
