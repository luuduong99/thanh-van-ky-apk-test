# Lâm Thiển — CP331 → CP332 art work order

## Tài liệu đã CHỐT, không hỏi chốt lại

- **CANON V2** `LT_CANON_BODY_REF_2026-10-28_V2`, SHA256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711` (mắt hổ phách, tóc bạc, hoa cài, trang phục trắng-xanh, phụ kiện vàng tối giản, +17% đã tính từ trước).
- **5 biểu cảm** `LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED`, SHA256 `ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7`: shy / angry / pain / embarrassed / alluring.
- Đồ hư hại 100/70/50/30 là trạng thái riêng, không đổi khi chuyển biểu cảm.

## Vấn đề CP331 đã giải quyết, giới hạn thật

- Chứng minh **5 frame có cùng một base** (tóc/trang phục và phụ kiện ngoài vùng chỉnh mặt giữ nguyên từng pixel).
- 5 file ORA chỉnh được; 7 patch RGBA thực mỗi frame, thử chuyển trạng thái trong GIF, 9 unit tests local PASS.
- **Chưa giải quyết**: nhận diện mặt mới chưa được user duyệt và khác CANON V2, chỉ native 258×364; các mảnh ảnh còn có da/tóc; master chứa sẵn mắt/mày/miệng; lớp inpaint không được duyệt và đang hidden; không có semantic sprites/rig.

## CP332 — công việc artist thực sự, theo thứ tự

1. **Mặt chủ/nguồn có chất lượng thật:** dựng lại cùng một nhân vật theo CANON V2, không lấy tranh CP331/CP330 làm nguồn nhận dạng. Đặt các điểm neo đôi mắt, mũi, môi, đường hàm; giữ màu mống mắt hổ phách.
2. **Xóa hoàn toàn nét mặt baked khỏi base**, tự vẽ da/lông mi bị che, mí/đồng tử bên dưới, viền miệng và vùng dưới tóc thành clean underpaint. Đừng dùng OpenCV inpaint làm nền cuối.
3. **Vẽ từng bộ phận vào lớp alpha thật**: eye_L/R, upper/lower eyelids, brow_L/R, mouth, blush_L/R, tear/effect nếu cần. Các lớp này không chứa da/tóc, giữ vị trí neo nhất quán giữa năm biểu cảm.
4. **Đưa 5 sắc thái lên CÙNG master**; mắt, má, góc nhìn và miệng phải khác rõ theo bảng được duyệt. Ở biểu cảm pain, đừng làm mày/mắt như angry; shy khác embarrassed cả mắt/đầu và đỏ má; alluring chủ động nhìn nhưng không thay hình thể.
5. **Artist QA:** ghép composite ở 256px, 132px, 64px, thử blink/mouth open-close/offset và che khuất với tóc; không lộ nền, không mắt đôi, không drift khuôn mặt.
6. **Chỉ khi user duyệt sprite art cuối**, mới chuyển file vào Approved Assets, điền `sprite_paths` theo expression × wardrobe × integrity × pose và test Spine/Android APK.

## Các dấu hiệu phải FAIL

- Chỉ phóng ảnh poster 230×114 thành “4096” và tuyên bố có chi tiết gốc.
- Mặt/bông hoa/trang sức/màu mắt khác CANON V2 dù poster mới trông đẹp hơn.
- Chỉ đổi tên layer hoặc crop ảnh phẳng mà gọi là attachment độc lập.
- Dùng layer master còn in sẵn mắt/mày/miệng, hoặc underpaint có dấu vết mắt cũ.
- Khi đổi biểu cảm, tóc, tư thế, trạng thái hư hại hoặc trang phục tự thay đổi.
- Tự nhập bản CP331 hoặc demo atlas CP327 vào game.