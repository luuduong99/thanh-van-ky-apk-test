# Thanh Vân Ký — ƯU TIÊN MẪU MODEL & TRANG PHỤC CHO NHÂN VẬT MỚI

**Ngày chốt định hướng:** 2026-10-30  
**Phân loại:** **USER-APPROVED PRIORITY STYLE REFERENCES**; không phải CANON danh tính hoặc file sprite/rig hoàn chỉnh.

## Ảnh gốc đã được người dùng chỉ định ưu tiên

**Kho lưu bản gốc (Library):**
`/Thanh Van Ky/Character_References/Priority_Model_Outfits_2026_10_30/`

| Thứ tự | Tệp gốc trong Library | SHA-256 | Size | Ý nghĩa |
|---|---|---|---|---|
| 1 | `TVK_PRIORITY_MODEL_BLACK_HAIR_SILK_FULLBODY_20261030.png` | `04ef86ec87f53e9b2871a38d3a342261b3673795c18a96a364f646c69ca71aa0` | 941×1672 | **Ưu tiên chính** về dáng toàn thân, độ mềm và chất lượng render: nữ trưởng thành tóc đen, đầm lụa trắng-xanh |
| 2 | `TVK_PRIORITY_OUTFIT_SILVER_HAIR_SHEET_20261030.png` | `ffc8c3f8e194518460943a25bd807e98471fc76a47e02af194f367a3a306174e` | 1024×1536 | **Ưu tiên bổ sung** về dáng áo/cổ áo, form mềm, cấu trúc trang phục và layout front/back/expression; nữ tóc bạc là mẫu độc lập, không thay thế nhân vật tóc đen |
| DRAFT | `TVK_BANDEAU_STRAIGHT_NECKLINE_A_B_DRAFT_20261030.png` | `a36443e6e891ab6ddcf24ae167885693b69a4af90841493f144fafe658f0dbb3` | 1024×1536 | Preview đối chiếu biến thể **A cổ khoét sâu vs B quây ngang thấp**; **chưa được người dùng duyệt làm canon** |

**Quan trọng:** Các tệp nêu trên đã được lưu nguyên byte ở Library; không thay thế bằng ảnh tìm trên mạng hoặc ảnh sinh lại khi trình bày reference đã được chọn. Mọi hình mới phải ghi DRAFT cho đến khi riêng nhân vật đó được duyệt.

## Hướng tạo hình ưu tiên cho nhân vật tiếp theo

1. Nữ nhân vật trưởng thành, fantasy 2D anime mềm mại, sắc nét, đường nét và tỷ lệ cân đối. Có thể tham khảo cảm giác vóc dáng đầy đặn trong ảnh ưu tiên mà không áp một số đo duy nhất cho tất cả nhân vật.
2. **Chất liệu lụa mềm, tạo dáng gọn**; giảm mạnh các chi tiết bay lặp lại, dây rủ, kim tuyến và tua rua. Giữ 1–2 tà chính để tạo chuyển động, dải phụ chỉ khi thật sự cần.
3. **Trang sức ít nhưng có điểm nhấn**: hoa hoặc ngọc trên tóc, một chi tiết chính ở eo/ngực, ít dây vàng. Không biến mọi viền thành dây kim loại.
4. Có hai kiểu cổ áo trong thư viện thiết kế: **A khoét sâu** (từ reference) và **B quây ngang thấp** (mới): đường mép ngang hoặc hơi cong, ôm/ngăn nắp và đỡ vòng một, không xẻ chữ V sâu. **B là phương án cần preview/chốt riêng**, chưa là yêu cầu mặc định áp lên toàn bộ nhân vật.
5. Kiểm tra front / side / back và pose; tránh lỗi chân/giày bị khuất bất thường, vạt vải cắt qua chân và phụ kiện bị đứt. Ưu tiên toàn thân thấy rõ hai bàn chân.
6. Hướng triển khai game: tà ít hơn giúp giảm số layer/spline/physics nhưng vẫn phải tách lớp, underpaint, kiểm thử deform thật. **Không gọi concept PNG là rig, animation hoặc asset đã sẵn sàng APK.**
7. Không tự đổi nhân dạng Lâm Thiển: CANON riêng V2.1 `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, cơ thể +17% đã chốt và tính riêng từng nhân vật. Hai ảnh mới **chỉ là style/outfit reference cho nhân vật tiếp theo**, không ghi đè canon của người cũ.
8. Khả năng dùng cho Tô Nguyệt Ly hoặc nữ nhân vật khác: lựa chọn mood/outfit theo thiết kế riêng; cần phê duyệt nhận diện trước khi chốt CANON.

## Tiến độ

- ✅ Đã lưu **2 ảnh người dùng ưu tiên** trong Library, giữ SHA gốc.
- ✅ Đã tạo bản đề xuất A/B để so sánh kiểu cổ áo; đã lưu, **DRAFT**.
- ⬜ Kiểu cổ quây B cần duyệt riêng trước khi thành phương án mặc định/biến thể chính thức.
- ⬜ Chưa có sprites tách lớp, rig hoặc thực nghiệm animation cho các mẫu này.

**Bản bàn giao:** `TVK_Priority_Model_Outfit_References_20261030.zip`, kèm 3 PNG, `REFERENCE_PRIORITY_NOTE.md`, `manifest.json`. Đây là gói tham khảo; không phải bộ công cụ build game.

## Bản xem chi tiết bổ sung (DRAFT V2)

- `TVK_BANDEAU_STRAIGHT_NECKLINE_A_B_FULLVIEW_DRAFT_V2_20261030.png` — Library cùng thư mục, PNG **1536×1024**, SHA256 `ab7845995d7e98c9e393ec40e8f90e07e586d9ed4780e90c2df9dd5ea02b73f9`.
- Bảng thêm front/back + chi tiết để so sánh kiểu **A khoét sâu** với **B cổ quây ngang thấp** (phương án quây B vẫn **DRAFT/chưa nghiệm thu**).
- Dù là bản bổ sung, ảnh vẫn chứa nhiều vạt lụa phụ; cần tiếp tục giảm số tà/vải bay khi thiết kế bản dùng cho rig. Không tuyên bố đã có rig hoặc sprite hoàn chỉnh.
- Gói đầy đủ `TVK_Priority_Model_Outfit_References_20261030.zip` đã lưu trong chính thư mục Library, bao gồm **2 ảnh người dùng ưu tiên + 2 ảnh DRAFT mới + manifest + ghi chú**.
