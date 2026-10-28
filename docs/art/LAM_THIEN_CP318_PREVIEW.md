# Lâm Thiển — CP318: xem trước thiết kế Back mới (CHƯA DUYỆT)

**Ngày:** 2026-10-28  
**Trạng thái:** ĐÃ TẠO ẢNH CONCEPT MỚI — CHƯA ĐƯỢC NGƯỜI DÙNG DUYỆT, CHƯA CÓ RIG/APK.

## 1. Quy tắc áp dụng
- Theo [PROJECT_SPEC.md](../PROJECT_SPEC.md) mục 9: luôn dùng thiết kế **mới nhất đã được người dùng chốt** làm chuẩn triển khai. Không dùng lại proxy cũ cho preview chính.
- Lâm Thiển: giữ tóc bạc, mắt xanh, trang sức hoa, tông trắng–xanh–vàng. Front và tư thế tương tác đã duyệt giữ nguyên.
- Back: **hai bên hông khoét cân đối, đường nét phía sau nổi khối/tôn dáng rõ** theo bản được chốt ngày 2026-10-27.
- Giữ mốc thay đổi tỷ lệ thân trên +17% đã chốt và tổng thể cao/thanh hơn; không kéo giãn chân/hông tùy tiện. Đo tỷ lệ phải dựa trên mẫu nguồn cùng thước đo, **không tự tuyên bố concept này đạt +17% chính xác theo pixel**.

## 2. Nội dung CP318 đã thực hiện
- Tạo ảnh concept mới tập trung **góc nhìn từ phía sau**, có trang phục khoét hông và dáng phía sau rõ; sử dụng sheet Lâm Thiển để nhận diện, không coi ảnh Back kỹ thuật CP317 là bản triển khai.
- File bản xem trước: `TVK_CP318_LamThien_Back_Concept_Preview.png`; bản lưu lại trong Library: `/Thanh Van Ky/CP318_LamThien_Back_NEW_DESIGN_REVIEW_NOT_APPROVED.png`.
- Gói bàn giao trong phiên: `TVK_CP318_LamThien_NEW_DESIGN_PREVIEW_Handoff.zip`; gồm ảnh và README nhận diện tình trạng.
- **Lưu ý:** ảnh infographic gốc do AI tạo chứa các nhãn QA/10 test/check dấu tích chỉ mang tính minh họa. **Không có** kiểm thử ORA, alpha, bone hoặc physics thực tế được chạy trên ảnh mới. Ảnh bàn giao chỉ giữ phần hình nhân vật để tránh hiểu nhầm.

## 3. Giới hạn và bước cần duyệt
- File CP251 Back người dùng đã duyệt trước đây chưa truy xuất được trong các nguồn hiện tại. CP318 là bản thiết kế tái dựng theo các yêu cầu đã chốt, **không phải chính xác bản CP251 nguồn**.
- Mẫu mới **CHƯA DUYỆT**; không tự nâng trạng thái canon chỉ vì đã tạo preview.
- Chưa có ORA/Spine sprite phân lớp từ hình mới; chưa nghiệm thu seam tóc/gáy, khoét hông/tay áo, không có bản APK cập nhật.
- Sau khi người dùng duyệt preview: triển khai bộ sprite Front/Back/3/4 và tư thế tương tác nhất quán, tách lớp, kiểm tra chuyển động ±5px cùng tiêu chí QA cũ, rồi mới rig/physics/tích hợp APK.

**Điểm tiếp tục:** CP319 — nhận feedback/duyệt CP318; chỉnh đúng ảnh mới, KHÔNG quay về CP317 proxy hoặc Back PNG cũ.
