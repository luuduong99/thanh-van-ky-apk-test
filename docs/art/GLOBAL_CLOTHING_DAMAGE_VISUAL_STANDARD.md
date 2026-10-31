# Thanh Vân Ký — quy chuẩn vết bẩn, vết xước và rách trang phục

**Quyết định:** ĐÃ CHỐT yêu cầu mỹ thuật ngày 2026-10-28.  
**Phạm vi:** toàn bộ nhân vật (bao gồm Lâm Thiển), mọi mức trang phục và mọi góc/tư thế.  
**Tình trạng triển khai:** đặc tả + metadata, chưa tạo texture/rig cụ thể. Mức độ minh họa chi tiết cần duyệt bằng preview từng nhân vật.

## Loại tổn hại cần thể hiện đồng thời

- **Bẩn (`dirt`):** bụi đất, vết bùn, vết lem nhỏ, vệt bám theo mép áo/tà váy, ống tay hoặc điểm tiếp xúc môi trường; màu hợp loại vải và loại va chạm.
- **Xước/sờn (`abrasion`):** vệt cọ xát trên mặt vải, đường chỉ xù, họa tiết bị mòn, mép vải sờn; **ưu tiên hư hại vật liệu trang phục**, không tự sinh vết thương lên da nhân vật.
- **Rách (`tear`):** nứt/rạn đường may, lỗ rách nhỏ, vải tưa, mép rách, mảnh vải rủ, phụ kiện lỏng; bảo toàn tính liên tục về cấu trúc và các vùng che phủ phù hợp.

## Phân tầng cảm nhận theo chỉ số độ nguyên vẹn

| Độ nguyên vẹn | Bẩn | Xước/sờn | Rách | Cách đọc trực quan |
| --- | --- | --- | --- | --- |
| **100%** | không | không | không | Trang phục nguyên vẹn, sạch |
| **70%** | ít | vài vệt nhẹ | rất nhỏ, một vài vị trí | Va chạm nhẹ, không được trông rách nặng |
| **50%** | rõ hơn và rải ở các lớp | xước/sờn trung bình | một số vết rách thấy được | Đã trải qua chiến đấu, trang phục còn phom |
| **30%** | nhiều hơn, có chỗ đậm nhưng không phủ kín toàn bộ | sờn mạnh, đường chỉ bung và họa tiết bị mòn | nhiều, đa dạng kích cỡ; **cả các lớp che phủ còn lại cũng có dấu rách/sờn** | Hư hại nặng nhưng vải/lớp lót vẫn che phủ phù hợp |

Đây là **mức tăng tương đối bằng mắt**, không phải tỷ lệ phần trăm diện tích lộ da, lượng vết xước, mức rách hay hệ số +20% cố định. **Độ nguyên vẹn trang phục không tự gắn với % HP**: gameplay phải có quy tắc độ bền riêng được phê duyệt.

## Quy tắc sản xuất art & runtime

1. Vết bẩn/xước/rách phải **tích lũy theo mức hư hại**: trạng thái nặng hơn không tự làm mất toàn bộ vết bẩn hoặc rách đã có, trừ khi có hành động sửa/giặt/thay đồ rõ ràng.
2. Khu vực tổn hại **bám theo đúng mảnh trang phục** khi nhìn Front, Back, Side, 3/4, đứng, quỳ, nằm, ngồi ghế, dựa tường; phần hình ảnh có thể biến dạng theo nếp vải, chuyển động và trọng lực.
3. Không tự áp thêm vết bẩn hoặc rách chỉ vì đổi pose, góc camera hoặc mở cảnh trong phòng. `wardrobe_state` và `integrity` giữ nguyên như quy tắc toàn game đã chốt.
4. Cân đối với đặc tính vật liệu: **lụa/voan** ưu tiên vệt sờn mảnh, rách theo thớ, bụi nhẹ thấm nếp gấp; **vải dày/giáp** có dạng cọ xát khác. Màu sắc phải hỗ trợ đọc hình, không làm mất hoàn toàn bộ mặt và bản sắc nhân vật.
5. Giữ vùng che phủ phù hợp ở tất cả mức, nhất là 30%; không phát triển tổn hại thành việc lộ trực diện các vùng nhạy cảm. Vết bẩn/xước là đặc tính trên áo/vải, **không đồng nghĩa với thương tích cơ thể**.
6. Mẫu nhân vật là nguồn duy nhất cho silhouette và trang phục: **Lâm Thiển phải theo CANON BODY V2** [ảnh đã duyệt](https://drive.google.com/file/d/1mEsyn2wMo-MVQqhtbmdUiFfO8AaYhzUR/view?usp=drivesdk); các nhân vật khác có reference riêng.
7. Nếu dùng texture overlay phụ, phải có UV/anchor phù hợp từng mảnh vải, layer draw-order và mask, bảo đảm các vết không trôi vị trí khi chuyển pose, thay outfit hay rig chuyển động.
8. Không nhầm **dirty/scratched/torn art** với trạng thái `wardrobe` (chọn/cởi trang phục). Mỗi wardrobe hợp lệ có thể có bộ visual damage riêng; nếu chưa có asset đúng tổ hợp, game báo thiếu, không tự hiển thị đồ nguyên vẹn.

## Tác vụ kiểm thử / preview

- Preview **mặc đủ × 100/70/50/30** theo Front và Back từ mẫu đã duyệt; xác nhận sự khác biệt bẩn/xước/rách mạch lạc, không thay đổi tỷ lệ body. Tiếp đó duyệt Side/3⁄4 và pose nội thất.
- QA tracking: kiểm tra vết được neo vào cấu trúc áo/tà/tay áo; vị trí không di chuyển vô cớ khi đổi góc, không bị lặp pattern đối xứng không tự nhiên.
- QA alpha, seam, draw-order, underpaint, chuyển động và độ che phủ, rồi mới kết nối asset vào `wardrobe × integrity × pose`.
- Chỉ đánh dấu artwork hư hại hoàn thành khi file texture/sprite/rig thực tồn tại và được duyệt; **metadata về độ bẩn/xước/rách không tạo ra ảnh hoặc animation**.

## Nguồn quy chuẩn

- [Global appearance contract](GLOBAL_CHARACTER_APPEARANCE_SPEC.md).
- [Lâm Thiển — kế hoạch bản V2](LAM_THIEN_NEXT_TASKS_AFTER_CANON_V2.md).
- [Lâm Thiển — kế hoạch hư hại ban đầu](LAM_THIEN_OUTFIT_DAMAGE_IMPLEMENTATION_PLAN.md).
