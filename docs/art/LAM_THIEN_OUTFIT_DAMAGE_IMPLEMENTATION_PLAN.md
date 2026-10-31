# Lâm Thiển — kế hoạch triển khai trang phục, thay đồ và hư hại

**Ngày:** 2026-10-28. **Trạng thái:** KẾ HOẠCH, chưa có artwork phân lớp hoặc gameplay hoàn chỉnh.

**Ảnh chuẩn đã duyệt:** https://drive.google.com/file/d/10jKNq-VL62sv1gez5PHlVT9QKyJp_Cvd/view?usp=drivesdk

## 1. Những quyết định đã chốt

- Trang phục có 4 mức **độ nguyên vẹn**: **100%, 70%, 50%, 30%**. Đây là độ bền quần áo, **không phải tỷ lệ da lộ ra** và **không tự đồng nghĩa với ngưỡng HP**.
- Cả áo trong, áo ngoài, váy, tay áo, phụ kiện đều bị ảnh hưởng ở những mức hư hại thấp. Giữ che phủ phù hợp ở mọi mức độ.
- Tình trạng hư hại lưu độc lập, không tự hồi phục khi hồi HP. Có thao tác sửa quần áo riêng.
- Tính năng tháo/thay trang phục tại màn Nhân vật và biến thể outer_removed riêng với trạng thái rách do chiến đấu. Việc chọn đồ ở trước trận; không tự thay trang bị giữa trận.
- Có thể hiển thị artwork 2D lúc **lần đầu đạt ngưỡng hư hại mới**; không lặp hình mỗi lượt. Trạng thái tiếp nối qua hội thoại/ảnh nhân vật/cảnh trong phòng khi có tài nguyên cùng trạng thái.
- Chiến đấu trên một màn chung, tối đa 4 nhân vật với HP độc lập.

## 2. Cần làm ngay khi tách lớp ảnh đã duyệt

1. Tách **thân nhân vật / underpaint**, áo trong, áo ngoài, tay áo trái phải, váy/vạt trước sau, các phần khoét hông, phụ kiện tóc, nơ, dây vàng. Giữ tỷ lệ cơ thể và trang phục mới nhất đã duyệt, không dùng CP317/318 cũ.
2. Thiết kế layer dùng chung cho 100 / 70 / 50 / 30 để không làm lại skeleton. Mỗi mức dùng texture/biến dạng khác nhau, không crop thiếu phần che khuất.
3. Chuẩn bị biến thể áo ngoài tháo ra và outfit thay thế, **không nhầm với hư hại combat**.
4. Preview Front + Back bốn mức trước, rồi Side / 3/4 và các tư thế trong phòng. Duyệt riêng art các trạng thái trước khi nối rig.
5. Sau đó mới nối độ bền thật, hoạt ảnh chuyển mức, quản lý lưu trạng thái; kiểm tra ảnh khi đổi tư thế, hồi máu, sửa áo, chuyển màn, và test APK.

## 3. Ma trận công việc

| Độ nguyên vẹn | Cách thể hiện | Trạng thái hiện có |
|---|---|---|
| 100% | Trang phục mặc định từ ảnh đã duyệt | Ảnh concept; chưa phân lớp |
| 70% | Hư hại nhẹ, vải và phụ kiện có dấu va chạm | Chưa có asset |
| 50% | Hư hại vừa ở nhiều nhóm trang phục | Chưa có asset |
| 30% | Hư hại nặng **kể cả trên mảnh vải còn che phủ**: mép rách, chỉ bung, xước và nếp vải lệch; vẫn giữ vùng che phủ kín đáo | Chưa có asset |

**Chưa chốt riêng:** Công thức ánh xạ sát thương/HP sang độ bền quần áo và tiêu chí kích hoạt từng mốc cụ thể. Không gán sai 70% HP = trạng thái 70% độ nguyên vẹn.

**Điểm tiếp tục:** Phân lớp mẫu Lâm Thiển 100% trước; thiết kế bốn bộ texture đồng bộ ngay trong pipeline, rồi nghiệm thu từng bộ. Đây chưa phải báo cáo hoàn thành cởi/thay đồ, animation, rig hay APK.


## 4. Bổ sung 28/10 — hư hại cuối và đề xuất cởi đồ

### ĐÃ CHỐT — cập nhật hiệu ứng 30%

- Ở cấp **30%**, ngay cả những mảnh trang phục còn đảm nhiệm việc che phủ cũng **có hiệu ứng rách/hao mòn** (mép sờn, vải rách, đường may bung, nếp xô lệch) thay vì để chúng hoàn toàn nguyên vẹn.
- Duy trì hình thể đúng reference đã duyệt và mức che phủ phù hợp; dùng lớp lót/miếng vải có thiết kế để các vùng cần che vẫn kín. Không đồng nhất % nguyên vẹn với % da lộ ra.
- Thực hiện đồng bộ ở thân áo, tay áo, vạt váy và phụ kiện, kiểm tra front/back/3-4 cùng các tư thế có asset.

### MỚI CHỈ LÀ ĐỀ XUẤT — các mức tháo/thay trang phục riêng tư

- Cân nhắc **3 trạng thái**: (1) mặc đủ trang phục, (2) tháo lớp ngoài, (3) bộ nội y fantasy riêng tư.
- Trạng thái (3) đề xuất dùng **voan/lưới xuyên sáng ở lớp phủ**, thêm **lớp lót không xuyên thấu ở vùng cần che phủ**, tiết chế phụ kiện vàng. Không thiết kế lớp vải hoàn toàn xuyên thấu để lộ các vùng nhạy cảm.
- **Chưa được người dùng chốt số cấp/thiết kế nội y**. Chưa tạo asset và không thay registry canon. Nếu được duyệt, ghi trạng thái wardrobe riêng biệt với độ bền quần áo 100/70/50/30; không tự động dùng các trạng thái hư hại cho sự kiện tháo đồ.


## 5. Quyết định mới nhất về mức rách và thay đổi tư thế — ĐÃ CHỐT 2026-10-28

- **Cập nhật mới nhất thay thế đề xuất cũ tăng rách +20%**: hạ bớt mức rách cho tự nhiên. Các mốc độ bền quần áo 100% / 70% / 50% / 30% **giữ nguyên**. Kể cả lớp che phủ ở 30% cũng được vẽ dấu hiệu hư hại nhưng vẫn che kín các vùng cần che.
- **Ảnh lựa chọn mới được người dùng chốt trong hội thoại**: `blob:https://chatgpt.com/8d8b9f33-3a9b-47c6-a677-c31dd0dcfccc`. **Chưa truy xuất/không lưu được bytes từ blob URL**. Hình thực được nhận sau này phải được đối chiếu, lưu ảnh gốc và hash; không tự điền dữ liệu hình.
- **Quy tắc đồng bộ qua pose**: tiếp tục các trạng thái đang mặc và hư hại khi đổi Front/Back/Side/3/4, quỳ/nằm/ngồi trên giường, ghế/sofa, dựa tường, hội thoại và chiến đấu. Không reset trạng thái hoặc sinh vết rách ngẫu nhiên khi đổi pose. Mỗi pose có biểu cảm/động tác tự nhiên phù hợp với bối cảnh.
- **Trạng thái thay/cởi đồ** độc lập với hư hại chiến đấu. Chi tiết số mức và chất liệu chính xác sẽ đối chiếu khi có ảnh đã chốt; giữ che phủ phù hợp.
- **Nguồn sử dụng**: mẫu ngoại hình Lâm Thiển gốc 28/10 trên Drive đã xác minh; mẫu biến thể trang phục được chốt nhưng **asset chưa nhận**. Không nhận là đã có hình biến thể chính thức để rig.
- **Hồ sơ chi tiết**: `docs/art/LAM_THIEN_CLOTHING_VARIANT_APPROVAL_2026_10_28.md`.


## 6. Mức cởi cuối phải giữ khi đổi tư thế — ĐÃ CHỐT

- **Nguồn ẢNH MỚI đã khôi phục:** [Bảng trạng thái & biểu cảm](https://drive.google.com/file/d/1M-6KIEeon7HX4Qn56UlhGMfV76Lr-sN5/view?usp=drivesdk); [Bảng kế hoạch](https://drive.google.com/file/d/1ZgMB8nkRlkar3-MYCrH32uQaYxO29S5Q/view?usp=drivesdk). Đây là **ảnh thật người dùng đã gửi** ngày 28/10, thay thế tình trạng thiếu file từ liên kết `blob:` đã mô tả trong mục 5. File nguyên bản đã được sao lưu và xác minh checksum; xem `LAM_THIEN_EXPRESSION_ACTION_REFERENCE_2026_10_28.md`.
- **Không reset mức cởi cuối:** khi ở state riêng tư cuối, đổi Front/Back/Side/3/4, quỳ/nằm/ngồi giường, ghế/sofa, dựa tường, cũng như đổi màn không đưa nhân vật về `outer_removed` hoặc `default`. Cử chỉ và biểu cảm đổi theo tư thế, **mức trang phục và cấu trúc trang phục vẫn giữ**.
- Kế hoạch ID kỹ thuật: `private_fantasy` là tên đề xuất cho mức cởi cuối, cần ảnh riêng từng pose và lớp lót che phủ; không dùng lọc trong suốt hay crop hình mặc đủ để giả lập.
- Khi thiếu art cho cặp `pose × wardrobe`: **giữ giá trị state** nhưng hiển thị thiếu asset và vô hiệu vùng chạm không có mapping; không tự fallback sang ảnh mặc đủ. Không đánh dấu từng pose hoàn tất khi chưa có sprite.
- Độ hư hại 100/70/50/30 tiếp tục độc lập, không tự giảm hoặc reset vì chuyển pose; hiệu ứng rách bám cấu trúc lớp vải và vẫn che phủ phù hợp.


## 7. Bổ sung bẩn / xước / rách theo loại sát thương (ĐÃ CHỐT)

- **Mẫu body/costume mới nhất:** [CANON V2](LAM_THIEN_CANON_BODY_V2_2026_10_28.md) ([PNG nguồn](https://drive.google.com/file/d/1mEsyn2wMo-MVQqhtbmdUiFfO8AaYhzUR/view?usp=drivesdk)); **không tạo trạng thái rách dựa trên trang phục V1 cũ**.
- Áp dụng ba thành phần chính: **bụi/bùn/vệt bẩn**, **vết trầy/sờn/đường chỉ xù trên lụa**, **rách theo thớ vải/đường may**. Mỗi loại tăng tương đối theo mức độ hư hại; sự kết hợp phụ thuộc kiểu va chạm và môi trường.
- **70%:** dấu nhỏ, rải rác. **50%:** rõ hơn và tích lũy. **30%:** dấu mạnh ở các lớp trang phục, **kể cả mảnh còn che phủ cũng sờn/rách**, nhưng vẫn bảo đảm lớp che phủ cần thiết.
- Tách `garment_damage` khỏi `wardrobe_state` và khỏi thương tích cơ thể. Ghi nhãn vị trí bẩn/xước/rách theo mảnh vải để các pose Front, Back, Side, Back Turn, giường, ghế, tường đều thể hiện đúng dấu đã có.
- **Đã có:** quy chuẩn + metadata `damageVisualProfile`. **Chưa có:** bản vẽ bẩn/xước/rách thực tế cho bốn trạng thái và các tư thế; cần preview để người dùng duyệt trước khi rig/đưa vào APK.

Xem [quy chuẩn chung về vết bẩn/xước/rách](GLOBAL_CLOTHING_DAMAGE_VISUAL_STANDARD.md).

