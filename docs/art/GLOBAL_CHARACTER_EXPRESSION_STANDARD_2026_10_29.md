# Thanh Vân Ký — Quy chuẩn biểu cảm nhân vật chính (2026-10-29)

**TRẠNG THÁI: ĐÃ CHỐT QUY TẮC ÁP DỤNG CHUNG** theo xác nhận người dùng khi duyệt bộ 5 biểu cảm Lâm Thiển; **không phải đã chốt hình riêng hoặc đã vẽ 5 biểu cảm cho mỗi nhân vật khác**.

## Năm cảm xúc cơ sở cho nhân vật chính trưởng thành phù hợp

| ID ổn định | Cảm xúc | Dấu hiệu bắt buộc phải nhận ra |
|---|---|---|
| `shy` | Ngại ngùng | Né ánh mắt nhẹ, mày mềm, má hồng nhẹ |
| `angry` | Tức giận | Mắt sắc, mày ép/nhíu, miệng căng |
| `pain` | Đau đớn | Mắt co/khép, mày cong nhăn, biểu hiện nén đau |
| `embarrassed` | Xấu hổ | Né ánh mắt mạnh và cúi đầu hơn shy, má đỏ rõ |
| `alluring` | Quyến rũ | Ánh nhìn chủ động, mí hạ nhẹ, cười tinh tế/tự tin |

Đây là **khung phân biệt cảm xúc**, không phải khuôn mặt dùng chung. Các biểu cảm bình thường, cười, ngạc nhiên, mệt, v.v. vẫn giữ theo thiết kế riêng của nhân vật. Với nhân vật không phù hợp bối cảnh tình cảm hoặc chưa trưởng thành, không áp biểu cảm `alluring`; không áp những nội dung nhạy cảm lên nhân vật chưa trưởng thành.

## Tùy biến riêng từng nhân vật

1. **Đọc canon riêng** của từng nhân vật trước khi vẽ; không copy khuôn mặt, cấu trúc mắt, tóc, trang phục, vóc dáng hoặc tỷ lệ +17% từ Lâm Thiển.
2. **Giữ 5 cảm xúc dễ phân biệt**, nhưng tùy biến nét mày/mí/môi, mức đỏ má, góc đầu, mức cường điệu và cử chỉ theo tính cách/tình huống của từng nhân vật. Có thể khác rõ giữa Tô Nguyệt Ly và Lâm Thiển.
3. **Không dùng cùng sprite cho hai nhân vật**; mỗi nhân vật cần phiên bản biểu cảm của chính mình.
4. **Preview riêng từng nhân vật** theo 5 trạng thái trước khi sản xuất layer/rig. Duyệt biểu cảm không tự thay model chính thức.
5. Kiểm tra cả chân dung thoại kích thước nhỏ và cận mặt, theo các góc nhìn khả dụng. `shy` không được chỉ đổi blush thành `embarrassed`; `angry` phải khác `pain`; `alluring` phải khác `shy`.
6. **Runtime:** `expression` theo `characterId` độc lập với `wardrobe`, `integrity`, `pose`, `action`. Không tự reset các state khác; không hiển thị nhầm hình khuôn mặt nhân vật này cho nhân vật khác.
7. **Phân biệt trạng thái:** chính sách chung **APPROVED**, preview năm nét mặt Lâm Thiển **APPROVED**, biểu cảm/tư liệu từng nhân vật khác **PENDING INDIVIDUAL PREVIEW**, sprite/rig/animation/APK **PENDING** đến khi có kiểm chứng thật.

## Tài liệu nguồn

- [Mẫu 5 biểu cảm Lâm Thiển đã duyệt](LAM_THIEN_FIVE_EXPRESSIONS_APPROVED_2026_10_29.md).
- [Global character appearance](GLOBAL_CHARACTER_APPEARANCE_SPEC.md).
- [Project spec](../PROJECT_SPEC.md) — quy tắc toàn game.

**Dành cho các phiên sau:** Không tự áp nguyên một mẫu face biểu cảm từ Lâm Thiển cho người khác. Chỉ chia sẻ *cấu trúc 5 cảm xúc, cách phân biệt và quy trình review*, kết hợp với model canon và tính cách của nhân vật đó.
