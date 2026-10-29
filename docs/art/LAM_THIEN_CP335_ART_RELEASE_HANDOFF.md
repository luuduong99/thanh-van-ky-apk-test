# Thanh Vân Ký — CP335 | Art release gate và đối chiếu 5 biểu cảm Lâm Thiển

**Ngày:** 2026-10-29  
**Kết quả:** ĐÃ TRIỂN KHAI CƠ CHẾ KHÓA ART CHƯA DUYỆT TRONG ANDROID + KIỂM FILE THẬT TRƯỚC RELEASE.  
**Tình trạng mỹ thuật:** CHƯA ĐỦ ĐIỀU KIỆN. **Spine/APK:** CHƯA BUILD/NGHIỆM THU.

## A. Hai nguồn đã duyệt, đúng thứ tự ưu tiên

1. **CANON V2 ngoại hình** `LT_CANON_BODY_REF_2026-10-28_V2`, SHA256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711`: mặt, tóc bạc, mắt hổ phách, hoa cài, phụ kiện, trang phục trắng–xanh–vàng, tỷ lệ +17% đã được tích hợp.
2. **Bộ 5 biểu cảm đã chốt** `LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED`, SHA256 `ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7`: `shy / angry / pain / embarrassed / alluring`. Đây là chuẩn **sắc thái biểu cảm**; nếu ảnh sheet có mắt xanh hoặc trang phục khác, vẫn ưu tiên ngoại hình V2.
3. Không đổi bốn mức nguyên vẹn trang phục `100/70/50/30` hoặc quy tắc độc lập `expression / wardrobe / integrity / pose / action`.
4. Nhân vật khác dùng quy chuẩn **phân biệt rõ năm cảm xúc**, nhưng hình và độ nhấn phải tùy tính cách từng người; không sao chép nguyên model Lâm Thiển.

## B. Thực tế bản preview mới CP335

- Đã tạo bản bảng minh họa CP335 **1536×1024 RGB phẳng**, SHA256 `7935e04f5fa04c3bd9d772577ad7ddbc806a9e5723629d8b963bb0611d7315d1`, và bảng **đối chiếu nguồn** `CP335_SOURCE_PRIORITY_VISUAL_GATE.png`.
- Bản mới thể hiện năm cảm xúc tương đối rõ, màu mắt ấm, độ chi tiết cao hơn vector CP333. **Nhưng** viền áo/trang sức vàng/hoa cài và một số chi tiết cấu trúc mặt khác CANON V2; không chứng minh năm tư thế dùng cùng master.
- Các ô *Layer/Atlas/Production Ready/Spine* vẽ sẵn trong poster **chỉ là hình pixel**, KHÔNG phải PNG alpha từng bộ phận, ORA semantic, texture atlas hay Spine skeleton đã tạo. **Không thay thế CANON V2, không đăng ký sprite.**
- Tạo `CP335_DIALOGUE_THUMBNAIL_QA.png` để đánh giá ở kích thước 132/64px. Cả hai preview là tư liệu Development, **không phải art sản xuất đã được người dùng duyệt**.

## C. Lỗi thật tìm thấy và sửa ở Android

**Trước CP335:** `CharacterExpressionCatalog.resolveSprite` chấp nhận một đường dẫn `sprite_paths` nếu ID biểu cảm nằm trong danh sách user-approved và file có mặt. Điều này chưa yêu cầu **phê duyệt riêng file sprite thành phẩm**. Một bảng biểu cảm được duyệt không đồng nghĩa sprite được phép đi vào game.

**Đã sửa:**

- `app/src/main/java/vn/thanhvanky/prototype/CharacterExpressionCatalog.kt` thêm cổng `production_release`, bắt buộc `status=approved_for_runtime`, `artist_qa_passed=true`, `runtime_qa_passed=true`, `user_asset_approval_id` có thực, ID + SHA đúng CANON V2/5 biểu cảm, manifest SHA256 và hash cho đúng từng PNG.
- Bộ resolver vẫn kiểm **`characterId × expression × wardrobe × integrity × pose` chính xác**, không fallback sang trang phục 100% hoặc mặt trung tính, chặn path traversal.
- `app/src/main/assets/character_expression_profiles.json` khai báo rõ **`production_release.status=blocked_pending_art`**, tất cả `sprite_paths={}`; Lâm Thiển vẫn **được duyệt 5 ý tưởng biểu cảm**, Tô Nguyệt Ly vẫn **chưa có art 5 nét được duyệt riêng**. Không giả việc đã có asset mới.

## D. Kiểm thử trên mã và ảnh thực

1. **17/17 Kotlin unit scenario PASS** trên compiler `kotlinc` với JSON/State stub, gồm trường hợp path có thật nhưng release chưa duyệt **phải từ chối**; đúng canon/SHA/QA/user approval thì mới trả ảnh; cấm fallback và path traversal. **Không phải Android Gradle build.**
2. **14/14 Python tests PASS**, dùng PNG RGBA tổng hợp được lưu/đọc thật: kiểm manifest, SHA, hình thiếu, đường dẫn lạ, asset trùng giữa các mức integrity, mode RGB sai, ảnh native quá nhỏ, alpha giả, thiếu user acceptance, thiếu QA.
3. `tools/verify_expression_art_release.py` dùng trong GitHub CI: khi chưa có art thì đảm bảo path **trống**, khi có art thì sẽ đọc actual `app/src/main/assets/characters/.../*.png` để đối chiếu **SHA256 chính xác**, kích thước nhỏ nhất từ 512 px, alpha RGBA có ý nghĩa, manifest SHA và kết quả QA.
4. **GitHub Actions run `40823727298`: SUCCESS** cho CP335 facial art release gate; workflow CP324 và expression consistency cũng SUCCESS trên lần chạy liên quan. CI không kiểm mỹ thuật, rig hoặc APK.
5. Không tạo bất cứ `approved_sprite_hashes` giả nào; trạng thái production là **BLOCKED** theo thiết kế.

## E. File bàn giao và checksum

- **ZIP:** `TVK_LamThien_CP335_Art_Release_Gate_NOT_APPROVED.zip` SHA256 `d656146585681ce1a5b05d322fdab3a12eccb2c5f21b2afd6cc9e9d773dcf2df` (16 file, ZIP CRC PASS).
- Backup: ChatGPT Library `/Thanh Van Ky/Development/CP335_Art_Release_Gate/`.
- ZIP gồm: 2 PNG approved nguyên bytes, 1 PNG candidate flat, 2 bảng preview QA, manifest nguồn, Kotlin resolver/test, Python validator/test, cấu hình mẫu `NEXT_PRODUCTION_ART_ACCEPTANCE_TEMPLATE_NOT_APPROVED.json`.
- GitHub: [candidate manifest](LAM_THIEN_CP335_VISUAL_GATE_MANIFEST.json), `tools/verify_expression_art_release.py`, `tests/art/test_cp335_release_gate.py`, `tests/art/test_cp335_reference_gate.py`, `.github/workflows/cp335-expression-production-gate.yml`.

## F. CP336 — việc bắt buộc để thực sự có art cho game

1. Không tiếp tục lặp bảng poster “Production Ready” hoặc cắt 5 vùng bằng crop rồi gọi sprite. **Cần một face master high-fidelity native** thực tế đúng hình CANON V2, có hai góc **Front + 3/4** và cùng nhận diện.
2. Vẽ lại `hair_back / hair_front / face_underpaint / eye_left/right / iris / lashes / lids / brows / mouth / blush` bằng art độc lập sạch, không còn mắt/miệng in sẵn trong nền. Tạo layer tóc/da ẩn cho chuyển động, có nguồn edit ORA/PSD/SVG.
3. Tạo đủ `shy, angry, pain, embarrassed, alluring` từ **cùng face master**, đúng chuẩn biểu cảm đã duyệt nhưng mắt vẫn **hổ phách**; QA ở 256/132/64px và thử blink/mouth/occlusion.
4. Sau khi người dùng **duyệt asset art thành phẩm** (KHÔNG hỏi lại quyết định CANON V2/5 nét mặt) và có bằng chứng artist QA, mới khai báo `sprite_paths`, `production_release`, SHA từng file; chạy **CP335 release gate** rồi Spine/Android APK/test thiết bị.

**Không được báo hoàn thành P0-02/P0-03/P1-03/P2 từ CP335.** CP335 là tiến độ thực ở việc **chặn art chưa duyệt xuất hiện trong game**, còn phần vẽ thực vẫn thiếu.
