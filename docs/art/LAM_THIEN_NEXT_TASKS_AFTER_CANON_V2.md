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


## P1-03 — 5 biểu cảm đã CHỐT (2026-10-29)

- [x] **Preview năm biểu cảm đã được người dùng duyệt:** `shy`, `angry`, `pain`, `embarrassed`, `alluring` của Lâm Thiển; ảnh SHA256 `ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7` được sao lưu vào Approved References. **Không cần hỏi duyệt lại hình này.**
- [x] Tạo [spec APPROVED](LAM_THIEN_FIVE_EXPRESSIONS_APPROVED_2026_10_29.md), [metadata đã duyệt](LAM_THIEN_FIVE_EXPRESSIONS_APPROVED_2026_10_29.json), liên kết trong Design Registry/Model Card V2 và [global standard](GLOBAL_CHARACTER_EXPRESSION_STANDARD_2026_10_29.md).
- [ ] **Vẽ face layer thật theo body/face CANON V2** cho cả 5 nét mặt, giữ mắt/tóc/màu da/nét nhận diện. Cần chân mày, mí, mắt, miệng, blush/tear theo từng loại; không copy poster thành sprite.
- [ ] **Rig và QA:** chuyển `expression` qua Front/3⁄4 và giao diện hội thoại cỡ nhỏ; kiểm 5 nét phân biệt rõ; không reset wardrobe/integrity/pose; test animation/Spine trên asset thật.
- [ ] **Nhân vật khác**: tạo bộ preview riêng năm cảm xúc dựa trên canon/tính cách của từng nhân vật (đầu tiên có thể là Tô Nguyệt Ly), phải duyệt riêng; không chép art Lâm Thiển.
- **Phân biệt:** P1-03 mới **được duyệt về hướng art 5 biểu cảm**, chưa phải `DONE` kỹ thuật, không làm thay đổi P0-02/P0-03 chưa hoàn thành hoặc P1/P2 khác.


## CP324 — 5 biểu cảm: Android state & QA (2026-10-29)

- [x] Thêm `character_expression_profiles.json` và `CharacterExpressionCatalog.kt` dùng đúng năm mã biểu cảm **đã duyệt** của Lâm Thiển, không auto approve/copy art sang Tô Nguyệt Ly.
- [x] Thêm 5 nút chọn biểu cảm + nút reset `normal` trong `CharacterInteractionActivity.kt`. Sửa hành vi **đổi pose/mở wardrobe tự đặt lại biểu cảm**; giữ state độc lập theo `characterId`.
- [x] `resolveSprite` kiểm đúng `expression × wardrobe × integrity × pose`, trả thiếu ảnh nếu sprite chưa có, không dùng nhầm ảnh nền/ảnh 100%.
- [x] Tạo 10 crop nguyên pixel từ preview 5 biểu cảm đã chốt, ZIP có SHA và manifest, lưu tại Library Approved References; ảnh chỉ tham khảo.
- [x] Kiểm resolver trong môi trường Kotlin mock: 11/11 PASS. Đã commit Python tests/CI workflow, **chưa có bằng chứng Github Actions PASS hay APK mới**.
- [ ] **P1-03 sprite/rig/animation** chưa hoàn thành: cần vẽ face layers thật dựa CANON V2, QC ảnh nhỏ, Front/3⁄4 và integration/Spine. P0-02/P0-03 cũng chưa qua cổng art.
- **Tiếp tục:** [CP324 handoff](LAM_THIEN_CP324_EXPRESSION_RUNTIME_HANDOFF.md) → dựng face sprites V2 → QA dưới góc nhìn hội thoại và lưu game → Spine/APK. Không hỏi duyệt lại 5 nét mặt.


## CP325 — OpenRaster vùng biểu cảm từ preview APPROVED (2026-10-29)

- [x] Tạo **5 file ORA chỉnh sửa được** từ chính ảnh 5 biểu cảm đã chốt, tổng cộng **35 vùng ảnh có alpha pixel thật** (7 vùng/biểu cảm: 2 mắt, 2 mày, 1 miệng, 2 má); mỗi file còn có nguồn reference gốc ở layer ẩn. Kích thước native chỉ 285–303×385. Những layer này là **pixel patch feather từ ảnh phẳng, không phải bộ phận khuôn mặt độc lập để rig**.
- [x] Tạo biểu đồ vùng ảnh, bảng thu nhỏ thoại 132/64px, manifest SHA và QA mã nguồn. **5/5 local tests PASS**, chạy `--strict` bị chặn như thiết kế do chưa có sprite V2.
- [x] Lưu ZIP + ảnh QA tại `/Thanh Van Ky/Development/CP325_Face_Region_Prototypes/`, tạo [CP325 handoff](LAM_THIEN_CP325_FACE_ART_HANDOFF.md), [manifest](LAM_THIEN_CP325_FACE_REGION_PROXY_MANIFEST.json), `tools/cp325/validate_cp325_face_proxies.py`, metadata tests/CI workflow. GitHub Actions chưa được xác minh.
- [ ] **P1-03 vẫn CHƯA XONG:** cần vẽ/tách **mắt/mày/miệng thật theo CANON V2** với underpaint/alpha đúng, dùng quy chuẩn biểu cảm làm đối chiếu, thử hội thoại/Spine thật. Không đăng ký patch CP325 như `sprite_paths`.
- [ ] **P0-02/P0-03 giữ trạng thái chưa hoàn thành:** cần full-body Front/Back đủ độ phân giải, artwork 15 lớp thật đúng V2, điểm neo và QA.
- **Điểm tiếp tục:** CP326 dựng face sprites V2 độc lập và kiểm composite 5 trạng thái. Không cần chốt lại thiết kế concept đã được duyệt; asset mới cần QA riêng.


## CP326 — lớp nét mặt độc lập từ CANON V2 (2026-10-29)

- [x] Trích nguồn face V2 thật (bbox `[1160,0,1390,114]`, **native chỉ 230×114 px**, SHA canon giữ nguyên); tạo nền inpaint **thử nghiệm**, không coi là underpaint đã duyệt.
- [x] Vẽ mới **35 thành phần alpha** (7 vùng × 5 biểu cảm) bằng nét vector tự dựng, không cắt da/tóc từ sheet biểu cảm như CP325; đóng gói **5 OpenRaster độc lập** + contact preview, manifest SHA, script tạo lại và QA.
- [x] Local QA `tools/cp326/test_cp326_face_local.py`: **6/6 PASS**. Kiểm ORA CRC/lớp/alpha/compositing bằng `tools/cp326/validate_cp326_face.py`; `--strict` FAIL đúng dự kiến. ZIP và công cụ lưu Library Development `/Thanh Van Ky/Development/CP326_Vector_Face_Prototype/`.
- [ ] **Art P1-03 CHƯA ĐẠT:** nét mắt/môi hiện khác phong cách hình biểu cảm đã duyệt, underpaint inpaint còn lỗi, nguồn quá nhỏ và chưa có full-body layer canonical. **Cấm** đưa bản CP326 demo vào `sprite_paths` hoặc APK.
- [ ] **CP327 tiếp theo:** phục hồi nguồn layer art V2 độ phân giải sản xuất hoặc redraw sát V2, hoàn thiện face master và 5 bộ attachment thật, QA ảnh cỡ thoại 132/64px, ghép pose/wardrobe/damage rồi chạy Spine thực.
- **Bàn giao:** [CP326 handoff](LAM_THIEN_CP326_FACE_VECTOR_HANDOFF.md), [manifest](LAM_THIEN_CP326_VECTOR_FACE_MANIFEST.json). Không chốt lại mẫu 5 nét mặt đã duyệt; không thay hình thể V2/tỷ lệ +17%.


## CP327 — texture atlas 35 phần nét mặt (2026-10-29)

- [x] Từ 5 ORA **demo CP326**, xuất **35 layer** đã cắt alpha thành atlas RGBA 2048² + JSON bbox/offset, preserve exact `expression × part`; có nguồn ZIP bền vững trong Library Development.
- [x] **Phát hiện + sửa** alpha-composite vô tình đổi RGB layer má bằng direct pixel paste; 35/35 region so đúng bytes từ ORA, atlas non-overlap, SHA và reproducible; **5/5 local tests PASS**.
- [x] Bảng [so sánh canon/approved/draft](LAM_THIEN_CP327_RIG_ATLAS_HANDOFF.md) cho thấy poster concept CP327 **không đạt**: mắt không đúng V2, khác face và phụ kiện. Không dùng thay mẫu chính thức.
- [x] Thêm [CP327 handoff](LAM_THIEN_CP327_RIG_ATLAS_HANDOFF.md), [manifest](LAM_THIEN_CP327_ART_GATE_MANIFEST.json), exporter/validator và GitHub Actions kiểm metadata.
- [ ] **Mỹ thuật P1-03 CHƯA ĐẠT:** chưa có full-resolution **CANON V2 face master**, underpaint được duyệt, mắt/mày/miệng layer chất lượng anime cuối; atlas prototype **không được** dùng làm Spine production/Android asset.
- [ ] **CP328 (ưu tiên):** khôi phục/vẽ lại source V2 face thật ở độ phân giải sản xuất, chi tiết mắt hổ phách/tóc/phụ kiện đúng, 5 biểu cảm được duyệt → chỉnh face alpha/underpaint → QA nhỏ trong game → Spine/APK.
- Mẫu V2 và 5 cảm xúc, tỷ lệ +17% và mức damage 100/70/50/30 **giữ nguyên**; P0-02/P0-03/P1-03/P2 còn chờ nghiệm thu.


## CP328 — QA khóa màu mắt CANON V2 (2026-10-29)

- [x] Kiểm SHA nguồn mặt V2; xác định crop native `230×114`, hai vùng mắt hổ phách với 124/105 pixel amber-matching, **0** blue-matching; đây là phép kiểm heuristic có thể lấy mẫu cả da, không phải màu mống mắt tuyệt đối.
- [x] Tạo `tools/cp328/cp328_face_color_gate.py`, test source + ảnh ứng viên theo ROI do artist định nghĩa. **9/9 local tests PASS** gồm mô phỏng mắt xanh bị chặn; bảng kiểm tra so canon và 5 nét được duyệt.
- [x] Lưu [CP328 handoff](LAM_THIEN_CP328_FACE_IDENTITY_HANDOFF.md), [gate manifest](LAM_THIEN_CP328_FACE_MASTER_GATE.json), ZIP tại ChatGPT Library Development; source tests & CI workflow ghi trên GitHub. **Không đổi nguồn V2 / biểu cảm / damage**.
- [ ] **CP329:** làm face master art thật native high-res, mắt hổ phách, tóc/phụ kiện/bố cục V2, underpaint do họa sĩ hoàn thiện; tạo 5 nét trên cùng khuôn mặt và sprite alpha tách lớp; QA ở khung thoại/góc Front và 3⁄4.
- [ ] **Rig/Spine/APK** chờ art nghiệm thu. Các concept CP328 nháp, dù có text “production-ready” do model vẽ, **không được dùng làm asset**. P0-02/P0-03/P1-03/P2 vẫn mở.


## CP329 — Face Master Intake theo hai nguồn đã duyệt (2026-10-29)

- [x] Tạo 6 ORA chỉnh sửa được: **1 face master 11 slot + 5 expression 7 slot mỗi loại**. Khóa source CANON BODY V2 và sheet biểu cảm (SHA256), hai eye ROI và tọa độ chuyển từ native crop `230×114` sang canvas guide `2048×2048`. Bảng đối chiếu CP329 ghi rõ mặt V2 khác **mẫu sắc thái**.
- [x] **6/6 ORA PASS cấu trúc**, 8/8 bài test local PASS; mode production `--strict` cố ý chặn vì **0/46 layer mỹ thuật được vẽ**, không có underpaint thực hoặc duyệt asset cuối.
- [x] Lưu ZIP, PNG QA và mã/manifest trong Library Development `/Thanh Van Ky/Development/CP329_Face_Master_Intake/`; commit công cụ và CI GitHub `cp329-face-art-intake.yml`. CI metadata/synthetic CP329 **SUCCESS** run `40812464457`.
- [ ] **P0-02/P0-03 và P1-03 CHƯA HOÀN THÀNH:** cần redraw high-resolution đúng V2 và đưa *nội dung art thật* vào các lớp để QA; không nhầm x8 guide hoặc poster AI với HD art.
- [ ] **CP330 (tiếp):** vẽ face master/underpaint sạch, vẽ 35 lớp nét mặt thật phù hợp 5 cảm xúc (mắt hổ phách), test ở 256/132/64 và góc Front/3⁄4, duyệt sprite art → Spine → Android APK. Không cần hỏi lại V2, +17%, damage 100/70/50/30, hay 5 biểu cảm đã chốt.
- **Đầu mối:** [CP329 handoff](LAM_THIEN_CP329_FACE_MASTER_HANDOFF.md) · [manifest](LAM_THIEN_CP329_FACE_INTAKE_MANIFEST.json). `sprite_paths` vẫn **chưa đăng ký** vì game art chưa hoàn thiện.


## CP330 — Kết quả 5 ORA phân rã vùng mặt có alpha thật (2026-10-29)

- [x] 5 mặt nháp riêng kích thước **native 251–260×370 px**, tạo 5 ORA có **7 layer vùng nét mặt có alpha/ảnh thật** mỗi file (35 layer) + `face_base_cutout` + underpaint tự động + source guide ẩn.
- [x] QA local **9/9 PASS**: nội dung vùng ảnh, đúng source SHA, composite pixel-perfect với ảnh nháp, cutout không chồng, thử chuyển dịch mắt/miệng không tạo lỗ alpha. Production gate `--strict` **FAIL đúng** vì không đạt điều kiện art chính thức.
- [x] Sao lưu gói ZIP, preview, generator, QA và manifest vào Library Development. [CP330 handoff](LAM_THIEN_CP330_FACE_TRIAL_HANDOFF.md), [art manifest](LAM_THIEN_CP330_ART_TRIAL_MANIFEST.json).
- [ ] **Năm mặt khác nhau, không phải một face master**; chưa khớp hoàn toàn CANON V2, underpaint còn cần vẽ lại, bản 250px không phải native HD. **Không** đưa vào `sprite_paths` hay rig Spine.
- [ ] **CP331 ƯU TIÊN:** tạo face master duy nhất đúng V2 ở độ phân giải thật; vẽ lại mắt/mày/miệng/má 5 trạng thái có alpha sạch + underpaint, thử dialogue/avatar và biến dạng ở Front/3/4 → nghiệm thu sprite art rồi mới Spine/APK.
- Không chốt lại 5 biểu cảm, V2, tỷ lệ +17% hoặc damage 100/70/50/30; chỉ nghiệm thu **asset thực sự được sản xuất**.
