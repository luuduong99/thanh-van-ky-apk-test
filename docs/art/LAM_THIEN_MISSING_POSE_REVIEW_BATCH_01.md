# Thanh Vân Ký — Lâm Thiển · P0 art review batch 01 (tư thế còn thiếu)

**Ngày mở batch:** 2026-10-28  
**Trạng thái:** TÁM TƯ THẾ CHỜ DUYỆT ẢNH MINH HỌA. Không có ảnh nào tự động thành canon, sprite hoạt động hoặc Spine rig sau khi tạo preview.

## Mẫu cơ sở bất biến

- [Hình thể và phục trang Lâm Thiển đã chốt 28/10](https://drive.google.com/file/d/10jKNq-VL62sv1gez5PHlVT9QKyJp_Cvd/view?usp=drivesdk): tóc bạc dài, cài hoa, trắng–xanh nhạt–vàng, phụ kiện vàng vừa phải, tỷ lệ cơ thể chuẩn và vải khoét hông cân đối.
- [Bảng biểu cảm/tư thế/hành động tham khảo đã chốt](https://drive.google.com/file/d/1M-6KIEeon7HX4Qn56UlhGMfV76Lr-sN5/view?usp=drivesdk).
- Các quyết định trang phục `wardrobe` và mức hư hại `integrity` phải giữ khi chuyển pose cho **mọi nhân vật**.
- Trên concept đầu của batch chỉ minh họa **wardrobe=default, integrity=100** để đối chiếu cơ thể/pose. Biến thể wardrobe và 70/50/30 là phase sau, không được giả thành đã hoàn thành.

## 8 pose cần có ảnh tham khảo riêng

| ID | Nhãn xem trước | Cảnh/khung hình | Điểm kiểm tra trước khi duyệt |
| --- | --- | --- | --- |
| `side` | Góc nghiêng | toàn thân, camera ngang | cơ thể/giày/chiều cao đúng base; các chi tiết khớp front/back |
| `front_three_quarter` | Trước 3/4 | toàn thân | nhận diện mặt/tóc, chiều dài chân, thân trên và họa tiết cùng model |
| `back_three_quarter` | Sau 3/4 | toàn thân | vải/tóc/eo-hông ở cùng vị trí cấu trúc; không đổi tỷ lệ |
| `back_turn` | Ngoảnh lại | thân và mặt nhìn lại sau vai | thể hiện mặt rõ, vai xoay vừa, không méo lưng/ngực |
| `bed_side_lying` | Nằm nghiêng giường | phòng ngủ, giường | trọng lực tóc/vải, nằm tự nhiên, không nhầm nằm ngửa `bed_recline` |
| `bed_sit` | Ngồi mép giường | phòng ngủ, giường | tư thế ngồi cân đối, vải rủ xuống đúng |
| `chair_sit` | Ngồi ghế | phòng riêng, ghế | tiếp xúc ghế chân/tay đúng, tóc/vạt không xuyên ghế |
| `wall_lean` | Dựa tường | phòng riêng, tường | tiếp xúc vai/tay/đế giày; không sai tư thế |

## Ma trận duyệt theo nhiều vòng

**P0–01:** mỗi pose có preview nhận diện, camera/bối cảnh, baseline 100% đầy đủ.  
**P0–02:** người dùng chốt pose + art rồi mới sinh sprite từng pose có alpha sạch.  
**P1–01:** duyệt các cấp cởi/trang phục riêng cho **cùng pose** (không chỉ mức cuối); giữ lớp che phủ phù hợp.  
**P1–02:** duyệt 70/50/30 theo từng wardrobe × pose, đồng bộ vị trí vết rách; ở 30% các mảnh còn che vẫn có dấu hư hại.  
**P1–03:** bộ mặt/expression và action cho đúng bối cảnh.  
**P2:** đưa vào rig/atlas, runtime test, APK chỉ khi có art và kiểm thử thực.

## Quy tắc tránh nhận nhầm tiến độ

- Ảnh poster tổng hợp là **concept để review**. Không phải 8 ảnh PNG alpha riêng, không phải ORA/PSB có layer và không phải animation.
- Chưa nhận được kết quả duyệt của user = **pending**.
- Nếu poster có chữ/số liệu AI sai hoặc hình thể chưa thật khớp, đánh dấu vùng sai rồi sửa preview; không thay file đã chốt tự động.
- Khi có ảnh chốt, lưu nguyên bản và checksum, rồi mới chuyển trạng thái của pose tương ứng từ `plannedPoses` sang `poses` trong catalogue.
