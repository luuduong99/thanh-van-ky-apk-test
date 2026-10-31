# Thanh Vân Ký — CP406 / Lâm Thiển — Mí mắt dưới dạng lớp vẽ 4× (DRAFT)

**Ngày:** 2026-10-30  
**Trạng thái:** Nguồn chỉnh sửa + preview hoạt ảnh hoàn thành về **kỹ thuật**. **CHƯA ĐẠT/CHƯA CÓ DUYỆT MỸ THUẬT**. Không release sprite/animation production hoặc tự ghép vào APK.

## Nguồn bắt buộc và giới hạn

- Chỉ dùng `LAM_THIEN_CANON_V2_1_FINAL_20261029.png` — 941×1672 RGBA, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- Crop biểu cảm chính xác `(25,684,193,881)` = **168×197 native**. Mí mắt trong 2 ROI `LEFT (29,93,71,124)` / `RIGHT (83,70,129,110)`.
- Baseline chính xác `CP402_CLOSED_ROOT_CANDIDATE_NOT_APPROVED.png` — SHA256 `0391ba0cb906bf5334f176ac28a508cad4afa700fe6cb7c2deb52affaf1ac5f6`.
- **Quan trọng:** 4× là kích thước hiển thị có anti-alias/nét vẽ bổ sung **không phải nguồn CANON 4× chất lượng gốc**. Không tự gắn nhãn HD master; cảnh, cơ thể, nhận diện vẫn chỉ dùng ảnh CANON.

## CP406 đã làm thật

1. Tạo lớp `soft_skin_shadow`, `upper_crease_warm`, `lash_tapered_core`, `separated_lash_strands`, `inner_corner_warmth` dưới dạng nét vector supersample rồi ghép trên nền CP402, chỉ trong hai ROI mắt.
2. `CP406_EYELID_8_LAYER_DISPLAY_DRAFT.ora`: 8 lớp — 1 CANON 4× visible, 1 CP402 baseline hidden, 5 lớp paint hidden, 1 closed-composite hidden; lớp ghép mặc định vẫn hiển thị ảnh gốc.
3. File `CP406_CLOSED_EYE_4X_OVERLAY_DRAFT.png` **672×788** chỉ để xem/tinh chỉnh, không phải sprite đã duyệt. Khác CANON 30.111 pixel hiển thị trong vùng mắt; ngoài mắt **0**.
4. Tạo chuỗi 15 tư thế chớp mắt 4×, 72 frame MP4/30fps/2,4 giây, GIF và bảng so sánh đúng 3 mốc CANON/CP402/CP406. Tất cả hình đã crop/sửa cùng một ảnh CANON.
5. **15/15 local unit tests PASS**, gồm SHA nguồn, SHA baseline, 8 lớp ORA, 15 pose, mở đầu/đóng cực đại/mở cuối và tính bất biến mọi pixel ngoài hai mắt/alpha. Public repo không chứa ảnh riêng: dự kiến 6 PASS và 9 SKIP — không đồng nghĩa nghiệm thu art.

## Đánh giá mỹ thuật

- Bản CP406 làm đường mí dễ kiểm tra ở độ phân giải hiển thị và tách riêng nhiều loại nét, khác cách tô 1px trước đó.
- **Chưa chứng minh vượt CANON ở mức họa sĩ**: một số chân mi còn mảnh/đều và nền da vẫn chỉ nội suy từ ảnh 168×197.
- **Không promote** CP406 thành master; CP402/CP403 vẫn là baseline kiểm tra kỹ thuật, CANON V2.1 là nguồn danh tính duy nhất. Nếu muốn nghiệm thu cuối, cần frame mắt nhắm vẽ tay thực sự (hoặc nguồn master mặt độ phân giải cao), so sánh sát khuôn mặt và cho người dùng phê duyệt.
- Chưa test thực tế trên Android; video CP406 không phải video được render bởi app. Không thay đổi mã game / APK production ở checkpoint này.

## Tiếp nối đúng việc

1. Dùng ORA 8 lớp CP406 như nguồn chỉnh sửa độc lập, tăng chất lượng chân mi và da ở màn hình/native, không nhân bản mặt bằng AI.
2. Khi keyframe được nghiệm thu mới chốt tập pose và tích hợp vào runtime debug → QA điện thoại → production approval.
3. Không tạo hàng loạt checkpoint "kiểm thử PASS" nếu chưa có tiến bộ mỹ thuật hoặc phát hiện lỗi mới.

**Asset release:** `visual_qa=NOT_APPROVED`; `production_sprite_paths={}`; `android_qa=NOT_TESTED`; `blink_feature_complete=false`.