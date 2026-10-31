# Thanh Vân Ký — Lâm Thiển CP400: eyelid paint + animated blink review

**Ngày:** 2026-10-30  
**Trạng thái thực:** Có bộ sprite 9 khung và các preview động thực tế để kiểm tra. **Chưa hoàn tất mỹ thuật và chưa nghiệm thu để dùng làm hình ảnh nhân vật trong APK.** Không dùng kết quả kiểm thử pixel làm sự phê duyệt mỹ thuật.

## Đã làm trong CP400

- CANON duy nhất: `LAM_THIEN_CANON_V2_1_FINAL_20261029.png` **941×1672 RGBA**, SHA-256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- Khung mặt hợp lệ: `(25,684,193,881)` → **168×197 native**. Không sử dụng ảnh AI của nhân vật khác, ảnh vẽ lại khuôn mặt, hoặc upscale làm nguồn.
- Nguồn nhắm cũ CP398 **Soft**, SHA-256 `5ce4ab198235a58905d8f867f53973d7d49d3e9686bb769675568d454c142c17`. CP400 tinh chỉnh lớp da dưới mí, sắc độ mi, nếp mí và lấy lại **vệt mi nguyên gốc có kiểm soát** từ CANON.
- **9 khung**: mắt mở → chuyển tiếp → nhắm → mở. Các khung giữa dùng hòa trộn *chỉ trong ROI mắt* để xem trước; chưa phải lưới cử động mí nâng cao.
- **Các tệp xem:** `CP400_BLINK_SIDE_BY_SIDE_DRAFT.mp4` (CANON cố định bên trái, hoạt ảnh bên phải), `CP400_BLINK_PREVIEW.gif`, `CP400_BLINK_PREVIEW.png` (APNG), `CP400_CANON_VS_BLINK_REVIEW.png`.
- **File nguồn:** 9 PNG native, atlas 1512×197, ORA 7 lớp (source CANON là layer duy nhất visible, các art layer/closed composite hidden), Python tạo artwork, Python tạo MP4, unit tests.
- **Kiểm tra:** 14/14 bài kiểm thử PASS với nguồn kín: hash, mode/kích thước, pixel original crop, 0 pixel thay đổi ngoài hai ROI cho tất cả khung, mở đầu/cuối đúng nguồn CANON, đóng khác source, 5 overlay layers alpha, 7 ORA layers, CRC/merged source, 9 frames GIF/APNG/atlas, chặn source giả trước khi ghi output.

## Không được ghi nhầm là đã hoàn tất

- Bản nhắm CP400 ở native vẫn đang cần **duyệt mỹ thuật**: độ dài sợi mi, nếp mí, vùng da sáng/tối khi thay hình trên màn Android, nhất là trong các cảnh thoại. Phần source face chỉ 168×197: phiên bản phóng to không thành HD master.
- GIF/APNG/MP4 xác nhận **có chuyển động phát được**, **không xác nhận** FPS Android, deform rig/Spine, hay sprite tích hợp vào game.
- Chưa có sự đồng ý cuối cùng từ người dùng đối với hình mắt nhắm CP400. **Không được đưa vào `app/src/main/assets/characters` hoặc chỉnh `sprite_paths`**, không được đặt `artist_qa_passed=true`.
- Giữ nguyên các mẫu trang phục A/B mới chỉ làm reference cho các nhân vật khác, không được thay ảnh CANON Lâm Thiển.

## Gate bắt buộc để hoàn tất hẳn mắt nhắm / chớp mắt

1. Người dùng duyệt bản closed-eye (ưu tiên kiểm tra video MP4 + ảnh zoom native). Nếu chưa đạt, sửa chính xác những chỗ bị phản hồi, không tiếp tục tạo vô hạn bản vá tự động.
2. Chuyển bản được duyệt sang mắt nhắm keyframe/layer hoàn chỉnh trong hệ artwork thật, vẽ lại in-between để iris không bị ghosting, có kiểm soát mỹ thuật.
3. Tạo sprite manifest SHA và tích hợp đúng expression/pose/state đã duyệt, kiểm tra trên Android bằng APK, rồi mới mở release gate.

**Tình trạng quản lý:** `visual_qa=PENDING_USER_APPROVAL`, `sprite_paths={}`, `apk_integrated=false`, `released=false`.