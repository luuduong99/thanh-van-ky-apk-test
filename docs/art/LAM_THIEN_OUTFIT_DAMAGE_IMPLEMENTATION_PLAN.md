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
| 30% | Hư hại nặng nhưng còn che phủ phù hợp | Chưa có asset |

**Chưa chốt riêng:** Công thức ánh xạ sát thương/HP sang độ bền quần áo và tiêu chí kích hoạt từng mốc cụ thể. Không gán sai 70% HP = trạng thái 70% độ nguyên vẹn.

**Điểm tiếp tục:** Phân lớp mẫu Lâm Thiển 100% trước; thiết kế bốn bộ texture đồng bộ ngay trong pipeline, rồi nghiệm thu từng bộ. Đây chưa phải báo cáo hoàn thành cởi/thay đồ, animation, rig hay APK.
