# CP326 — Lâm Thiển: lớp mắt/mày/miệng độc lập trên CANON V2 (2026-10-29)

**Mốc thực hiện:** đã tạo **5 ORA có 35 lớp alpha nét mặt được vẽ mới độc lập từ vector** trên một mặt nguồn CANON V2; 6/6 local test PASS. **MỚI CHỈ LÀ DEMO KỸ THUẬT, KHÔNG PHẢI ART ĐÃ DUYỆT / SPINE / APK**.

## Nguồn bất biến

- **CANON V2 body/face/costume:** `LT_CANON_BODY_REF_2026-10-28_V2`, SHA-256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711`. [Ảnh nguồn Google Drive](https://drive.google.com/file/d/1mEsyn2wMo-MVQqhtbmdUiFfO8AaYhzUR/view?usp=drivesdk). Tỷ lệ +17% đã nằm trong V2, không đổi.
- **5 biểu cảm đã duyệt:** `LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED`, `shy/angry/pain/embarrassed/alluring`, SHA-256 `ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7`; nguồn [APPROVED](LAM_THIEN_FIVE_EXPRESSIONS_APPROVED_2026_10_29.md). Bộ này chỉ làm chuẩn **sắc thái**, không ghi đè mặt và màu mắt canon V2.
- **Quy chuẩn các nhân vật khác:** [GLOBAL_CHARACTER_EXPRESSION_STANDARD_2026_10_29.md](GLOBAL_CHARACTER_EXPRESSION_STANDARD_2026_10_29.md). Không copy mặt, mắt, body, tỷ lệ từ Lâm Thiển sang Tô Nguyệt Ly.

## Thao tác kỹ thuật có kết quả thực

1. Trích trực tiếp vùng mặt trong ảnh CANON V2 từ bbox `[1160,0,1390,114]`, **kích thước bản nguồn chỉ 230×114 px**, ghi checksum V2. Phóng 4× tạo canvas làm việc `920×456` để đặt layer. Đây **không phải nâng chất lượng lên HD**.
2. Tạo nền tạm bằng thuật toán CV2 inpaint xóa vị trí mắt/mày/miệng cũ. Nền này **còn artifact và không phải underpaint do họa sĩ xác nhận**.
3. Vẽ mới **7 layer alpha RGBA độc lập** cho mỗi `shy`, `angry`, `pain`, `embarrassed`, `alluring`: `blush_image_left/right`, `eye_image_left/right`, `brow_image_left/right`, `mouth`. Layer vector mới **không chứa pixel cắt từ da/tóc của poster**, khác với các pixel-patch CP325.
4. Đóng gói thành **5 file ORA**, mỗi file có 7 layer biểu cảm + 1 nền tạm + 1 lớp `GUIDE_CANON_V2_ORIGINAL_REFERENCE_ONLY` ẩn; `mergedimage.png` để preview.
5. Tạo ảnh so sánh `CP326_FIVE_FACE_COMPOSITES_TECH_DEMO.png` và manifest kiểm nguồn, lớp/alpha, SHA và tình trạng.
6. QA trực tiếp bằng `tools/cp326/validate_cp326_face.py`: **5/5 ORA hợp lệ**, mỗi file đủ 7 layer RGBA có pixel, không lặp, ảnh preview merged tái tạo đúng từ các layer hiển thị. Chạy local `tools/cp326/test_cp326_face_local.py`: **6/6 PASS**. `--strict` FAIL **đúng dự kiến** vì không được duyệt vào production.

## Nguồn file và bàn giao

- ZIP **`TVK_LamThien_CP326_Vector_Face_Prototype_NOT_GAME_READY.zip`**, SHA-256 `377086143ce7a85449e9ade18d1de02f64431ba15e8c8024b2ce5bc86f37f4f6`, 19 files, ZIP CRC PASS.
- Library backup: `/Thanh Van Ky/Development/CP326_Vector_Face_Prototype/` (gồm ZIP, contact sheet, manifest, generator, validator, test). **Không lưu vào Approved production art**.
- [Manifest file & alpha](LAM_THIEN_CP326_VECTOR_FACE_MANIFEST.json).
- Mã tạo (chạy lại với `--canon <V2.png> --out <dir>`): `tools/cp326/create_cp326_face_vectors.py`. Phụ thuộc Python Pillow/Numpy/OpenCV/CairoSVG.
- Validator binary: `tools/cp326/validate_cp326_face.py` (Pillow).
- Test file ORA binary được backup tại Library và trong ZIP: `tools/cp326/test_cp326_face_local.py`; test chỉ chạy khi có binary địa phương.
- Metadata unit test: `tests/art/test_cp326_vector_contract.py`; workflow `.github/workflows/cp326-vector-face-contract.yml`. CI metadata không kiểm được file ORA nếu không có ZIP trên runner.

## Phân định chất lượng / điều kiện nghiệm thu

- **Có file art alpha độc lập thật**, nhưng **chưa đạt mỹ thuật**. Dấu hiệu rõ: nét vector nhìn không giống nét vẽ anime tinh tế trong bảng đã duyệt, ảnh gốc quá bé, kỹ thuật inpaint làm mềm da và thiếu vùng da thật dưới mi/mắt.
- **Không tự dùng CP326 như sprite game**, không điền `sprite_paths`, không đánh dấu P1-03 hoàn tất, không nói đã có Spine rig, build APK hoặc biểu cảm đã hoạt động bằng artwork thật trên Android.
- **Không yêu cầu chốt lại** concept V2/5 biểu cảm — đã APPROVED. Preview CP326 mới là bản kỹ thuật, **chưa được duyệt** làm replacement.
- Phải dùng nguyên nhân vật V2 và art tách lớp độ phân giải sản xuất để vẽ lại mắt/lông mày/môi/da. Lặp QA biểu cảm cỡ 132px/64px, hướng nhìn và nét mặt khác biệt; sau đó kiểm underpaint/occlusion, draw order, Spine và APK.

## CP327 — điểm tiếp tục

1. Ưu tiên tìm/khôi phục nguồn **layer art full-body/face ở độ phân giải cao đúng CANON V2**; nguồn V2 hiện tại chỉ là poster. Nếu không có, cần một lượt redraw art thật theo V2, gửi preview *asset* để nghiệm thu chứ không hỏi lại style đã chốt.
2. Làm sạch underpaint và vẽ lại năm expression trên cùng face master, đồng nhất màu mắt/đường nét/tóc/phụ kiện với V2.
3. Tách các bản PNG alpha có vùng ẩn được bù đầy đủ để animating eyelids/mouth; đo mốc trên mỗi góc Front/3⁄4.
4. Test mặt ở kích thước đối thoại, ghép với body đúng trạng thái wardrobe × integrity × pose, kiểm các nét không giật hoặc hiện hai đôi mắt, mới khai báo `sprite_paths` và Spine.
5. Chạy pipeline CI Android thực, kiểm APK trên thiết bị và lập phiếu nghiệm thu. **P0-02/P0-03, P1-03, P2 vẫn chưa DONE**.


## Bổ sung QA UI và bản động kỹ thuật CP326 (2026-10-29)

- `CP326_DIALOGUE_THUMBNAIL_QA_TECH_DEMO.png`: đối chiếu 5 biểu cảm khi giảm xuống 132px và 64px; ở cỡ nhỏ có sự khác biệt nhưng vẫn chưa đạt chất lượng anime/source duyệt.
- `CP326_EXPRESSION_SWITCHING_TECH_DEMO.gif`: mô phỏng đổi state giữa 5 expression trên cùng nền face; **chỉ là GIF chuyển ảnh, không có rig hoặc Spine animation**.
- Hai file trên đã được lưu Library Development cùng ZIP và **được bổ sung vào ZIP cuối**. Vì vậy SHA-256 ZIP là `377086143ce7a85449e9ade18d1de02f64431ba15e8c8024b2ce5bc86f37f4f6`, tổng 21 file; checksum bản ZIP 19 file trước đã thay thế. ZIP CRC PASS.
- Nghiệm thu production nghiêm ngặt vẫn FAIL đúng kỳ vọng; không nhập bất kỳ attachment demo nào vào `sprite_paths`.
