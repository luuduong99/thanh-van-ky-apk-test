# CP336 — Lâm Thiển | Source Front/3⁄4 thật và cổng QA face-master 2 góc
**2026-10-29 · TRẠNG THÁI: source audit + tooling DONE; production face art NOT DONE.**

## 1. Nguồn đã duyệt — giữ bất biến

- **Model ngoài hình**: `LT_CANON_BODY_REF_2026-10-28_V2`, PNG RGBA 1672×941, SHA-256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711`. Tóc bạc, **mắt hổ phách**, hoa trắng/vàng tiết chế, trang phục trắng–xanh–vàng. Tỷ lệ +17% đã tích hợp vào V2, không áp thêm.
- **Năm sắc thái đã duyệt**: `LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED`, PNG 1536×1024, SHA-256 `ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7`. ID `shy, angry, pain, embarrassed, alluring`. Chỉ dùng làm chuẩn nét cảm xúc, không đổi danh tính/màu mắt/trang phục V2.
- **Giữ nguyên trang phục/damage**: 100/70/50/30 và state `expression / wardrobe / integrity / pose / action` độc lập.

## 2. Xác định giới hạn nguồn thật (không giả HD)

Đã kiểm trực tiếp ảnh nguồn được chốt, đối chiếu Google Drive folder `Lam_Thien_Canon_V2_20261028`; nguồn Drive này chỉ có PNG/ZIP ảnh phẳng, README và MODEL_CARD; không có bản ORA/PSD/KRA gốc trong folder hoặc tên file search Drive có quyền truy cập. Không kết luận nguồn thật không tồn tại ở nơi khác.

Các crop **giữ nguyên byte pixel**, tọa độ tính trên ảnh V2 1672×941:

| Reference | Crop XYXY | Native pixel | Kết luận |
| --- | --- | --- | --- |
| Front-labeled image | [14,116,159,267] | **145×151** | Face hơi nghiêng, chưa phải trực diện chuẩn rig |
| 3⁄4-labeled image | [321,116,464,267] | **143×151** | Khá giống góc Front; chưa đủ hai master khác góc |
| V2 closeup | [1160,0,1390,114] | **230×114** | Mặt có chi tiết rõ hơn nhưng vẫn quá nhỏ |

- Lưu ảnh V2 và 5 biểu cảm gốc khớp SHA, crop và contact board `CP336_APPROVED_ANGLES_AND_EXPRESSIONS.png`.
- **Không upscale thành HD giả**. Phần cần giải quyết bằng vẽ lại native: true Front + true 3/4 với đường nét V2.
- **Ảnh mới CP336** dạng poster có chữ *Production Ready v2.3* chỉ là PNG phẳng do hệ thống tạo, không có source semantic/Spine; **NOT APPROVED, không dùng làm model game**.

## 3. Thay đổi kỹ thuật có thật

Tạo `tools/cp336/validate_head_layers.py` để chuẩn bị nghiệm thu art *đúng cấu trúc*. Cấu trúc đầu vào là **2 góc** `front` và `three_quarter`. Mỗi góc có **4 lớp master dùng chung** `hair_back / face_underpaint / hair_front / ornament`; mỗi biểu cảm có **13 PNG alpha semantic**: mày trái/phải, lòng trắng mắt trái/phải, iris trái/phải, lông mi trái/phải, mí trái/phải, miệng, má trái/phải.

Bộ công cụ đọc **file PNG thực**, kiểm SHA-256, path traversal, canvas/ROI, RGBA và alpha nonempty, da underpaint đủ alpha tại các điểm mẫu, kiểm màu mắt hổ phách (heuristic), bộ 5 mã và base dùng chung. **Đây là gate kỹ thuật, không thể tự đánh giá mỹ thuật đạt CANON V2.**

- Với art thật, số slot tối thiểu **2 × [4 master + 5 × 13 semantic] = 138 file PNG RGBA**, có thể tái sử dụng layer khi thực sự tương đồng. Đó là định dạng staging để QA; **chưa tạo 138 sprite sản xuất**.
- **16/16 local tests PASS**: 12 test chạy trên 138 PNG alpha tổng hợp (gồm cases fail mắt xanh, thiếu vùng, alpha bị thủng, RGB thay vì RGBA, sai SHA/path) + 4 test đối chiếu nguồn/crop với ảnh người dùng đã duyệt.
- Chạy `--strict` trên fixture 128px → **FAIL có chủ đích** vì thiếu art native ≥1024px và không có art QA/user acceptance.
- GitHub source tests `tests/art/test_cp336_head_layers.py` và `tests/art/test_cp336_reference_contract.py` + CI `cp336-face-master-qa.yml` chỉ kiểm mã nguồn và fixture synthetic. **Ảnh approved gốc trong ZIP Library không ở GitHub runner** nên QA nguồn ảnh thực 4 tests được làm local.
- **Android CP335 vẫn chặn**: `character_expression_profiles.json` có `production_release.status=blocked_pending_art`, `sprite_paths={}`, không thay sang approved hoặc gắn ảnh phẳng.

## 4. Gói nguồn và bàn giao

- ZIP: `TVK_LamThien_CP336_Source_Master_Gate_NOT_SPINE_READY.zip`, SHA-256 **`54fe65d7201fb7b616a79ab8c030eeeb70b2291d50a2998689b2825964e864e4`**, **161 entries**, ZIP CRC PASS.
- Gói chứa: hai ảnh gốc approved, 8 crop reference, board QA, manifest SHA/bbox, `README.md`, script tạo board, validator, 138 PNG **SYNTHETIC_TEST_FIXTURE_NOT_ART** (dùng để test, không dùng game), 16 tests nguồn/validator và báo cáo strict gate.
- ChatGPT Library Development: `/Thanh Van Ky/Development/CP336_Face_Master_Source_And_QA/`. Không đưa nguồn R&D CP336 vào Approved Production Art.
- [Manifest nguồn](LAM_THIEN_CP336_SOURCE_MASTER_MANIFEST.json). Có SHA từng crop và cờ `real_production_png_layers_created=0`.

## 5. Điều kiện mới được gọi là hoàn thiện — CP337

1. **Cần artist redraw** một mặt Front nhìn thực sự trực diện + một góc 3/4 thật sự, cùng nhận diện CANON V2. **Có source ORA/PSD/SVG và native high-resolution**, không phóng poster hoặc lấy hình AI phẳng.
2. Tạo clean face underpaint (không baked mắt/miệng), tóc đủ vùng ẩn, 13 nhóm alpha ngữ nghĩa cho 5 nét mặt cả hai góc. Mỗi bộ phải giữ base thật sự chung trong cùng angle.
3. Chạy `validate_head_layers.py` kỹ thuật, QA trực quan ở **256/132/64 px**, kiểm blink/mouth/mesh, draw order và tỷ lệ trang sức/màu mắt so với V2.
4. Gửi **preview sprite art hoàn thiện** để người dùng nghiệm thu art mới; không hỏi chốt lại ngoại hình V2 hoặc bộ 5 sắc thái.
5. Chỉ sau nghiệm thu visual+alpha và user acceptance, điền `production_release`, SHA các PNG và `sprite_paths`, tiếp tục Spine/Android, build APK và test thiết bị.

**CP336 đóng phần kiểm nguồn, cấu trúc QA và bàn giao, không đóng P0-02/P0-03/P1-03/P2.**
