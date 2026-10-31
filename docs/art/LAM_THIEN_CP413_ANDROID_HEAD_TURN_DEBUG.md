# Thanh Vân Ký — CP413 | Android debug: soi khe ghép đầu Lâm Thiển khi nghiêng

**Ngày:** 2026-10-30. **Branch:** `map-2d-prototype`. **Trạng thái:** TECHNICAL_DEBUG / ART_NOT_APPROVED.

## Nguồn chính xác

- Lâm Thiển **CANON V2.1 +17%**, `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, 941×1672 RGBA.
- SHA-256: `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- Crop front standing: `(16,180,224,623)`, **208×443 px**. Portrait biểu cảm `(25,684,193,881)` là pose khác và không được ghép mắt vào front đứng.
- Ảnh source nằm ngoài repo công khai. APK debug yêu cầu chọn PNG thông qua Android file picker và xác minh **raw bytes SHA-256** trước khi decode. Không dùng fallback asset nếu SHA sai.

## Tiến độ thực tế

1. Thêm `TVKCP413HeadTurnDebugView.kt`, render từ ảnh front standing đúng CANON. Góc **0° vẽ chính bitmap CANON chưa biến dạng**. Các góc -4°, -2°, +2°, +4° dùng rough polygon đầu đã được chỉ rõ là **technical cutout**; phần dưới đầu được cố ý để trắng giúp phát hiện thiếu họa sĩ vẽ. **Các dải trắng là lỗi chờ sửa**, không phải hiệu ứng game.
2. Gắn vào `TVKCombinedIdlePreviewActivity.kt` sau picker đã khóa nguồn CP410/CP411; cho chọn 5 góc, tắt mesh motion và dừng clock khi soi đầu. Không đồng thời mở CP411 guide. Gắn nút mở debug từ màn hình tương tác Lâm Thiển.
3. Không import art nhắm mắt giả, không sửa CANON, không thay bản 100/70/50/30 đã chốt. Không có rig Spine, không có sprite production.
4. Kết quả nghiên cứu CP412 ở ảnh 208×443 tại các góc -4°/-2°/0°/+2°/+4°: **271 / 174 / 0 / 174 / 276** pixel lộ phần cần vẽ, chỉ là thước đo mask kỹ thuật. CP413 Android biểu diễn trực quan phụ thuộc này; chưa xác minh pixel-count trên thiết bị thật.

## Kiểm thử và APK

- [GitHub Actions CP413 source guard](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/41071306636): **SUCCESS, 6/6 static PASS**. Bộ này xác minh phần mã/guard, **không** xác nhận mỹ thuật.
- [GitHub Actions Android APK](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/41071295753): **SUCCESS (`assembleDebug`)**. Artifact `12984997611` (name `thanh-van-ky-debug-apk`). APK size **8,817,067 bytes**; SHA-256 **`5d2382090a2df082fed950096ac570c59cb1db61a55fdb623d3451fd95ee54c0`**.
- APK kiểm tra có class `TVKCP413HeadTurnDebugView` trong dex; **không có** ảnh `LAM_THIEN_CANON` hay atlas riêng CP409 trong ZIP entries.
- Chưa có xác nhận chạy trên **điện thoại thật**. `Android build SUCCESS` không tương đương device QA.
- Gói private review `TVK_CP413_Android_Review_Pack.zip` có APK + CANON nguyên byte + README, SHA-256 `5a486fc902bc098e1f724e3760846002a8e7b7523b796d19030a52b2eb87ef4f`. Lưu trong ChatGPT Library `/Thanh Van Ky/Development/CP413_Head_Turn_Debug/`. Không commit private CANON lên GitHub.

## Hướng sử dụng debug trên điện thoại

1. Cài APK debug, mở nhân vật Lâm Thiển.
2. Chọn `CP413 | Kiểm tra đường ghép đầu (DEBUG)` (có thể dùng nút CP410).
3. Trong màn hình, chọn `1. CANON V2.1`, chọn PNG gốc từ ZIP review, app xác minh SHA.
4. Bấm `CP413 | Soi khe ghép khi nghiêng đầu (DEBUG)`, thử 0°, -2°, +2°, -4°, +4°.
5. Ghi lỗi vùng tóc/gáy/cổ/viền đầu để vẽ lại; không nghiệm thu rig nếu có dải trắng, duplicate head hoặc mất phụ kiện.

## Release gates / bước tiếp

`art_approved=false`, `independent_head_rig_ready=false`, `eye_sprite_correct_pose_present=false`, `spine_ready=false`, `production_release.status=blocked_pending_art`, `sprite_paths={}`, `android_device_verified=false`.

**CP414 (không nên làm thêm mask-only):** Tập trung tạo **master lớp vẽ thật** cùng pose: mặt/đầu, mí đóng đúng front standing, tóc trước/sau, underpaint cổ/gáy/vai, rồi visual QA trên CANON native + preview chuyển động 5 góc. Chỉ sau nghiệm thu ảnh thật mới đổi sang rendering rig chính thức và kiểm tra APK trên Android vật lý.

Tham chiếu: [CP412](LAM_THIEN_CP412_SAME_POSE_ART_INTAKE.md) và [Sổ kinh nghiệm](../TVK_LESSONS_LEARNED.md).