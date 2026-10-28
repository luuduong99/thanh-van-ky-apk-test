# CP322 — Lâm Thiển | Thử nghiệm alpha 5 góc nhìn, KHÔNG THAY CANON V2

Ngày: 2026-10-28. **Status: TECHNICAL PIPELINE TRIAL PASSED; VISUAL ART NOT APPROVED; P0-02/P0-03 PENDING.**

## Quy tắc bắt buộc / không hồi quy
- **CANON Lâm Thiển đã chốt**: `LT_CANON_BODY_REF_2026-10-28_V2`, [Google Drive](https://drive.google.com/file/d/1mEsyn2wMo-MVQqhtbmdUiFfO8AaYhzUR/view?usp=drivesdk), SHA256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711`.
- **Mẫu hư hại chính thức** 100/70/50/30 theo hình user duyệt, SHA256 `03251b5ec9b020b325687b530c98e026622ba7b3334466ab5d2323a0a89c9e23`.
- **Bản preview thử kỹ thuật mới** chỉ là nguồn tạo PNG alpha để kiểm pipeline. Một số tỷ lệ/cụm trang sức/trang phục khác V2. **Không được nâng thành canon, asset gameplay, mẫu layer hay Spine rig** mà không có lượt duyệt mới. +17% đã nằm trong canon, không cộng lại.

## Artifact đã tạo và nghiệm thu kỹ thuật tại phiên này
- ZIP `TVK_LamThien_CP322_Alpha_Trial_NOT_APPROVED.zip` — SHA256 `bf73215eaa09baa27d024c0aeaf864137a90d1d06d3291bc5e2975790062a437`, ZIP CRC: PASS.
- Library backup: `/Thanh Van Ky/Development/CP322_Alpha_Trial/TVK_LamThien_CP322_Alpha_Trial_NOT_APPROVED.zip`.
- 5 PNG **native-resolution alpha** dưới đây, không phóng thành 2048×3072 và không giả có 15 layer:

| Draft view | Native PNG | Pixel alpha >16 | Alpha coverage |
| --- | --- | ---: | ---: |
| Front | 192×427 | 56,419 | 68.82% |
| Side | 147×427 | 35,006 | 55.77% |
| Back | 199×427 | 51,748 | 60.90% |
| Front 3/4 | 186×427 | 54,491 | 68.61% |
| Back 3/4 | 186×427 | 47,695 | 60.05% |

- Có `CP322_DRAFT_ALPHA_CONTACT.png` so sánh trên nền tối, cho thấy pixel alpha và các lỗi rìa trắng còn phải sửa.
- `docs/art/LAM_THIEN_CP322_ALPHA_TRIAL_MANIFEST.json`: lưu checksum chính xác và cờ `NOT_APPROVED` + `new_visual_is_not_canon`.
- `tools/validate_lam_thien_cp322_proxy.py`: kiểm checksum, native dimensions, giải mã IDAT/PNG scanline filters 0–4 để tính alpha thật, kiểm CRC, cấm thay canon, `--strict` luôn fail đối với bản nháp.
- `tests/art/test_lam_thien_cp322_proxy.py`: unit test với PNG tổng hợp, kiểm alpha decode, CRC, khóa canon và gate strict. **Kiểm thử trong container: 4/4 PASS**, kiểm đủ 5 ảnh thực trên manifest PASS; chưa có bằng chứng GitHub Actions CI tương ứng.

## Diễn giải đúng về tiến độ
- **HOÀN THÀNH:** kỹ thuật trích PNG alpha mẫu, lưu SHA, mã kiểm tra và bản backup.
- **CHƯA HOÀN THÀNH:** art CANON V2 Front/Back/Side/3/4 ở độ phân giải sản xuất, 7 landmark trên mỗi góc, 15 layer tô thật trong ORA và kiểm alpha/underpaint, rig/physics, texture 4 mức và APK.
- **Không dùng** 5 ảnh dự thảo trong thư mục production character assets; chỉ dùng để thử xuất PNG/alpha và lỗi compositing.

## Đường tiếp tục ưu tiên P0-02 → P0-03
1. Dựng độc lập Front/Back độ phân giải đủ bằng chính mẫu CANON V2, không tự thay body/face/trang phục/tỷ lệ, gửi preview trước khi chốt.
2. Sau đó dựng Side/3-4, đo 7 landmark thật trên từng view, gán cùng đường xương/slot.
3. Điền art thật vào 15 layer ORA, kiểm alpha seams, gáy/vai, tay áo, tóc, váy và underpaint; thử transform ±5 px, không tạo lỗ alpha.
4. Chỉ khi qua QA art mới chuyển sang damage texture 100/70/50/30, biểu cảm, animation, runtime battle và APK.

**Không tự đánh dấu P0-02/P0-03 hoàn thành do có 5 PNG alpha nháp.**


## Bổ sung kiểm chứng / nguồn và CI (2026-10-28)

- Ảnh nguồn dự thảo **không được duyệt**: `CP322_SOURCE_UNAPPROVED_CONCEPT.png`, RGB 1536×1024, SHA256 `f171a06f9d67cb510cd46067a30d12763850620970e3d724c93d5c8a681c2d60`; đã lưu **riêng trong Library Development**, không nằm trong Approved References: `/Thanh Van Ky/Development/CP322_Alpha_Trial/CP322_SOURCE_UNAPPROVED_CONCEPT.png`.
- Chạy kiểm tra thực tế trong cây source tương đương GitHub: **4/4 unittest PASS**; manifest của 5 PNG alpha: PASS, CRC/IDAT/alpha occupancy: PASS. `--strict`: **FAIL như mong đợi** do `NOT_APPROVED`.
- Đã thêm `.github/workflows/cp322-art-alpha-validation.yml` chạy unittest trên push/PR phù hợp. **Chưa xác minh job GitHub Actions đã chạy hoặc PASS**; không dùng kết quả local thay CI.
- ZIP cuối cùng trên Library có SHA256 `bf73215eaa09baa27d024c0aeaf864137a90d1d06d3291bc5e2975790062a437`, CRC PASS, 10 entry (5 PNG, contact sheet, manifest, README, validator, test).
