> **MODEL LÂM THIỂN MỚI NHẤT (28/10/2026):** [CANON BODY V2](LAM_THIEN_CANON_BODY_V2_2026_10_28.md) / [PNG gốc](https://drive.google.com/file/d/1mEsyn2wMo-MVQqhtbmdUiFfO8AaYhzUR/view?usp=drivesdk). Áp dụng V2 cho mọi pose/outfit/damage mới; link ảnh cũ trong tài liệu là lịch sử. Task list P0–P2 chi tiết của Lâm Thiển: [LAM_THIEN_NEXT_TASKS_AFTER_CANON_V2.md](LAM_THIEN_NEXT_TASKS_AFTER_CANON_V2.md).

# Thanh Vân Ký — kế hoạch công việc tiếp theo (đặc tả toàn nhân vật)

**Ghi ngày:** 2026-10-28. **Cơ sở:** [GLOBAL_CHARACTER_APPEARANCE_SPEC.md](GLOBAL_CHARACTER_APPEARANCE_SPEC.md), [GLOBAL_CHARACTER_ASSET_BACKLOG.json](GLOBAL_CHARACTER_ASSET_BACKLOG.json).

## Tiến độ đã có thực

- [x] Quy tắc **mọi mức cởi** và mức hư hại tiếp tục qua **mọi tư thế** — đã ghi toàn dự án.
- [x] `CharacterAppearanceState.kt` — quản lý trạng thái wardrobe / integrity / pose / expression / action theo ID nhân vật.
- [x] `CharacterInteractionActivity.kt` — đọc trạng thái chung, báo thiếu ảnh thay vì âm thầm mặc lại hoặc dùng sai pose; biểu cảm/action có metadata theo cảnh và touch.
- [x] `MainActivity.kt` — chỉ số độ nguyên vẹn demo của **Tô Nguyệt Ly** đọc chung cùng kho trạng thái; avatar demo không giả trang phục nguyên vẹn khi state thay đổi.
- [x] Catalogue cho **Tô Nguyệt Ly** và **Lâm Thiển** khai báo `default`, `outer_removed`, `private_fantasy`; 4 mốc 100/70/50/30; danh sách 8 pose cần bổ sung mỗi người.
- [x] Công cụ `tools/validate_global_appearance.py` + `tests/art/test_global_appearance.py`, workflow APK có gate dữ liệu.
- [x] Tạo thêm ảnh minh họa hệ thống **chờ duyệt** (concept, không thay canon): [Global Appearance preview](https://drive.google.com/file/d/1QjqPz6gJnT0vl9zr5mWme4_x0BvCCh7Y/view?usp=drivesdk), 1536×1024 RGB, SHA-256 `33e432d7373eaddc0ad54305b466baf15c2233045bbe6356f9907c9036ac5b8e`. Lưu dự phòng ChatGPT Library trong `/Thanh Van Ky/Approved References/Global_Appearance_References/`.

**Chưa xác nhận:** CI/assembleDebug có thể tự chạy trên push nhưng chưa nhận được kết quả pass ở thời điểm cập nhật; chưa chạy Unity/Spine và APK thực tế trên máy Android.

## P0 — đóng khung kỹ thuật và tạo artwork nền

| Việc | Sản phẩm cần có | Điều kiện nghiệm thu |
|---|---|---|
| P0-01 — kiểm tra build/CI | Report APK debug + log checker art | GitHub Actions pass và APK thực sự có artifact |
| P0-02 — nguồn art bản chuẩn | PNG/layer có provenance từng nhân vật | Không dùng proxy/CP318/319 thay ảnh canon Lâm Thiển; Tô Nguyệt Ly có reference riêng |
| P0-03 — layer nhân vật | tóc trước/sau, mặt, tay, thân/underpaint, áo/vạt, phụ kiện, các cutout | Alpha/seam/draw order đúng khi dịch layer; không gãy phom |
| P0-04 — hoàn thành các pose nền chưa có | Front, Back, Side, Front/Back 3/4, Back Turn và pose nội thất cho 2 nữ chính | Cùng một hình thể/khung cảnh đúng; không dùng flip/crop thay ảnh pose thật |
| P0-05 — kiểm tra state logic | Thử các cấp wardrobe × integrity × 3 pose | Bất kỳ mức cởi nào không reset khi đổi pose; thiếu ảnh thì báo rõ |

## P1 — làm trang phục và biểu cảm theo trạng thái

| Việc | Sản phẩm cần có | Điều kiện nghiệm thu |
|---|---|---|
| P1-01 — các mức cởi | Áo đủ, tháo lớp ngoài, lớp trang phục riêng tư, theo mọi pose | Giữ mức hiện tại khi chuyển cảnh; voan/lớp lót kín phù hợp |
| P1-02 — cấp hư hại | 100/70/50/30 cho từng wardrobe và pose | Mức 30% có rách cả trên lớp còn che phủ; mức rách cân đối, không áp +20% cứng |
| P1-03 — hình biểu cảm | Bộ mặt/đầu phản ứng: normal, smile, blush, surprise, troubled, tired | Đúng nhân vật, context; không đổi hình thể |
| P1-04 — chuyển động | hit, idle, hair/sleeve movement, adjust outfit, relax và các pose indoor | Start/loop/end hoặc rig thực; không giả chỉ bằng lắc một ảnh |
| P1-05 — tái dùng asset | Bộ bone slot, texture-variant, underpaint, atlas | Không phải rig lại từ đầu cho mỗi wardrobe level |

## P2 — gameplay và APK thực

| Việc | Sản phẩm cần có | Điều kiện nghiệm thu |
|---|---|---|
| P2-01 — combat damage | Kết nối sát thương thật với độ bền trang phục riêng, mỗi nhân vật HP riêng | Hình 2D xuất hiện ở lần đầu đạt mốc; không tự thay đổi khi heal HP |
| P2-02 — lưu tiến trình | Save/load tất cả nhân vật & outfit/damage/pose/action | Đổi nhân vật/chương, thoát/mở game không reset |
| P2-03 — QA Android | APK thử cảm ứng/hotspot trên thiết bị Android | Không crash, đúng tỷ lệ ngang, tương thích tư thế và mọi trạng thái |
| P2-04 — chương I hoàn chỉnh | Cảnh, NPC, nhiệm vụ, trận nhiều thành viên cùng màn | Chạy xuyên suốt thay vì chỉ màn demo |

## Phạm vi số lượng art

Từ catalogue hiện có: **2 nhân vật × 12 pose (4 hiện đăng ký hoạt động + 8 cần artwork) × 3 mức wardrobe × 4 mức độ nguyên vẹn = 288 tổ hợp**.

- Hiện có **8 vị trí ảnh pose mặc đủ/100% được khai báo trong prototype cũ**; các hình đó vẫn cần đối chiếu canon và nâng chất lượng.
- **280 tổ hợp còn lại là phần việc chưa xác minh/thiếu tài nguyên** (không có nghĩa toàn bộ đã được kiểm tra từng đường dẫn trên filesystem).
- **Chưa tính** frame biểu cảm, hoạt ảnh nhiều khung, góc combat và các bộ trang phục mới trong tương lai. Sản xuất nên dùng rig/layer dùng chung để tránh vẽ 288 ảnh độc lập khi có thể tái sử dụng hợp lý.

## Quy tắc chặn nghiệm thu giả

- Ảnh preview chỉ là concept, không phải sprite theo state. Bản đồ đường dẫn `integrityImages` chưa đồng nghĩa ảnh tồn tại.
- Không ghi art/rig/physics/APK hoàn tất nếu chưa có file thực + build/test tương ứng.
- Mỗi nhân vật mới phải được thêm vào catalogue và theo **cùng quy chuẩn**; không đồng nhất thiết kế gương mặt/vóc dáng với Lâm Thiển.


## P1 supplement — effects for clothing wear

**ĐÃ CHỐT YÊU CẦU MỸ THUẬT:** Không chỉ rách. Mỗi nhân vật và mỗi wardrobe khi bị hư hại cần có **vết bẩn, xước/sờn vải và rách vải** tương ứng độ nguyên vẹn 100/70/50/30. Phối hợp loại vết tùy va chạm/môi trường và chất liệu. Cần preview chốt trước khi dùng cho Spine/APK.

- [ ] **P1-02B:** Art sample 4 mức độ cho Lâm Thiển CANON V2 và kiểm tra giữ nguyên điểm neo vết qua Front/Back/Side/pose nội thất.
- [ ] **P1-02C:** Sau khi template Lâm Thiển đạt art QA, áp dụng cùng **quy tắc**, không sao chép vết bẩn/texture/người sang Tô Nguyệt Ly và các nhân vật khác.

Chi tiết: [GLOBAL_CLOTHING_DAMAGE_VISUAL_STANDARD.md](GLOBAL_CLOTHING_DAMAGE_VISUAL_STANDARD.md).
