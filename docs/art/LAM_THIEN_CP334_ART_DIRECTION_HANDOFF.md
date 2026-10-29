# Thanh Vân Ký — CP334: Review art khuôn mặt Lâm Thiển (29/10/2026)

**TRẠNG THÁI:** Đã tạo và kiểm tra **bộ 5 preview ứng viên** chất lượng hình tốt hơn CP333, cùng bảng đối chiếu và ORA workspace. **CHƯA được người dùng duyệt làm khuôn mặt chính thức, CHƯA có art sprite ngữ nghĩa tách độc lập hoặc Spine/APK được nghiệm thu.**

## Hai chuẩn phải tuân thủ

1. **CANON BODY/FACE V2** `LT_CANON_BODY_REF_2026-10-28_V2` (SHA256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711`): giữ khuôn mặt, mắt hổ phách, tóc bạc, hoa và trang phục trắng–xanh–vàng, vàng vừa phải. **+17% đã có trong CANON V2**, không cộng thêm.
2. **5 biểu cảm chính thức** `LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED` (SHA256 `ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7`): `shy / angry / pain / embarrassed / alluring`. Dùng làm chuẩn **cảm xúc**, không thay CANON hình thể/màu mắt. `wardrobe`, `integrity` với các mức 100/70/50/30, `pose` và `action` vẫn độc lập.

## Có gì mới

- Một bảng concept mới CP334 **1536×1024 RGB phẳng**, SHA256 `1286237fd958990ffaf69f3b57c6997b00fbcd756d93887c351bb6ee84dda9ee`. Bảng mới có chữ *Production Ready v2.1*, *PNG RGBA*, *Spine-ready* và *atlas 2048²* do hệ thống vẽ vào ảnh; **những chữ đó không xác nhận file thực sự có tính năng này**.
- Từ **chính PNG mới**, tạo **5 chân dung ứng viên riêng** ở kích thước gốc xấp xỉ 252–256×364 px, không phóng làm HD giả; giữ thứ tự đúng 5 cảm xúc. Cùng các bản crop hướng cảm xúc APPROVED để họa sĩ kiểm.
- Tạo ba ảnh phục vụ QA:
  - `preview/CP334_FIVE_EXPRESSIONS_CANDIDATE_PREVIEW.png`: 5 chân dung riêng, cắt phần chữ “Production Ready”.
  - `preview/CP334_CANON_V2_IDENTITY_DIFFERENCES.png`: so hình mặt nguồn CANON V2 native 230×114 với ứng viên và checklist sai khác.
  - `preview/CP334_APPROVED_EMOTION_VS_NEW_CANDIDATE.png`: mỗi cột đối chiếu cảm xúc đã duyệt với art mới chưa duyệt.
  - `preview/CP334_DIALOGUE_THUMBNAIL_QA.png`: xem trực tiếp tại 256/132/64px.
- Tạo `CP334_VISUAL_REVIEW_WORKSPACE_NOT_RIG.ora`: **7 lớp** gồm review background, 5 layer **chân dung phẳng** và một lớp chú thích, dùng để mở trong Krita. **Đây không phải 7 semantic facial layers**, không có eye/brow/mouth dưới dạng bộ phận độc lập/clean underpaint.
- Gói Library Development có `CP334_ART_REVIEW_MANIFEST.json`, ảnh gốc V2 và emotion guide SHA đã duyệt, PNG candidate, preview, review ORA và công cụ Python.

## Kết quả QA

- **8/8 local package tests PASS**; 5/5 candidate crops khớp từng pixel với nguồn mới, CANON và ảnh biểu cảm đúng SHA, ORA reference 7 lớp hợp lệ, ZIP CRC PASS, không có art/rig/APK flag được mở.
- ZIP cuối `TVK_LamThien_CP334_Art_Direction_Review_NOT_GAME_READY.zip`, SHA256 `8602b28f6df43952b6f70adcdffd4c0945bd0463ba6144c449a0a5b192a5dc8b` (23 tệp). Library `/Thanh Van Ky/Development/CP334_Art_Direction_Review/`.
- Bộ `tests/art/test_cp334_review_package.py` và GitHub workflow `cp334-concept-art-review.yml` kiểm **metadata** trong repo; chúng không có ảnh/ORA nhị phân từ Library để nghiệm thu mỹ thuật.
- **Điểm cải thiện thị giác:** mắt hổ phách ấm hơn và chất tóc chi tiết hơn CP333, năm nét khác biệt khá rõ ở cỡ portrait.
- **Lỗi còn lại:** model mới có hoa/vàng/trang sức nhiều hơn V2, đường viền áo/neckline khác, độ mềm của mặt so V2 chưa xác nhận; năm đầu nghiêng và tay khác nhau, **không cùng face master có thể rig**. Dù preview đẹp, **không dùng làm art model chính thức**.

## Điều kiện bắt buộc cho CP335 — tránh lặp nhiều vòng crop/atlas

1. **Một face master chất lượng mỹ thuật cao theo V2** (độ phân giải native thực sự, không upscale ảnh canon bé) và một biến thể **Front / 3⁄4** nhất quán.
2. Họa sĩ/drawing thực hiện **layer clean face underpaint, hair_front/back, 2 eyes/iris/lashes/eyelids/brows, mouth, blush** độc lập, không cắt da/tóc lẫn vào patch. Dùng CP333 SVG/ORA làm scaffold kỹ thuật nếu hữu ích, nhưng phải **redraw hoàn toàn phần nét chưa giống V2**.
3. Chứng minh năm biểu cảm thuộc **cùng một nhân dạng và head proportion**, chỉ thay bộ attachment; test blink/miệng/draw-order/occlusion ở 256,132,64px. Đối chiếu iris hổ phách với CANON V2, không dùng mắt xanh của sheet cảm xúc như màu mới.
4. Preview một hoặc hai góc `Front` và `3/4` có khuôn mặt giống **CANON V2** để nghiệm thu **art mới**. **Không hỏi chốt lại V2 hay 5 sắc thái**.
5. Sau khi qua art visual approval + binary alpha QA mới đăng ký sprite trong Android và thực hiện rig/Spine, chạy APK test. P0-02/P0-03/P1-03/P2 còn mở.

**Mục tiêu tiếp theo là asset art được vẽ lại thực sự, không lập thêm checkpoint kỹ thuật chỉ gồm flat crops từ poster.**
