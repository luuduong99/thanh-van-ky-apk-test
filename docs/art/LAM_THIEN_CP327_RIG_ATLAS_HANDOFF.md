# CP327 — Lâm Thiển: chuẩn hóa preflight atlas 35 lớp biểu cảm (2026-10-29)

**KẾT QUẢ: MỐC KỸ THUẬT (EXPORT/QA) ĐÃ XONG; FACE ART CHẤT LƯỢNG SẢN XUẤT VẪN CHƯA XONG.** Không chốt lại CANON V2 hoặc năm biểu cảm; không nhập bản nháp CP327 vào APK.

## Nguồn chính thức

- CANON BODY/FACE V2: `LT_CANON_BODY_REF_2026-10-28_V2`, SHA-256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711`, [ảnh gốc Drive](https://drive.google.com/file/d/1mEsyn2wMo-MVQqhtbmdUiFfO8AaYhzUR/view?usp=drivesdk).
- Bộ năm biểu cảm ĐÃ DUYỆT: `LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED`, SHA-256 `ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7`: `shy / angry / pain / embarrassed / alluring`. [Đặc tả biểu cảm](LAM_THIEN_FIVE_EXPRESSIONS_APPROVED_2026_10_29.md).
- **Quy tắc ưu tiên:** body canon V2 quyết định mắt hổ phách, mặt/tóc/phụ kiện/trang phục/tỷ lệ; năm biểu cảm quyết định *sắc thái nét mặt*, không thay đổi nhân dạng. Tỷ lệ +17% đã có trong V2.

## Art direction — bản nháp mới

- Hai poster CP327 mới được tạo để so sánh nét biểu cảm, nhưng ánh mắt thiên xanh và một số nét mặt/phụ kiện không đúng CANON V2. **CHỈ LÀ DRAFT; KHÔNG APPROVED**, không dùng làm source sprite/rig. Poster có chữ “2048 / Spine-ready” do generator vẽ vào ảnh **không phải bằng chứng có layer hay animation**.
- Đã tạo bảng kiểm kỹ thuật `CP327_ART_ALIGNMENT_QA.png` đối chiếu V2, các biểu cảm đã duyệt và poster mới; nhãn `NOT APPROVED` rõ ràng.
- Nguồn mặt V2 hiện có chỉ native **230×114 px**, không được xem là HD dù upscale lên canvas lớn.

## Công việc kỹ thuật đã hoàn thành

1. Từ **năm ORA vector thử nghiệm CP326** (không phải ORA production), export riêng 7 phần mặt mỗi biểu cảm: `brow_image_left/right`, `eye_image_left/right`, `mouth`, `blush_image_left/right`.
2. Tạo **atlas RGBA thật 2048×2048** gồm **35 attachment không rỗng**, cắt bbox alpha chặt và giữ offset về canvas gốc 920×456. JSON ghi `expression,slot,atlas_rect_xywh,original_bbox_xyxy,offset_in_original_canvas_xy`, kèm SHA256 của file ORA nguồn.
3. Viết `tools/cp327/export_cp327_atlas.py` (định dạng **engine-neutral**: PNG+JSON, **KHÔNG PHẢI file atlas Spine chính thức**), `tools/cp327/validate_cp327_atlas.py` (CRC source, per-region byte equality, no-overlap, SHA, mốc CANON), và 5 unit tests thực trên ORA: **5/5 PASS**.
4. **Lỗi đã phát hiện và sửa ngay:** cách alpha-composite đầu tiên thay đổi pixel RGB dưới các patch blush; thay thành direct `paste` để **giữ nguyên từng byte RGBA nguồn**. Audit sau sửa so trực tiếp `tobytes()`, 35/35 khớp, không còn chồng vùng. **Dùng checksum ZIP/atlas cuối cùng bên dưới**, không dùng hash của lần xuất đầu.
5. Chế độ `--strict` cố ý FAIL vì art từ CP326 vẫn chưa được chốt production; không register sprite paths trong `character_expression_profiles.json`.
6. Thêm GitHub `tests/art/test_cp327_atlas_contract.py` và workflow `.github/workflows/cp327-face-atlas-preflight.yml` cho metadata/packer; ORA Library không nằm trên GitHub runner nên job không chứng minh chất lượng art/file binary.

## File và checksum

- **ZIP cuối:** `TVK_LamThien_CP327_Rig_Atlas_Preflight_NOT_GAME_READY.zip`; SHA256 **`69be3de41b2e33dd15dd67899b27bb2b7a4ef86813afe3e91443f7b51e1b14db`**; ZIP CRC PASS.
- **Atlas PNG:** `CP327_TECH_DEMO_FACE_ATLAS_RGBA.png`; SHA256 **`2ef4e619e6d496598db835093e1be5f72ca8b7385ee3bfdc84f24188d7ea9739`**.
- Sao lưu ChatGPT Library Development: `/Thanh Van Ky/Development/CP327_Rig_Atlas_Preflight/`.
- [Hợp đồng CP327 cuối cùng](LAM_THIEN_CP327_ART_GATE_MANIFEST.json), [tọa độ 35 vùng](LAM_THIEN_CP327_TECH_ATLAS.json).
- Source CP326 và production gates: [CP326 handoff](LAM_THIEN_CP326_FACE_VECTOR_HANDOFF.md).

## Kiểm tra và phân định tiến độ

| Hạng mục | Kết quả |
|---|---|
| 5 biểu cảm và CANON V2 | **APPROVED (từ trước), bất biến** |
| 35 vector source CP326 có alpha | **TECHNICAL DEMO**, chưa đạt mỹ thuật |
| Atlas đóng gói + bbox/offset | **QA kỹ thuật PASS, byte-for-byte** |
| Độc lập wardrobe/damage/expression state trong Android | Đã có code CP324, **chưa xác minh APK mới** |
| Face master độ phân giải sản xuất theo V2 | **MISSING** |
| Underpaint do họa sĩ hoàn thiện, 5 nét chuẩn V2 | **MISSING** |
| Spine skeleton/mesh animation | **MISSING** |
| Android APK chạy và nghiệm thu | **MISSING** |

## CP328 — bước tiếp theo

1. Lấy lại file source gốc ORA/PSD/KRA nếu có (Drive hiện chưa tìm thấy) hoặc **vẽ lại native face master đủ pixel theo ảnh CANON V2**. Không tự tăng tỷ lệ +17% lần nữa; không thay màu mắt, mặt, tóc, trang sức.
2. Hoàn thiện **underpaint tự nhiên và attachment mắt/mí/mày/miệng thật**, không dùng ảnh inpaint hoặc vector demo CP326. Mỗi biểu cảm dùng cùng nhân dạng, thay đổi đủ rõ sắc thái đã chốt.
3. QA chân dung trong UI game ở 132px/64px, góc Front/3⁄4 và clipping, mesh overlap; đối chiếu 5 cảm xúc.
4. **Chỉ sau nghiệm thu art** mới xuất atlas Spine 4.1 / Unity hoặc renderer Android đích, gắn vào nhân vật, kiểm pose × wardrobe × integrity; build APK và test thiết bị.

**Không cần hỏi duyệt lại CANON V2 hay bộ 5 biểu cảm. Preview mỹ thuật CP327 không phải đề nghị tự đổi canon.**
