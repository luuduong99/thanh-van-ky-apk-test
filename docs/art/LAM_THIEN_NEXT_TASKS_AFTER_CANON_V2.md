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


## CP331 — một master cố định cho năm biểu cảm, mới ở mức R&D (2026-10-29)

- [x] Tạo một base flat thống nhất kích thước native `258×364`; xuất 5 ORA có 7 patch alpha/biểu cảm (35 patch) và 5 ảnh composite, thumbnail 132/64px, GIF chuyển frame. Khác CP330 ở chỗ tóc/phụ kiện/trang phục bất biến pixel ngoài vùng mặt.
- [x] **9/9 local test PASS**, audit ORA real source + stack/CRC/nonempty alpha/composition + pixel invariance, strict art gate cố tình FAIL vì asset chưa được duyệt.
- [x] Lưu ZIP trong Library Development và [CP331 handoff](LAM_THIEN_CP331_SHARED_FACE_HANDOFF.md), [artist work order](LAM_THIEN_CP331_ARTIST_WORK_ORDER.md), công cụ Python + CI kiểm metadata.
- [ ] **Vấn đề CP332 thực sự:** master hiện chỉ là tranh mới chưa duyệt, native 258×364, có nét mắt/mày/miệng **baked**; các patch dính nền; underpaint thuật toán chưa hoàn thiện. **Không dùng làm sprite**, Spine/Android APK chưa nghiệm thu.
- [ ] **CP332:** dựng lại một face master *art HD native thật* theo CANON BODY V2, clean underpaint, 35 layer semantic cho năm cảm xúc, test avatar/dialogue 256/132/64px và Front/3⁄4, gửi preview nghiệm thu **asset mới**; sau art QA mới tích hợp và test APK.
- **Giữ nguyên:** V2, +17%, 5 sắc thái và damage 100/70/50/30; không hỏi chốt lại các tiêu chuẩn này.


## CP332 — semantic face layers mới vẽ độc lập, artist approval pending (2026-10-29)

- [x] Tạo 6 ORA binary có thể chỉnh sửa: 1 sạch **master base 10 layer** và 5 biểu cảm cùng base giữ nguyên hash. **65 layer nét mặt RGBA alpha** riêng (13/biểu cảm: mắt trắng, iris, mi, mí, mày, má, môi), không có ảnh crop skin/hair từ poster, underpaint mặt không chứa feature baked.
- [x] SVG source bản vector native 1024, PNG alpha, composite preview, bảng đối chiếu CANON V2 và năm biểu cảm APPROVED; **10/10 unit tests local PASS**, audit ZIP/alpha/recompose 6 ORA PASS; strict sản xuất **FAIL đúng kỳ vọng**.
- [x] Sao lưu gói `TVK_LamThien_CP332_Semantic_Face_Study_NOT_APPROVED.zip` SHA `a70a383076592c986bd887bd4477c71b6c60f9bf13a3e711b9c20b1376dbeb01` vào Library Development. GitHub có [handoff](LAM_THIEN_CP332_SEMANTIC_FACE_HANDOFF.md), [manifest](LAM_THIEN_CP332_SEMANTIC_STUDY_MANIFEST.json), source + CI metadata.
- [ ] **CP332 art production CHƯA ĐẠT:** khuôn mặt mới chỉ là minh họa vector đơn giản, không đủ giống CANON V2. Chưa có art Front/3⁄4 đủ chuẩn, hair deformations, Spine skeleton/animation, APK hoặc biến thể wardrobe/damage thật. Không nhập vào `sprite_paths`.
- [ ] **CP333 ưu tiên:** nâng chất lượng họa sĩ trên đúng 10 + 13 layer semantic, đảm bảo danh tính V2 + mắt hổ phách, hair/face/choker/hoa, kiểm độ rõ cả 5 biểu cảm ở 256/132/64px, đủ góc/underpaint, gửi duyệt **art thành phẩm** rồi mới nối Spine và build APK.
- **Quyết định vẫn đã chốt**: V2, +17% trong V2, năm biểu cảm, bốn mức hư hại 100/70/50/30. Không hỏi lại hoặc thay ngầm.


## CP333 — tinh chỉnh source SVG semantic (2026-10-29)

- [x] Chỉnh vector hair highlights, filigree hoa vàng, amber iris, lông mi, chân mày và môi **thực trên SVG**, không crop poster. Đã xuất **6 ORA**, 10 layer base chung và **65 attachment RGBA** (13×5); base da sạch không baked nét mặt.
- [x] **13/13 local ORA tests PASS**, 9/9 source contract local PASS, ZIP CRC PASS, strict art gate FAIL đúng kỳ vọng; nguồn CANON V2 và năm cảm xúc giữ nguyên SHA. Có before/after review + bảng kiểm 256/132/64px.
- [x] [CP333 handoff](LAM_THIEN_CP333_FACE_POLISH_HANDOFF.md), [manifest](LAM_THIEN_CP333_ART_HANDOFF_MANIFEST.json), source/validator/tests/workflow GitHub; gói ZIP SHA256 `1f8aa806758332194e258f941530b18b54e00991c877c3397a274d7c134517ad` đã sao lưu Library Development.
- [ ] **MỸ THUẬT CÒN MỞ:** vector CP333 vẫn chưa giống đủ CANON V2, thiếu Front/3⁄4, underpaint tóc cho mesh/deform, Spine và APK. Không tự điền `sprite_paths`; poster infographic có chữ “production ready” không xác nhận điều này.
- [ ] **CP334 ưu tiên:** redraw chất lượng cao **trên semantic layer đã có**, kiểm nhận diện/góc/5 nét mặt và QA ở 256/132/64px; sau nghiệm thu mỹ thuật mới rig/animation và build APK.
- **Không chốt lại:** body V2, tỷ lệ +17% đã có, 5 nét biểu cảm, 4 mốc hư hại 100/70/50/30.


## CP334 — 5 portrait ứng viên mỹ thuật và QA nguồn (2026-10-29)

- [x] Tạo 5 ảnh preview mới từ một bảng phẳng, mỗi ảnh đúng 5 mã `shy/angry/pain/embarrassed/alluring`, bảo vệ SHA của CANON V2 và sheet biểu cảm đã chốt.
- [x] Tạo bảng đối chiếu mặt V2, approved expression directions và ứng viên mới, cùng QA thu nhỏ 256/132/64; một **review workspace ORA 7 layer flat**, không phải attachment để rig.
- [x] QA binary **8/8 local tests PASS**, ZIP CRC sạch, 5 crop trùng byte nguồn, ORA review hợp lệ. Lưu tại Library Development với ZIP SHA256 `8602b28f6df43952b6f70adcdffd4c0945bd0463ba6144c449a0a5b192a5dc8b`. [CP334 handoff](LAM_THIEN_CP334_ART_DIRECTION_HANDOFF.md).
- [ ] **Art chưa đạt**: candidate mắt hổ phách/chi tiết tóc tốt hơn CP333, nhưng hình dáng và phụ kiện khác V2; model vẫn là flat concept chưa có underpaint/layer semantic; không Spine/Android APK.
- [ ] **CP335:** ưu tiên **redraw thực trên chung face master Front + 3/4** từ V2, clean underpaint, iris/lashes/eyelids/brows/mouth/blush tách riêng và QA nhỏ; gửi preview asset rồi mới làm rig/Spine/APK. **Không tạo thêm atlas/crop để đánh dấu sai tiến độ.**


## CP335 — Khóa sử dụng sprite chưa được duyệt (2026-10-29)

- [x] Xác minh thiết kế V2 và 5 cảm xúc đã chốt; tạo bảng QA so bản concept CP335 (flat, chưa duyệt) với canon, thử 132px/64px.
- [x] **Sửa runtime thật:** `CharacterExpressionCatalog.resolveSprite` yêu cầu `production_release`, nguồn V2/biểu cảm đúng SHA, QA artist+runtime, nghiệm thu **asset mới** từ người dùng, manifest SHA và hash từng file. Thiếu các điều kiện thì không trả ảnh, không fallback.
- [x] Thêm `tools/verify_expression_art_release.py`, **17/17 Kotlin local scenarios** và **14/14 Python tests PASS** (gồm SHA file PNG/alpha/path) và workflow `cp335-expression-production-gate.yml` trên GitHub. **Run `40823727298` SUCCESS.**
- [x] Lưu [CP335 handoff](LAM_THIEN_CP335_ART_RELEASE_HANDOFF.md), [manifest concept](LAM_THIEN_CP335_VISUAL_GATE_MANIFEST.json), ZIP SHA256 `d656146585681ce1a5b05d322fdab3a12eccb2c5f21b2afd6cc9e9d773dcf2df` tại Library Development.
- [ ] **ART CHƯA CÓ:** CP335 generated sheet vẫn PNG phẳng, không có shared master Front/3⁄4, clean semantic layer, artist approval hoặc real asset registration. `production_release` tiếp tục BLOCKED.
- [ ] **CP336 ưu tiên:** dựng thật một head master đúng CANON V2, sạch underpaint, hai góc Front/3⁄4, 5 nét alpha độc lập và cùng nhân dạng; duyệt art rồi mới đưa vào sprite manifest/Spine/Android APK. **Không hỏi lại CANON V2, tỷ lệ +17% hay 5 nét đã chốt.**


## CP336 — xác minh góc mặt từ CANON thật và QA 138-slot art intake (2026-10-29)

- [x] Đối chiếu checksum chính thức CANON V2/5 biểu cảm. Cắt **đúng pixel** nguồn V2: front-labeled 145×151, 3/4-labeled 143×151, closeup 230×114; hai góc V2 hiện gần giống nhau nên **chưa phải hai head masters rig**.
- [x] Tạo [CP336 handoff](LAM_THIEN_CP336_FACE_MASTER_HANDOFF.md) + [manifest nguồn](LAM_THIEN_CP336_SOURCE_MASTER_MANIFEST.json), bảng xem Front/3/4 + 5 cảm xúc đã duyệt. Có ZIP nguồn/lossless crop trong Library Development.
- [x] Thêm validator `tools/cp336/validate_head_layers.py` kiểm 2 angle, base master dùng chung, 13 semantic parts ×5, checksum PNG RGBA, alpha/skin ROI, iris amber/path safety; không tự chấm mỹ thuật.
- [x] **16/16 local tests PASS:** 12 bài trên 138 PNG **synthetic fixture** và 4 bài so pixel với nguồn approved thật. `--strict` FAIL đúng dự kiến; ZIP SHA256 `29d4f59402243a300357f6ab7e46440956e39bb1f7609cce988f8670daf8bde5`. GitHub CP336 workflow run `40829848852` **SUCCESS**. CP335 release gate vẫn BLOCK art chưa duyệt.
- [ ] **CP337 ART THẬT:** vẽ native head master Front và 3/4 theo CANON V2 (hai góc phân biệt rõ), dưới tóc có skin underpaint sạch; 13 facial layers ×5 trên từng góc, mắt hổ phách, hoa tóc/viền vàng tiết chế; QA 256/132/64, blink/mesh/occlusion. **Sau nghiệm thu art thành phẩm** mới đăng ký sprite/Spine/APK.
- [ ] `production_release` vẫn `blocked_pending_art`, `sprite_paths={}`. P0-02/P0-03/P1-03/P2 chưa DONE. **Không hỏi chốt lại** CANON V2, +17%, năm cảm xúc hay damage 100/70/50/30.


## CP337 — khởi tạo triển khai art Front/3/4 thực (2026-10-29)

- [x] Kiểm nguồn CANON V2 + các crop CP336; xác minh Drive source chưa có source ORA/PSD/KRA thật qua quyền truy cập hiện tại.
- [x] Tạo work order [CP337](LAM_THIEN_CP337_FRONT_THREE_QUARTER_WORK_ORDER.md), bảo vệ hai nguồn approved và ghi tiêu chuẩn đủ 2 góc để nghiệm thu.
- [ ] Chân dung FRONT được yêu cầu tạo riêng qua task `880ac92b-bf38-48ae-bd33-e7fde597efd8` đang **PENDING** tại checkpoint; chưa có ảnh kết quả được kiểm. **Không gọi là completed sprite**.
- [ ] 3/4 asset và clean native layered artwork cần sản xuất; 13 semantic parts × 5 expressions mỗi góc vẫn chưa có production art. CP335 release gate BLOCKED, Spine/APK NOT DONE.


## CP337 — user visual QA FAIL / chuyển hướng bảo toàn body V2 (2026-10-29)

- [x] Hai generation jobs hoàn thành: Front `880ac92b-bf38-48ae-bd33-e7fde597efd8`, 3/4 `263c4531-2b33-4f2a-9ef5-5f5029a5b450`. **CẢ HAI KHÔNG ĐẠT** đối chiếu body/trang phục theo phản hồi người dùng. Không coi successful generation là approved art.
- [x] Ghi nhận lỗi *design drift*: pose/góc mới từ prompt không giữ chính xác body và outfit; dùng generated Front làm nguồn 3/4 nhân sai lệch.
- [ ] **ƯU TIÊN TIẾP:** khóa 100% CANON V2 **body + costume** (tỷ lệ +17% đã tích hợp), dựng chi tiết face/head theo đúng V2 *trong phạm vi không đổi trang phục*, đối chiếu trước khi tiếp tục Front/3/4, biểu cảm và rig.
- [ ] Bản preview kế tiếp **phải nhìn thấy đủ đường nét body/cổ áo/tay áo/phụ kiện để so sánh**, không chỉ crop khuôn mặt. Gate FAIL khi neckline, silhouette, phân bố vàng, hoa tóc, body proportion hoặc fabric khác mẫu chốt; approval manual chứ không phải tự đánh giá text.
- [ ] `production_release.status=blocked_pending_art`, `sprite_paths={}`, CP337/Spine/APK vẫn **NOT DONE**.
