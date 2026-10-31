# CP329 — Lâm Thiển | Face Master Intake / hướng dẫn vẽ art thật (2026-10-29)

**KẾT QUẢ THỰC TẾ:** Đã tạo nguồn vẽ/tách lớp ORA có thể chỉnh sửa, gắn nguồn CANON V2 và 5 biểu cảm đã duyệt, kiểm thử file thật. **CHƯA CÓ KHUÔN MẶT ĐƯỢC VẼ LẠI Ở ĐỘ PHÂN GIẢI SẢN XUẤT; CHƯA CÓ GAME SPRITE / SPINE / APK.** Đây là checkpoint kỹ thuật/bàn giao cho artist, không được đánh dấu hoàn thành P0-02/P0-03/P1-03.

## Nguồn bất biến, thứ tự ưu tiên

1. **CANON BODY/FACE V2 chính thức** `LT_CANON_BODY_REF_2026-10-28_V2`: PNG 1672×941, SHA256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711`; [ảnh gốc Google Drive](https://drive.google.com/file/d/1mEsyn2wMo-MVQqhtbmdUiFfO8AaYhzUR/view?usp=drivesdk). Mắt **hổ phách**, tóc bạc, hoa/phụ kiện/trang phục theo V2. Tỷ lệ **+17% đã tích hợp vào V2**; không cộng lại.
2. **5 biểu cảm đã duyệt** `LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED`: `shy/angry/pain/embarrassed/alluring`, SHA256 `ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7`; chỉ quyết định sắc thái nét mặt, **không thay danh tính/màu mắt/khuôn mặt CANON**.
3. Bốn mức hư hại trang phục `100/70/50/30` và việc giữ state độc lập với `expression/pose/wardrobe` không thay đổi.
4. Các poster CP328/CP329 tự tạo, dù có chữ “production-ready”, **không có bằng chứng là file nhiều lớp**, một số bị sai mắt xanh; KHÔNG sử dụng làm model chuẩn hoặc sprite.

## Artifact bàn giao thật

**ZIP** `TVK_LamThien_CP329_Face_Master_Intake_NOT_GAME_READY.zip`, SHA256 **`e6b8e952b2a7028ac2314cf95d5fb0c94d008b9c0baf6c2064dc2b7130c91b9d`**; ZIP CRC PASS; lưu ChatGPT Library **Development** tại `/Thanh Van Ky/Development/CP329_Face_Master_Intake/`.

Trong ZIP:
- `reference/CANON_V2_FACE_NATIVE_230x114.png`: crop đúng ảnh V2, không xóa/chỉnh thiết kế.
- `preview/CP329_ART_SOURCE_LOCK_AND_REVIEW.png`: board bên trái là khuôn mặt CANON V2; bên phải là 5 sắc thái biểu cảm đã duyệt, **không được dùng bên phải để thay body/face chuẩn**.
- `ora/CP329_FACE_MASTER_EMPTY.ora`: canvas 2048×2048, **11 layer mỹ thuật trống**, một guide CANON V2 ẩn trong ORA.
- `ora/CP329_{shy,angry,pain,embarrassed,alluring}_EXPRESSION_EMPTY.ora`: **5 file ORA, mỗi file 7 layer trống** dành cho mắt trái/phải, lông mày, miệng, má; không phải ảnh chụp vẽ lại.
- `manifest.json`: nguồn SHA256, layer names, bbox và tọa độ mapping.
- Mã tạo, validator, bài kiểm thử Python và hướng dẫn Krita để tiếp tục vẽ.

**Cảnh báo độ phân giải:** crop V2 **native 230×114**. Guide đưa lên canvas 2048×2048 bằng nearest-neighbor ×8 (kích thước guide 1840×912, origin [104,568]); đây là **phóng ảnh tham chiếu**, không tăng chi tiết nguồn hay biến thành art HD. Các vùng mắt tham khảo, **không phải iris-only**:
- eye_image_left native `[69,57,105,88]` → canvas `[656,1024,944,1272]`
- eye_image_right native `[130,30,176,61]` → canvas `[1144,808,1512,1056]`

## Kiểm thử (bằng file thật, không chỉ tên layer)

- SHA canonical/approved emotion: **2/2 đúng**; native crop nguồn đúng.
- 6 ORA hợp lệ (OpenRaster MIME, stack.xml, PNG RGBA 2048², guide ẩn, alpha): **6/6 PASS cấu trúc**.
- **0/46 lớp mỹ thuật đã vẽ** (11 master + 5×7 expression), QA không tự đánh dấu DONE.
- `python3 -m unittest discover -s tests -p 'test_cp329_art_intake.py' -v` chạy từ ZIP đã giải nén: **8/8 PASS local**.
- `python3 tools/validate_cp329_intake.py . --strict`: **FAIL cố ý** (đúng) vì chưa có art/underpaint do artist duyệt và chưa có xác nhận sprite thành phẩm.
- **GitHub Actions CP329 metadata/synthetic ORA gate:** run `40812464457` **SUCCESS**. Không có file ORA Library trên CI; không suy ra art/Spine/APK PASS.
- CP328 color-lock CI đã được sửa lỗi thiếu trường JSON `registered_android_asset_paths` và xác minh lần chạy lại **SUCCESS** (run `40810511227`).

## Những trở ngại còn nguyên

1. Face source gốc trên poster vẫn rất nhỏ; không đủ để chuyển thẳng thành layer production bằng crop/upscale.
2. CP326/327 vector và atlas là đồ thử kỹ thuật nhưng **chưa khớp chất lượng anime**, không có clean underpaint thực. Không đăng ký vào `sprite_paths`.
3. CP329 là **art intake kit**, không phải mẫu art đã được duyệt. Toàn bộ 46 lớp còn trống; dùng ORA template trong Krita để vẽ lại bản thực chất lượng sản xuất.
4. Android có code chọn 5 biểu cảm từ CP324, nhưng không có bộ face sprite phù hợp và APK mới chưa được nghiệm thu.

## CP330 — công việc tiếp tục

1. Hoàn thiện **face master mới vẽ thật** ở chất lượng sản xuất: mặt, tóc, vùng da/underpaint, eye sockets, phụ kiện theo **CANON V2**, mắt hổ phách đúng.
2. Đưa **7 nhóm attachment alpha độc lập × 5 biểu cảm** vào các ORA, dùng approved preview làm hướng cảm xúc; không crop poster thành art.
3. Test CP328 eye color guard bằng ROI mống mắt thật do artist định vị, QA alpha/occlusion/draw order, thử biến dạng mí/môi; kiểm 256/132/64px và góc 3/4.
4. Chụp preview asset đã ghép và gửi người dùng **duyệt kỹ thuật/mỹ thuật thành phẩm** (không hỏi duyệt lại model hay 5 biểu cảm). Khi đạt mới cập nhật `sprite_paths`, rig Spine và build APK.
5. Nếu tiếp tục không tìm được source layered/HD, nêu rõ cần redraw. Không được giả một canvas 2048 hay poster đẹp là sprite/Spine hoàn thành.

**Không thay đổi** CANON V2, 5 biểu cảm, tỷ lệ +17% hay 100/70/50/30.
