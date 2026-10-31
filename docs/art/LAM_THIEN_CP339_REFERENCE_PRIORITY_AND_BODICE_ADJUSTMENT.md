# CP339 — Lâm Thiển: xác nhận lại thứ tự nguồn & đề xuất chỉnh thân áo (2026-10-29)

## Quyết định hiện hành của người dùng

Người dùng cung cấp lại **ba ảnh trực tiếp** và chỉ định:
- **Ảnh 2 = mẫu chính thức định hướng model/body/trang phục/góc nhìn/tư thế/damage** (user uploaded PNG 1536×1024, SHA256 `3cd8977383ba2fd2563a8f3c07aa85e5a7af4572d37c0fdb80d0e52cba0a3501`).
- **Ảnh 3 = mẫu chính thức định hướng năm biểu cảm** `shy, angry, pain, embarrassed, alluring` (user uploaded PNG 1536×1024, SHA256 `186ec1fef284d702229af9e10c6d27a7f3e27b664b22f204863a3f20469d6a50`). Nội dung chữ “Production Ready”, “layer”, “Spine”, “atlas” bên trong ảnh **không chứng minh file chứa layer hay Spine thực tế**.
- **Ảnh 1 = chỉ là tham chiếu để chỉnh phần thân áo/ngực**: kiểu dáng bodice/cúp áo/nếp vải ở phần ngực và tỷ lệ vòng một của Ảnh 2/3 được mong muốn gần bằng Ảnh 1 (user uploaded PNG 1400×1540, SHA256 `5bd69fff139c4908d122786655babbf08301e345388f1fe6fa6d6b42e21e3d99`). **Không áp dụng toàn bộ model / góc / màu / quần áo / biểu cảm từ ảnh 1**.
- **Phạm vi thay đổi dự kiến:** cân chỉnh silhouette phần ngực và cấu trúc thân áo của ảnh 2, ảnh 3 theo ảnh 1; giữ đủ trang phục, không tạo khỏa thân. Đảm bảo nhất quán về dáng áo khi đổi góc nhìn/tư thế, qua các mức trạng thái 100/70/50/30. Nếu một chi tiết vải/cúp áo bị che khi đổi góc thì phải vẽ đúng phối cảnh, không nhân cùng một ảnh crop.
- **Các phần phải giữ:** tạo hình nhận diện, vóc dáng tổng thể ngoài phạm vi tinh chỉnh được nêu, tỷ lệ +17% đã duyệt, tóc/phụ kiện/kiểu dáng chính và màu sắc trang phục của ảnh 2; nội dung cảm xúc từ ảnh 3; bốn mức hư hại nguyên vẹn và chi tiết phụ có thể lược nhẹ theo CP338 khi thật cần thiết.
- **Lưu ý về mâu thuẫn nguồn:** nếu màu mắt/ornament giữa ảnh 2 và 3 khác nhau, màu sắc và nhận diện lấy **model chính ảnh 2**; ảnh 3 chỉ quyết định sắc thái biểu cảm. Không lẫn thay đổi ngầm.
- **Không xem là chốt ảnh chỉnh sửa:** đây là hướng thay đổi người dùng **đề xuất và yêu cầu xem xét**. Chỉ khi bản **preview sau chỉnh** được người dùng chấp thuận mới thay đổi “approved revised art”; các ảnh chuẩn gốc không bị ghi đè. Không tự nhận đã có lớp RGBA, ORA, Spine, APK.

## Bài kiểm QA trước nghiệm thu

1. Hiển thị **Ảnh 1 tham chiếu vùng bodice**, **Ảnh 2 toàn thân** và **Ảnh 3 cận biểu cảm**, cạnh **preview chỉnh**, với cùng vị trí so sánh; tránh chỉ so ảnh mặt.
2. Kiểm tra dáng cơ thể tổng thể không đổi, chỉ điều chỉnh mức độ đầy đặn/đường thân áo trong phạm vi người dùng đã nói; giữ kiểu áo/cổ áo/phối trắng–xanh–vàng và đồ trang sức đặc trưng từ ảnh 2.
3. Đặc biệt không phát sinh thiết kế bodice hoàn toàn mới, tăng/giảm không chủ đích, thay chất liệu/vùng che phủ mạnh hoặc làm sai nhận diện.
4. QA góc Front/3⁄4/Back (nếu có thể thấy vùng thân áo), 5 biểu cảm, damage 100/70/50/30, ảnh thoại thu nhỏ 256/132/64px.
5. Phân loại `PASS`, `PASS_WITH_MINOR_NOTES`, `REVISE`. **Không dùng kết quả gen ảnh để tự phê duyệt**. Sau user preview acceptance mới làm source phân lớp thật và rig.
6. Android `production_release` tiếp tục `blocked_pending_art` và `sprite_paths={}` cho tới khi có source asset đủ QA.

## Tình trạng
Đã ghi lại đúng thứ tự ưu tiên và SHA256 của 3 file do người dùng cung cấp. **Chưa tạo bản art sửa được nghiệm thu; chưa cập nhật sprite/Spine/APK.**
