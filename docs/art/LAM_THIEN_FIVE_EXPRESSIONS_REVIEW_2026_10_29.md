> **ĐÃ ĐƯỢC DUYỆT NGÀY 2026-10-29 — TÀI LIỆU REVIEW ĐƯỢC LƯU LÀM LỊCH SỬ.** Không dùng trạng thái “chờ duyệt” bên dưới để xác định tiến độ hiện hành. Nguồn chính thức: [LAM_THIEN_FIVE_EXPRESSIONS_APPROVED_2026_10_29.md](LAM_THIEN_FIVE_EXPRESSIONS_APPROVED_2026_10_29.md), [metadata đã duyệt](LAM_THIEN_FIVE_EXPRESSIONS_APPROVED_2026_10_29.json). Preview được giữ nguyên SHA `ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7` và đã lưu trong **Approved References**. CANON BODY V2 giữ nguyên.

---

# Thanh Vân Ký — Lâm Thiển: chuẩn hóa 5 biểu cảm (review 2026-10-29)

**Trạng thái:** ĐẶC TẢ ĐỀ XUẤT + ẢNH PREVIEW ĐÃ TẠO / **CHỜ NGƯỜI DÙNG DUYỆT**. Chưa phải sprite face đã tách lớp, animation Spine hay APK.

## Phạm vi

Người dùng yêu cầu làm **rõ cả 5 biểu cảm**, không chỉ “Ngại ngùng” và “Quyến rũ”:

1. **Ngại ngùng** (`shy`)
2. **Tức giận** (`angry`)
3. **Đau đớn** (`pain`)
4. **Xấu hổ** (`embarrassed`)
5. **Quyến rũ** (`alluring`)

Đây là 5 biểu cảm được nâng độ nhận diện, **không thay thế** các expression khác đã có trong game như bình thường, dịu dàng, mỉm cười, ngạc nhiên, mệt.

## Nguồn hình ảnh và thứ tự ưu tiên

- **CANON BODY/FACE/TRANG PHỤC V2 ĐÃ CHỐT:** `LT_CANON_BODY_REF_2026-10-28_V2`, [ảnh gốc V2 trên Google Drive](https://drive.google.com/file/d/1mEsyn2wMo-MVQqhtbmdUiFfO8AaYhzUR/view?usp=drivesdk), SHA256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711`. Giữ nhận diện tóc bạc, mặt, tỷ lệ hình thể V2 và trang phục trắng–xanh–vàng. +17% đã nằm trong V2, không cộng lần nữa.
- **ẢNH PREVIEW MỚI — CHỜ DUYỆT:** `LAM_THIEN_5_EXPRESSIONS_PREVIEW_PENDING_20261029.png`; PNG RGB, **1536×1024**, SHA256 `ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7`. Sao lưu ChatGPT Library Development tại `/Thanh Van Ky/Development/Lam_Thien_Expression_5_20261029/LAM_THIEN_5_EXPRESSIONS_PREVIEW_PENDING_20261029.png`. **Không coi preview này tự động thay thế khuôn mặt/costume CANON V2.**
- Poster tự sinh có thể sai chi tiết chữ hoặc cách thể hiện một số họa tiết; chỉ dùng để **xem và duyệt sắc thái 5 nét mặt**, không dùng làm đo đạc xương/chiều cao/độ bền.
- Không nhầm các ảnh tạo mới với bộ face PNG alpha tách lớp. Chỉ đưa vào production sau khi người dùng phê duyệt preview và art được tái dựng đúng tạo hình canon.

## Bảng đặc tả phân biệt trực quan

| ID | Biểu cảm | Mắt / hướng nhìn | Lông mày | Miệng | Má / đầu / cử chỉ | Độ nhấn |
| --- | --- | --- | --- | --- | --- | --- |
| `shy` | Ngại ngùng | Nhìn lệch, tránh giao tiếp thoáng qua, vẫn mở mắt tương đối | Hơi nhíu/nâng vào giữa | Hé nhỏ hoặc mím rất nhẹ | Hồng nhạt, đầu hơi cúi, tay có thể giữ nhẹ trước cổ | Nhẹ-vừa |
| `angry` | Tức giận | Nhìn thẳng, mắt sắc, mí trên ép xuống | Nhíu rõ, hướng vào giữa | Mím mạnh hoặc hơi mở để phản đối | Ít đỏ má, đầu thẳng, cơ hàm căng | Mạnh, không lẫn ngại ngùng |
| `pain` | Đau đớn | Nheo/nhắm một phần, khó giữ ánh nhìn | Nhíu cong lên ở giữa | Hé mở hoặc nhăn vì nén đau | Đầu hơi gục/nghiêng, nét căng và có thể có nước mắt nhẹ | Mạnh-vừa, không nhầm tức giận |
| `embarrassed` | Xấu hổ | Tránh mắt rõ, có thể cụp mạnh hoặc nhắm bớt | Cong/chụm mềm | Mím nhẹ, hơi run | Má đỏ rõ, đầu cúi hơn `shy`, đưa tay gần mặt một cách tự nhiên | Mạnh hơn shy |
| `alluring` | Quyến rũ | Mí hạ nhẹ, nhìn thẳng hoặc liếc có chủ ý | Thả lỏng | Mỉm cười lệch khóe tinh tế | Má ửng rất nhẹ, đầu nghiêng mềm, ánh nhìn tự tin | Rõ nhưng tiết chế, không cần hở thêm trang phục |

### Quy tắc so sánh nhanh

- `shy` vs `embarrassed`: khác rõ **độ đỏ má**, **mức né ánh mắt** và **góc cúi đầu**. Không dùng cùng một mắt/miệng chỉ thay đỏ má.
- `angry` vs `pain`: tức giận có **mắt sắc/mày hạ**, đau đớn có **mắt co/nhăn và mày nhíu cong**; miệng và hướng đầu cũng phải khác.
- `alluring` vs `shy`: quyến rũ **chủ động giao tiếp bằng mắt**, nét mặt tự tin; ngại ngùng lảng tránh. Không diễn tả bằng thay outfit, thân hình hoặc pose gợi dục.
- Kiểm tra tất cả 5 ở **kích thước chân dung trong hộp thoại thật**; không chỉ dựa vào poster phóng to.

## Triển khai layer/Spine (sau khi duyệt)

1. Giữ lớp `face_base`, `hair_front`, `hair_back`, `eye_left/right`, `mouth` theo chuẩn CP320/CP321. Cho phép bổ sung slot `brow_left/right`, `eyelids`, `blush`, `tear_small` nếu thực tế rig cần.
2. Chuẩn bị từng trạng thái mắt, mày, miệng, má trong spritesheet/atlas alpha **thật**, với dấu mốc đồng nhất giữa Front và 3/4. Mọi nét mặt phải được đối chiếu với CANON V2, không đổi shape mặt hay vị trí phụ kiện khi đổi expression.
3. `expression` độc lập với `wardrobe`, `integrity`, `pose`, `action` theo `CharacterAppearanceState`. Chuyển expression không reset quần áo hoặc hư hại 100/70/50/30.
4. Các góc Side/Back tùy khả năng nhìn thấy mặt: điều khiển biểu cảm theo độ lộ gương mặt; không tự dựng một front face giả trên góc sau.
5. QA ở 5 expression × Front/3⁄4 × normal/dialogue/combat scene, xem cận mặt và hình thu nhỏ; thử chuyển trạng thái không giật/méo mesh.
6. **Gate trạng thái**: preview mới = `pending_user_approval`; thực tế layer/animation/APK = `pending_production`. Chỉ tick DONE khi có file, QA và duyệt riêng.

## Tiếp tục

Chờ người dùng xem preview 5 biểu cảm. Sau khi được chốt, lưu ảnh vào khu Approved References, cập nhật registry expression và triển khai sprite tách lớp đúng CANON V2. Trong khi chờ, phần P0-02/P0-03 xây dựng fullbody/layer và CP323 QA tiếp tục giữ đúng trạng thái còn thiếu.
