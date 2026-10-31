# Thanh Vân Ký — CP417: same-pose source-lash blink DEBUG (2026-10-30)

**Nhân vật:** Lâm Thiển · **CANON khóa:** `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, 941×1672 RGBA, SHA-256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`. **Branch:** `map-2d-prototype`.

**Trạng thái:** `TECHNICAL_ANIMATION_DRAFT`, `PENDING_USER_VISUAL_APPROVAL`. Không thay CANON, không thêm art vào production assets, không phải rig/Spine, chưa thử điện thoại thật.

## Thay đổi có thể xem thực tế

- CP416 có hai bản mắt nhắm, nhưng có lúc trông như **hai đường mi chồng** ở kích thước gốc; hình CANON đứng vốn đã có hàng mi trên khá đậm. CP417 giữ nguyên **tất cả pixel hàng mi trên y50–51** thay vì vẽ lại thêm một đường đen.
- Tạo **5 khung source-locked cùng tư thế đứng**, progress 0/25/50/75/100; frame 0 là crop `(16,180,224,623)` = 208×443, **pixel-exact CANON**; những khung còn lại chỉ che dần phần iris bên dưới hàng mi nguồn ở ROI trái `(88,50,104,56)` và phải `(107,50,124,57)`. Không dùng mặt biểu cảm khác pose.
- Atlas `CP417_SAME_POSE_5FRAME_ATLAS_DRAFT.png` kích thước **1040×443** và SHA256 `cb6cbe03cb1b9ccd3201e4a6bb6ba0e9cc3225111c4f78d441d7d9d7296d05cb`; số pixel thay đổi với source lần lượt `[0,104,119,144,144]`, ngoài ROI **0**. Số pixel trùng ở 75/100% **không** có nghĩa hai khung giống nhau hoặc art mượt đẹp; kiểm tra 1× vẫn bắt buộc.
- Preview `CP417_CANON_VS_BLINK_REVIEW.png`, GIF `CP417_BLINK_TIMING_DEBUG.gif` có nguồn đúng, không mang nhận diện nhân vật khác. ORA **5 lớp**: 1 CANON visible + 4 khung nháp ẩn, mergedimage pixel-exact.
- **Android debug**: màn hình `TVKCP417SamePoseBlinkActivity` chỉ mở khi `FLAG_DEBUGGABLE`; dùng Android file picker chọn **hai file riêng** CANON và atlas, khóa SHA-256 nguyên byte, kích thước và kiểm từng pixel nằm ngoài ROI. Viewer dùng atlas toàn thân trong một màn hình, nhịp 2.4 giây, đóng ~150ms, giữ ~80ms, mở ~190ms. Không bundle CANON private trong GitHub hoặc APK.
- QA: local 14/14 tests PASS có private CANON; public CI chỉ PASS nhóm static và SKIP nhóm private. Android build CI chỉ xác nhận APK biên dịch, **không** chứng minh đã chạy trên máy thật.

## Giới hạn cần giải quyết trước production

1. Kích thước mắt đứng thật chỉ khoảng 13–15 px, nên 5 khung không tương đương animator-smooth HD. Có thể nhìn quá ít khác biệt ở cỡ game; hình 100% still draft.
2. Không có master vẽ tay đủ độ phân giải cùng pose, không có underpaint cổ/gáy/tóc hoàn chỉnh, không có hair/bone rig, texture/mesh và Spine import hợp lệ.
3. Cần người dùng xem bản `CP417_CANON_VS_BLINK_REVIEW.png` và preview Android rồi duyệt mỹ thuật, chưa tự cấp APPROVED_CANON.
4. Tỷ lệ +17%, nhận diện, trang phục, tóc và các ảnh damage tham khảo giữ nguyên. 4 ảnh reference ngày 30/10 **không** trở thành sprites.

**Release gate:** `visual_approval=PENDING_USER`, `sprite_paths={}`, `spine_ready=false`, `apk_production_ready=false`, `android_device_verified=false`, `production_release.status=blocked_pending_art`.

## Tệp và cách thử

- ZIP private cho người dùng: `TVK_CP417_SamePose_SourceLash_Blink_Debug_Review.zip` chứa APK debug **nếu build CI hoàn thành**, PNG CANON gốc, atlas và hướng dẫn (không có private art trong repository public).
- Đường vào: chọn Lâm Thiển trong game → `CP417 | Mắt nhắm đúng pose (DEBUG)` → chọn CANON, sau đó chọn atlas CP417; ấn Tạm dừng/Tiếp tục.
- Script: `tools/art/cp417_source_lash_blink.py`. Test: `tests/art/test_cp417_source_lash_blink.py`. APK activity: `app/src/main/java/vn/thanhvanky/prototype/TVKCP417SamePoseBlinkActivity.kt`.

**Bước tiếp theo CP418:** ưu tiên đánh giá độ tự nhiên của mắt khép cùng CANON và art underpaint gáy/cổ/tóc đúng pose; không tiếp tục tăng số checkpoint bằng cách đếm test nhỏ nếu chưa cải thiện chất lượng thật.
## CP417 — CI và APK thực sự xác minh

- [Source QA workflow](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/41080652448) **SUCCESS**; 14 tests discovered, **5 PASS / 9 SKIP** vì private CANON không có trong checkout GitHub. Với nguồn thật trên máy dựng, **14/14 local PASS**.
- [Android debug APK workflow](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/41080652547) **SUCCESS**, artifact `12990370039`; tệp `TVK_CP417_Android_Debug_Preview.apk` **8.822.005 bytes**, SHA-256 `633d72189b1cef1f756865f816df296678539afd7d466c7667559ad820887680`.
- Đã kiểm tra CRC ZIP của APK và thấy `TVKCP417SamePoseBlinkActivity` cùng atlas SHA trong DEX; **không có CANON/atlas nguồn trong assets**. Gói `TVK_CP417_Android_SamePose_Blink_Review_Pack.zip` chứa APK + private CANON + atlas + hướng dẫn, SHA-256 `0182e8fa32cad4774a10a769021e3ffe4b7fc06c78cb49f33885babee847cf12`, lưu trong Library `/Thanh Van Ky/Development/CP417_SamePose_SourceLash_Blink_Review/`.
- **Không** xác nhận đã chạy thiết bị vật lý, chất lượng FPS, nghiệm thu vẽ mắt hay rig. Trạng thái release art vẫn `blocked_pending_art`.
