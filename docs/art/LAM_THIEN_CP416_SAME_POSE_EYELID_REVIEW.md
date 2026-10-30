# Thanh Vân Ký — CP416 | Lâm Thiển: mắt nhắm đúng pose đứng (source-locked ART DRAFT)

**Ngày:** 2026-10-30  
**Trạng thái:** `DRAFT_VISUAL_REVIEW_REQUIRED` — không thay CANON, không đưa vào art production, không import APK.

## Điều gì đã thay đổi thật

- Dùng **chính xác bản CANON V2.1** `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, 941×1672 RGBA; SHA-256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- Tách crop **cùng tư thế đứng** `(16,180,224,623)` = 208×443. **Không** ghép mặt biểu cảm (168×197) khác góc nhìn, không biến ảnh reference thành CANON, không tự tăng/giảm tỷ lệ hình thể +17%.
- Vẽ **hai phương án mí mắt nhắm** bằng đường cọ/vector được chỉ định riêng trên đúng face source: `RESTFUL` (nhẹ) và `COMPLETE` (khép rõ). Mỗi phương án có **3 lớp RGBA độc lập**: `SKIN` (màu da che phần đồng tử lấy mẫu từ chính má CANON), `CREASE` (nếp mí) và `LASH` (nét mi). Đây là **painted low-resolution candidate**, không phải lớp khôi phục HD do họa sĩ đã nghiệm thu.
- Tạo atlas ngang `CP416_OPEN_SOFT_CLOSED_ATLAS_DRAFT.png` gồm 3 frame 208×443; frame đầu **pixel-identical** với crop CANON. Không tích hợp atlas vào Android/Spine vì người dùng chưa duyệt.
- Có **GIF thử trạng thái** mở–khép nhẹ–đóng–mở, đánh dấu `TIMING_PROXY_NOT_APPROVED`. Nó chỉ kiểm sơ bộ nhịp, **không** đại diện cho eyelid deformation mượt thật; không chứng minh FPS Android.
- ORA **9 lớp** gồm 8 lớp thử nghiệm ẩn (2 composite + 6 lớp paint), **chỉ CANON đứng visible**; `mergedimage.png` pixel-exact. Có thể mở bằng Krita để chỉnh riêng lớp mi và da, không cần vẽ lại từ đầu.

## Bằng chứng và giới hạn

| Kiểm tra | Kết quả |
|---|---|
| Raw SHA CANON / RGBA / crop source | PASS |
| `RESTFUL` chỉ sửa 2 ROI mắt | **249 pixel thay đổi**, **0 ngoài ROI** |
| `COMPLETE` chỉ sửa 2 ROI mắt | **247 pixel thay đổi**, **0 ngoài ROI** |
| Neutral / atlas frame 0 / ORA merged | **pixel-identical CANON** |
| 6 lớp alpha art không rỗng, đều ở ROI mắt | PASS |
| 12 bài kiểm thử cục bộ khi có CANON private | **12/12 PASS** |
| [GitHub Actions CP416](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/41078692596) | **SUCCESS: 5 PASS / 7 SKIP** (không có private CANON) |
| Đã nhận duyệt mỹ thuật / blinking theo hình học mí thật | **NO** |
| Master HD, tóc/gáy/cổ phân lớp / rig/Spine | **NO** |
| APK production art, test điện thoại thật | **NO** |

**Giới hạn chất lượng quan trọng:** mắt trên sprite đứng chỉ rộng khoảng 13–15 px. Ảnh phóng lớn chỉ là viewing proxy, **không có thêm chi tiết thật**. Hai phương án cần người dùng đánh giá **tại cỡ nhân vật trong game và ở crop phóng đại**. Nếu chưa đẹp, không dùng cho game; bước hiệu quả là vẽ lại vùng mặt đúng pose ở độ phân giải cao hơn, vẫn đối chiếu pixel/nhận diện CANON.

## Tài liệu và tiếp nối

- `outputs/CP416_CANON_NATIVE_AND_ZOOM_REVIEW.png`: xem ba trạng thái cạnh nhau, tất cả dựa đúng CANON.
- `outputs/CP416_BLINK_STATE_TIMING_PROXY_NOT_APPROVED.gif`: thử nhịp chuyển trạng thái **không phải animation cuối**.
- `outputs/CP416_OPEN_SOFT_CLOSED_ATLAS_DRAFT.png`: atlas 3 khung 208×443; không nhập game.
- `outputs/CP416_SAME_POSE_CLOSED_EYE_EDITABLE_NOT_APPROVED.ora`: 9 lớp chỉnh sửa; nguồn CANON visible.
- `tools/art/cp416_front_pose_eyelid_art.py`: dựng lại source-locked; `tests/art/test_cp416_front_pose_eyelid_art.py`: QA chống sai nguồn và nâng trạng thái art giả.
- Tệp private CANON/ORA/PNG/ZIP nằm riêng trong Library `/Thanh Van Ky/Development/CP416_Same_Pose_Eyelid_Review/`; **repo công khai chỉ chứa code, tests, tài liệu.**

## Điều kiện tiếp tục CP417

1. Xem và chọn/reject ứng viên mí nhắm dựa trên **chính khuôn mặt gốc**. Không tự cho visual approval vì số test PASS.
2. Nếu đạt: chỉnh nét mi/da theo feedback, thử các khung **eyelid geometry** trung gian mượt, không phải chỉ crossfade 3 ảnh; kiểm tại cỡ 1×.
3. Song song cần master tóc/gáy/cổ **được vẽ sạch và phân lớp thật** để thử ±2°/±4°, không dùng rough mask hoặc inpaint CP415 làm final.
4. Chỉ tích hợp rig/Spine/Android sau visual approval và test thực thiết bị.

**Release gate bất biến:** `production_release.status=blocked_pending_art`, `sprite_paths={}`, `spine_ready=false`, `apk_art_ready=false`, `physical_android_tested=false`.