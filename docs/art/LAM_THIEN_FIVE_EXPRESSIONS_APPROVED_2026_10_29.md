# Thanh Vân Ký — Lâm Thiển | 5 BIỂU CẢM CHÍNH THỨC (đã duyệt 2026-10-29)

**TRẠNG THÁI: ĐÃ CHỐT MẪU BIỂU CẢM / CHƯA HOÀN TẤT FACE SPRITES, SPINE HOẶC APK.**

**Bằng chứng duyệt:** người dùng xác nhận ngay sau khi xem bảng preview năm biểu cảm: “tôi thích như này, chốt biểu cảm này nha. Note vào cho tôi để tránh bị quên và làm sai hoặc nhầm khi hoàn thiện nhân vật. Các nhân vật khác cũng nên như này nhưng tinh chỉnh lại xíu cho các nhân vật khác”.

## 1. Ảnh mẫu BẮT BUỘC đối chiếu

- **Mẫu 5 biểu cảm đã chốt:** `TVK_LamThien_5_Expressions_APPROVED_20261029.png`.
- **SHA-256 chính xác:** `ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7`; 1536×1024 px; PNG RGB; file concept phẳng, **không phải sprite đã rig**.
- **Bản sao lưu đã xác nhận:** ChatGPT Library `/Thanh Van Ky/Approved References/Lam_Thien_Expressions_20261029/TVK_LamThien_5_Expressions_APPROVED_20261029.png`.
- **Tạo hình canon cơ thể/khuôn mặt/trang phục KHÔNG ĐỔI:** `LT_CANON_BODY_REF_2026-10-28_V2`, [ảnh V2 chính thức](https://drive.google.com/file/d/1mEsyn2wMo-MVQqhtbmdUiFfO8AaYhzUR/view?usp=drivesdk), SHA-256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711`.
- **Thứ tự ưu tiên:** CANON V2 quyết định *danh tính, khuôn mặt, tỷ lệ, tóc và trang phục*; ảnh biểu cảm mới quyết định *cách diễn đạt năm cảm xúc*. Nếu chi tiết tạo hình trên poster biểu cảm khác CANON V2, giữ V2 và điều chỉnh **nét mặt**, không thay model chính thức.
- **+17% đã nằm trong CANON V2**; không cộng lại hay sao chép sang nhân vật khác.
- **Không** chuyển ảnh concept thành sprite/pose khác bằng crop/flip rồi tuyên bố đã hoàn thành art.

## 2. Năm biểu cảm ĐÃ CHỐT

| Emotion ID | Tên | Mắt/hướng nhìn | Lông mày | Miệng | Má và đầu | Phân biệt bắt buộc |
|---|---|---|---|---|---|---|
| `shy` | **Ngại ngùng** | Nhìn lệch, tránh mắt thoáng qua | Nâng/chụm nhẹ | Hé nhỏ hoặc mím kín đáo | Má hồng nhẹ, đầu cúi nhẹ | Vẫn mở mắt, dịu hơn `embarrassed` |
| `angry` | **Tức giận** | Nhìn thẳng sắc và căng | Ép/nhíu rõ vào giữa | Mím mạnh hoặc mở nhỏ phản đối | Giữ đầu thẳng, ít ửng má | Sắc, có lực đối kháng; không giống đau |
| `pain` | **Đau đớn** | Nheo/khép một phần, mắt co lại | Nhíu cong căng ở giữa | Hé mở khi nén đau | Đầu hơi gục, nét căng, nước mắt rất nhẹ nếu hợp cảnh | Co rút do đau, khác `angry` |
| `embarrassed` | **Xấu hổ** | Né ánh nhìn rõ hơn `shy`, cúi mắt | Cong mềm/chụm nhẹ | Mím nhỏ, có thể hơi run | Má đỏ rõ, đầu cúi nhiều hơn, tay gần mặt | Phải khác `shy` ở **mắt + má + đầu**, không chỉ tăng sắc đỏ |
| `alluring` | **Quyến rũ** | Mí hạ nhẹ, nhìn trực diện/liếc chủ động | Thư giãn | Cười mỉm tinh tế, khóe môi hơi lệch | Hồng rất nhẹ, đầu nghiêng mềm | Tự tin, có chủ ý, không phải ngại ngùng |

**Cả 5 biểu cảm đều được chốt đồng thời.** Không được cắt giảm xuống 2 loại, không dùng cùng một mắt/miệng rồi thay riêng màu má. Những biểu cảm cũ như bình thường, dịu dàng, mỉm cười, ngạc nhiên, mệt vẫn tồn tại; đây là nhóm **được làm rõ bổ sung**, không xóa các state khác.

## 3. Quy tắc không được nhầm trong sản xuất

1. Đọc **ảnh biểu cảm được duyệt + CANON BODY V2** cùng lúc. Mẫu biểu cảm quyết định cường độ cảm xúc; body V2 quyết định tạo hình.
2. Đánh giá năm nét mặt riêng biệt **ở kích thước chân dung hội thoại trong APK**, không chỉ ở ảnh phóng to. Kiểm tra đủ mí mắt, chân mày, miệng, mức ửng má, góc đầu.
3. Cho phép các slot `brow_left/right`, `eyelids`, `blush`, `tear_small` cùng `face_base`, `eye_left/right`, `mouth`, `hair_front/back`. Slot bổ sung là yêu cầu kỹ thuật dự kiến, **chưa xác nhận đã tách thật**.
4. Biểu cảm tách khỏi `wardrobe`, `integrity`, `pose`, `action`; chuyển cảm xúc không làm reset trang phục, hình thể, mức rách 100/70/50/30 hoặc cảnh.
5. Khi đổi góc Front/3⁄4/Side, giữ đúng tinh thần biểu cảm và nhận diện riêng, không ép mặt Front vào góc Back. Kiểm tra blink/transition tránh méo khuôn mặt.
6. **Trạng thái nghiệm thu:** preview 5 biểu cảm **APPROVED**; asset alpha, rig, animation, tích hợp UI và APK **NOT DONE**. Chỉ tick DONE khi có ảnh thật, kiểm chứng và QA.

## 4. Áp dụng nhân vật khác

Áp dụng **cùng bộ 5 sắc thái phân biệt rõ** và cùng tiêu chí kiểm tra cho các **nhân vật chính trưởng thành phù hợp bối cảnh** (bao gồm Tô Nguyệt Ly), nhưng **không sao chép trực tiếp mặt, ánh mắt, màu đỏ má, tỷ lệ cơ thể hoặc phong thái của Lâm Thiển**.

- Giữ đúng face/body canon, tính cách và cách nói của mỗi nhân vật.
- Tinh chỉnh cường độ theo cá tính: người điềm tĩnh tức giận kiềm chế hơn; người hoạt bát có biểu cảm xấu hổ rõ hơn; người tự tin thể hiện quyến rũ thiên về ánh nhìn/nụ cười của chính họ.
- Có bảng preview 5 biểu cảm riêng từng nhân vật, người dùng duyệt trước khi gắn vào game.
- Không áp biểu cảm lãng mạn/quyến rũ vào nhân vật chưa trưởng thành hoặc bối cảnh không phù hợp.
- Chuẩn dùng toàn game: [GLOBAL_CHARACTER_EXPRESSION_STANDARD_2026_10_29.md](GLOBAL_CHARACTER_EXPRESSION_STANDARD_2026_10_29.md).

## 5. Tài liệu và triển khai

- [Metadata 5 biểu cảm đã duyệt](LAM_THIEN_FIVE_EXPRESSIONS_APPROVED_2026_10_29.json).
- [Đặc tả review lịch sử (đã được duyệt, không còn pending)](LAM_THIEN_FIVE_EXPRESSIONS_REVIEW_2026_10_29.md).
- `LAM_THIEN_DESIGN_REGISTRY.json` quản lý approved expression profile **độc lập** với approved body design.
- Thuộc **P1-03 / face-expression art/rig**; ưu tiên tiếp tục P0 full-body/layer trước, không tự đánh dấu P1-03 hoàn tất.


## Tiến độ thực hiện CP324 (2026-10-29)

Phần **kết nối runtime state/UX** đã được triển khai thử trong Android: bộ chọn `shy / angry / pain / embarrassed / alluring`, nút reset `normal`, lưu theo nhân vật, không reset expression khi đổi pose/mở wardrobe; thiếu sprite giữ trạng thái nhưng không dùng nhầm ảnh nền. Danh sách asset ở `app/src/main/assets/character_expression_profiles.json` **chưa có sprite_paths** vì art face alpha thật chưa được tạo. Có 10 crop từ preview đã chốt làm handoff **REFERENCE ONLY**; không coi crop là sprite.

Xem [LAM_THIEN_CP324_EXPRESSION_RUNTIME_HANDOFF.md](LAM_THIEN_CP324_EXPRESSION_RUNTIME_HANDOFF.md). **Không có thay đổi quyết định duyệt 5 nét mặt hoặc CANON V2; animation/Spine/APK vẫn chờ.**
