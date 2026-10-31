# CP325 — Lâm Thiển: thử nghiệm OpenRaster vùng mặt cho 5 biểu cảm (2026-10-29)

**KẾT QUẢ:** 5 file ORA có thể chỉnh sửa, gồm tổng 35 vùng alpha chứa pixel thật. **ĐÂY CHỈ LÀ PROXY REFERENCE TỪ POSTER — KHÔNG PHẢI FACE SPRITE HOÀN CHỈNH VÀ KHÔNG ĐỦ ĐỂ RIG SPINE/APK.** Không đánh dấu P0-02/P0-03 hoặc P1-03 đã xong.

## Nguồn thiết kế bất biến

1. **CANON BODY V2:** `LT_CANON_BODY_REF_2026-10-28_V2`, SHA256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711`. Nguồn [Google Drive](https://drive.google.com/file/d/1mEsyn2wMo-MVQqhtbmdUiFfO8AaYhzUR/view?usp=drivesdk); +17% đã nằm trong V2, tuyệt đối không áp thêm.
2. **5 BIỂU CẢM ĐÃ DUYỆT:** `LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED`, `shy/angry/pain/embarrassed/alluring`, preview SHA256 `ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7`. [Nguồn chính thức](LAM_THIEN_FIVE_EXPRESSIONS_APPROVED_2026_10_29.md).
3. Hai nguồn không thay thế nhau: poster biểu cảm quyết định *sắc thái*; body V2 quyết định *nhận diện và thiết kế cơ thể/mặt/trang phục*. Các ảnh bên dưới không được thêm vào thư mục production assets hoặc khai báo `sprite_paths`.

## File art thử nghiệm có thật

- `TVK_LamThien_CP325_Face_Region_Prototypes_NOT_SPINE_READY.zip` SHA256 **`8cc9bac61fb843c84444cae57668318f9d5c40a3538d7e8262ae585493aacf3e`**.
- Sao lưu ChatGPT Library: `/Thanh Van Ky/Development/CP325_Face_Region_Prototypes/TVK_LamThien_CP325_Face_Region_Prototypes_NOT_SPINE_READY.zip` (**Development**, không phải Approved Production Art).
- 5 ORA theo năm biểu cảm; mỗi ORA có **7 layer pixel patch RGBA**: `brow_image_left/right`, `eye_image_left/right`, `mouth`, `blush_image_left/right`, cùng **1 layer ảnh gốc được ẩn**. Các layer có điểm ảnh thật, alpha bị giới hạn trong vùng khoanh nhưng **bao gồm da/tóc từ bản phẳng**, không phải phần mắt/miệng được vẽ tách ra độc lập.
- Kích thước mỗi ORA gốc **285–303 × 385 px** (không upscale giả thành 2048×3072). Không dùng chúng làm texture atlas hoặc spine attachments trong game.
- Ảnh `CP325_FACIAL_REGION_ANNOTATIONS_REFERENCE_ONLY.png` — checksum `29ae1c26044491606c0148f0e84de3f01bbc40900c57e0c6baec8f58d8ef38f1` — hiển thị chính xác 7 vùng/biểu cảm.
- Ảnh `CP325_DIALOGUE_THUMBNAIL_QA_REFERENCE_ONLY.png` — checksum `33eb19bd5f29b0b507da8132fbeb0419fdbd014f1164025d310169202b6ded2d` — dùng đối chiếu độ nhận diện ở 132/64px, không thay QA của sprite thật.

## QA và kiểm thử

- Kiểm tra tất cả 5 ORA: ORA XML/ZIP CRC/mimetype/canvas, 7 patch nonempty/alpha thật + guide hidden, checksum dữ liệu gốc, RGB pixel dưới alpha đồng nhất với nguồn, không tràn bbox; **5/5 unit tests local PASS**.
- `python3 tools/cp325/validate_cp325_face_proxies.py <extracted_archive>/CP325` → PASS ở mức *reference proxy*.
- `python3 tools/cp325/validate_cp325_face_proxies.py <extracted_archive>/CP325 --strict` → **FAIL cố ý và đúng**, do chưa phải asset được vẽ theo V2.
- Script: `tools/cp325/validate_cp325_face_proxies.py`, test local cùng thư mục ZIP. `docs/art/LAM_THIEN_CP325_FACE_REGION_PROXY_MANIFEST.json` ghi tọa độ, SHA256, trạng thái cho từng ảnh. `tests/art/test_cp325_face_proxy_contract.py` + workflow `cp325-face-proxy-contract.yml` bảo vệ metadata trong GitHub (**không chứng nhận tệp ORA thực**).
- **GitHub Actions / build Android:** chưa có bằng chứng chạy hoặc PASS; APK mới chưa được tạo hay nghiệm thu.

## Vấn đề kỹ thuật còn tồn tại

1. Poster biểu cảm được duyệt có khuôn mặt và trang phục khác chút so với source CANON V2, nên **không được dùng nguyên các patch làm sprite chính thức**.
2. Kích thước portrait rất nhỏ, thiếu vùng mắt/mày/miệng bị che và dưới tóc. Patch feather chỉ làm nổi bật phần cần **vẽ lại**, không cung cấp underpaint.
3. P0 Front/Back art full-body và ORA 15 lớp CANON V2 vẫn chưa hoàn tất. Đây là phụ thuộc trước khi hoàn thành rig và liên kết với wardrobe × damage × pose.
4. Các trạng thái runtime và 5 nút chọn đã được triển khai ở CP324, nhưng `app/src/main/assets/character_expression_profiles.json` vẫn **không có `sprite_paths`** vì chưa có sprite đủ điều kiện.

## Bước tiếp theo (CP326 — art thật)

1. Trên **khuôn mặt chính thức CANON V2**, vẽ lại riêng khu vực mắt, mi, lông mày, miệng, má, với **pixel alpha sạch và underpaint** ở độ phân giải phù hợp; không lấy vùng có da/tóc từ patch.
2. Dùng các hộp khoanh trong CP325 để đối chiếu *cách biểu cảm* của năm ảnh đã chốt, nhưng phải đo riêng điểm neo trên face nguồn V2 có đủ pixel.
3. Xuất ORA/PNG alpha có các bộ phận độc lập và composite thành chân dung từng biểu cảm; QA mắt/mày/miệng không xuyên qua tóc, mặt không nhảy khi đổi biểu cảm, tỉ lệ mắt/mũi/môi đồng nhất.
4. So sánh ở **132px và 64px** trong UI hội thoại, kiểm `shy` vs `embarrassed`, `angry` vs `pain`, `alluring` vs `shy`; gửi preview thành phẩm để nghiệm thu asset (không phải hỏi chốt lại concept).
5. Chỉ sau khi qua QA art: điền đường dẫn chính xác vào resolver `expression × wardrobe × integrity × pose`, rig/Spine thật, animation kiểm trên runtime, Android build và APK test.

**Kết luận CP325:** 5 bộ ORA tham chiếu/cấu trúc tách vùng đã làm và được kiểm thử; tiến độ sản xuất sprite độc lập cho CANON V2 vẫn **CHƯA HOÀN THÀNH**.


## Bổ sung xác minh GitHub Actions (2026-10-29)

Đã kiểm tra trực tiếp workflow runs và job steps từ GitHub đối với commit `4cab946f91efdaf5c08988df85f76bb2d0b88929`:

- **CP325 approved expression region contract:** run `40804686901`, job `123220694185` (`reference-metadata`) **SUCCESS**; bước “Ensure CP325 patches are never mislabeled as game art” **SUCCESS**.
- **CP324 character expression runtime contract:** run `40804686882`, job `123220694606` (`approved-expression-runtime`) **SUCCESS**; bước kiểm 5 state và no-fallback **SUCCESS**.
- **Approved character expressions consistency:** run `40804686885`, job `123220694407` **SUCCESS**.
- Đây là chứng cứ CI chạy **trên GitHub**, không phải chỉ local. Tuy nhiên CP325 CI chỉ đọc hợp đồng metadata, **KHÔNG chứa hoặc kiểm được các ORA trong Library**; kết quả ORA 5/5 là QA local riêng. Không suy ra Android Gradle `assembleDebug`, hoạt ảnh Spine, artwork đúng canon hoặc APK đã pass.
- Những câu 'CI chưa xác minh' ở phần lịch sử trước được thay bằng kết quả xác minh mới của ba workflow nêu trên; các workflow khác cần đối chiếu run của chính mình.
