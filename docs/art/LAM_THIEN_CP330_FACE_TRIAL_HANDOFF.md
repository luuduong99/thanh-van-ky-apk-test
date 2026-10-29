# Thanh Vân Ký — CP330: 5 ORA biểu cảm có layer ảnh thật (2026-10-29)

**KẾT QUẢ:** hoàn thành **thử nghiệm phân rã 5 chân dung vừa sinh thành 35 layer RGBA có pixel thật**. **KHÔNG PHẢI production face master, KHÔNG THAY CANON V2, KHÔNG ĐƯỢC DUYỆT SPINE/APK.**

## Khóa hai nguồn đã được người dùng duyệt
- **Body/face chính thức:** `LT_CANON_BODY_REF_2026-10-28_V2` (SHA256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711`), mắt hổ phách, tóc bạc và phụ kiện/trang phục trắng–xanh–vàng, +17% đã tích hợp.
- **Sắc thái 5 biểu cảm chính thức:** `LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED` (SHA256 `ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7`). Năm mã `shy, angry, pain, embarrassed, alluring`.
- **Ảnh mới CP330** là poster minh họa AI KHÁC nguồn approved (SHA256 `ebffd161e2d400a33a7b337d870c950c9de7cf967b842a5d9c515f1447df4089`). Các chữ *Final Art*, *Spine-ready* nằm bên trong poster **không phải là sự thật**. Chỉ dùng trong thư mục Development.

## Tài nguyên đã tạo/kiểm thật

- **ZIP:** `TVK_LamThien_CP330_Face_Art_Decomposition_NOT_APPROVED.zip`, SHA256 `a1e1f4ec14d89263ff6797a445cc93c4e7140a1e08f1930bfee27d2560842172`; 30 file, ZIP CRC PASS. Lưu ChatGPT Library `/Thanh Van Ky/Development/CP330_Face_Painted_Region_Trial/`.
- 5 ảnh ứng viên kích thước **native** lần lượt 260×370, 257×370, 257×370, 256×370, 251×370 px; **không phóng thành hình HD giả**.
- 5 ORA, mỗi ORA chứa **7 layer biểu cảm alpha nonempty** `brow_image_left/right, eye_image_left/right, mouth, blush_image_left/right`, một lớp `face_base_cutout` có vùng alpha rỗng đúng chỗ, một lớp `automatic_underpaint_REQUIRES_ARTIST_REVIEW` (OpenCV Telea) và một `GUIDE_UNAPPROVED... ` ẩn. Kết quả layer ghép lại **khớp từng pixel với ảnh CP330 mới**, KHÔNG phải khớp canon V2.
- Kiểm thử đổi vị trí mắt/miệng ± vài pixel không có lỗ alpha; **không khẳng định underpaint đẹp hoặc đúng mỹ thuật**. Tất cả 5 chân dung hiện có khuôn mặt/tư thế KHÁC NHAU, **chưa có face master chung**.

## QA có kết quả
- Local `python -m unittest discover -s tests -v` trên bộ ZIP: **9/9 PASS**.
- `python tools/audit_cp330.py . --out qa_result.json`: PASS mức kỹ thuật (5 ORA, SHA, 35 alpha, source composite, alpha cutouts, CRC).
- `python tools/audit_cp330.py . --strict`: **FAIL có chủ đích**; ngăn nhận nhầm prototype là production.
- GitHub: `tools/cp330/build_cp330.py`, `tools/cp330/audit_cp330.py`, `tests/art/test_cp330_art_trial_contract.py`, workflow `cp330-face-art-trial.yml`, manifests JSON. CI chỉ kiểm metadata + synthetic; không đọc ORA nhị phân trong Library.

## Vì sao chưa được coi là đã vẽ xong Lâm Thiển?
1. **Một tranh phẳng mới được chia vùng**, chưa là mắt/mày/miệng vẽ tách hoàn chỉnh; patch có thể lẫn da và tóc.
2. **Khuôn mặt master chưa đồng nhất** giữa 5 trạng thái.
3. Art nguồn mới không phải BODY/FACE CANON V2, chưa được duyệt làm mặt mới; bản V2 gốc vẫn là chuẩn duy nhất.
4. Underpaint do thuật toán nội suy, **chưa nghiệm thu mỹ thuật**; bản nguồn chỉ khoảng 250 px rộng.
5. Chưa có Spine skeleton/mesh/animation, đường dẫn sprite trong app và APK sản xuất.

## CP331 — Việc ưu tiên để thực sự tiến tới hoàn thiện

1. **Dựng một face master high-resolution có chi tiết thật** khớp khuôn mặt V2, mắt hổ phách, tóc/trang sức; không copy từng khuôn mặt khác nhau của CP330 vào rig.
2. Vẽ *cùng một face master* với 5 nét biểu cảm đã duyệt, tách **attachment sạch** (không kèm da nền) và tự vẽ underpaint. Áp dụng vùng da che bởi mí/lông mày/tóc để biến dạng không lộ vùng trống.
3. Xuất master/attachments dưới dạng ORA + PNG alpha, QA mắt/mày/miệng, các thử dịch/biến dạng và canvas native. So at 256px,132px,64px.
4. **Duyệt asset game hoàn thiện** theo đúng CANON V2; sau đó mới điền `sprite_paths`, rig Spine, test Android/APK. Không hỏi lại approval của thiết kế V2 hay năm cảm xúc.
5. Có thể tiếp tục triển khai các phần gameplay không phụ thuộc art, nhưng **không lắp ảnh nháp CP330 vào game**.

**Trạng thái:** CP330 tech trial DONE; P0-02/P0-03/P1-03 nghệ thuật/Spine/P2 APK **NOT DONE**.
