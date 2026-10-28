# Lâm Thiển — quyết định trang phục, độ rách và đồng bộ tư thế (28/10/2026)

**Trạng thái quyết định:** **NGƯỜI DÙNG ĐÃ CHỐT PHƯƠNG ÁN THAM CHIẾU MỚI** trong hội thoại bằng câu: “hãy dùng này đi. Chốt phần này. Nhớ lưu lại để làm tài liệu. Tránh bị nhầm sau này. Nhớ là cũng sẽ áp dụng khi đổi tư thế đó nha”.

**Trạng thái ảnh gốc của quyết định này:** **CHƯA NHẬN ĐƯỢC FILE ẢNH**. Liên kết người dùng cung cấp là object URL tạm thời của trình duyệt: `blob:https://chatgpt.com/8d8b9f33-3a9b-47c6-a677-c31dd0dcfccc`. URL `blob:` không thể dùng lại như đường dẫn tải xuống, và không cho phép xác thực pixel/hash hoặc sao lưu ảnh vào GitHub/Drive. **Không tự nhận đã lưu được ảnh từ liên kết này**; không dùng ảnh khác thay thế rồi gọi là ảnh vừa chốt. Cần tệp PNG/JPG/ảnh đính kèm thực tế để đăng ký thành **verified approved asset**.

## Phần quy tắc đã xác nhận

- **Bỏ yêu cầu tăng rách cố định +20%.** Người dùng đã thay bằng phương án **giảm bớt độ rách một chút để hình ảnh hài hòa**; mức chính xác về hình dáng rách phải đối chiếu trực tiếp ảnh được chọn khi có file gốc.
- Giữ **bốn mức độ nguyên vẹn** `100% / 70% / 50% / 30%`; các con số là trạng thái độ bền trang phục, **không phải tỷ lệ lộ da**.
- Ở cấp `30%`, **kể cả những phần vải còn che phủ** vẫn có dấu sờn, rách nhẹ trên mép, đường may bung hoặc nhăn/xô lệch — **không giữ nguyên mới 100%**, nhưng luôn đảm bảo những vùng cần che vẫn được che phủ phù hợp.
- Tháo/thay trang phục (`wardrobe`) **khác** hư hại chiến đấu (`damage`); các chi tiết vải mỏng/voan, mức xuyên sáng và số cấp tháo đồ chỉ được mô tả/chốt chính xác sau khi có ảnh gốc thực tế. Giữ phương án lớp lót che phủ phù hợp nếu sử dụng vải xuyên sáng.
- Tỷ lệ cơ thể, tóc bạc, trang phục trắng–xanh–vàng, chi tiết vàng vừa phải phải bám [mẫu ngoại hình Lâm Thiển đã duyệt](https://drive.google.com/file/d/10jKNq-VL62sv1gez5PHlVT9QKyJp_Cvd/view?usp=drivesdk). Không tự thay thiết kế mặt/cơ thể dựa trên bản rách đồ.

## Quy tắc bất biến — ÁP DỤNG KHI ĐỔI TƯ THẾ

**Trang phục đang mặc + mức độ hư hại + biểu cảm/hành động phù hợp phải đi theo nhân vật**, không reset khi xoay tư thế, đổi cảnh hoặc từ chiến đấu sang tương tác/hội thoại.

| Nhóm tư thế / bối cảnh | Yêu cầu khi tạo art và triển khai |
| --- | --- |
| Front, Side, Back, góc 3/4, quay đầu qua vai | Cùng bộ trang phục và cùng mức hư hại; vết rách ở **cùng vị trí thuộc cấu trúc quần áo**, không sinh ngẫu nhiên khi đổi góc |
| `bed_kneel_forward` (quỳ giường, ngoảnh lại) | Dùng pose riêng, vải/tà rơi theo tư thế; giữ trạng thái hư hại đã có |
| `bed_recline` (nằm ngửa trên giường) | Không tráo với pose nằm sấp; ứng xử vải, tóc, biểu cảm theo trọng lực và cảnh |
| Ngồi giường, ngồi ghế/sofa, nằm nghiêng, tựa tường | Có asset riêng từng tư thế; nếp gấp, rách áo, che phủ và đồ dùng/khung cảnh phù hợp |
| Battle, hồ sơ nhân vật, tương tác indoor, hội thoại | Lấy trạng thái mặc đồ/hư hại được lưu; chỉ hiện sprite đúng pose nếu có asset, không crop ảnh cũ rồi nhận là ảnh mới |

**Biểu cảm/hành động:** trạng thái va chạm, mệt, lúng túng, chỉnh trang phục, thư giãn phải biến đổi theo hoàn cảnh và tính cách nhân vật, không dùng một khuôn mặt/pose cho mọi cấp độ. Chỉ đổi biểu cảm chứ không làm biến dạng mẫu cơ thể đã duyệt.

## Tiêu chí chuẩn bị tài nguyên

1. Khi có PNG/JPG thực từ người dùng, **lưu bản gốc bất biến**, ghi nguồn, kích thước, hash, ngày chốt và đường dẫn ở `LAM_THIEN_DESIGN_REGISTRY.json` hoặc đăng ký biến thể trang phục mới. Không ghi blob URL là đường dẫn lưu trữ thật.
2. Từ ảnh đã xác minh, đối chiếu tạo bộ biến thể `100 / 70 / 50 / 30` và mức thay/cởi đồ theo chính ảnh đó; giữ phân lớp, underpaint, seam, draw order theo bộ rig.
3. Đối chiếu ít nhất Front + Back + Side/3/4 và một tư thế trên giường; tiếp tục ghế và tường. Mọi biến thể phải khớp tình trạng đang lưu.
4. Có hình thực cho mọi pose/trạng thái được sử dụng trước khi bật nút trong APK. Chưa có file nghĩa là chưa thể nghiệm thu art/physics/APK.

## Quy tắc ưu tiên nguồn

- **Nguồn ngoại hình gốc vẫn đang có thể xác minh:** `TVK_LamThien_Approved_Reference_20261028.png`.
- **Nguồn trang phục/rách đồ mới:** người dùng đã chốt phương án có liên kết `blob:`, nhưng **chưa có file ảnh để lưu/xác nhận**; yêu cầu **không lấy proxy CP317, preview CP318/CP319 hay các ảnh hư hại trước đó để thay thế**.
- Quyết định bằng chữ được lưu trong tài liệu này **không chứng minh ảnh đã được nhập hoặc hoàn tất sprite**.
