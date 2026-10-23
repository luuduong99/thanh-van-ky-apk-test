# Chương I — Sương trên Thanh Vân Sơn

**Trạng thái:** Kịch bản triển khai gameplay (bản đầu, chưa tích hợp APK).

## Luồng chơi
Bản đồ Thanh Vân Sơn → chạm "Bắt đầu chương I" → cảnh sân Thanh Vân Tông → đối thoại với Tô Nguyệt Ly → lựa chọn → cập nhật cờ truyện → quay lại bản đồ.

## Hội thoại
1. **Dẫn truyện:** Sương sớm phủ trên lối đá. Sau nhiều ngày xa tông môn, nam chính trở về dưới tiếng chuông ngân.
2. **Tô Nguyệt Ly:** "Huynh về rồi! Muội đã đợi từ sáng. Chuyến đi có thuận lợi không?"
3. **Nam chính:** "Có chút trắc trở, nhưng thấy muội bình an là tốt rồi."
4. **Tô Nguyệt Ly:** "Đêm qua linh khí ở Rừng Trúc biến động. Muội lo có chuyện chẳng lành."
5. **Dẫn truyện:** Một cơn gió lạnh lướt qua mái hiên, mang theo mùi trúc ẩm.
6. **Tô Nguyệt Ly:** "Chúng ta nên làm gì trước khi trời tối?"

## Lựa chọn có hậu quả
- **A — Cùng Nguyệt Ly đến Rừng Trúc:** đặt `chapter1_choice=forest`, mở mục tiêu "Điều tra Rừng Trúc"; Nguyệt Ly đi cùng.
- **B — Trở về đại điện chuẩn bị:** đặt `chapter1_choice=sect`, mở mục tiêu "Hỏi chấp sự về dị tượng"; Nguyệt Ly đi cùng.

Cả hai đặt `chapter1_complete=true`. Lần sau quay lại Nguyệt Ly sẽ nhắc lựa chọn trước đó. Chưa quy định điểm thiện cảm để tránh tự chốt ngưỡng quan hệ.

## Tiêu chí tích hợp APK
- Dùng đúng asset `characters/heroines_reference.png` (vùng trái) và `characters/main_portrait.png`.
- Hộp thoại tiếng Việt, gõ chữ nhanh vừa; chạm lần một hiện hết câu, chạm tiếp mới qua câu khác.
- Hai lựa chọn là nút bấm riêng, không bỏ qua khi chạm liên tiếp.
- Lưu lựa chọn bằng SharedPreferences hoặc hệ lưu tương đương; mở lại ứng dụng vẫn giữ cờ.
- Không tự tuyên bố có rig phân lớp, biểu cảm riêng hoặc tư thế ôm/hôn khi chưa có asset.
- Build GitHub Actions và kiểm tra APK thật trước khi đánh dấu hoàn thành.

## Việc tiếp theo
Tích hợp màn chương I vào MainActivity Kotlin hiện có; sau đó mở rộng scene, biểu cảm, UI và chiến đấu theo PROJECT_SPEC.md.
