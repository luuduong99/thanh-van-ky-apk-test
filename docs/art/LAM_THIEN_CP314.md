# Lâm Thiển — CP314 | Back view / art handoff

Ngày: 2026-10-28. Trạng thái: ĐANG THỰC HIỆN, chưa là asset Spine đã nghiệm thu.

## Quy chuẩn đã chốt
- Giữ Lâm Thiển theo mẫu gốc, tóc bạc, trang phục trắng–xanh–vàng, tư thế đã duyệt.
- Giữ mốc **+17%**. Chỉ tinh chỉnh nhẹ chiều cao / tỷ lệ tổng thể để cân đối, tránh thấp/lùn; gửi preview trước khi cập nhật model chính thức.
- Quy trình này áp dụng cho nhân vật sau, nhưng không đồng nhất hình dáng/nhận diện giữa nhân vật.

## Chuyển giao CP312–313
- CP312: ORA 8 lớp, 0px thay đổi composite đứng yên theo báo cáo trước; mép tô lót gáy–vai còn lộ.
- CP313: ORA 10 lớp; di chuyển 365 pixel gán nhầm da sang lớp chân tóc, bổ sung nét trang sức xanh–vàng; 4 test PASS, không ghi nhận alpha hole mới khi dịch ±5px (số liệu từ báo cáo phiên trước, cần xác minh lại khi có ORA).
- Chưa hoàn tất ranh giới tóc/scalp–gáy–da vai và hai tay áo. Chưa nghiệm thu Spine/physics.

## CP314 làm tiếp
1. Tóc/scalp/gáy: đúng chồng lớp, loại vùng da gán sai, giữ đường viền tóc và silhouette.
2. Da vai: khử mép tô lót giả, khôi phục vùng bị tóc che, không để thủng alpha.
3. Dây trang sức/cổ áo xanh–vàng: đúng lớp, không đè tóc.
4. Hai tay áo: làm sau khi xử lý xong vùng gáy/vai, kiểm tra draw order và mép kín.
5. Kiểm thử: so ảnh trước/sau, từng lớp riêng, composite tĩnh không lệch ngoài phạm vi sửa; thử dịch tóc ±5px, xuất ảnh so sánh và yêu cầu duyệt.

## Nguồn
- [Ảnh Back tham chiếu Drive](https://drive.google.com/file/d/148KmIDibZZTxUikYCU0LbSScGN5cewox/view?usp=drivesdk) (PNG phẳng, RGB 207×656).
- [Sheet nhân vật Drive](https://drive.google.com/file/d/1FllTp2v-SEVn54vP7_olDOCbNfPplXvx/view?usp=drivesdk).
- Preview khoanh vùng CP314: TVK_CP314_LamThien_Back_SeamReview.png trong cuộc trò chuyện này.
- Cần bản **CP313 ORA 10 lớp** để chỉnh trực tiếp. Không thấy bản này trong Drive/GitHub hiện có; ảnh PNG phẳng không tái tạo trung thực các lớp.

**Điểm tiếp tục:** CP314 tóc/scalp–gáy–vai → tay áo → so sánh composite/alpha → preview duyệt. Không tự đánh dấu hoàn tất.
