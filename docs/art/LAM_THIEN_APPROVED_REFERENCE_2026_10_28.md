# Lâm Thiển — bảng thiết kế đã chốt (CANON ART REFERENCE)

**Ngày chốt:** 2026-10-28  
**Trạng thái:** **APPROVED VISUAL REFERENCE** (đã được người dùng xác nhận bằng câu “ok chốt như này nha”).  
**Không phải:** asset Spine/ORA đã tách lớp, rig, animation hoặc APK đã tích hợp.

## Mở nguyên ảnh gốc

**[ẢNH CHÍNH THỨC — TVK_LamThien_Approved_Reference_20261028.png](https://drive.google.com/file/d/10jKNq-VL62sv1gez5PHlVT9QKyJp_Cvd/view?usp=drivesdk)**

- Google Drive: thư mục **Thanh Van Ky - Approved References**; ảnh gốc ở chế độ riêng tư, không đổi quyền chia sẻ.
- ChatGPT Library dự phòng: `/Thanh Van Ky/Approved References/TVK_LamThien_Approved_Reference_20261028.png`.
- Kích thước: **1672 × 941 px**; PNG RGB; dung lượng **2,761,199 bytes**.
- SHA-256: `4b6cbf29ee8aef6aa2d927e7bb89428a9fda5bca1bb67a3f1c7b08e3a94129fd`. Dùng hash để xác minh đúng file đã được duyệt, không vô tình lấy ảnh CP317–CP319 hoặc ảnh khác có cùng tên.

## Nội dung đã duyệt cho Lâm Thiển

1. Đúng nhân vật **Lâm Thiển** trưởng thành: mái tóc bạc dài, hoa và phụ kiện tóc, biểu cảm anime mềm mại; giữ nhận diện đặc trưng.
2. Trang phục tiên hiệp fantasy **trắng – xanh nhạt – vàng**, tông thanh nhã; **giảm mật độ dây/xích/trang sức vàng**, chỉ dùng vừa đủ để tạo điểm nhấn.
3. Giữ **tỷ lệ hình thể trong chính bảng ảnh đã chốt** làm mốc trực quan; thân trên đầy đặn, eo/hông tự nhiên và nhất quán giữa Front, Side, Front 3/4, Back, Back Turn, Back 3/4. Không tự tăng/giảm các bộ phận khi thay góc quay hoặc đổi pose.
4. Phần hông trang phục khoét cân đối và đường nét mặt sau đúng mẫu đã duyệt; không hồi quy về các ảnh Back/CP317 proxy cũ.
5. Giữ chiều cao tổng thể thanh thoát; quy chuẩn +17% là **mốc điều chỉnh riêng của Lâm Thiển đã chốt trong các phiên trước**, không được tuyên bố ảnh này có sai lệch chính xác +17% bằng pixel nếu chưa có bản đo gốc.
6. Các tư thế trong phòng: **nằm trên giường**, **quỳ trên giường/ngoảnh lại**, **ngồi trên giường**, **ngồi trên ghế**, **dựa tường**. Mỗi tư thế phải dùng bối cảnh/đạo cụ trong phòng tương ứng; các biến thể phải giữ đúng thiết kế nhân vật. Lưu ý tách tư thế nằm ngửa nghỉ ngơi `bed_recline` khỏi tư thế quỳ và ngoảnh lại `bed_kneel_forward`, không dùng một pose thay cho pose kia.
7. Sử dụng bảng biểu cảm, chi tiết trang phục, góc nhìn và cách phân nhóm layer làm tham khảo khi dựng sprites tách lớp, nhưng ảnh poster hiện chỉ là một ảnh phẳng.

## Tránh suy diễn từ poster

- Các nhãn minh họa / bảng thông số có thể do AI tự tạo (chẳng hạn số đo B/W/H, chiều cao, ngày sinh, CV, tên tiếng Nhật) **không trở thành lore hay thuộc tính nhân vật** nếu người dùng chưa phê duyệt riêng.
- Hình minh họa `Layer` trong poster **không chứng minh đã có texture PNG riêng, alpha/underpaint, skeleton, physics hay chuyển động**.
- Khi cần thay đổi hình thể hoặc chi tiết trang phục, tạo preview mới; bản cũ vẫn lưu lịch sử, **chỉ thay canon sau khi được duyệt**.

## Ứng dụng cho nhân vật sau

Dùng bảng này như **chuẩn trình bày mỹ thuật**: 6 góc nhìn nhất quán, biểu cảm, chi tiết chất liệu/phụ kiện, bảng màu, sơ đồ tách lớp, và cảnh tương tác indoor phù hợp. **Không sao chép khuôn mặt, màu tóc, vóc dáng, số đo, tạo hình hoặc trang phục Lâm Thiển sang nhân vật khác.**

Xem quy chuẩn chung: [CHARACTER_ART_DIRECTION_REFERENCE.md](CHARACTER_ART_DIRECTION_REFERENCE.md).

## Điều kiện trước khi đưa vào APK

1. Dựng các hình pose/turnaround nhất quán từ nguồn đã duyệt; không thay bằng CP317/CP318 bản cũ.
2. Tách layer và vẽ underpaint chính xác; kiểm tra alpha, seam, thứ tự layer, tóc/tay áo và biến dạng ở từng pose.
3. Chạy kiểm thử hình thực tế, có preview trước/sau; chỉ sau khi nghiệm thu art mới rig và tích hợp APK.
