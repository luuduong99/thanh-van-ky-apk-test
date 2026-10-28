# Thanh Vân Ký — Lâm Thiển · CP319 clean design review

**Ngày:** 2026-10-28  
**Trạng thái:** BẢNG REVIEW ĐÃ TẠO · CONCEPT CHƯA DUYỆT · CHƯA TẠO RIG/APK

## Tiến triển từ CP318

- Đã tách ảnh CP318 mới (725 × 981 RGB) thành hình Back riêng, hình tóc bay riêng và vùng kiểm tra tóc–gáy–vai, khoét hông, tay áo, phụ kiện.
- Tạo `CP319_LamThien_Clean_Primary_Back_Review.png` làm ảnh review chính, lấy từ **khung Back mới không bị đè chữ**. Giữ nguyên từng pixel nghệ thuật nguồn trong các tệp crop; chỉ thay đổi bố cục, phóng ảnh để đọc dễ hơn.
- Kiểm tra nguồn ảnh bằng SHA-256: `29bca1bb136394bcca3b31f05b0c4f43e8dbe15766f921436d2a27649e729e26`.
- Bảng này là bản review CP318, **không phải bản mới được người dùng chốt riêng**, không phải ORA/Spine, không chứng minh chuyển động tóc hoặc tính toán +17% ở pixel ảnh.
- Bản "tóc bay" là **một hình tạo sẵn khác trong cùng ảnh concept**, không phải ảnh thử rig hay hai frame được dựng từ cùng skeleton.

## Tiêu chí hình ảnh đã được người dùng chốt để đối chiếu

1. Giữ Lâm Thiển tóc bạc, nhận diện anime fantasy, trang phục trắng–xanh–vàng, phụ kiện tinh xảo.
2. Back có khoảng khoét bên hông cân đối và đường nét phía sau rõ, theo quyết định 2026-10-27. Không được quay về PNG Back cũ hoặc CP317 proxy làm hình xem chính.
3. Mốc +17% là quy chuẩn hình thể đã xác nhận trong tài liệu; không được gắn nhãn "đạt +17% chính xác" với concept CP318 khi không có phép đo giữa hai ảnh chuẩn.
4. Các thiết kế góc Front, 3/4 và tư thế tương tác phải đồng bộ, giữ chi tiết nào đã chốt nếu không có điều chỉnh mới được người dùng xác nhận.

## Công cụ chặn sử dụng nhầm thiết kế

- `docs/art/LAM_THIEN_DESIGN_REGISTRY.json`: phân biệt **yêu cầu mới nhất đã được duyệt** với **ảnh CP318 đang chờ duyệt**, liệt kê nguồn cũ bị deprecate cho mục đích art.
- `tools/art/validate_design_registry.py`: không cho phép mô tả asset hoàn thành/ràng buộc production với ảnh chưa duyệt hoặc CP317 proxy.
- `tests/art/test_design_registry.py`: 5 bài test tự động; đạt trên môi trường chạy cục bộ. GitHub Actions cần kiểm tra riêng.
- Gate chỉ bảo vệ trạng thái/tài liệu. **Không thể chứng minh silhouette/alpha/physics bằng script này.**

## Phân lớp cần triển khai sau khi duyệt preview (định hướng kỹ thuật)

| Nhóm | Cần tách | Ghi chú |
|---|---|---|
| Tóc | tóc sau, tóc trước, lọn bay, trâm và hoa | Dựng underpaint vùng gáy/vai, không cắt polygon cứng |
| Cơ thể | đầu, cổ, thân, vai và tay, hông/chân theo khớp | Không bóp méo tỷ lệ đã chốt |
| Trang phục | thân áo, 2 tay áo, vạt trước/sau, 2 lớp vải bên hông | Khoét hông phải đúng hình chốt, không lấp mất khoảng khoét |
| Trang sức | dây lưng, dây xanh/vàng, nơ, họa tiết | Giữ draw order khi tóc/tay áo dịch chuyển |
| Gói hình | ảnh Front/Back/3/4 và các góc cảnh dùng trong game | Cần cùng một bộ mỹ thuật, không ghép concept độc lập làm khung animation |

## Điều kiện để chuyển sang CP320

- Xác nhận bản concept CP318/CP319 có cần chỉnh không. Chỉ khi duyệt mới cập nhật `latest_user_approved_design` và chọn ảnh chuẩn cho production.
- Chuẩn bị hình độ phân giải đủ cao, tách layer có alpha/underpaint. Ảnh CP318 hiện là **RGB có nền**, không thể trực tiếp biến thành asset rig hoàn chỉnh bằng kiểm thử crop.
- Chạy kiểm tra các vùng seam, chuyển động tóc/tay áo và phần khoét hông; gửi hình từng lớp + composite để nghiệm thu; sau đó mới Spine/physics và APK.

**Quy tắc bất biến:** luôn dùng thiết kế được người dùng duyệt gần nhất; các bản cũ được giữ lại để lịch sử/QA, không được dùng làm preview chính.