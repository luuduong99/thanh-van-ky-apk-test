# Thanh Vân Ký — CP374 Lâm Thiển / Floor-shadow candidate cleanup

Ngày 2026-10-30. **Trạng thái: TECHNICAL DRAFT / VISUAL QA NOT PASSED / KHÔNG ĐƯỢC TÍCH HỢP APK.**

## Quy tắc CANON bắt buộc

- **Chỉ dùng đúng** `LAM_THIEN_CANON_V2_1_FINAL_20261029.png` (941×1672 RGBA, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`).
- Nhân vật Lâm Thiển đã chốt tỉ lệ cơ thể +17%, tóc bạc/tím, trang phục trắng–xanh–vàng, biểu cảm, tư thế và 4 mức integrity (100/70/50/30). **Không chỉnh CANON**.
- Tất cả các ảnh kiểm tra trong CP374 chỉ là CANON thật, crop từ CANON và bản alpha thử của cùng nhân vật, ghi rõ không phải art duyệt.

## Đã hoàn thành trong CP374

1. Đọc **đúng nguồn** CP373: crop Front `(13,172,230,630)` = **217×458 px thực**, 19 source-region/mask, chưa có native painted high-resolution art.
2. Áp dụng **bộ lọc rất thận trọng** chỉ lên dải màu xanh-xám ở khu vực sàn: `y=431..451`, `x=37..164`, không chạm vùng `x=76..126, y>=410` bảo vệ giày; giữ toàn bộ 431 hàng đầu. Đây là bước **gỡ ứng viên bóng sàn**, không phải xóa hết bóng hoặc cleanup bằng tay.
3. Loại alpha của **1.030 pixel** nghi là bóng sàn, **không đổi RGB bất cứ pixel nào**; giữ lại ảnh/mask alpha trước và sau, mask các pixel bị loại để khôi phục nếu cần.
4. Hai vùng mũi guốc xanh ở **CANON source** giữ **163/163 pixel bên trái** và **146/146 bên phải**, không tự ý vẽ màu xanh mới.
5. Cập nhật 19 PNG mask + 19 PNG region, **ORA 21 lớp**: 19 lớp vùng ảnh nguồn visible, một lớp các ứng viên sàn bị loại **ẩn** để hoàn tác, một lớp CANON reference **ẩn**. ORA hợp lệ, ghép tĩnh tái tạo chính xác kết quả alpha thử.
6. **10/10 local tests PASS** trên nguồn CANON thực; bản kiểm thử layout GitHub thiếu nguồn private chạy **2 pass / 8 skipped**. Đây là kiểm thử kỹ thuật (hash, màu, alpha, giày, CRC, lớp), **không phải art accepted**.

## Lỗi vẫn tồn tại / release gate

- **Vẫn còn dải bóng sàn và viền lụa trắng cần sửa bằng tay.** Có khả năng một vài màu vải trùng màu sàn; lớp loại bỏ đã được giữ riêng để phục hồi khi review.
- **204 pixel thiếu hidden underpaint** theo thử chuyển động tay của CP373 vẫn chưa được khắc phục; đừng hiểu việc gỡ bóng là đã tạo được anatomy/layer ẩn.
- 19 nguồn ảnh chỉ là 19 vùng cắt pixel, **không phải các bộ phận được vẽ lại**. Không được gọi ảnh phóng to từ 217×458 là master HD.
- Chưa có full-body native-quality art, five expression attachments, four integrity states, two approved motion keyframes, Spine rig hay APK mới.
- `production_release.status=blocked_pending_art`; `sprite_paths={}`; `visual_qa=NOT_PASSED`.

## CP375 — ưu tiên thực hiện tiếp

1. Dùng đúng CANON làm khóa hình, vẽ độc lập **Front full-body tại độ phân giải sản xuất**, theo semantic parts thật: tóc trước/sau, face/eyes/mouth, torso/bodice, vai/tay trái-phải, váy/đuôi lụa, chân và cả **hai mũi guốc xanh**. Vẽ chi tiết bị che khuất (underpaint) chứ không dùng source-part polygons thay thế.
2. Manual clean mép lụa/alpha với 100% zoom và trình bày 2 pose cánh tay thực, kiểm lỗ khi xoay/dịch theo nhiều góc. Phần CP374 chỉ là guide cho bước này.
3. Xuất ORA/PSD/KRA master chất lượng sản xuất, QA silhouette/bodice/face/color theo CANON, gửi preview đối chiếu để người dùng xác nhận **trước khi** rig/Spine và tích hợp Kotlin Android.

## Tệp trong bộ bàn giao

- `OUTPUT/qa/CP374_CANON_FLOOR_BEFORE_AFTER_NOT_APPROVED.png` — so sánh từ ảnh chuẩn duy nhất.
- `OUTPUT/source/CP374_PARTIAL_FLOOR_REMOVAL_NOT_ART.png` — alpha source-draft sau gỡ bóng một phần.
- `OUTPUT/masks/CP374_REMOVED_FLOOR_CANDIDATES.png` — mask những pixel bị gỡ, có thể hoàn tác.
- `OUTPUT/ora/CP374_FRONT_19_REVISED_SOURCE_MASKS_NOT_RIG.ora` — 19 visible + 2 hidden.
- `OUTPUT/CP374_REPORT.json`, `cp374_floor_cleanup.py`, `test_cp374_floor_cleanup.py`, `CP374_TEST_LOG.txt`, `CP373_SOURCE/` và CANON gốc byte-identical.

**Kết luận:** CP374 hoàn thành *cleanup alpha có kiểm soát và có thể hoàn tác*, **không** hoàn thành tranh toàn thân hay Spine/APK. Không sử dụng ảnh thử này như CANON hoặc sprite thành phẩm.