# Thanh Vân Ký — CP331 | Đồng bộ năm biểu cảm bằng cùng một master (2026-10-29)

**TRẠNG THÁI: THỬ NGHIỆM KỸ THUẬT CÓ FILE THẬT / ART CHƯA DUYỆT / CHƯA CÓ SPINE, APK.**

## 1. Hai nguồn thiết kế đã chốt (tuyệt đối không thay đổi)

- **CANON BODY/FACE V2 chính thức:** `LT_CANON_BODY_REF_2026-10-28_V2`, SHA256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711`. Tóc bạc dài, mắt hổ phách, phụ kiện/hoa tóc và trang phục trắng–xanh–vàng theo V2; tỷ lệ +17% **đã** nằm trong mẫu.
- **Năm biểu cảm đã duyệt:** `LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED`, SHA256 `ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7`: `shy`, `angry`, `pain`, `embarrassed`, `alluring`. Không hỏi lại chốt biểu cảm.
- Bốn mức trang phục `100/70/50/30`, `wardrobe`, `pose`, `action` vẫn độc lập với `expression`.
- **BẢN ẢNH MỚI CP331 CHƯA ĐƯỢC DUYỆT:** SHA256 `a923f2125fbac40bd3a5975cc50d22ff12926d4f69b6d461d76f6be647c8a729`; poster có chữ *Production Ready*, nhưng đó chỉ là chữ trong ảnh do AI tạo, **không chứng minh** sprite/Spine/gỡ alpha đúng hoặc được người dùng xác nhận.

## 2. Vấn đề kỹ thuật đã xử lý thực tế

CP330 có năm face nền khác nhau, nên tóc/phụ kiện/đường hàm có thể thay đổi khi chọn emotion. CP331 **dùng chung một bản nền phẳng cố định**, chỉ biến đổi vùng ảnh mày/mắt/miệng/má:

- Một master flat RGB thực (cắt ở kích thước **native 258×364 px** từ poster mới, không tự nhận là high-res);
- Năm file `.ora` OpenRaster chỉnh sửa được, **7 alpha patch chứa pixel mỗi file, tổng 35**;
- Mỗi ORA giữ *chính xác cùng một layer nền visible* và kèm một layer underpaint OpenCV ẩn, một guide unapproved ẩn;
- **Tóc, phụ kiện, trang phục và khu vực ngoài các ROI mặt bất biến pixel** giữa năm ảnh composite;
- Đã tạo preview năm biểu cảm ở kích thước gốc, thu nhỏ 132px và 64px, ảnh đối chiếu với crop CANON V2 và GIF chỉ mô phỏng đổi hình (không phải animation);
- **Test local trên file ORA thật: 9/9 PASS**, tính ZIP CRC, stack/PNG, compositor khớp preview, 35 patch không rỗng, cùng master SHA, hình không thay ngoài vùng mặt.
- **`audit_cp331.py --strict` trả FAIL đúng thiết kế** do art chưa đạt chất lượng/sự phê duyệt.

## 3. Bất cập mỹ thuật còn tồn tại — không được phép bỏ qua

1. Master dùng **ảnh phẳng sinh mới**, chưa được xác nhận giống tạo hình/cấu trúc mặt CANON V2.
2. Kích thước 258×364 là native của crop poster; **không phải artwork 2048/4096 native**. Poster V2 hiện chỉ cung cấp khuôn mặt 230×114 px.
3. Layer `SHARED_FLAT_MASTER_WITH_BAKED_FACE_FEATURES_NOT_RIGGABLE` vẫn in sẵn mắt/mày/miệng. Các patch là crop ảnh bao gồm da/tóc với feather; **không phải bộ phận mặt semantic tách sạch**. Khi biến dạng mạnh có nguy cơ lộ mắt cũ/đường nối.
4. Layer `INPAINT_UNDERPAINT_DRAFT_HIDDEN_NOT_APPROVED` là kết quả thuật toán, **không được họa sĩ hoàn thiện**, và được giữ hidden.
5. Một số transition có seam/blur ở mắt/mày. Bảng preview này **không phải đề xuất thay CANON V2** và chưa đạt nghiệm thu art.
6. Chưa có file Spine skeleton, mesh, 3/4 view đúng, state-combinations sprite, Android APK được build/test. `sprite_paths` trong app vẫn không đăng ký.

## 4. Files, checksum, kiểm tra

- **ZIP CP331:** `TVK_LamThien_CP331_Shared_Face_Technical_Trial_NOT_APPROVED.zip`, SHA256 `e48174f1b0831942cc03f0ff5a0f98d51ae83ee01540135f24b6ffa9b2232578` (62 tệp, ZIP CRC PASS).
- Đã sao lưu nguyên gói tại ChatGPT Library: `/Thanh Van Ky/Development/CP331_Shared_Face_Technical_Trial/` (Development, không phải Approved References).
- [Manifest CP331](LAM_THIEN_CP331_SHARED_FACE_TRIAL_MANIFEST.json), [Work order cho artist](LAM_THIEN_CP331_ARTIST_WORK_ORDER.md).
- Công cụ: `tools/cp331/create_cp331.py`, `tools/cp331/audit_cp331.py`, `tools/cp331/test_cp331_local.py` (real ORA).
- **GitHub CI**: test trên metadata không có ORA nhị phân trong repo; phải tách rõ CI với local QA.

## 5. Định hướng tiếp theo CP332

**Ưu tiên sản xuất đúng phần còn thiếu, không lặp các gói tách crop kỹ thuật:**

1. **Vẽ lại face master high-res native đúng CANON V2** với chân dung nhận diện, mắt hổ phách, tóc/hoa/phụ kiện; không lấy portrait CP331 làm canon.
2. **Underpaint sạch không còn nét mắt/miệng baked** và có vùng vật thể bị che để animate mắt, mí, tóc.
3. Tạo attachment mắt/mày/miệng/má thật (không chứa da/tóc nền) đủ năm biểu cảm dùng chung face master; xuất ORA/PNG alpha; dựng cả góc Front/3⁄4 cần thiết.
4. Artist QA bằng ảnh composite kích thước 256/132/64px, thử move/blink/mouth/draw-order, kiểm không alpha-hole hoặc đổi nhận dạng khuôn mặt. Gửi **preview asset cuối** để người dùng nghiệm thu riêng; không hỏi duyệt lại hướng thiết kế/5 cảm xúc.
5. Chỉ sau art QA mới điền asset paths, rig Spine, build và test APK.

**Không đánh dấu P0-02, P0-03, P1-03 hoặc P2 đã hoàn thành chỉ vì CP331 có 35 mảnh alpha và 9 bài test PASS.**


## Xác minh GitHub Actions thực tế (2026-10-29)

- Workflow `CP331 shared-face identity technical contract`: **SUCCESS**, run `40817371764`, job `shared-face-metadata` ID `123261502899` trên commit `0bab1c9f8dd8d78af6843de111c7b8f7db17097d`.
- GitHub CI chỉ kiểm **metadata/điều kiện không được đưa ảnh chưa duyệt vào production**. Khả năng mở/ghép 5 ORA nhị phân, so CRC và pixel ngoài vùng mặt được kiểm **local 9/9 PASS** trên gói Library; GitHub runner không có ORA này.
- Kết quả **không phải** nghiệm thu art, Spine, Android Gradle hay APK.
