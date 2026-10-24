# Chương I — Sương trên Thanh Vân Sơn

**Trạng thái hiện tại (kiểm tra 2026-10-24):** Đã có **bản luồng Chương I trên APK Android** gồm bản đồ, 6 đoạn đối thoại, hai lựa chọn và lưu cờ trong SharedPreferences. **Chưa hoàn thành/kiểm thử đầy đủ** phần nhiệm vụ hậu lựa chọn, hoạt ảnh và giao diện theo bản thiết kế.

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


## Đối chiếu với source và trạng thái nghiệm thu (2026-10-24)

**Đã có trong repository:** `MainActivity.kt` chứa bản đồ → hội thoại Chương I → hai lựa chọn Rừng Trúc / Thanh Vân Tông, ghi `complete`, `choice` qua `tvk_chapter_1`. `CharacterInteractionActivity.kt` có danh sách Tô Nguyệt Ly/Lâm Thiển, bốn tư thế cơ bản (đứng trước, đứng sau, quỳ trên giường, nằm ngửa trên giường), ảnh từng tư thế và bản thử phản ứng chạm. `TVKCharacterMotionView.kt` vẽ biến dạng PNG để tạo nhịp thở/tóc/tác động nhẹ.

**Đã xác minh build:** GitHub Actions [#40062868665](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/40062868665) hoàn thành **success**, artifact `thanh-van-ky-debug-apk`. Đây là xác nhận **biên dịch**, không xác nhận đã chạy/tối ưu trên Xiaomi.

**Các tiêu chí vẫn chưa đạt:** hình và giao diện nền bản đồ/hội thoại đúng chuẩn mỹ thuật; nội dung nhiệm vụ tiếp diễn sau hai lựa chọn; NPC phản ứng theo cờ ở lần gặp lại; hoạt ảnh biểu cảm phân lớp và cặp đôi (nắm tay/ôm/hôn); cởi đồ bằng tài nguyên hiển thị đủ theo từng pose; hiệu chỉnh tọa độ chạm sau khi chốt sprite; màn nhân vật/túi đồ/vũ khí; hệ thống chiến đấu tối đa 4 thành viên với HP từng người, và ba ngưỡng rách đồ 2D theo sát thương. Chưa có thử nghiệm APK thực tế trên điện thoại.

**Nguồn kiểm kê chi tiết, chuẩn để theo dõi tiếp:** [PROJECT_SPEC.md — mục 16](PROJECT_SPEC.md#16-kiểm-kê-nghiệm-thu-chương-i-tư-thế-và-tương-tác--2026-10-24).

**Lịch sử thay đổi 2026-10-24:** Cập nhật trạng thái từ "chưa tích hợp APK" sang "đã có luồng demo đã build"; vẫn giữ các mục kiểm thử/chất lượng chưa xong, không đóng Chương I.
