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



## CP320 — đã chuẩn bị contract, tiếp tục P0-02/P0-03 (2026-10-28)

- [x] Đã kiểm tra nguồn CANON BODY V2 trên Drive và **lưu bản PNG preview hư hại được duyệt** vào ChatGPT Library; SHA-256 giữ nguyên như trong [tài liệu approved damage](LAM_THIEN_DAMAGE_PREVIEW_APPROVED_2026_10_28.md).
- [x] Khởi tạo [ma trận view/pose/layer và mốc đo](LAM_THIEN_CP320_VIEW_CALIBRATION.json) + [công cụ kiểm tra CP320](../../tools/check_lam_thien_cp320.py) + unit test.
- [ ] **P0-02 giữ trạng thái CHƯA HOÀN THÀNH:** cần full-body source thực để điền bảy mốc/ảnh ở từng view, preview được duyệt và đối chiếu CANON V2.
- [ ] **P0-03 giữ trạng thái CHƯA HOÀN THÀNH:** cần bộ PNG alpha/ORA/PSD và QA draw-order, seam, underpaint; không thay bằng ảnh crop hoặc poster.
- [ ] **P1-02A**: mẫu độ bẩn/xước/rách đã duyệt ở cấp **hướng dẫn hình ảnh**, chưa hoàn thành texture cho Front + Back riêng theo CANON V2 và wardrobe × integrity × pose.
- **Điểm tiếp tục:** làm Front–Back chuẩn V2 trước, Side/3⁄4 tiếp theo, nhập mốc, tách layer và QA. [Handoff CP320](LAM_THIEN_CP320_HANDOFF.md). Không đóng checkpoint khi chỉ mới có khai báo JSON.



## CP321 — khung ORA Front/Back đã kiểm tra (2026-10-28)

- [x] Tạo/sao lưu template ORA Front và Back; mỗi file canvas 2048×3072, 15 layer art RGBA + 1 guide. CRC và kích thước đã kiểm tra trực tiếp, kết quả PASS.
- [x] Tạo công cụ `tools/validate_lam_thien_cp321_ora.py` và unit test; `--strict` dùng chặn nghiệm thu thiếu art.
- [ ] **P0-02 CHƯA ĐẠT**: còn thiếu hình full-body riêng biệt và 7 mốc đo trực tiếp cho các góc nhìn, không lấy tọa độ từ các crop poster ~100–160px.
- [ ] **P0-03 CHƯA ĐẠT**: kiểm alpha trực tiếp cho thấy **0/15 art layer có pixel ở Front, 0/15 ở Back**. Cần vẽ art thật, kiểm underpaint, occlusion, seam, tỷ lệ và nhận duyệt.
- **Điểm tiếp tục:** hoàn thiện ảnh full-body Front/Back theo V2 → nhập landmark → đổ layer vào ORA → kiểm QA → mới mở rig. Xem [CP321 handoff](LAM_THIEN_CP321_HANDOFF.md).


## CP322 — thử nghiệm PNG alpha 5 view, KHÔNG PHẢI art đã duyệt (2026-10-28)

- [x] Đã tạo gói **technical alpha trial**, 5 PNG RGBA native-resolution, manifest/checksum, thử nghiệm compositing và test PNG alpha đọc pixel thật (local: 4/4 unit tests PASS). Lưu riêng tại ChatGPT Library `/Thanh Van Ky/Development/CP322_Alpha_Trial/`.
- [x] Commit `tools/validate_lam_thien_cp322_proxy.py`, `tests/art/test_lam_thien_cp322_proxy.py`, `LAM_THIEN_CP322_ALPHA_TRIAL_MANIFEST.json` với cờ `NOT_APPROVED`; production strict gate không cho dùng nhầm concept.
- [ ] **P0-02 CHƯA ĐẠT**: 5 hình thử không khớp đủ ngoại hình CANON V2 và quá nhỏ để dùng rig; cần vẽ lại theo V2 và gửi preview.
- [ ] **P0-03 CHƯA ĐẠT**: PNG alpha cả nhân vật không phải 15 layer riêng biệt; ORA Front/Back vẫn 0/15 art layer thật, cần phân lớp đúng và QA.
- **Tiếp tục:** Front/Back đúng CANON V2 → Side/3/4 → 7 landmark → layer ORA thực → QA. Xem [báo cáo CP322](LAM_THIEN_CP322_ALPHA_TRIAL_HANDOFF.md). Không thay reference đã chốt hay 4 mốc hư hại.


### CP322 — bổ sung kết quả kiểm thử

- [x] 5/5 PNG alpha qua kiểm tra PNG IDAT/CRC và occupancy; **4/4 unit tests local PASS**.
- [x] Lưu bản concept thử không duyệt và ZIP alpha tại Library Development, **không thay V2 canon**.
- [x] Tạo workflow `.github/workflows/cp322-art-alpha-validation.yml`.
- [ ] Kết quả GitHub Actions chưa xác minh; art chuẩn V2, 15 layer thật và rig vẫn còn mở.


## CP323 — kiểm thử OpenRaster bằng pixel alpha thật (2026-10-29)

- [x] Tạo `tools/validate_lam_thien_cp323_layers.py` và `tests/art/test_lam_thien_cp323_layers.py`: giải mã PNG thật để đếm pixel alpha hữu hiệu, phát hiện layer trống/trùng/nguồn lỗi, kiểm CRC, source path, canvas 2048×3072, guide có bị hiển thị.
- [x] Chạy local **5/5 unit test PASS**. Audit **hai ORA CP321**: cấu trúc PASS nhưng **0/15 art layer có pixel** ở Front lẫn Back, `--strict` trả FAIL đúng kỳ vọng. ZIP báo cáo và ảnh QA đã lưu trong ChatGPT Library Development.
- [x] Thêm workflow `.github/workflows/cp323-openraster-art-gate.yml`. Kết quả chạy GitHub Actions chưa kiểm chứng, không đánh dấu CI PASS.
- [ ] **P0-02 chưa hoàn thành**: chưa có Front/Back full-body riêng biệt, high-resolution *đúng CANON V2*, chưa có 7 điểm neo đo từ full-body thật.
- [ ] **P0-03 chưa hoàn thành**: ORA vẫn rỗng, cần vẽ thành phần nhân vật thực, QA mặt/tóc–gáy–vai, underpaint/tay áo/draw-order và chốt visual.
- **Tiếp tục bắt buộc:** hoàn thiện art Front/Back theo mẫu V2 hiện hành → gửi preview để duyệt → nhập 7 landmarks → vẽ/tách layer → chạy strict gate + art QA thủ công → Spine; ảnh AI thử nghiệm không được xem là model canon.
- Xem [CP323 handoff](LAM_THIEN_CP323_HANDOFF.md). Không chấm P0 đạt chỉ vì có thêm script hoặc ORA rỗng.


## P1-03 — bổ sung review 5 biểu cảm (2026-10-29)

- [x] Đã tạo **preview chờ duyệt** và [đặc tả 5 biểu cảm](LAM_THIEN_FIVE_EXPRESSIONS_REVIEW_2026_10_29.md) gồm: Ngại ngùng, Tức giận, Đau đớn, Xấu hổ, Quyến rũ.
- [ ] Người dùng duyệt preview/độ nhấn cụ thể; ảnh hiện tại lưu trong Library Development, không chuyển sang Approved References khi chưa xác nhận.
- [ ] Sau khi duyệt, dựng phiên bản các nét mặt đúng CANON V2, tách alpha layers mắt/mày/miệng/blush, animation Spine và QA hình nhỏ trong UI thoại.
- [ ] Chạy QA biểu cảm qua Front/3/4 và các trạng thái wardrobe, integrity, pose; không đánh dấu P1-03 xong từ ảnh concept phẳng.
- **Không đổi** bản CANON V2, tỷ lệ +17% đã tích hợp, hay mẫu hư hại 100/70/50/30.
