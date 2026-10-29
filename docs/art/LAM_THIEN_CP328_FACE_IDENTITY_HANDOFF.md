# CP328 — Lâm Thiển: khóa màu mắt & nhận diện face CANON V2 (2026-10-29)

**TRẠNG THÁI:** QA nguồn và bảo vệ màu mắt **ĐÃ LÀM**; **face master độ phân giải sản xuất, tách layer mỹ thuật, Spine và APK CHƯA HOÀN THÀNH**.

## Nguồn chính thức (không thay đổi)

- **CANON V2:** `LT_CANON_BODY_REF_2026-10-28_V2`, 1672×941 PNG poster, SHA-256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711`. [Drive — ảnh chuẩn](https://drive.google.com/file/d/1mEsyn2wMo-MVQqhtbmdUiFfO8AaYhzUR/view?usp=drivesdk).
- **5 biểu cảm đã duyệt:** `LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED`, SHA-256 `ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7`, `shy / angry / pain / embarrassed / alluring`. [Hồ sơ biểu cảm](LAM_THIEN_FIVE_EXPRESSIONS_APPROVED_2026_10_29.md).
- **Quy tắc quyết định:** CANON V2 quyết định **cấu trúc mặt, mắt hổ phách/vàng ấm, tóc bạc, hoa cài, phụ kiện, trang phục và tỷ lệ +17% đã tích hợp**. Sheet 5 biểu cảm quyết định **cách thể hiện cảm xúc**. Không để mắt xanh hoặc trang sức mới từ preview AI thay thế bản V2.
- Mức độ hư hại trang phục `100/70/50/30` và các trạng thái outfit/pose giữ độc lập, không sửa.

## Kiểm tra bằng ảnh gốc thật

1. Đọc đúng file canon có checksum. Crop mặt `[1160,0,1390,114]`: **230×114 pixel native**. Phóng to để xem không làm tăng độ chi tiết nguyên bản.
2. Mở hai vùng mắt tương đối trên crop: `eye_image_left=[69,57,105,88]`, `eye_image_right=[130,30,176,61]`.
3. Lấy mẫu HSV OpenCV, ngưỡng amber hue `5..27`, blue hue `80..135` kèm ngưỡng saturation/brightness và kiểm từng ROI. Trên nguồn V2:
   - Eye image left: **124 amber-matching pixels, 0 blue-matching pixels**.
   - Eye image right: **105 amber-matching pixels, 0 blue-matching pixels**.
4. **Rất quan trọng:** ROI nhỏ vẫn chứa một phần da/mi và ảnh nén. Đây là phép kiểm tra cảnh báo **sự trôi màu xanh rõ rệt**, **không** thay phép duyệt mắt/mặt bằng người và không cung cấp một màu RGB duy nhất chính xác cho mống mắt.
5. Mã `tools/cp328/cp328_face_color_gate.py` kiểm checksum ảnh nguồn; có chế độ `--candidate --iris-rois` cho **ảnh face master mới** nếu họa sĩ tự khoanh đúng hai mống mắt. Thiếu ROI, ảnh nguồn sai SHA hoặc ảnh cố tình đổi thành mắt xanh sẽ bị chặn; ảnh mắt nhắm không phù hợp kiểm kiểu này.
6. **9/9 unit test local PASS**, gồm nguồn đúng SHA, màu hổ phách nguồn, giả lập hai mắt xanh, ROI thiếu, ảnh phóng to không được coi native, và hai test candidate có/không có mắt xanh.
7. Bản **CP328 infographic mới** được tạo trong phiên có màu mắt xanh và mô tả “production ready” ngay trên tranh. **KHÔNG DUYỆT**, không sử dụng làm face master hay giả là đã có 35 sprite PNG/Spine.
8. Tạo bảng QA `CP328_CANON_V2_FACE_IDENTITY_QA.png` so canon và 5 biểu cảm đã duyệt, kèm tiêu chí nghiệm thu. Đây là ảnh QA/tài liệu, không phải sprite.

## Artifact & backup

- `TVK_LamThien_CP328_Canon_Face_Color_Lock_Package.zip` — SHA256 `3cbbe39054a02ca04b25e4ef40398bb9b8ecbd5a74923c9632c71206e228078f`, ZIP CRC PASS; gồm chương trình, test, manifest, ảnh QA và crop nguồn đã bảo vệ.
- ChatGPT Library: `/Thanh Van Ky/Development/CP328_Canon_Face_Color_Lock/`. Không đưa các bản art chưa duyệt vào Approved References.
- [Hợp đồng dữ liệu CP328](LAM_THIEN_CP328_FACE_MASTER_GATE.json), [test CI](../../tests/art/test_cp328_color_contract.py), [workflow](../../.github/workflows/cp328-face-color-lock.yml).
- GitHub CI **chưa có kết quả tại thời điểm viết**; cần kiểm tra workflow trực tiếp sau commit. CI metadata/synthetic không đánh giá được các ORA/SPINE nhị phân.

## Không được tự đánh dấu DONE

| Gate | Trạng thái |
|---|---|
| CANON V2 body/face và 5 sắc thái biểu cảm | **Approved** từ trước |
| CP328 màu mắt/canonical crop/negative test | **Technical QA passed** |
| Face art mới độ phân giải sản xuất | **Missing** |
| Artist-approved clean underpaint | **Missing** |
| 5 nét mặt vẽ trên cùng một face master, lớp alpha thật | **Missing** |
| Spine skeleton/mesh/draw-order/animation | **Missing** |
| Android asset registration và APK nghiệm thu | **Missing** |

## CP329 — điểm tiếp tục

1. Khôi phục file layered source V2 đúng canon (nếu tìm được) hoặc **dựng lại art native high-resolution**, không upscale poster để tự nhận HD.
2. Giữ **mắt hổ phách** ở mọi biểu cảm mở mắt; đối chiếu với ảnh nguồn V2. Khóa mặt, cấu trúc mắt/mũi/miệng, tóc, hoa và phụ kiện.
3. Vẽ **face master + underpaint thật** và attachment PNG alpha mắt trái/phải, lông mày, mí, môi, má. Bản alpha phải không dính da/tóc cũ, có vùng ẩn đủ để rig.
4. Ghép 5 biểu cảm đã duyệt với cùng identity, QA ở **132px/64px**, góc Front/3/4, không reset trạng thái outfit/damage/pose.
5. Duyệt bản **sprite art thành phẩm** (không cần duyệt lại canon hay định nghĩa cảm xúc); rồi mới import Spine, kiểm draw order/clipping/animation, kết nối Android và build APK thử.

**Không sử dụng CP326/CP327 atlas demo làm game art chỉ vì unit test thành công.**
