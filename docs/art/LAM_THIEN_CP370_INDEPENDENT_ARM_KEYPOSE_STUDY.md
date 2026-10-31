# Thanh Vân Ký — CP370, hai tư thế tay áo bằng đường vẽ riêng (2026-10-29)

**Trạng thái: TECHNICAL DRAFT / VISUAL QA NOT PASSED.** Không dùng thay CANON, không nhập APK, chưa Spine/rig/animation hoàn chỉnh.

## Nguồn chuẩn không thay đổi

- Ảnh **Lâm Thiển CANON V2.1** do người dùng duyệt, `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, 941×1672 RGBA.
- SHA-256 bất biến: `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- Crop pixel-exact mặt trước: `(13,172,230,630)`, 217×458 px. Canvas vector 1302×2748 chỉ là kích thước làm việc 6×, **không phải khôi phục độ phân giải nguồn thật**.
- Chỉ CANON này làm ảnh tham chiếu. CP370 idle/raised là bản vẽ của Lâm Thiển dạng DRAFT; không dùng hình người khác.

## Điều đã làm thật

- Giữ 4 lớp bất động từ CP369: tóc sau, vải thân áo khuất, da vai khuất và phụ kiện vai vàng.
- Dựng **3 SVG đường Bézier độc lập cho tư thế nâng tay**: cánh tay/bàn tay; tay áo lụa có nếp rủ mới theo trọng lực; vòng vàng cổ tay ở tọa độ mới. Các đường vẽ raised không phải ảnh bitmap xoay từ tư thế idle.
- Tạo **hai bộ source hình độc lập**, mỗi bộ 7 SVG + 7 PNG RGBA full-canvas; hai tệp `.ora` mỗi tệp có 7 lớp art visible và 1 lớp ảnh nguồn CANON hidden (8 lớp tổng).
- Kèm hai PNG ghép nền trong suốt và preview gồm đúng CANON Lâm Thiển gốc so với hai tư thế **UNAPPROVED**.
- **9/9 kiểm thử local PASS** (8 phép kiểm có nguồn CANON thật + 1 contract test không cần ảnh; trên CI thiếu ảnh riêng tư thì 8 phép kiểm asset sẽ skip): nguồn SHA không bị đổi, từ chối ảnh sai trước khi tạo output, raised SVG path khác idle, 7 alpha layers hiện có, hai ORA CRC hợp lệ, vai vàng cố định, cổ tay di chuyển và kiểm tra lót khớp vùng nhỏ, cổng APK vẫn chặn.
- Tại ROI khớp vai crop `(56,121,85,170)`, khi chuyển idle → raised có **2.996 pixel** mới lộ và **0 pixel thiếu underpaint** *theo ngưỡng alpha và vùng khảo sát hẹp*. Không được diễn giải thành đảm bảo toàn nhân vật không có lỗi khớp.

## Đánh giá và giới hạn

- **VISUAL QA NOT PASSED**. Nét vector hiện đơn giản rõ rệt so với tranh vẽ CANON. Bàn tay và nếp áo cần họa sĩ tinh chỉnh, chưa có full-body native character master hay alpha clean theo mọi tư thế.
- Có hai **key pose SVG vẽ đường hình khác nhau**, nhưng **chưa có animation nội suy, physics tóc/vải, Spine rig hoặc kiểm FPS Android**.
- Phần vai/art chỉ gồm nửa bên trái; chưa có các semantic layers mặt, tóc trước, thân, váy, tay phải, hai chân/guốc xanh và 5 biểu cảm / damage 100-70-50-30 để đưa game.
- `production_release.status=blocked_pending_art`, `sprite_paths={}`; không thay CANON V2.1.

## CP371 tiếp theo

1. Nâng chất lượng tay, cổ tay, lụa (nhất là tư thế nâng tay) bằng vẽ tay chi tiết, theo đúng CANON và hình thể đã duyệt; kiểm 2 key pose với cùng góc nhìn/canvas và mép silhouette.
2. Làm art thật các lớp cơ thể Front chưa có, đặc biệt mặt/tóc và hai mũi guốc xanh; giữ nguyên tỷ lệ +17% đã chốt và nhận diện nhân vật.
3. Chỉ sau preview được người dùng duyệt mới tạo rig/Spine và nối game, chạy build APK, đo FPS trên thiết bị.

File mã: `cp370_two_hand_authored_poses.py`; test: `test_cp370_two_hand_authored_poses.py`; dữ liệu kỹ thuật: `OUTPUT/CP370_REPORT.json`.
- **ZIP hoàn thiện sau sửa CI import:** SHA256 `6845f2543befe36c7dabb19d2e097e0821b71485ca7d7835b6f7e8dd2bb18e9e`, 43 entries, ZIP CRC PASS; bản cập nhật lưu Library cùng thư mục CP370.
