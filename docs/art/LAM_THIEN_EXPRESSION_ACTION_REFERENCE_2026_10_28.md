# Thanh Vân Ký — Lâm Thiển: biểu cảm, hành động, pose và roadmap (bản tham khảo được người dùng xác nhận)

**Ngày:** 2026-10-28. **Nguồn:** 2 ảnh PNG người dùng đính kèm trực tiếp trong hội thoại để thay thế liên kết blob không thể tải ở phiên trước. **Trạng thái:** VISUAL REFERENCE SAVED + USER APPROVED DIRECTION; chưa phải sprite/animation/rig/APK hoàn chỉnh.

## Ảnh nguyên bản được lưu và kiểm chứng

| Nội dung | Ảnh đã lưu | SHA-256 |
| --- | --- | --- |
| Biểu cảm, hành động, các tư thế trong phòng, thay trang phục và trạng thái hư hại | [TVK_LamThien_Expression_Action_Pose_Outfit_Approved_20261028.png](https://drive.google.com/file/d/1M-6KIEeon7HX4Qn56UlhGMfV76Lr-sN5/view?usp=drivesdk) | `96caa07b59abd998f905dc19da732a3ebe455ab50863d934865da9a4eace94b2` |
| Lộ trình art / layer / rig / gameplay | [TVK_LamThien_Production_Roadmap_Approved_20261028.png](https://drive.google.com/file/d/1ZgMB8nkRlkar3-MYCrH32uQaYxO29S5Q/view?usp=drivesdk) | `380d21c2b8f6e862ce7b7a9f4b751e8625716a9c02b06b3bb672e4d0dc49b31a` |

**Kích thước:** cả hai ảnh 1672×941 PNG RGBA. **Bản sao:** `/Thanh Van Ky/Approved References/Interaction_And_Roadmap_20261028/` trong ChatGPT Library và `Thanh Van Ky - Approved References/Interaction_And_Roadmap_20261028/` trên Google Drive.

**Mẫu ngoại hình gốc riêng biệt (canon base):** [TVK_LamThien_Approved_Reference_20261028.png](https://drive.google.com/file/d/10jKNq-VL62sv1gez5PHlVT9QKyJp_Cvd/view?usp=drivesdk). Hai ảnh mới **không thay thế hình thể/face/hair của ảnh gốc đã chốt**; chúng bổ sung biểu cảm/pose/trang phục/roadmap.

## Những quy tắc phải thực hiện

1. **Biểu cảm linh hoạt theo bối cảnh:** thường, dịu dàng, cười, ngạc nhiên, khó xử, mệt; khi chiến đấu có nhận đòn, giữ thăng bằng, chỉnh trang phục; khi trong phòng có cử chỉ thư giãn. Không dùng một mặt cho mọi state.
2. **Tư thế trong phòng:** nằm giường, quỳ giường ngoảnh lại, ngồi mép giường, ngồi ghế, dựa tường. `bed_recline` theo đặc tả riêng vẫn là nằm ngửa nghỉ ngơi, `bed_kneel_forward` là quỳ/ngoảnh lại. Pose bị vẽ khác trong bảng minh họa không tự thay quyết định cũ.
3. **Mức nguyên vẹn 100/70/50/30:** áp dụng lên tất cả các nhóm quần áo; cấp 30% vẫn có dấu rách/sờn ngay trên những mảnh còn che phủ; các vùng cần che vẫn kín đáo. Không áp dụng tăng lượng rách mặc định +20% (đề xuất cũ đã bị thay thế). Sự lựa chọn mới ưu tiên lượng rách vừa phải, tự nhiên.
4. **Trục wardrobe độc lập damage:** outfit đầy đủ → tháo lớp áo ngoài → biến thể trang phục riêng tư cuối. Ảnh poster là reference định hướng, không chứng minh asset từng lớp hiện đã có; lớp voan có thể xuyên sáng nhưng lớp lót tại vùng cần che không xuyên thấu.
5. **QUY TẮC QUAN TRỌNG — MỨC CỞI CUỐI THEO MỌI TƯ THẾ:** nếu người chơi đang chọn biến thể trang phục riêng tư cuối (`private_fantasy`, tên ID đề xuất), chuyển pose Front/Back/Side/3/4/quỳ/nằm/ngồi/dựa tường hoặc cảnh tương tác **không được reset sang outer_removed/default**. Chọn costume state theo nhân vật (không theo pose), lấy đúng ảnh riêng cho tổ hợp costume×pose; nếp vải/ribbon/hair/biểu cảm thay đổi tự nhiên nhưng trạng thái mặc đồ không đổi.
6. **Nếu thiếu ảnh `private_fantasy × pose`:** giữ nguyên outfit ID đã lưu và **hiển thị thông báo asset thiếu**, không tự fallback sang hình nhân vật mặc đầy đủ, cũng không giả mạo từ ảnh khác; tương tác phụ thuộc hotspot của ảnh thật bị vô hiệu.
7. **Độ hư hại không reset qua pose/cảnh:** 100/70/50/30 lưu riêng với wardrobe; khi chuyển góc, vị trí rách bám cấu trúc vải, biểu hiện khác do trọng lực nhưng không sinh hư hại mới.

## Ma trận tối thiểu để nghiệm thu

| Nhóm cảnh | Outfit mặc đủ | Tháo áo ngoài | Mức cuối | Hư hại 70/50/30 |
| --- | --- | --- | --- | --- |
| Front / Back / Side / 3/4 | cùng base, đúng góc | phải có image riêng | **giữ state, image riêng** | đúng các vị trí rách |
| Quỳ/nằm/ngồi trên giường | image riêng đúng pose | image riêng | **giữ state, image riêng** | trạng thái giữ liên tục |
| Ngồi ghế / dựa tường | image riêng đúng bối cảnh | image riêng | **giữ state, image riêng** | trạng thái giữ liên tục |
| Chuyển battle → tương tác | giữ outfit | không reset | **không tự mặc lại** | không tự phục hồi khi hồi HP |

**Lưu ý:** Ma trận là yêu cầu phải làm, **không phải chứng nhận đã có đầy đủ asset**. Poster AI có thể chứa chiều cao, số đo, ngày sinh, thông tin minh họa và layer mẫu; không đưa thành canon lore hay nhận là rig thật nếu chưa được duyệt/xác minh riêng.

## Ưu tiên việc tiếp theo

- **P0:** xác nhận nguồn ảnh, đồng bộ pose và ma trận biểu cảm/hành động; tạo file layer sạch từ tạo hình gốc được chốt.
- **P1:** dựng biến thể trang phục và texture theo mức hư hại 100/70/50/30 ở từng pose; kiểm tra skin coverage, alpha, vị trí seam.
- **P2:** rig + chuyển động thật; tích hợp logic giữ wardrobe/damage khi đổi pose; thử APK thực tế trên thiết bị.

**Đã lưu:** ảnh PNG nguyên bản và metadata. **Chưa hoàn thành:** layer, trang phục theo từng pose, rig, hoạt ảnh thực và xác nhận build APK.
