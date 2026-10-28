# CP320 — P0: Chuẩn hóa góc nhìn và chuẩn bị tách layer (2026-10-28)

**Trạng thái: BẮT ĐẦU, chưa nghiệm thu P0-02/P0-03.** Đã lưu hợp đồng hiệu chuẩn và bộ kiểm tra tự động. Không có bằng chứng đủ để tuyên bố đã dựng full-body turnaround, ORA/PSD, rig hay APK.

## Nguồn chính thức
- **Canon V2**: [PNG gốc trên Google Drive](https://drive.google.com/file/d/1mEsyn2wMo-MVQqhtbmdUiFfO8AaYhzUR/view?usp=drivesdk), 1672×941 RGBA, SHA256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711`; ảnh phẳng đã duyệt, không phải file layer.
- **Damage preview**: PNG bốn cột 100/70/50/30 đã được người dùng chốt. Đã lưu **nguyên byte** vào ChatGPT Library: `/Thanh Van Ky/Approved References/Lam_Thien_Damage_20261028/TVK_LamThien_Damage_4Levels_Approved_20261028.png`, SHA256 `03251b5ec9b020b325687b530c98e026622ba7b3334466ab5d2323a0a89c9e23`. Bản này là chuẩn hình ảnh hư hại, **không thay canon body V2**.
- Kiểm tra Drive tìm `CP313` (28/10): không tìm thấy ORA 10 lớp trong kết quả tìm tên; không nhận PNG phẳng như ORA.

## Kết quả đã làm (hạ tầng P0)
- Tạo `docs/art/LAM_THIEN_CP320_VIEW_CALIBRATION.json`: danh sách 6 view, 6 pose độc lập, mốc neo và taxonomy 15 layer; giá trị `asset_path`, `layered_asset_path`, `landmarks_normalized` còn **null** do chưa có artwork full-figure đủ để đo thật.
- Tạo `tools/check_lam_thien_cp320.py`: kiểm tra SHA/dimensions PNG, cảnh báo thiếu mốc/asset, kiểm 7 landmark chuẩn hóa (0..1), chống cộng lại +17% và chống đánh đồng ảnh phẳng với layer.
- Thêm `tests/art/test_lam_thien_cp320.py`: kiểm hợp đồng hợp lệ, strict gate chưa pass, từ chối mốc giả và signature sai.
- Nguồn ảnh canon V2 và preview damage được giữ riêng, không tự ý crop/flip tạo ra sprite giả.

## Kế hoạch sản xuất cụ thể (theo thứ tự)

1. **P0-02A / Front–Back**: trích từ nguồn full-body độ phân giải đủ, giữ chiều cao/tỷ lệ từ CANON V2. Gửi ảnh so sánh mặt trước–sau; xác nhận phần gáy–vai, tóc, tay áo và hông.
2. **P0-02B / Side–3/4**: tạo bản vẽ full-body từ V2 (không lật front làm back), đồng nhất màu tóc/bề mặt, silhouette, chi tiết lụa và phụ kiện; gửi preview để duyệt.
3. **P0-02C / 7 mốc**: đo trên **ảnh full-body riêng biệt**, nhập `head_top`, `chin`, `shoulder_center`, `waist_center`, `hip_center`, `knee_center`, `ankle_center` theo tọa độ `[x,y]` chia theo kích thước crop. Mốc là tọa độ quan sát thật, không lấy số B/W/H minh họa làm pixel.
4. **P0-03A / Layer 15 nhóm**: tóc trước/sau, cơ thể + underpaint, mặt/mắt/miệng, trang phục trong/ngoài, tay áo L/R, váy trước/sau, phụ kiện và damage overlay. Mỗi layer có alpha thật và file chỉnh sửa ORA/PSD đi kèm.
5. **P0-03B / QA**: xuất composite so với preview được duyệt, kiểm seam, lỗ alpha, cutout, draw order, tóc gáy/vai, tay áo với thử dịch/biến dạng; chỉ tick hoàn tất khi có file và ảnh đối chiếu.

**Quy trình chống hồi quy:** Ảnh body V2 đã tích hợp tỷ lệ +17% từ lịch sử, **không cộng thêm**. Không dùng CP317–319 làm canon; không tái dùng silhouette của Lâm Thiển cho nhân vật khác. Tất cả wardrobe state và độ bền độc lập khi đổi tư thế.

## Chạy kiểm tra

```bash
python3 tools/check_lam_thien_cp320.py
# Khi tải đúng PNG nguồn về máy:
python3 tools/check_lam_thien_cp320.py --canon path/to/TVK_LamThien_CANON_BodyCostume_V2_20261028.png --damage path/to/TVK_LamThien_Damage_4Levels_Approved_20261028.png
# Gate production: phải fail khi art/layer/preview chưa đủ; chỉ pass sau nghiệm thu
python3 tools/check_lam_thien_cp320.py --strict
python3 -m unittest discover -s tests/art -p 'test_lam_thien_cp320.py'
```

## Tiêu chí đóng checkpoint
- Mọi view bắt buộc có source đủ độ phân giải, 7 landmark, ảnh review được chốt, file layer thực và thử nghiệm alpha/occlusion.
- Tài nguyên đã đo không được thay hình thể V2; cảnh quay indoor là pose khác, không làm reset wardrobe/integrity.
- Đến lúc hoàn thành bước trên, mới đánh dấu P0-02 và P0-03 DONE. Hiện tại: **P0-01 done, CP320 contract+validator done, các sản phẩm art chưa done.**
