# Thanh Vân Ký — CP323: Alpha/ORA production gate

**Đã chốt từ trước:** Lâm Thiển CANON BODY V2 (`LT_CANON_BODY_REF_2026-10-28_V2`), SHA-256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711`.

**Phạm vi CP323:** Kiểm thử bộ lọc *kỹ thuật* của file OpenRaster Front/Back. Không dùng kết quả để kết luận khuôn mặt, trang phục, tỷ lệ, alpha seam, Spine rig hoặc APK đã hoàn thiện. Không thay đổi ngoại hình CANON V2. Không sử dụng các concept mới chưa duyệt làm nguồn chính thức.

## Đã làm
- Tạo validator `tools/validate_lam_thien_cp323_layers.py` bằng Pillow. Đọc pixel alpha thật của 15 layer; bắt buộc PNG RGBA IDAT hợp lệ, đúng canvas 2048×3072 và cấu trúc OpenRaster; kiểm tra layer rỗng, source path, duplicate PNG, guide hiển thị.
- Tạo 5 unit test với ảnh synthetic PNG **đọc được thật**, không chỉ giả header.
- Chạy trực tiếp với file `TVK_LamThien_CP321_Empty_ORA_Templates.zip` từ CP321:
  - Cả Front và Back: ZIP/ORA/PNG structural PASS.
  - Alpha pixel thực ở 15 art layer: **0/15** ở mỗi view.
  - Có 17 production blocker mỗi view (15 empty slots/guide + placeholder status).
  - `--strict`: FAIL *đúng mong đợi*, nên chưa production-ready.
- Khóa nguyên ảnh CANON V2. Crop từ poster (xấp xỉ 103–160 px chiều rộng) không dùng làm ảnh rig 2048×3072. Ngay cả ảnh tạo mới nếu chưa được duyệt cũng không thay được model chính thức.

## Chạy lại
```bash
python3 -m pip install Pillow
python3 -m unittest discover -s tests/art -p 'test_lam_thien_cp323_layers.py' -v
python3 tools/validate_lam_thien_cp323_layers.py --zip TVK_LamThien_CP321_Empty_ORA_Templates.zip --strict --output cp323.json
```

## Tồn đọng cần đạt để được phép rig
1. Vẽ nguồn **full-body Front và Back** có độ phân giải đủ theo CANON V2 và gửi preview để người dùng duyệt.
2. Đo 7 landmarks từ chính hai ảnh mới (không gán mốc ước tính từ crop poster).
3. Điền các lớp tóc trước/sau, mặt/mắt/miệng, thân và underpaint, các lớp lụa, tay áo, váy, trang sức vào ORA. `damage_overlay` có thể rỗng ở integrity=100.
4. Guide nguồn ẩn khi xuất; từng layer có alpha hợp lệ, không sao chép full nhân vật lên tất cả slot; kiểm tra thủ công vùng tóc–gáy–vai, tay áo và che khuất.
5. So composite với CANON V2 + duyệt hình; sau khi cả gate kỹ thuật và **nghiệm thu mỹ thuật riêng** đạt mới rig/Spine, animation và APK.

Không coi việc `technical_ready=True` là thay thế được duyệt art của người dùng.

## Artefact thực tế & checksum (2026-10-29)

- Gói QA local `TVK_LamThien_CP323_Art_Gate_QA.zip` (SHA-256 `97549a185ecfeae01aa3ce3f6846d0664d1d708e744260ab048f694706c341b6`), backup Library: `/Thanh Van Ky/Development/CP323_Production_Art_Gate/`.
- Bảng đối chiếu `CP323_REFERENCE_AND_ALPHA_QA.png` (SHA-256 `013e25f3a9ad58bccdb5bb6b0225eb62f41bbe39b43e5e7a02f5e2852d6491b6`).
- Audit chạy trực tiếp trên **hai ORA** trong `TVK_LamThien_CP321_Empty_ORA_Templates.zip`: cả hai có cấu trúc/CRC đúng, mỗi file 15 slot art đều 0 pixel alpha; mỗi view 17 blocker cho gate production.
- `python -m unittest discover -s tests/art -p 'test_lam_thien_cp323_layers.py'` chạy tại container, **5/5 PASS**. Chế độ `--strict` trả exit code 1 như kỳ vọng trên hai ORA trống.
- GitHub Actions workflow `.github/workflows/cp323-openraster-art-gate.yml` đã thêm; **chưa có bằng chứng runner GitHub đã PASS**.
- Các preview được sinh trong quá trình thử nghiệm và không khớp hoàn toàn mẫu V2 **không được duyệt**, chỉ dùng đối chiếu nội bộ; không nhập vào registry hay thay ảnh model chính thức.
