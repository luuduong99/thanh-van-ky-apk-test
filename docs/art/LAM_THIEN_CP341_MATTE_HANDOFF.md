# CP341 — Lâm Thiển | Phục hồi alpha tóc và vải từ CANON V2.1 (2026-10-29)

**Tình trạng:** Hoàn tất **R&D khử nền** trên một Front nhỏ, **không phải** art/Spine/APK đã được nghiệm thu.

## Nguồn bắt buộc và bất biến

- User-approved current CANON V2.1: `LT_CANON_V2_1_FINAL_USER_APPROVED_2026_10_29`, file `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, 941×1672 RGBA 9:16, SHA-256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- Nguyên vẹn kiểu áo/ngực, vóc dáng +17% đã có sẵn, tóc bạc, hoa, phụ kiện, màu trắng–xanh–vàng, năm biểu cảm, các mức hư hại 100/70/50/30; đặc biệt 30% không được cường điệu.
- CP337 ảnh khác body/áo đã bị từ chối, V2/CP338/CP339 là lịch sử; không lấy những ảnh đó thay nguồn hiện hành.

## Công việc trực tiếp lên file ảnh đã làm

1. Từ **crop nguồn exact** Front `[13,177,228,626]` (215×449), dùng kết quả CP340 GrabCut làm lõi; tính alpha theo **độ khác biệt màu so với nền trắng của bảng** để phục hồi dải tóc bạc, tay áo trắng-xanh và các mảnh vải dài bị loại trước đó. Không sinh lại người/trang phục bằng AI, không đổi RGB **bất kỳ pixel nào**.
2. Xuất `source/FRONT_CP341_REFINED_SINGLE_FOREGROUND_NOT_RIG.png` RGBA (alpha thật), `source/FRONT_CP341_EDITABLE_ALPHA_MASK.png` grayscale 215×449, `ora/CP341_FRONT_MATTE_REVIEW_NOT_RIG.ora` gồm **3 layer raster**: CP341 foreground visible, CP340 alpha hidden, crop gốc hidden. Chúng dùng để sửa mask/đối chiếu, **không là layer riêng tóc/da/áo/biểu cảm**.
3. Chụp `preview/CP341_BEFORE_AFTER_ALPHA_QA.png`, có một khung original, một CP340 thiếu tóc/vải, một CP341 phục hồi hơn. Ảnh nguồn hoàn chỉnh được đóng cùng gói để tự chạy code và test.
4. Metric nhị phân alpha lớn hơn 128: CP340 **35,564 pixel** → CP341 **55,547 pixel** (tăng **19,983 pixel**). Đây là **số pixel được phục hồi vào matte**, **không** đồng nghĩa tăng đúng 100% hay đánh giá art đẹp. Các vùng mép trái/phải và dải vải dài có thêm alpha rõ rệt.
5. **13/13 unit tests trên binary thật PASS**: SHA ảnh gốc, crop exact, RGB không đổi, alpha mask giống file ảnh, bốn vùng alpha recovery, label/viền panel được loại, ORA ZIP/CRC/stack/mergedimage trùng PNG, hash output, cờ chặn release.
6. ZIP `TVK_LamThien_CP341_Matte_Recovery_NOT_SPINE_READY.zip`, **12 file, ZIP CRC PASS**, SHA256 `08d8aa08bc4b00163e092d056f1e067a5652b0f80b9462e5308277dbe8baacb1`. ChatGPT Library Development: `/Thanh Van Ky/Development/CP341_Canon_V2_1_Matte_Recovery/`.

## Điểm chưa đủ, không được báo hoàn tất

- **Nguồn nhỏ 215×449**, nhiều chi tiết lụa/tóc đã hòa với nền trắng; phương pháp tách nền không thể tự suy ra nét vẽ bị thiếu. Vẫn còn **halo trắng**, shadow chân/vạt và các mép chưa sạch; cần chỉnh mask/pixel thủ công.
- **Không có lớp ngữ nghĩa thực** (skin_underpaint, hair_back/front, bodice, arms, eyes, mouth, sleeves). ORA chỉ dùng để đối chiếu ba biến thể ảnh phẳng. Chưa có art native high-resolution, frame animation, Spine skeleton/mesh hay APK.
- `app/src/main/assets/character_expression_profiles.json` tiếp tục `production_release.status=blocked_pending_art`, `sprite_paths={}`. Không dùng PNG mới làm asset sản xuất trước khi chốt sprite mới riêng.

## Ưu tiên CP342

1. Sửa tay mép alpha tóc/lụa trong suốt và loại shadow sàn ở chân/hai vạt, **trên chính file RGBA CP341** mà không đổi thiết kế V2.1.
2. Dựng mới **một Front artist-quality** native từ body/trang phục V2.1; vẽ tách underpaint thật (da bên dưới tay, tóc sau gáy, phần vải bị che khi xoay) và các bộ phận di chuyển. Preview so full silhouette và bodice.
3. QA chuyển động hai tay/tóc/vạt, render chuyển trạng thái, rồi mới chuyển sang 5 biểu cảm và 4 mức damage từ V2.1. Chỉ sau khi user duyệt **art sprite thành phẩm** mới đăng ký SHA/path, Spine, Android APK.
4. **Không lặp việc tạo ra nhiều poster hoặc crop mà gọi production**: P1 chỉ đạt khi có native layer art khác thực sự và tái tổng hợp chính xác.

## File liên quan

- [Manifest](LAM_THIEN_CP341_MATTE_MANIFEST.json)
- `tools/cp341/build_cp341.py` — bản nguồn tái tạo trong gói CP341 và source GitHub tham khảo.
- `tools/cp341/test_cp341_binary_local.py` — chạy trên ZIP giải nén; các PNG/ORA nhị phân lưu Library, **không nằm trong GitHub runner**.
- [Kế hoạch chính thức CANON V2.1](LAM_THIEN_PLAN_AFTER_CANON_V2_1.md)
