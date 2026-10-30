# TVK — CP415 | Lâm Thiển: tô thử lớp tóc/cổ nằm dưới đầu, giữ nguyên CANON

**Ngày:** 2026-10-30 · **Branch:** `map-2d-prototype` · **Trạng thái:** `PAINT_STUDY_NOT_APPROVED` (không phải production art).

## Mục đích và nguồn

- Dùng nguyên bản `LAM_THIEN_CANON_V2_1_FINAL_20261029.png` (**941×1672 RGBA**, SHA-256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`).
- Crop đứng chính diện `(16,180,224,623)` = **208×443** pixel; giữ tỷ lệ người +17% và mọi nhận diện/chi tiết CANON.
- Không lấy mặt từ vùng portrait 168×197 khác pose, không tái sinh nhân vật. Không nhúng CANON private vào repo public.

## Công việc đã thực hiện thực tế

1. Trên nền CP411/CP412 rough head capsule, tạo **3 lớp RGBA có màu và nét vẽ được khai báo bằng tọa độ**: 
   - `HAIR_PIGMENT`: phần tóc phía sau/ở tiếp giáp cổ, 969 pixel alpha không rỗng.
   - `NECK_SKIN`: màu da khuất dưới mặt/cằm, 545 pixel.
   - `COLLAR_SHADOW`: vùng bóng chuyển tiếp tóc–cổ–cổ áo, 120 pixel.
2. Các nét bổ sung được giới hạn **bên trong rough mask của đầu**, nên ở tư thế trung tính 0° đầu nguồn che toàn bộ phần mới; ảnh ghép **pixel-identical** với CANON gốc.
3. Đã tạo 5 góc kiểm tra `−4°, −2°, 0°, +2°, +4°`; bảng so sánh CP412 (chỉ inpaint) với CP415 (inpaint + 3 paint overlays). Lần thử đầu có **halo tím quanh đỉnh tóc khi xoay**, đã loại bỏ bằng cách giới hạn lớp tóc ở vùng cổ/tóc dưới; đây là bài học QA trực quan quan trọng.
4. Có ORA **7 lớp**: ba lớp màu **ẩn**, lớp đầu source-mask thử nghiệm **ẩn**, backing hỗn hợp inpaint + paint **ẩn**, lớp mí nhắm cùng pose **trống và ẩn**, 1 lớp CANON chính diện **hiển thị**. `mergedimage` giữ nguyên từng pixel ở crop đứng.
5. Mã tạo lại và unittest sử dụng nguồn private thực: **12/12 local tests PASS**, gồm exact SHA, source tamper rejection, 3 layer nonempty, painting không ra ngoài head matte, no crown halo, 5-angle render, ORA CRC + merged pixel exact, block premature art approval.

## Giới hạn và cổng nghiệm thu

**Không quảng bá bước này là đầu–tóc/rig đã được vẽ hoàn chỉnh.** Cụ thể:

- Mặt nạ CP411/CP412 vẫn **thô**, còn cắt tóc không đúng từng sợi và có thể lộ seam khi di chuyển.
- Backing vẫn dựa vào **OpenCV inpaint kỹ thuật** bên dưới các lớp màu mới, không phải underpaint toàn bộ do họa sĩ tô hoàn chỉnh.
- Ba lớp mới là **scripted pigment study**, không phải painter-grade master. Pixel gốc đứng 208×443 quá thấp để tự suy ra một vùng mắt HD thật.
- **Chưa có master mắt nhắm đúng pose đứng**, chưa có animation đúng source/fullbody rig/Spine, và chưa có kiểm thử trên Android vật lý.
- `visual_qa=NOT_APPROVED`, `artist_underpaint_ready=false`, `spine_ready=false`, `apk_art_ready=false`, `sprite_paths={}`, `production_release.status=blocked_pending_art`.

## Bằng chứng bàn giao

- `outputs/CP415_BEFORE_AFTER_5_ANGLES_CANON.png` — 2 hàng x 5 góc so sánh; dùng pixel nguồn thật, không tạo nhân vật mới.
- `outputs/CP415_PAINT_LAYERS_CANON_BOARD.png` — 3 layer paint tách riêng cạnh source.
- `outputs/CP415_UNDERPAINT_PIGMENT_STUDY_NOT_APPROVED.ora` — master thử có thể chỉnh Krita.
- `outputs/CP415_REPORT.json` — thông số và SHA các tệp.
- `tools/art/cp415_source_locked_underpaint.py`; `tests/art/test_cp415_source_locked_underpaint.py`.
- ZIP private `TVK_CP415_LamThien_Pigment_Underpaint_Study_NOT_APPROVED.zip` chứa tất cả file đầu vào CANON đúng SHA. Repo public chỉ có tool, test và docs (không có CANON PNG).

## CP416 — bước tiếp theo phải có art chứ không chỉ tăng test

1. Bắt đầu từ cùng CANON: vẽ lại **đường cắt tóc từng sợi** và **underpaint scalp/gáy/cổ hoàn chỉnh** tại độ phân giải cao hơn trên đúng pose, không chỉ tô các miếng ROI hoặc đổi sắc pixel.
2. Có một master mí nhắm đúng góc nhìn đứng, nhận diện gương mặt và màu sắc giữ chính xác; nếu không thể làm từ crop 208×443, phải có nguồn master độ phân giải cao được chủ dự án phê duyệt thay vì phóng to và gọi là HD.
3. Xem bản 0°, ±2°, ±4° ở native và phóng lớn; người dùng duyệt thẩm mỹ trước khi mở khóa rig/Spine và ghép Android.