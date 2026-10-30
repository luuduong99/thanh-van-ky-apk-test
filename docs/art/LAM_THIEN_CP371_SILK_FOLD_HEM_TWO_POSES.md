# Thanh Vân Ký — CP371: Lâm Thiển / tinh chỉnh lụa và viền hai tư thế

**Checkpoint:** CP371, 2026-10-30. **Kết quả:** art vector chỉnh sửa được + kiểm thử cấu trúc, **VISUAL QA NOT PASSED**. Không thay thế CANON, chưa rig/Spine hoặc APK.

## 1. CANON bất biến

- Chỉ dùng đúng file người dùng chốt `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, kích thước **941 × 1672 RGBA**, SHA-256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- Crop Front không sửa pixel `(13, 172, 230, 630)` (217 × 458 px). Khung vẽ `1302 × 2748` là geometry vector trên canvas 6×, **không** có nghĩa tranh gốc đã được vẽ lại HD hay tạo đủ underpaint.
- Mỗi preview chỉ gồm CANON của chính Lâm Thiển và những bản thử của chính Lâm Thiển, có ghi rõ **DRAFT / UNAPPROVED**. Không đổi tỷ lệ +17%, mẫu trang phục, màu tóc, mắt, hai đầu guốc xanh hoặc 5 biểu cảm và 4 damage stages đã chốt.

## 2. Art và file mới (thực tế)

- Từ CP370 tạo thêm **2 lớp SVG mới cho từng tư thế**:
  - `08_silk_folds_light`: nếp lụa sáng đậm/nhạt, đường cong Bézier tách biệt giữa idle và raised.
  - `09_hem_blue_gold_thread`: đường thêu xanh–vàng rất mảnh theo mép tay áo, đường vẽ riêng ở hai tư thế.
- Tinh chỉnh các đường gấp/ngấn nhỏ trên tay của **cả hai** pose bằng nét vẽ bổ sung. Giữ nguyên các lớp đứng yên gồm tóc sau, vùng da/vải khuất và vàng vai; vòng cổ tay vẫn đi theo cánh tay.
- Hai bộ source `OUTPUT/idle/` và `OUTPUT/raised/`: **9 SVG + 9 PNG alpha** mỗi pose; hai file `.ora` mỗi file **10 lớp** (9 art visible, 1 CANON reference hidden). PNG composite trong suốt riêng cho hai tư thế.
- Preview `OUTPUT/CP371_CANON_CP370_CP371_TWO_POSES_NOT_APPROVED.png` đặt ảnh gốc CANON cạnh CP370 idle/CP371 idle/CP371 raised. Không dùng ảnh mạng hoặc hình tượng thay thế.
- Dữ liệu JSON `OUTPUT/CP371_REPORT.json` từ phép kiểm nguồn thực; mã dựng `cp371_refine_pose_details.py`; kiểm thử `test_cp371_refine_pose_details.py`.

## 3. Kết quả QA trên ảnh/canvas thật

- **11/11 local unit tests PASS** (chạy với đúng ảnh CANON). Các kiểm thử bao gồm checksum, sai CANON từ chối trước khi tạo output, SVG là path riêng, layer có nội dung, ORA CRC và số lớp, một CANON guide hidden, thay đổi pixel từ CP370, các lớp bất động không đổi giữa hai pose và trạng thái blocked.
- Số pixel RGBA thay đổi so với CP370: **idle 19.833**, **raised 35.436**. Đây chỉ là kiểm tra file có thay đổi thật, **không có nghĩa mức giống CANON cao hơn**.
- Kiểm tra nội dung hai overlay ở trong tay áo hoặc sát mép tay áo: idle folds **100%**, idle hem **100%**; raised folds **96,11%**, raised hem **100%**. Đây là containment cục bộ theo threshold alpha, không phải phép kiểm toàn bộ rig.
- ORA idle SHA-256 `5b3846bfaaab588efb5adbca73e44af745b96b70c42f50332a3a08b216eac7e6`.
- ORA raised SHA-256 `128da881cdcca62dc3ecc97217f647732f4d37725984ea4ea53e9b44a29754f2`.
- **Visual QA = NOT_PASSED**: so với CANON, vẽ tay, nếp vải, phụ kiện vẫn giản lược rõ rệt. Không có art toàn thân/native face, tóc trước, váy/tay phải/chân và giày vẽ riêng hoàn chỉnh. Chưa thể xác nhận ảnh sẽ sắc nét như CANON hay FPS/physics mượt khi đưa vào game.

## 4. Trạng thái / tiếp tục CP372

- `production_release.status=blocked_pending_art`, `sprite_paths={}`, `rig_ready=false`, `apk_ready=false`. Không bật art gate hoặc nhập bản thử vào Android.
- CP372: ưu tiên vẽ **phần tay+bàn tay/giáp vàng/nếp lụa chân thực theo CANON**, kiểm soát số lớp, silhouette và vùng hidden underpaint ở hai tư thế. Tạo thêm các lớp semantic full-body còn thiếu. Mọi art mới cần xem cạnh CANON và được duyệt trước khi rig/Spine và APK.