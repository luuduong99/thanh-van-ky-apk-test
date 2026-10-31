# TVK — CP409 Lâm Thiển / blink theo chuyển động mí (DRAFT)

**Ngày:** 2026-10-30. **Mục tiêu:** giải quyết vấn đề người dùng phát hiện ở CP407: mắt nhắm giống ảnh phủ lên mắt mở. **Không đánh dấu hoàn tất mỹ thuật.**

## Nguồn CANON duy nhất

- `LAM_THIEN_CANON_V2_1_FINAL_20261029.png` — 941×1672 RGBA.
- SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- Vùng biểu cảm giữ nguyên pixel gốc `(25,684,193,881)` → 168×197.
- Vùng chỉnh sửa chỉ gồm mắt trái `(29,93,71,124)` và mắt phải `(83,70,129,110)` theo crop. Dáng/áo/tóc CANON và tỷ lệ +17% giữ nguyên.

## Thay đổi thực tế từ CP407

- Loại bỏ hoàn toàn phép hòa trộn **ảnh mắt nhắm hoàn chỉnh đè lên ảnh mắt mở**. Không lấy CP402/407 closed bitmap làm đầu vào.
- Mô hình hóa mí trên di chuyển xuống (82%) và mí dưới nâng lên (18%); khẩu độ mắt co liên tục trong các tư thế trung gian.
- Phần mống mắt còn lộ ra được **nén theo khẩu độ hình học**, mí đang đóng được phủ bằng sắc độ da phục dựng từ chính CANON; lông mi di chuyển theo mép mí thay vì nằm trên một hình ảnh tĩnh.
- Có **15 tư thế** từ mở → nhắm → mở. Video 72 khung, 30 FPS/2,4 giây. Hai atlas: native 2520×197 (Android debug), 4× 10080×788 (soi chi tiết, **không phải master HD**). PNG native đầu/cuối khớp pixel với crop CANON.
- Ảnh vùng **ngoài hai mắt** và alpha gốc không đổi qua các tư thế (đã kiểm pixel).
- Trình xem debug `TVKBlinkAtlasPreviewActivity.kt`: chế độ CP409 được kích hoạt khi Intent có `cp409_review=true`, chỉ cho phép chọn đúng atlas native SHA `d9234630eab9e13ec07527e2c7b6fbbacd849117bf2e4983bf35ac4bcf73a07e` từ file picker, không nhúng ảnh riêng vào APK. Nút CP402 cũ tiếp tục dùng atlas CP402 cũ; hai chế độ tách biệt.

## Nghiệm thu và giới hạn

- 16 bài kiểm thử phát hiện; môi trường cục bộ có ảnh CANON chạy **15 PASS, 1 SKIP** (SKIP là kiểm tra giao diện Kotlin chỉ có trong checkout GitHub). Trong repo công khai không có CANON, dự kiến **7 PASS, 9 SKIP**, *không* là nghiệm thu mỹ thuật.
- **ART QA = NOT_APPROVED.** Mí nhắm còn cần họa sĩ tinh chỉnh chất liệu da và mi. Phóng 4× từ crop 168×197 **không tạo chi tiết mỹ thuật gốc mới**.
- **Android build ≠ chạy thành công trên máy thật.** Đường Android đã được thêm dưới debug-only, không thay sprite production hay công bố đã ghép với rig toàn thân.
- CP408 vẫn là demo full-body mesh riêng; CP409 mới là kênh mắt hình học. Chưa có nguồn tách lớp để cùng biến dạng trong một rig thật.

## Cách kiểm tra

1. Cài APK debug của cùng commit CP409 (nếu CI build thành công).
2. Trên trang tương tác nhân vật **Lâm Thiển**, chọn `CP409 | Chớp mắt theo mí (DRAFT)`.
3. Chọn **đúng** `CP409_15_POSE_NATIVE_SHA_LOCKED_DRAFT.png` trong điện thoại. App xác minh SHA-256.
4. Dùng Tạm dừng/Từng khung/Pixel–Mịn để so sánh mở CANON bên cạnh mô phỏng mới. Không chọn atlas CP407/CP402 ở chế độ CP409.

## Bước tiếp theo

CP410: họa sĩ sửa keyframe mắt và da theo bản hình học, xác nhận native/zoom; nếu đạt thì đồng bộ kênh mắt với đầu/body thật, test thiết bị rồi mới cân nhắc đưa vào runtime sản xuất. **Không tăng checkpoint nếu chỉ là vá pixel hoặc tăng test.**

## Xác minh build cuối lượt

- [CP409 GitHub QA](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/41058915025): **SUCCESS**. CI công khai chạy 16 bài, **7 PASS / 9 SKIP** vì CANON nằm trong Library, không đưa vào repo.
- [Android Debug Build](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/41058907069): **SUCCESS**, artifact `12978088196`, `app-debug.apk` **8,807,444 bytes**, SHA256 `efbd703fc7f564196fc4bd7c76631064227fdd433cf8e434f6c80ce5e5fedd3f`.
- Đã kiểm tra nội dung APK không có bitmap CANON/atlas CP409 nhúng vào assets; phải chọn atlas qua Android picker theo đúng SHA.
- Không có bằng chứng đã chạy kiểm thử trên điện thoại thật. Build thành công **không** tương đương rig hoàn thành hay mỹ thuật được duyệt.