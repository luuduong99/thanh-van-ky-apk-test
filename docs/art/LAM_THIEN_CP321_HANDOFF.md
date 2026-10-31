# CP321 — Lâm Thiển | OpenRaster Front/Back scaffold và kiểm tra thật

Ngày: 2026-10-28. **Trạng thái:** Đã tạo bộ khung ORA có thể chỉnh sửa; **CHƯA HOÀN THÀNH TÁCH ART THẬT / RIG / APK**.

## Dữ liệu chuẩn được giữ nguyên
- Canon body/costume: `LT_CANON_BODY_REF_2026-10-28_V2`; ảnh trên [Google Drive](https://drive.google.com/file/d/1mEsyn2wMo-MVQqhtbmdUiFfO8AaYhzUR/view?usp=drivesdk), SHA256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711`.
- Thông số +17% đã nằm trong V2; **không cộng thêm**.
- Preview hư hại 100/70/50/30 theo mẫu đã chốt, lưu tại Library `/Thanh Van Ky/Approved References/Lam_Thien_Damage_20261028/`. Chỉ dùng cho tham khảo, không coi là sprite.

## Artifact có thật
- `TVK_LamThien_CP321_Empty_ORA_Templates.zip` — SHA256 `fe3726c0fae00ba7d233643a070719925fb0f6f0c6a207057e67819196894fb9`.
- Sao lưu Library: `/Thanh Van Ky/Approved References/Lam_Thien_Canon_V2_20261028/TVK_LamThien_CP321_Empty_ORA_Templates.zip`.
- `LT_CP321_front_EMPTY_LAYER_TEMPLATE.ora` — SHA256 `d72951b2bf18b5ac2cd20eb9ff00737bcde122fae0e9132fd058099bbcce7618`.
- `LT_CP321_back_EMPTY_LAYER_TEMPLATE.ora` — SHA256 `876b04c31cb0fa298b150996f7bdb5c76190a02e077d79ddd2f01e6f4d478315`.
- Contact sheet và guide PNG của từng góc là **tham chiếu phẳng**, không sử dụng làm hình vẽ phân lớp.

## Kết quả kiểm tra thực tế (đọc trực tiếp ORA)

| Kiểm tra | Front | Back |
|---|---:|---:|
| Đọc ZIP/CRC | PASS | PASS |
| Canvas 2048×3072 | PASS | PASS |
| Số layer mỹ thuật | 15 | 15 |
| Layer có pixel alpha thật | **0/15** | **0/15** |
| Có 1 layer guide | Có | Có |
| Art/rig sẵn sàng | **NO** | **NO** |

Trong bản template guide đang hiển thị để hỗ trợ dựng hình; cần tắt guide trước khi export. `0/15` là kết quả đo trực tiếp alpha của từng PNG trong ORA, không phải ước lượng.

## Công cụ và kiểm thử
- `tools/validate_lam_thien_cp321_ora.py` kiểm CRC, MIME/stack/canvas, đúng 15 slot, PNG RGBA và kích thước 2048×3072, nhận diện dấu `[EMPTY]`; `--strict` chặn nhận sản phẩm chưa hoàn thiện.
- `tests/art/test_lam_thien_cp321_ora.py` kiểm test giả lập ORA đúng/sai, file không hợp lệ và gate nghiêm ngặt.
- **Lưu ý:** đã xác minh archive thật bằng Python/Pillow trong phiên này; tests GitHub mới được commit, chưa có kết quả CI được xác nhận.

## Những bước làm tiếp (P0-02 rồi P0-03)
1. Tạo *full-body art độc lập* và kiểm lại Front/Back theo canon V2 từ góc nhỏ trong poster. Không phóng to crop rồi nhận là ảnh rig-ready.
2. Đo 7 landmark thật trên từng full-body và cập nhật `LAM_THIEN_CP320_VIEW_CALIBRATION.json`.
3. Vẽ nhân vật **vào các layer ORA**: tóc trước/sau, mặt/mắt/miệng, thân/underpaint, áo/váy/tay áo, trang sức và overlay. Chỉ chuyển trạng thái `[EMPTY]` sau khi có pixel thật.
4. QA kiểm alpha holes, vùng gáy/vai/2 tay áo, layer ordering, underpaint, vật che phủ; xuất composite so sánh hình gốc cho người dùng duyệt.
5. Mới mở bước Front/Back rig/animation; sau đó lần lượt Side/3/4 và pose còn thiếu.

**Không tick P0-02/P0-03 DONE chỉ vì đã dựng khung, crop hoặc tạo JSON.**
