# CP324 — Lâm Thiển: triển khai 5 biểu cảm đã duyệt vào runtime Android (2026-10-29)

**CHECKPOINT: HOÀN THÀNH PHẦN KHAI BÁO/RUNTIME STATE; CHƯA CÓ SPRITE FACE, RIG SPINE HAY APK MỚI ĐƯỢC NGHIỆM THU.**

## Nguồn chính thức, tuyệt đối không thay thế

- **Body/face/costume CANON V2:** `LT_CANON_BODY_REF_2026-10-28_V2`, [PNG gốc trên Google Drive](https://drive.google.com/file/d/1mEsyn2wMo-MVQqhtbmdUiFfO8AaYhzUR/view?usp=drivesdk), SHA-256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711`; tỷ lệ +17% đã áp dụng từ trước.
- **Năm biểu cảm ĐÃ DUYỆT:** `LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED`, [tài liệu chính thức](LAM_THIEN_FIVE_EXPRESSIONS_APPROVED_2026_10_29.md), SHA-256 preview `ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7`.
- Năm mã cố định **`shy`, `angry`, `pain`, `embarrassed`, `alluring`** (Ngại ngùng, Tức giận, Đau đớn, Xấu hổ, Quyến rũ).
- **Không dùng** concept CP322 hoặc poster biểu cảm để thay hình mặt/body CANON V2. Các ảnh cropping chỉ là tài liệu tham khảo, chưa có layer/alpha thật.

## Phần code đã triển khai

1. **[character_expression_profiles.json](../../app/src/main/assets/character_expression_profiles.json):** đăng ký 5 trạng thái được duyệt cho Lâm Thiển với nguồn checksum, `sprite_paths={}` do chưa sản xuất. Tô Nguyệt Ly có trạng thái `individual_preview_required`, không bị gán sprite/mặt Lâm Thiển.
2. **[CharacterExpressionCatalog.kt](../../app/src/main/java/vn/thanhvanky/prototype/CharacterExpressionCatalog.kt):** chỉ trả option từ profile được duyệt; `resolveSprite` yêu cầu **expression × wardrobe × integrity × pose** khớp chính xác và đường dẫn an toàn `characters/{characterId}/...`. Không có sprite thật sẽ trả `null`, không lấy nhầm mặt trung tính hoặc trang phục 100%.
3. **[CharacterInteractionActivity.kt](../../app/src/main/java/vn/thanhvanky/prototype/CharacterInteractionActivity.kt):**
   - Bổ sung danh sách chọn 5 biểu cảm đã chốt cho Lâm Thiển; **“Bình thường” là nút trở về trạng thái trung tính đã có, không phải biểu cảm thứ sáu mới chốt**.
   - Lưu `expression` theo từng nhân vật bằng `CharacterAppearanceState`; khi chọn biểu cảm không đụng `wardrobe`, `integrity`, `pose` hoặc `action`.
   - **SỬA LỖI:** đổi tư thế trước đây tự reset biểu cảm thành `normal`/`relaxed`; đã loại bỏ hành vi này. Mở tủ đồ cũng không tự reset biểu cảm.
   - Khi biểu cảm được chọn ở góc nhìn thấy mặt mà thiếu artwork đúng tổ hợp, **ẩn ảnh không phù hợp + hiển thị thông báo thiếu sprite**. Góc nhìn mặt sau giữ state nhưng không ép render khuôn mặt đang bị che.
   - Tương tác/hội thoại được phép cố ý đổi biểu cảm theo tình huống; không được làm thay đổi outfit/integrity.
4. **[test_cp324_expression_runtime.py](../../tests/art/test_cp324_expression_runtime.py)** và **[workflow GitHub Actions](../../.github/workflows/cp324-expression-runtime.yml)** bảo vệ bộ 5, nguồn SHA/canon, giới hạn Tô Nguyệt Ly chưa duyệt và cơ chế không fallback.

## Tệp bàn giao hình tham chiếu (đã lưu vật lý)

- Tạo đúng **10 PNG crop pixel-identical** từ poster năm biểu cảm đã duyệt: 5 chân dung và 5 vùng mắt/miệng, thêm contact sheet, manifest JSON, README.
- ZIP `TVK_LamThien_CP324_Approved_Expression_Handoff.zip` SHA-256 **`d12dfa89ac0ae002095effd4d2e789d31bbcb09c23a1f4b857da29e4b906ca1a`**; nguồn gốc ảnh preview SHA-256 `ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7`.
- ChatGPT Library Approved References: `/Thanh Van Ky/Approved References/Lam_Thien_Expressions_20261029/CP324_Reference_Handoff/TVK_LamThien_CP324_Approved_Expression_Handoff.zip`.
- [Manifest tọa độ và checksum từng crop](LAM_THIEN_CP324_APPROVED_EXPRESSION_CROPS_MANIFEST.json) cho phép kiểm chứng byte; crop có nền, **không phải sprite PNG alpha tách lớp**.

## Kiểm tra đã làm & giới hạn báo cáo

- Đã đọc lại nguồn Kotlin và JSON trên GitHub sau khi commit.
- **Kotlin local stub test: 11/11 PASS** cho resolver (chỉ biên dịch resolver với mock `org.json` / `State`, không thay thế build Android).
- Metadata/nguồn approved được đối chiếu, chưa có bất kỳ `sprite_paths` thật nào.
- Python unit tests và GitHub Actions workflow **đã commit**, nhưng **chưa có bằng chứng CI GitHub đã chạy/PASS**, cũng **chưa có bản APK cập nhật được build hoặc chạy thử**. Không đánh dấu P1-03 DONE.
- P0-02/P0-03 vẫn chưa xong (source full-body/ORA layer art chưa hoàn thiện), nên hiện không có cơ sở xác nhận face sprites/Spine mesh thực.

## Bước tiếp theo — CP325 đề xuất

1. Dựng năm biến thể nét mặt trên **khuôn mặt thật CANON V2**, không sao chép crop poster vào rig. Tách `face_base`, `eye_left/right`, `brow_left/right`, `eyelids`, `mouth`, `blush`, `tear_small` (khi có).
2. Đối chiếu `shy`–`embarrassed`, `angry`–`pain`, `alluring`–`shy`; thử trong khung thoại thu nhỏ. Chốt riêng sản phẩm **sprite/alpha thật**.
3. Sau khi có cả model/wardrobe/integrity/pose art đúng nguồn, đăng ký đúng đường dẫn trong `sprite_paths`. Không đăng ký đường dẫn giả hoặc lấy hình cũ thay.
4. Kiểm chuyển biểu cảm nhanh, thay pose/trang phục, save/load; sau đó rig/animation Spine, GitHub CI, Android build APK, kiểm thử thiết bị.

**Không cần hỏi lại việc chốt năm biểu cảm**; đã được duyệt. Các nhân vật khác dùng [quy chuẩn chung](GLOBAL_CHARACTER_EXPRESSION_STANDARD_2026_10_29.md) nhưng duyệt art riêng theo canon riêng.
