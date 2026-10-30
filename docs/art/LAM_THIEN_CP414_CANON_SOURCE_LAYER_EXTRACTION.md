# Thanh Vân Ký — CP414 | Tách mẫu pixel CANON thành vùng chỉnh sửa cùng pose (CHƯA DUYỆT)

**Ngày:** 2026-10-30  
**Nhân vật:** Lâm Thiển | `map-2d-prototype`  
**Kết quả:** `SOURCE_PIXEL_REGIONS_DRAFT`; **KHÔNG** phải 11 layer art sạch, chưa sẵn sàng rig, Spine, Android production.

## Nguồn đã khóa

- CANON V2.1 +17%: `LAM_THIEN_CANON_V2_1_FINAL_20261029.png` 941×1672 RGBA.
- SHA-256 nguồn: `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- Vùng dáng đứng: `(16,180,224,623)` = 208×443. Không ghép/đổi bằng chân dung biểu cảm `(25,684,193,881)`.

## Làm được, có file thực

1. **11 PNG RGBA có pixel nguồn gốc thật, không rỗng**: tóc đỉnh/ mái, mặt/má, hai vùng mắt mở, hai phụ kiện, tóc trên trái/phải, cổ và khuy cổ, hai vùng tóc dài nghiên cứu. Các polygon được ước lượng thủ công theo tọa độ pose đứng; **vẫn còn nền trắng, đường cắt thô và vùng chồng lấn**; chưa phải matte/sprite production.
2. **2 RGBA rỗng có chủ đích**: cần vẽ thêm da/đầu/tóc khuất, và mí mắt đóng hoàn toàn đúng góc đứng. Tên lớp ghi rõ `EMPTY`.
3. `CP414_SOURCE_PIXEL_LAYERS_NOT_RIG_READY.ora`: **14 layer** = 11 nghiên cứu ẩn + 2 cần vẽ trống ẩn + 1 CANON đứng hiển thị; mergedimage là CANON từng pixel nguyên bản. Không xuất hai lớp rỗng thành hiệu ứng hoàn thành.
4. Bảng `CP414_HEAD_LAYER_INSPECTION_BOARD.png` minh họa tính chồng lấn/cắt thô, lớp alpha, nguồn; `CP414_LAYER_BOUNDARIES_4X_SOURCE.png` định vị vùng cần họa sĩ sửa trên ảnh thật. Zoom không tăng độ phân giải art.
5. `CP414_REPORT.json` ghi rõ SHA và trạng thái blocker. Công cụ và bài kiểm định có thể chạy lại từ nguồn hash đúng, không cần sửa engine.

## Kiểm chứng

- **11/11 bài test local PASS trên CANON thật**: khóa nguồn, từ chối sai SHA, nguồn pixel RGB không bị thay trong vùng mẫu, 14 lớp ORA đúng visibility và pixel merged, 2 art lớp trống, release gate đóng.
- [GitHub Actions CP414 run 41073132107](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/41073132107) **SUCCESS**: 11 bài được phát hiện, **6 PASS / 5 SKIP** do public repo không có CANON riêng tư. **Không suy diễn CI xanh là đã vẽ xong mỹ thuật.**
- Không thêm/đổi tệp ảnh Lâm Thiển vào `app/src/main/assets` và không tạo production APK.

## Bản chất blocker

Ảnh đứng chỉ rộng **208 px**, 2 mắt mỗi bên khoảng 13×10 và 15×10 px. Chia ảnh gốc theo vùng có thể giúp chuẩn bị lớp, **nhưng không thể tạo ra vùng gáy/cổ/tóc bị che khuất hoặc mắt khép painter-grade** mà nguồn chưa chứa. Các vùng alpha thô cần được họa sĩ sửa mép, thêm underpaint có chất lượng và kiểm tra chuyển động ±4° trong debug CP413. Không tuyên bố đã hoàn thiện vì có các file `.png`/`.ora`.

## CP415 — đường găng thật

1. Lấy mẫu CANON, vẽ **underpaint thật** cho cổ/gáy/scalp và mặt khuất ngay trong bản ORA; tách tóc trước/sau và vẽ lại đường viền theo đúng nhận diện. Không dùng inpaint tự động như final.
2. Vẽ đóng mắt cùng pose đứng trên đầu có phần nền da đúng, phóng so với CANON và cho người dùng duyệt ở native + zoom.
3. Kiểm tra pixel chính xác ở góc 0° và mép giao ±2°, ±4°; cho thử Android thật. Chỉ sau approval mới nâng `APPROVED_CANON`, rig/animation và tích hợp sprite.

**Gate giữ nguyên:** `production_release.status=blocked_pending_art`, `sprite_paths={}`, `visual_approved=false`, `rig_ready=false`, `spine_ready=false`, `android_device_verified=false`.

## File công khai

- `tools/art/cp414_canon_semantic_layers.py`
- `tests/art/test_cp414_canon_semantic_layers.py`
- `.github/workflows/cp414_source_pixel_layers.yml`

Bộ ZIP private chứa CANON **nguyên byte** và output để tái tạo, không được đưa nguồn riêng tư lên repo công khai.