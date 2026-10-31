# Thanh Vân Ký — CP332: Semantic Face Layer Study / Lâm Thiển

**Ngày 29/10/2026 — Kết quả kỹ thuật: HOÀN THÀNH. Trạng thái mỹ thuật: CHƯA ĐƯỢC DUYỆT. Spine/APK: CHƯA THỰC HIỆN.**

## Quyết định đã chốt cần giữ nguyên

- **CANON V2 chính thức:** `LT_CANON_BODY_REF_2026-10-28_V2`, ảnh SHA-256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711`; mắt **hổ phách**, tóc bạc dài và trang phục/phụ kiện trắng–xanh–vàng, tỷ lệ +17% **đã** có trong V2.
- **5 biểu cảm chính thức:** `LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED`, ảnh SHA-256 `ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7`; `shy, angry, pain, embarrassed, alluring`. Chỉ dùng để chỉ dẫn sắc thái, **không đổi danh tính khuôn mặt V2**.
- Bốn mức hư hại 100/70/50/30 và độc lập `wardrobe / integrity / pose / action / expression` không thay đổi.

## CP331 → CP332: cải tiến thực sự

CP331 có cùng một raster master nhưng nền vẫn **baked sẵn mắt/mày/miệng**, và các `eye`/ `mouth` layer còn là crop có da/tóc. CP332 thử một hướng mới: **vẽ bằng các vector path độc lập** với nền da hoàn chỉnh và *không có* mắt/mày/môi sẵn.

- **Một OpenRaster face master** gồm **10 layer nền** thực: tóc sau, trang phục phần vai, cổ, tai, da nền mặt, mũi/điểm neo, tóc trước, lọn tóc bên, hoa/phụ kiện vàng, choker/jewel.
- **Năm OpenRaster biểu cảm** (`shy, angry, pain, embarrassed, alluring`), mỗi ORA giữ lại 10 layer master **trùng hash** và thêm **13 attachment RGBA alpha riêng**, tổng **65 layer nét mặt**: má trái/phải, phần trắng mắt trái/phải, hai mống mắt hổ phách, hai viền mi, hai mí, hai chân mày và miệng.
- Các layer được xây từ SVG vector gốc **1024×1024**, không phải ảnh crop 250px hoặc poster được phóng to. **Độ phân giải output không có nghĩa đã đạt chất lượng anime/giống V2**.
- **Clean underpaint**: trên base không có nét mắt, lông mày hoặc miệng cũ. Da mặt có alpha liên tục dưới vùng mắt và môi. Tóc được xếp chồng trên các attachment để che đúng thứ tự.
- Có `source/svg` để chỉnh đường nét từng phần, `source/png` RGBA thật, `ora/` gồm sáu OpenRaster, `preview/` gồm ảnh so năm trạng thái và bản master không nét mặt, `reference/` chứa crop canon native và sheet cảm xúc đã duyệt.

## QA thực tế đã làm

- Đã mở trực tiếp **6 ORA**, kiểm ZIP CRC, OpenRaster mimetype, XML stack, kích thước PNG/alpha 1024×1024, **10 layer base giống byte giữa 5 bản**, và composite từ layer khớp mergedimage.
- **10/10 unit test local PASS**, bao gồm 65 attachment không rỗng, 5 composite khác nhau, cấu trúc base không có mắt/môi baked, alpha da vùng mắt/môi đủ và sắc mắt hổ phách (không xanh dương).
- `python source/validate_cp332.py --root . --strict`: **bị chặn đúng thiết kế** vì art chưa được người dùng duyệt và chưa có Spine/APK.
- GitHub workflow `.github/workflows/cp332-semantic-face-contract.yml` chỉ kiểm metadata/vector drawing synthetic. **ORA binary ở ChatGPT Library không nằm trong GitHub runner**; kết quả CI (nếu SUCCESS) không thay thế QA mỹ thuật.
- Chi tiết kỹ thuật: [manifest CP332](LAM_THIEN_CP332_SEMANTIC_STUDY_MANIFEST.json), `tools/cp332/build_cp332.py` và `tools/cp332/validate_cp332.py`.

## Điểm yếu còn cần xử lý

1. Mặc dù là **vector mới**, nét tạo hình **đơn giản, phẳng, không đạt phong cách anime CANON V2**; không được chuyển vào Approved References hoặc game.
2. Tỷ lệ mặt, mắt, mũi, tóc và phụ kiện cần **redraw/polish** theo V2 gốc. Bản vector là *technical geometry study* chứ **không** phải new canonical head model.
3. Chưa có các góc Front 3/4, Side hay Back phù hợp rig thực tế, chưa có đầy đủ underpaint tóc khi xoay/mesh, chưa QA facial features khi biến dạng vượt bài test cơ bản.
4. Chưa có `sprite_paths` production, Spine skeleton/mesh/blink/mouth animation hay APK được build/test. Trạng thái P0-02/P0-03/P1-03/P2 không thay đổi sang DONE.
5. Bất kỳ poster AI CP332 nào có chữ *Production Ready* cũng **không phải bằng chứng** tạo sprite/Spine; bản họa tiết mới chỉ phục vụ tham khảo nét vẽ.

## Gói bàn giao có thật

- **ZIP:** `TVK_LamThien_CP332_Semantic_Face_Study_NOT_APPROVED.zip`.
- **SHA256:** `a70a383076592c986bd887bd4477c71b6c60f9bf13a3e711b9c20b1376dbeb01`.
- **173 tệp trong ZIP**, CRC PASS (bộ 6 ORA, các source SVG, PNG alpha, manifest, audit JSON, test, README, preview và ảnh tham chiếu); `PACKAGE_INFO.json` nằm cạnh ZIP.
- **Library backup:** `/Thanh Van Ky/Development/CP332_Semantic_Face_Study/`.
- **Art QA board:** `CP332_CANON_V2_VS_SEMANTIC_STUDY_QA.png` — một bảng đối chiếu V2/5 emotions và bản vector; gắn rõ **NOT APPROVED**.

## CP333 — hướng tiếp tục có ý nghĩa

**Ưu tiên nâng mỹ thuật thật từ cấu trúc semantic hiện có, không lặp lại việc crop/atlas kỹ thuật:**

1. Dùng CANON V2 + sheet 5 biểu cảm đã duyệt làm **nguồn thiết kế bắt buộc**; vẽ lại khuôn mặt master có chất lượng chi tiết anime thực, đúng cấu trúc mắt hổ phách và phụ kiện. Không tự tăng +17% lần nữa.
2. Chỉnh từng SVG/PNG semantic (lông mi, tròng mắt, mí, lông mày, môi, má) thành các layer art chất lượng cao, giữ nền không baked; thêm vùng skin/hair underpaint cần thiết cho animation.
3. Test composite ở kích thước hội thoại 256/132/64px, test blink/eye movement, mouth shape, front 3⁄4 và hair occlusion, đồng bộ mọi tổ hợp outfit/damage/pose.
4. Gửi **preview mỹ thuật asset thật** để người dùng duyệt — không hỏi duyệt lại CANON V2, 5 cảm xúc hay các mức hư hại.
5. **Chỉ sau khi asset được duyệt** mới export atlas Spine phù hợp và thêm `sprite_paths`, kiểm rig/animation trong engine Android, build APK và test thiết bị thật.

**Kết luận:** CP332 cải thiện đáng kể **phân lớp ngữ nghĩa thật** so với CP331, nhưng **chưa hoàn thiện nhân vật Lâm Thiển để đưa vào game**.


## GitHub Actions đã xác minh (2026-10-29)

- Workflow `CP332 semantic facial-layer source contract` run **`40819544556`**, job **`123268528135` / `source-geometry-contract`**, kết quả **SUCCESS**.
- CI kiểm trực tiếp *source SVG/Python và render alpha synthetic*, 5 mã cảm xúc, metadata nguồn đã duyệt và chặn trạng thái art chưa duyệt. **CI runner không có sáu ORA binary trong Library**; kết quả 10/10 local thực trên ORA và kiểm ZIP CRC/recomposition vẫn là bằng chứng riêng.
- **Không** suy từ workflow xanh ra việc giống CANON V2 về mỹ thuật, rig/Spine hoặc APK đã chạy.
