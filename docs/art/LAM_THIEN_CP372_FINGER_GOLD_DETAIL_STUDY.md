# TVK — Lâm Thiển CP372 | Finger, wrist & shoulder gold details

**Ngày:** 2026-10-30. **Trạng thái: DRAFT / VISUAL QA NOT PASSED / không đưa vào APK.**

## Nguồn chuẩn
- File Lâm Thiển được duyệt: `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, 941×1672 RGBA; SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- Crop Front chính xác từ ảnh chuẩn `(13,172,230,630)` → 217×458. Canvas vector 1302×2748 là không gian làm việc x6, **không phải art nhân vật HD thực vẽ**.
- Giữ nguyên +17%, thân hình, tóc bạc, trang phục trắng/xanh/vàng, 5 biểu cảm, mức hư hại 100/70/50/30. **Không sử dụng ảnh nhân vật khác trong preview.**

## Các việc có file thực
1. Dựa trên 9 layer CP371, tạo 3 layer vector riêng: `10_hand_finger_engraving` (nét ngón tay), `11_wrist_gold_filigrane` (hoa văn vòng cổ tay), `12_shoulder_gold_filigrane` (hoa văn vai cố định).
2. Hai pose **idle/raised có nét tay và cổ tay được vẽ riêng**. Layer hoa văn vai giữ nguyên ở cả hai.
3. Các lớp bổ sung được **clip alpha** vào body part tương ứng (hand, wrist, shoulder), giảm nét lạc ra ngoài silhouette. Layer mới lưu cả source SVG độc lập và PNG alpha sau clip. Không chép raster CANON thành layer art rồi nhận là họa sĩ đã vẽ.
4. Mỗi tư thế có 12 raster art layers visible và một CANON reference hidden → ORA 13 lớp. Render một contact sheet có CANON thật + CP371 draft + CP372 idle/raised drafts.
5. Kết quả thay đổi của ảnh composite so CP371: **idle 2.598 px**, **raised 2.624 px** (các pixel có giá trị khác nhau, không phải đánh giá art đẹp hơn).
6. Test `python -m unittest -v test_cp372_finger_gold_detail.py`: **11/11 PASS** trên dữ liệu thật gồm SHA lock, từ chối source sai không tạo output, path SVG riêng, ORA CRC/13 layers, alpha clipping, shoulder fixed, hand/wrist pose-specific và release gate. Bài test cần file binary sẽ skip trên CI nếu không có private source.

## Hạn chế / release gate
- **VISUAL QA NOT PASSED**: các nếp lụa/ngón tay/trang sức mới vẫn giản lược so với ảnh CANON. Đây chỉ là bộ art *một phần tay áo*; không có art full body độc lập đúng chất lượng, không có các layer mặt, mắt, chân, hai guốc xanh/4 trạng thái hư hại và 5 biểu cảm thật.
- Kiểm clip alpha không đủ chứng minh hoạt ảnh không bị hở khi uốn mesh / rig. Không có Spine, physics, in-between motion, Android APK hay FPS đã xác nhận.
- `production_release.status=blocked_pending_art`, `sprite_paths={}`. Không thay CANON gốc, không tự đánh dấu asset đã duyệt.

## CP373 tiếp theo
1. Ưu tiên **thực sự dựng bộ Front full-body native semantically layered** đúng CANON: body/face/head front+back hair, bodice, hai tay, váy/vạt, hai guốc xanh và phần khuất khi xương di chuyển.
2. So ảnh với CANON tại cùng kích thước/góc; không dùng việc phóng lớn crop raster làm chứng nhận sprite HD. Kiểm alpha/draw order với xương, đưa hai pose để người dùng xét duyệt.
3. Chỉ sau khi đạt art/animation QA mới mở cổng rig và APK.

## Gói nguồn cuối cùng
- ZIP 64 entries, CRC PASS, SHA256 `721a17c057cc3732c1c8b084a81046fd2b4d1d1e9b11a5a7b1fe4a61d4118249`.
- ORA idle SHA256 `a045b28a5120e2be6e99956479b4f3bee157419530180ca3e06086fde080126a`.
- ORA raised SHA256 `bf002c5e8524f7e06086bd76491a1aebceeb433363ab8c21f9c31a43fb12ac92`.
- Hash ZIP xác minh file nén sau cùng; phần handoff bên ngoài ZIP có thể có thêm các dòng này.