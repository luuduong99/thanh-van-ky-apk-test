# Thanh Vân Ký — CP401: chớp mắt Lâm Thiển theo mí che mắt, **DRAFT**

**Ngày:** 2026-10-30. **Nhân vật:** Lâm Thiển, ảnh CANON V2.1 đã chốt.

## Kết quả đã làm

1. Dùng chính xác `LAM_THIEN_CANON_V2_1_FINAL_20261029.png` (941×1672 RGBA), SHA-256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`, crop nguyên vẹn `(25,684,193,881)` → 168×197.
2. Tạo một **keyframe nhắm mắt thử nghiệm** bằng cách nội suy da từ chính các pixel của CANON (OpenCV inpainting), rồi vẽ nét mi giảm độ dày ở khóe. Không thay ảnh khác, không đổi tóc/mặt/trang phục ngoài hai ROI mắt.
3. Cải thiện so với hòa trộn CP400: đối với khung trung gian, mí che mắt dần theo đường giới hạn hình học, thay vì cộng hai ảnh mắt mở và nhắm với alpha toàn vùng (dễ làm mống mắt trông như bóng mờ). Chuyển động vẫn là kỹ thuật ảnh 2D, **không phải rig/Spine**.
4. Xuất 15 tư thế mắt mở→nhắm→mở; 72 frame/30 FPS trong vòng 2.4 giây; video MP4 đối chiếu CANON (tĩnh) và bản CP401 (chuyển động); GIF, APNG, pose atlas, JSON báo cáo.
5. **13/13 unit tests PASS** trên nguồn riêng tư; **5 PASS / 8 SKIP** trong kiểm tra local mô phỏng CI công khai thiếu ảnh CANON. Không sửa ảnh CANON; **0 pixel thay đổi ngoài mắt** trong mọi khung đã kiểm.

## Đánh giá mỹ thuật

- Bản thử CP401 giúp loại bỏ hiện tượng hòa trộn iris trắng như bóng mờ ở khung trung gian; so với bản CP400, ảnh nhắm mắt vẫn chưa có underpaint/lông mi họa sĩ đủ chuẩn dùng ngay trong game.
- Mắt nhắm được dựng bằng công cụ từ crop nhỏ 168×197. Video/phóng ảnh là bản **resample**; không thể tự gọi là *HD master* hoặc sprite đã nghiệm thu.
- **Chưa đạt điều kiện release:** phải xem bản gốc và zoom, tinh chỉnh thủ công nếu cần, và nhận xác nhận mỹ thuật của người dùng. Chưa đăng ký `sprite_paths`, chưa tích hợp thử hoặc test APK.

## Tiếp theo — CP402

1. Họa sĩ hoàn thiện thủ công lớp mí/mi/da khớp nét CANON, cố gắng có lớp gốc độ phân giải cao hơn thay vì phóng pixel; trình xem preview ở native và zoom. Nhấn mạnh hai khóe mắt, bóng da và đầu lông mi.
2. Khi keyframe đã duyệt: dùng cơ chế mí che từ CP401 làm prototype, vẽ khung trung gian khớp style và nghiệm thu loop ở tốc độ thật.
3. Chỉ khi các khung được duyệt mới xuất atlas sprite có hash/manifest, tích hợp Android, kiểm tra mặt nạ/tốc độ/vsync trên thiết bị và xác minh APK. Nếu phần hình chưa đủ chất lượng, không tuyên bố hoàn thành.

**Cảnh báo:** `CP401_*_DRAFT*` chỉ là tài nguyên thử nghiệm. Không commit asset nguồn riêng tư vào GitHub công khai; lưu file thực trong Library/ZIP đính kèm. CANON và các thông số Lâm Thiển +17% vẫn được giữ nguyên.

## Chạy lại khi có nguồn riêng tư

```bash
python -m pip install Pillow numpy opencv-python-headless
python tools/art/cp401_occlusion_blink.py \
  --canon /path/to/LAM_THIEN_CANON_V2_1_FINAL_20261029.png \
  --out /path/to/CP401_OUTPUT
python -m unittest discover -s tests/art -p 'test_cp401_occlusion_blink.py' -v
```

`build_video.py` phụ trợ chỉ dùng để tạo video trình bày cục bộ, không có tác động lên ứng dụng Android.