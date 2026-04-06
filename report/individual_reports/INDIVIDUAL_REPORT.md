# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: Chu Bá Tuấn Anh
- **Student ID**: 2A202600012
- **Date**: 2026-04-06

---

## I. Technical Contribution (15 Points)

_Mô tả các phần đóng góp kỹ thuật trong quá trình phát triển Agent:_

- **Modules Implemented**:
  - `src/tools/book_meeting.py`: Tách bạch Single Responsibility, loại bỏ logic tự động gửi mail ẩn trong code phòng khi Agent bị lú, và thêm logic auto-correct lỗi ảo giác đơn vị của LLM (nếu `duration > 12`, tự tính toán lại thành số giờ `duration / 60`).
  - `src/agent/agent.py`: Inject Dynamic System Prompt. Đưa thẳng thời gian thực của hệ thống vào Prompt để tạo Grounding Context ngày giờ.
  - `src/agent/ui.py`: Bổ sung tuỳ chọn config `nine_router` vào giao diện Streamlit, thiết lập đọc giá trị model/API/Base URL mapping đúng từ `.env`.
- **Code Highlights**:
  ```python
  # Trong agent.py - Cung cấp Neo Thời Gian để tính toán thuật ngữ "tuần kế tiếp"
  current_date = datetime.now().strftime("%Y-%m-%d")
  return f"""...
  Important: The current date is {current_date}. Keep this in mind when dealing with scheduling such as 'next week' or 'tomorrow'.
  ..."""
  ```
- **Documentation**: Việc thiết lập lại agent theo flow: Tìm khung giờ rảnh -> Đặt Lịch độc lập -> Gửi Mail độc lập, cộng với việc đưa Time context, biến một LLM ảo giác thành một Agent hiểu mạch thời gian thực. Giao diện UI Streamlit cũng được tích hợp giúp test Nine Router nhanh, thay thế CLI tẻ nhạt.

---

## II. Debugging Case Study (10 Points)

_Phân tích lỗi mất đồng bộ dữ liệu nội bộ (Stale Data Cache) giữa các Tool._

- **Problem Description**: LLM gọi `book_meeting` thành công, lưu dữ liệu hệ thống. Sau đó LLM gọi `send_invitation_email` bằng đúng ID vừa được cấp nhưng tool trả về lỗi: `Booking ID không tồn tại`.
- **Log Source**: `logs/agent-20260406_*.log`
- **Diagnosis**: Các Tool (class) được thiết kế ban đầu để load dữ liệu file json (như `bookings.json`, `schedule.json`) _duy nhất một lần_ ở block `__init__()`. Khi Agent loop qua tool `book_meeting`, dữ liệu Json được update xuống ổ cứng thành công nhưng Class instance của `send_invitation_email` đã được khởi tạo từ trước, nó vẫn giữ cache data cũ của phiên làm việc. Do vậy, tool check memory cache không thấy ID mới nên văng lỗi.
- **Solution**: Sửa đổi toàn bộ các tool. Xóa/chuyển logic load biến từ `__init__` sang một hàm riêng biệt là `self._load_data()`. Cập nhật file tool để chạy `self._load_data()` ở ngay dòng đầu tiên trong mọi hàm thực thi (như `def send_invitation_email(...)`). Bắt buộc tool phải Fresh Read data từ ổ cứng mỗi khi được call.

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

_Suy ngẫm về sự khác biệt trong năng lực suy luận._

1.  **Reasoning**: Khối `Thought` hoạt động như một vùng nhớ nháp (Scratchpad). Khác biệt rõ nhất là sau bước nhận diện danh sách rảnh chung từ hệ thống, chat API zero-shot thường có xu hướng "nhắm mắt đoán luôn ID" hoặc ra lệnh gửi mail luôn trong tưởng tượng. Nhưng nhờ sinh ra `Thought`, Agent kịp dừng lại, tiếp thu `Observation`, và tự nhận thức: _À, cuộc họp tạo xong thì ID trả về là meeting_1, giờ mình sẽ dùng meeting_1 để đút vào hàm gửi mail_.
2.  **Reliability**: Trong các tình huống User hỏi FAQ, kiến thức tĩnh hoặc Trivia (VD: Thời khóa biểu của trường ngày nào?), Agent tốn token, xử lý cực chậm và chi phí cao gấp 5 lần do bị gò bò trong ReAct loop (tự sinh steps). Chatbot RAG truyền thống lại vạch ra đường đi ngắn và phù hợp hơn.
3.  **Observation**: Observation là chốt chặn ảo giác. Nó đập tan khuynh hướng "Chain Hallucination" - thói quen sinh ra toàn bộ quy trình ngay trong 1 response của LLM mã nguồn mở (ví dụ phi-3, qwen) chưa fine-tune Agentic. Việc đợi Observation cắt đứt sinh text sai và trói buộc LLM vào sự thật hệ thống.

---

## IV. Future Improvements (5 Points)

_Đề xuất đưa hệ thống này vào quy mô Production:_

- **Scalability**: Dữ liệu file `json` không thể xử lý truy cập song song (Concurrent access), đặc biệt khi phải đọc/ghi disk ở mỗi function call. Đưa vào DB (PostgreSQL) và tối ưu caching bằng Redis.
- **Safety**: Xây dựng Output Parser và Guardrails nghiêm ngặt. Phải bắt buộc có Sandbox ngăn LLM điền các địa chỉ giả để spam mail hệ thống (ví dụ: filter email domain hợp lệ @company.vn).
- **Performance**: Nhanh chóng đưa "Semantic Router" hoặc Agent Supervisor vào làm bộ lọc phễu. Phễu sẽ check intention của user: nếu là Q&A đơn giản -> điều hướng cho Chatbot. Chỉ điều hướng dạng task workflow đa bước vào cho ReAct Agent nhằm giảm thiểu Cost và tăng cường QoS.

---

> [!NOTE]
> Submit this report by renaming it to `GROUP_REPORT_[TEAM_NAME].md` and placing it in this folder.
