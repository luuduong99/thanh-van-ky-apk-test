# Thanh Vân Ký — CP418 | Soi 5 khung chớp mắt CANON đúng pose trong APK debug

**Ngày:** 2026-10-30  
**Branch:** `map-2d-prototype`  
**Trạng thái:** `DEBUG_REVIEW_READY_FOR_DEVICE_QA`, **ART_NOT_APPROVED**.

## Nguồn bắt buộc

- Lâm Thiển user-approved CANON V2.1 `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, 941×1672 RGBA, raw SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- Crop đứng `(16,180,224,623)` = **208×443**. Không dùng crop biểu cảm pose khác.
- CP417 5-frame atlas `CP417_SAME_POSE_5FRAME_ATLAS_DRAFT.png` = **1040×443**, raw SHA256 `cb6cbe03cb1b9ccd3201e4a6bb6ba0e9cc3225111c4f78d441d7d9d7296d05cb`.
- Hai eye ROI local: trái `(88,50,104,56)`, phải `(107,50,124,57)`. Source eyelash rows y50–51 không thay đổi.

## Tiến triển thực CP418

Đã **nâng cấp màn hình CP417 hiện có**, không tạo ảnh CANON mới:

1. Menu Lâm Thiển có nhãn **`CP418 | Soi mắt từng khung (DEBUG)`**. Vẫn dùng `TVKCP417SamePoseBlinkActivity` để giữ tương thích.
2. **Tạm dừng/chạy tiếp** và 5 nút `0/4`–`4/4` chọn khung trực tiếp. Bấm chọn khung sẽ tự dừng timeline.
3. **So mặt CANON / khung đang chọn** cùng góc, cùng crop, cạnh nhau. Phóng lớn bằng NEAREST (không giả ảnh HD), vẽ đường viền hai eye ROI để người duyệt biết vùng thay đổi.
4. Thay `Bitmap.getPixel` trong vòng lặp khoảng 370.000 lần bằng **hai lần bulk `getPixels`**, kiểm mọi khung khác CANON chỉ ở hai ROI. Bắt buộc raw SHA của cả CANON và atlas đúng; frame 0 vẫn phải pixel-identical.
5. Chỉ bật các nút kiểm tra sau khi chọn cả hai file hợp lệ. Sai ảnh/atlas phải fail-closed, xoá bản atlas cũ.

## Kiểm thử trên đúng nguồn

- Local private full test: **13/13 PASS**, gồm 7 kiểm tra mã và 6 kiểm tra trực tiếp CANON/atlas.
- Public GitHub (không chứa ảnh private): **đã xác minh SUCCESS 7 PASS/6 SKIP** — [run 41082343710](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/41082343710).
- Thay đổi so với CANON trên 5 khung: `0, 104, 119, 144, 144` pixel; **0 pixel ngoài ROI**; hai khung 3 và 4 **khác nhau 46 pixel**, không trùng nhau.
- Bảng `CP418_ALL_5_FRAMES_VISUAL_AUDIT.png` ghép đủ 5 dáng đứng, không cắt mất chân hoặc phụ kiện, cùng cận mặt zoom NEAREST. Hình này chỉ đọc lại pixel đã có.
- **Chưa kiểm chứng Android vật lý** (thiết bị, tỷ lệ UI, hiệu năng, cảm giác nháy mắt) và **chưa được user duyệt mỹ thuật**.

## Cách thử trên Android

1. Cài `TVK_CP418_Android_Debug_Preview.apk` (bản `debug`); vào **Tương tác nhân vật → Lâm Thiển → CP418 | Soi mắt từng khung (DEBUG)**.
2. Chọn `LAM_THIEN_CANON_V2_1_FINAL_20261029.png` trong SAF picker.
3. Chọn `CP417_SAME_POSE_5FRAME_ATLAS_DRAFT.png`. Chỉ file có SHA đúng mới được chấp nhận.
4. Bấm nút **Soi cận 2 mặt**; chọn từng khung `0/4` ... `4/4`; so hình mở gốc và hình đang chọn.
5. Bấm **Chạy lại** để xem loop, chuyển **Về toàn thân** để so cảm giác trong kích thước game.

## Chưa hoàn tất — release giữ BLOCKED

`visual_approval=PENDING_USER`, `spine_ready=false`, `sprite_paths={}`, `production_release.status=blocked_pending_art`, `android_device_verified=false`.

CP418 là công cụ giúp quyết định chất lượng art, **không làm tăng độ phân giải mắt 13–15px**, không tự hoàn thiện lớp tóc/gáy/cổ hay rig. Nếu hình nhắm vẫn chưa đẹp ở thiết bị thật, bước tiếp theo phải là **họa sĩ dựng lại master đầu đúng pose ở độ phân giải phù hợp** dựa CANON, giữ nhận diện, trang phục +17%; cần xem preview trước khi chốt. **Không lặp thêm hàng chục checkpoint chỉ mask vài pixel.**
## Xác minh Android debug build / bàn giao

- [GitHub Android build run 41082343613](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/41082343613): **SUCCESS**. Artifact `12989887360`, APK `TVK_CP418_Android_Debug_Inspector.apk`: **8.825.318 bytes**, SHA256 `29dcf40f65d05bb489331ef3b329eb026a854042f619448a0c479487fe3b59d9`.
- Đã kiểm tra APK ZIP CRC, DEX có class `TVKCP417SamePoseBlinkActivity` và text `CP418`; không có file private CANON hay CP417 atlas trong assets APK. Đây là **xác minh biên dịch/đóng gói, không phải chạy trên điện thoại thật**.
- Gói private `TVK_CP418_Android_Review_Pack.zip`: **12.643.773 bytes**, SHA256 `d3870e7527eeac812bbc35d9ae9272ff3693eb7e8ce7ebe0a5ecda98b54ad0fe` gồm APK + CANON exact bytes + atlas exact bytes + preview + README + manifest. Library: `/Thanh Van Ky/Development/CP418_Exact_CANON_Android_Frame_Inspector/`.
