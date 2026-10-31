# Thanh Vân Ký — Lâm Thiển CP316: khôi phục nguồn và xác minh ORA

**Ngày:** 2026-10-28  
**Trạng thái:** QA / hồ sơ nguồn **đã thực hiện**, chỉnh art CP313 **chưa thực hiện** vì thiếu file ORA nguyên gốc. Đây không phải rig/physics/APK hoàn thành.

## Quy chuẩn được giữ nguyên

- Lâm Thiển giữ nguyên nhận diện, mái tóc bạc, trang phục trắng–xanh–vàng, các tư thế đã duyệt.
- Giữ mốc **+17%**; chỉ tinh chỉnh nhẹ chiều cao/tỷ lệ tổng thể sau preview được duyệt, không tự áp dụng thay đổi lên ảnh gốc.
- Tất cả ảnh đánh dấu kỹ thuật chỉ là **tham chiếu**, không phải bản chỉnh sửa cuối.

## Nguồn đã rà soát trong phiên CP316

| Tài nguyên | Kết quả |
|---|---|
| `lin_qian_back.png` | 207 × 656, RGB, ảnh phẳng. SHA-256 `d2d663abc506ec70ff7a...` |
| `lin_qian_sheet.png` | 1448 × 1086, RGB, ảnh phẳng. SHA-256 `544a0040204c704684d4...` |
| `TVK_CP314_LamThien_Handoff.zip` | Quét đầy đủ ZIP: không có `.ora`. SHA-256 `e9afc168538c9a353e...` |
| `TVK_CP315_LamThien_ORA_QA_Handoff.zip` | Quét đầy đủ ZIP: không có `.ora`. SHA-256 `dc55625ca98c42d80d9...` |
| Drive (tên `CP312`, `CP313`, `linqian`, `.ora`) | Không có kết quả phù hợp từ tìm kiếm tên hiện tại. Không đồng nghĩa ORA không tồn tại ở nơi khác. |

**Lưu ý:** Các SHA rút gọn trên là đầu đoạn hash để đối chiếu nhanh; báo cáo JSON chứa **đầy đủ** hash của hai gói đã quét.

## Đã thực hiện

1. Tạo `tools/art/source_inventory.py`: tìm ORA trong tệp `.ora`, ZIP và ZIP lồng nhau; xuất `inventory.json` để tránh mất dấu nguồn.
2. Bước đánh giá cấu trúc: 10 lớp theo kỳ vọng, file lớp đọc được, số lớp có pixel thực, tên lớp gợi ý placeholder, missing source, chiều canvas và nội dung archive. `--min-nonempty 6` là **ngưỡng lọc kỹ thuật sơ bộ**, không phải điều kiện chứng minh bản gốc.
3. Kết quả quét thực tế trên thư mục bàn giao CP314 + CP315: **`NO_QUALIFYING_ORA_SOURCE`**, 2 ZIP, 0 ORA, 0 ứng viên đạt cấu trúc.
4. Tạo `reference/TVK_CP316_Back_Seam_Reference_Map.png`: 4 vùng kiểm tra hình back (tóc/chân tóc; gáy–vai; tay áo trái; tay áo phải) phóng to từ ảnh gốc, **không chỉnh pixel model**.
5. Chạy **10/10 unit tests PASS**: 5 test CP315 của thuật toán kiểm tra seam/alpha; 5 test mới CP316 của tìm nguồn, ZIP lồng nhau, phát hiện ORA giả 8 lớp rỗng, tên placeholder và missing layer. Đây là fixture giả lập, không chứng minh art CP313 đạt.
6. Workflows `.github/workflows/art-qa.yml` sẵn chạy bộ test trên nhánh `map-2d-prototype` khi file `tools/art`/`tests/art` thay đổi; chưa được xác nhận thông qua kết quả GitHub Actions trong phiên này.

## Lệnh tái sử dụng khi ORA xuất hiện

```bash
python -m pip install 'Pillow>=10,<14'
python -m unittest discover -s tests/art -v
python tools/art/source_inventory.py /path/to/CP313.ora --expect-layers 10 --min-nonempty 6 --out reports/cp316_source --require-candidate
python tools/art/audit_ora.py /path/to/CP313.ora --expect-layers 10 --out reports/cp313_baseline
```

Nếu hiện `STRUCTURAL_CANDIDATE_NEEDS_ART_REVIEW`, vẫn phải đối chiếu bằng mắt, thứ tự lớp, màu/nhận diện, composite và hash nguồn: không coi đây là xác nhận tác giả hay asset chuẩn. Chỉ sau đó chọn ROI trên kích thước canvas ORA thực (không dùng tọa độ thumbnail 207×656), chỉnh trực tiếp trên lớp nguồn và so pixel diff / alpha holes.

## CP317 — điểm tiếp tục

1. Khôi phục CP313 ORA 10 lớp (hoặc CP312 8 lớp và tiến trình chỉnh sang CP313) từ tệp xuất trong các phiên trước, thư mục tạm, bản lưu cá nhân, hoặc upload. Không tự chế một ORA 10 lớp bằng việc nhân bản ảnh phẳng.
2. Chạy source inventory + audit baseline, ghi đủ SHA và danh sách layer.
3. Sửa *tóc/chân tóc → gáy–da vai → dây trang sức → hai tay áo* trên ORA thật, giới hạn pixel ngoài ROI.
4. Chạy thử dịch chuyển tóc ±5 px, đảm bảo không lỗ alpha mới, tạo preview trước/sau để người dùng duyệt.
5. Chỉ sau khi đạt và duyệt mới nghiệm thu Spine/physics, kiểm tra Android APK.

**Chặn nghiệm thu:** Chưa có CP313 ORA thật = chưa thể xác nhận các mục CP317 2–5.