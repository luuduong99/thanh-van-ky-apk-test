# Lâm Thiển — preview bốn mức hư hại được duyệt (2026-10-28)

**Trạng thái: ĐÃ CHỐT THIẾT KẾ / CHƯA HOÀN TẤT ASSET VÀ RIG.**

Người dùng đã xác nhận preview bốn cột 100%–70%–50%–30% trong cuộc trò chuyện ngày 2026-10-28: “tôi rất ưng nha. chốt như này cho tôi. Cập nhật vào tài liệu để thực hiện”.

## Nguồn preview được duyệt
- Tệp PNG kết xuất trong cuộc trò chuyện: `a_wide_infographic_character_sheet_style_image_sho.png`.
- Kích thước: **1672 × 941**, RGB.
- SHA-256: `03251b5ec9b020b325687b530c98e026622ba7b3334466ab5d2323a0a89c9e23`.
- **Quan trọng:** Đây là tệp ảnh trong cuộc trò chuyện, **chưa xác minh đã có trên Drive/GitHub**. Trước khi production cần lưu bản PNG gốc vào kho asset bền vững và đối chiếu SHA-256; không coi đường dẫn cục bộ là URL lâu dài.

## Bảng mức độ nguyên vẹn — CHỐT

| Integrity | Visual damage |
|---|---|
| **100%** | Sạch sẽ, trang phục nguyên vẹn |
| **70%** | Bụi bẩn nhẹ, vài vết xước, vết rách rất nhỏ |
| **50%** | Bẩn rõ hơn, vải sờn, một số đường rách có thể nhận ra |
| **30%** | Bẩn/xước/rách nhiều; **cả những mảnh vải còn che phủ cũng phải sờn/rách**, đồng thời giữ che phủ phù hợp |

Preview là **chuẩn hướng nghệ thuật và mức độ tương quan**, không phải texture pixel-perfect/sprite đã rig. Không tự tăng rách theo % cố định, không hiểu integrity là phần trăm lộ da, không phát sinh nội dung hở vùng nhạy cảm.

## Quy tắc vận hành (áp dụng toàn bộ nhân vật)

- Giữ nguyên tạo hình canon riêng của từng nhân vật; với Lâm Thiển phải theo `LT_CANON_BODY_REF_2026-10-28_V2`. Không chuyển tỷ lệ cơ thể của Lâm Thiển sang nhân vật khác.
- Trạng thái `wardrobe_state` (đồ mặc/chọn) **độc lập** với `clothing_integrity` (100/70/50/30). Không reset khi đổi pose, góc nhìn Front/Back/Side/3/4 hoặc chuyển chiến đấu ↔ hội thoại ↔ màn nhân vật.
- Vết hư hại phải gắn với **cùng bộ phận vải** giữa các góc nhìn, không tự biến mất/đổi chỗ vô lý. Hồi HP không tự sửa/giặt quần áo.
- Phân bố bẩn/xước/rách linh hoạt theo chất liệu và tác động, nhưng cường độ tổng thể khớp một trong bốn cấp độ đã duyệt.
- Khi lần đầu giảm xuống ngưỡng mới trong chiến đấu, hiển thị artwork 2D phù hợp; các lần sau tiếp tục trạng thái đã lưu.
- Không có asset phù hợp thì báo thiếu, không tráo ảnh mức 100% để giả làm mức 30%.

## Kế hoạch triển khai / tiêu chí nghiệm thu

1. **Lưu nguồn:** đưa chính PNG đã duyệt vào Drive hoặc repo asset; ghi URL và kiểm SHA.
2. **Art:** tạo biến thể 100/70/50/30 từ model canon V2, từng phần áo/vạt/tay áo/vải phủ, mỗi góc nhìn và pose cần hỗ trợ. Dùng preview làm chuẩn so sánh chứ không dùng ảnh crop/flip để giả asset đã hoàn thiện.
3. **Rig:** tách lớp dưới/ngoài, lót che phủ và vùng vải hư hại; kiểm alpha, seam, draw order, biến dạng pose; kiểm thử Spine/animation thực.
4. **Gameplay:** mapping state riêng từng nhân vật, hiệu ứng 2D lần đầu chạm mốc, lưu và phục hồi state khi chuyển màn; kiểm thủ công cùng test tự động.
5. **QA/APK:** chụp ảnh ở 4 mức × các tư thế/góc được hỗ trợ, kiểm giao diện chiến đấu/hội thoại/nhân vật; chỉ ghi DONE khi có asset, test và APK thực tế.

**Tình trạng tại thời điểm chốt:** thiết kế/preview **APPROVED**; sprite nhiều mức, rig, animation, tích hợp APK **PENDING**, chưa nghiệm thu.

Tham chiếu: `docs/PROJECT_SPEC.md` §25–26, `docs/art/GLOBAL_CLOTHING_DAMAGE_VISUAL_STANDARD.md`, `docs/art/GLOBAL_CHARACTER_APPEARANCE_SPEC.md`, `docs/art/LAM_THIEN_NEXT_TASKS_AFTER_CANON_V2.md`.
