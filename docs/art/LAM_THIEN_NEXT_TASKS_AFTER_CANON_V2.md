# Thanh Vân Ký — triển khai Lâm Thiển theo CANON V2 (2026-10-28)

**Nguồn duy nhất cho tạo hình:** [mẫu V2 đã duyệt](https://drive.google.com/file/d/1mEsyn2wMo-MVQqhtbmdUiFfO8AaYhzUR/view?usp=drivesdk) — ID `LT_CANON_BODY_REF_2026-10-28_V2` — SHA `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711`.  
**Trạng thái:** mới chốt artwork phẳng, **chưa** có PSD/ORA/Spine rig/APK từ mẫu V2.

## P0 — khóa mẫu, chuẩn bị art gốc

- [x] **P0-01:** Lưu bản gốc nguyên byte + SHA/dimensions, sổ registry và model card. Xem file Canon V2.
- [ ] **P0-02:** Lấy mẫu chính diện, sau, side/3⁄4 đã duyệt và chuẩn hóa tọa độ cơ thể trên *cùng* hình V2. Thiết lập 5–8 mốc tọa độ rig (đỉnh đầu, cằm, vai, eo, hông, gối, bàn chân) sau khi có full-figure source đủ độ phân giải. **Không dùng B/W/H 102/60/110 làm cm hoặc chuẩn rig.**
- [ ] **P0-03:** Dựng layer thật: tóc trước/sau, mặt (mắt/miệng/blush), thân với underpaint hợp lệ, áo trong, áo ngoài, tay áo, tà váy trước/sau, chi tiết lụa và phụ kiện ít vàng. Xuất bộ PNG alpha, metadata mỗi layer, sheet kiểm tra seam/occlusion.
- [ ] **P0-04:** Dựng và **gửi duyệt preview** tám pose thiếu: Side, Front 3/4, Back 3/4, Back Turn, Bed Side Lying, Bed Sit, Chair Sit, Wall Lean. Pose giường đã chốt `bed_recline` và `bed_kneel_forward` vẫn riêng; kiểm tra tỷ lệ cơ thể không đổi qua pose.
- [ ] **P0-05:** Đối chiếu màn Anh hùng/UI ảnh chân dung đang dùng với V2; **không ép ảnh poster vào sprite** nếu chưa tách lớp/crop đúng.

## P1 — wardrobe, combat damage, animation

- [ ] **P1-01:** Tạo artwork các trang phục `default`, `outer_removed`, `private_fantasy` (tên trạng thái đề xuất kỹ thuật) từ V2, cùng silhouette, vải mềm và nội thất phù hợp, lớp lót che phủ kín. Phân biệt lớp cởi/thay với hư hại chiến đấu.
- [ ] **P1-02:** Tạo texture/slot cho `integrity=100/70/50/30` ở mỗi mức cởi và pose. 30% làm cả phần che phủ có sờn rách; không tự ý tăng +20% mức rách; test rách theo cùng cấu trúc quần áo ở mọi góc.
- [ ] **P1-03:** Bộ biểu cảm và hành động: bình thường, dịu dàng, cười, ngạc nhiên, khó xử, mệt; idle, trúng đòn, cân bằng, chỉnh áo, ngồi/nằm thư giãn. Mỗi tình huống tương ứng state; không giả đã có animation chỉ từ 1 tấm poster.
- [ ] **P1-04:** Spine/2D rig và secondary motion tóc, tay áo, vạt lụa. Test thứ tự layer, mask, draw order/physics trên texture thật; tránh vật xuyên người và đồ vật.

## P2 — logic gameplay, QA và APK

- [ ] **P2-01:** Dùng `CharacterAppearanceState.kt` cho mọi nhân vật; test tất cả mức cởi giữ khi đổi mọi pose; thiếu art đúng tổ hợp phải báo thiếu, không tự mặc lại.
- [ ] **P2-02:** Nối cơ chế chiến đấu vào trạng thái quần áo; **sát thương/HP → độ bền** cần được xác định rõ, không mặc định 70% HP = 70% trang phục. Hiển thị hình 2D khi lần đầu đến mốc.
- [ ] **P2-03:** Kiểm tra status GitHub Actions thực tế, CI, `assembleDebug`, lấy artifact APK. Test trên thiết bị thật, tốc độ/viewport ngang, khởi động lại, save/load, combat→room.
- [ ] **P2-04:** Sau khi Lâm Thiển qua các gate art/rig/gameplay, đóng gói **template tái sử dụng** cho Tô Nguyệt Ly và các nhân vật sau: skeleton conventions, slot names, layer naming, atlas/export, pose/matrix tests, art QA checklist. **Không tái sử dụng body/face và tỷ lệ +17% của Lâm Thiển cho người khác.**

## Bộ nguồn đang có để đối chiếu

- [Tạo hình V2](https://drive.google.com/file/d/1mEsyn2wMo-MVQqhtbmdUiFfO8AaYhzUR/view?usp=drivesdk) (canon mới nhất, được chốt).
- [Bảng biểu cảm/tư thế/trang phục đã ghi trước](https://drive.google.com/file/d/1M-6KIEeon7HX4Qn56UlhGMfV76Lr-sN5/view?usp=drivesdk) (bổ trợ chức năng, **ngoại hình cũ**).
- [Quy chuẩn chung mọi nhân vật](GLOBAL_CHARACTER_APPEARANCE_SPEC.md).
- [Danh mục 288 tổ hợp dự kiến 2 nhân vật](GLOBAL_CHARACTER_ASSET_BACKLOG.json) — đăng ký đường dẫn **không phải file art đã có**.

## Gate nghiệm thu

- **Art:** preview được duyệt, PNG alpha/layer thực + underpaint/seam chuẩn.
- **Rig:** file rig, bones/slots, animation/physics được xem bằng runtime thật.
- **Game:** state, UI, combat, save/load thực sự hoạt động đúng.
- **APK:** GitHub Actions/build và thiết bị Android đều kiểm chứng. Mỗi gate cần log/artifact hoặc ảnh chứng minh; không mark done dựa trên lời mô tả.


### Bổ sung P1-02A — chi tiết hiệu ứng bẩn, xước và rách

- [ ] **P1-02A.1:** Tạo bảng preview `default × 100/70/50/30` của Lâm Thiển CANON V2 cho Front + Back, phối hợp **vết bẩn, vết xước/sờn trên lụa và rách vải** theo mức độ thực tế. Duyệt mức tăng rõ ràng nhưng tự nhiên, không cộng hệ số rách cố định.
- [ ] **P1-02A.2:** Chốt điểm neo vết trên từng mảnh áo/tay áo/vạt, kiểm tra chuyển Side/3⁄4 và tư thế giường/ghế/tường không làm vết dịch vô cớ.
- [ ] **P1-02A.3:** Áp dụng các biến thể cho từng wardrobe state với chất liệu tương ứng; trường hợp không có sprite phải báo thiếu thay vì dùng ảnh 100%.
- [ ] **P1-02A.4:** QA alpha/underpaint, phối màu bẩn trên vải trắng–xanh, giữ che phủ ở 30%, rig và APK riêng. Không tự đồng nhất vết xước quần áo với thương tích trên da.

**Nguồn:** [GLOBAL_CLOTHING_DAMAGE_VISUAL_STANDARD.md](GLOBAL_CLOTHING_DAMAGE_VISUAL_STANDARD.md). `appearanceSystem.damageVisualProfile` là profile chuẩn dùng toàn game, **chưa tạo artwork thật**.

