# Thanh Vân Ký — Kế hoạch từ CANON V2.1

## P0 — Khóa nguồn và chất lượng chuẩn (đã thực hiện phần lưu)
- [x] Lưu **file gốc nguyên pixel** và SHA-256, ảnh duy nhất làm chuẩn chính thức.
- [x] Ghi model, tỷ lệ +17% đã áp dụng, kiểu áo ngực, biểu cảm và trạng thái hư hại.
- [ ] Đối chiếu trực quan thêm độ nhất quán giữa các góc Front/Side/Back/3/4 và màu mắt trên sheet; mọi nghi vấn được gắn review, không tự ý thay.

## P1 — Sản xuất art game thực
- [ ] Tách thành các bộ art riêng cho góc Front và 3/4 đầu tiên, chọn một pose chuẩn; không upscale crop mà tự coi là nét vẽ mới.
- [ ] Dựng file ORA/PSD/KRA editable native theo layer thật: tóc trước/sau, body, áo/váy, phụ kiện, facial underpaint, mắt/mày/miệng, đồ trang trí rủ.
- [ ] Ghép test trên 1 pose/góc, bảo đảm đường cắt alpha, vùng vẽ ẩn, rig draw-order, đồng nhất form.
- [ ] Sinh năm nét mặt từ cùng một face master; kiểm các cỡ thoại 256/132/64.
- [ ] Dựng các mức integrity 100/70/50/30 qua overlay dirt/scuff/tear, không thay đổi hình thể hay phóng đại damage 30.
- [ ] Hoàn thiện Side/Back/3/4 Back và các pose còn lại theo cùng model; không vẽ lại trang phục khác.
- [ ] Gửi preview có đối chiếu CANON và kiểm tính liên tục qua góc nhìn; phê duyệt art sprite riêng.

## P2 — Rig + game runtime
- [ ] Nhập asset thật vào Spine / bộ rig 2D tương đương; kiểm bone, mesh, clipping, chuyển động tóc/tua, blink, mouth.
- [ ] Nối `expression × wardrobe × integrity × pose` vào game, bật art release gate sau khi thật sự được nghiệm thu.
- [ ] Kiểm tra damage đổi lần đầu khi HP qua ngưỡng, trạng thái giữ khi hội thoại và tương tác theo spec.

## P3 — Build APK & nghiệm thu
- [ ] GitHub Actions build Android debug APK; lưu artifact có thể tải.
- [ ] Chạy smoke test Android: chọn nhân vật, trang phục, 5 biểu cảm, damage 4 mức, combat/dialogue và save/load.
- [ ] Đóng băng release và cập nhật PROJECT_SPEC với commit/tag, version và APK SHA.

**Không coi chỉ ảnh phẳng hoặc ảnh đã được chốt là đã có Spine, layer hay APK.**

## CP340 — kết quả triển khai thực (2026-10-29)

- [x] Kiểm hash gốc V2.1 lại tại file nguồn: SHA `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`, 941×1672 RGBA.
- [x] Cắt **14 ảnh tham chiếu native giữ nguyên pixel**: 5 angle, 5 facial expression, 4 damage 100/70/50/30. `9/9 local binary tests PASS` gồm so pixel/CRC/source RGB/alpha.
- [x] Thử **một Front alpha thực** native 215×449 từ source (chỉ thay alpha), ORA 2 layer có source crop ẩn; có preview `CP340_FRONT_ALPHA_SIDE_BY_SIDE.png`. Art này **không** phải sprite sạch/rig/underpaint; kích thước từ infographic không phải master HD.
- [x] Lưu [CP340 handoff](LAM_THIEN_CP340_SOURCE_EXACT_FRONT_ALPHA_HANDOFF.md), [manifest](LAM_THIEN_CP340_ALPHA_TRIAL_MANIFEST.json), script/QA + ZIP SHA256 `51cafc14800032712eeed7f0d1ff47edf6f486659ac38c28279298a1be0cb535` ở Library Development.
- [ ] **Bước P1 kế tiếp — REDRAW ART THẬT:** từ cutout làm guide, họa sĩ cần redraw native high-res thành semantic RGBA + clean underpaint (body, áo, tóc, tay, phụ kiện), QA silhouette/bodice V2.1 trước các biểu cảm/góc còn lại.
- [ ] Preview của nguồn V2.1 cho thấy `3/4 Front` chưa rõ khác Front ở khuôn mặt; artist phải làm phối cảnh đúng khi thực hiện view production mà **không thiết kế lại model**. Vẽ damage/biểu cảm theo đúng bản mới nhất, không tăng vết rách ở 30.
- [ ] CP335 art gate còn **BLOCKED**, Spine/APK chưa hoàn thành. Không tự chốt bản alpha trial.


## CP341 — Refine alpha foreground trên crop Front gốc (2026-10-29)

- [x] CANON V2.1 vẫn được SHA-checked (941×1672, SHA `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`); không thay RGB nhân vật hay trang phục.
- [x] Phục hồi tóc bạc/viền tay áo/vạt vải sáng từ source crop 215×449 bị CP340 làm mất; alpha >128 tăng 19.983 pixel có kiểm vùng. Tạo **PNG RGBA**, **mask grayscale chỉnh sửa được**, **ORA 3 lớp so sánh (không phải bộ phận rig)** và preview.
- [x] **13/13 local binary tests PASS**, ZIP CRC PASS; [CP341 handoff](LAM_THIEN_CP341_MATTE_HANDOFF.md), [manifest](LAM_THIEN_CP341_MATTE_MANIFEST.json), gói ZIP SHA `08d8aa08bc4b00163e092d056f1e067a5652b0f80b9462e5308277dbe8baacb1` tại Library Development.
- [ ] **CP342 cần thực hiện:** cleanup thủ công white halo + shadow dưới chân và vạt, tạo **art native Front semantically layered** với underpaint thực và vùng vải/tóc ẩn khi bone chuyển động. Preview bắt buộc so silhouette/body/bodice với CANON V2.1 để tránh sai mẫu.
- [ ] Mới sau Front artist-approved: tách 5 nét biểu cảm độc lập, 4 mức hư hại vừa phải, góc nhìn khác; rig/Spine và Android APK vẫn chưa DONE. CP335 release gate tiếp tục BLOCK.


## CP342 — xử lý bóng sàn trong alpha Front (2026-10-29)

- [x] Dùng CANON V2.1 SHA `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`; RGB bảo toàn tuyệt đối. Chỉnh alpha chỉ vùng 39 dòng cuối; vùng thân/bodice trên **không thay**.
- [x] Giảm dải bóng nền xanh-xám dưới giày/vạt: 2.364 pixel alpha khác, vùng sàn giảm 209.000 alpha-unit, giày giữa giữ nguyên. Xuất PNG, mask, delta và ORA 4 layer so sánh, không phải skeleton/semantic art.
- [x] **13/13 binary tests PASS** (file PNG/ORA thật); ZIP 15 file SHA `76d8fd962688dde6356d4853b5e522b5ce78567a1e08ae3739668851ec5ebf66`, sao lưu Library Development. [Handoff](LAM_THIEN_CP342_SHADOW_CLEANUP_HANDOFF.md).
- [ ] **CP343 P1 ART THẬT:** vẽ lại **Front native high-res đúng CANON V2.1** thành body, tóc trước/sau, face/skin underpaint, tay, bodice, tay áo, phụ kiện và vạt lụa có alpha sạch/vùng che khuất. Preview 1 pose quay/di chuyển có draw-order và không lộ lỗ dưới lớp.
- [ ] Chỉ sau art Front mới tạo 5 expression attachments, 4 damage overlays giữ giới hạn 30% từ CANON, góc/tư thế còn lại, user asset acceptance, Spine và APK.
- [ ] Cổng CP335 Android vẫn `blocked_pending_art`, `sprite_paths={}`. Không coi PNG flat 215×449 là asset hoàn thiện.


## CP343 — phân vùng ảnh thật theo Front, kiểm chuyển động (2026-10-29)

- [x] Tách **10 PNG vùng/source-pixel**, 10 mask grayscale riêng, tạo **ORA 10 lớp**, giữ đúng RGB và alpha của CP342 khi ghép ở tư thế ban đầu. **12/12 binary tests PASS**, source đúng CANON V2.1.
- [x] **Kiểm tra di chuyển hai tay** ±10px/+5px: **1.798 pixel bị hở** do không có da/vải vẽ bên dưới; 1.098 pixel nhô ra. Kết luận **FAIL no hidden underpaint**, chưa thể rig thật.
- [x] Bảng QA source-composite-mask, bản đồ màu lớp và preview hở khớp; lưu [CP343 handoff](LAM_THIEN_CP343_REGION_LAYER_HANDOFF.md), [manifest](LAM_THIEN_CP343_REGION_LAYER_MANIFEST.json). ZIP 34 files SHA `b61169d5b3fdb04dbbbd38df3ab080b2662e9332fabcc9c6ecaf660691ce9519` đã sao lưu Library Development.
- [ ] **CP344 ưu tiên:** vẽ lại một vùng tay trái–vai/thân áo **có vùng ẩn thật**, chỉnh alpha đường biên thủ công và xem thử 2 frame với dịch/rotation nhỏ; không để lỗ/mất váy/đổi bodice. Sau QA tay trái mới làm tay phải/tóc.
- [ ] Chưa native painted high-res art, chưa có layer mặt thật, năm expression sprites, damage overlay hay Android/Spine. **Release tiếp tục BLOCK**.


## CP366 — Partial sleeve vector artwork (2026-10-29)
- [x] Sáu mảng SVG vẽ độc lập dùng cho tay/vai/tóc/vải bên trái; ORA 7 lớp; 5/5 structural tests PASS.
- [ ] **Visual QA NOT_PASSED**: sai khác đường nét, nếp lụa và đồ trang sức so với CANON; không thể thay thế ảnh chuẩn. Không phải full-body sprite/Spine/APK.
- Tài liệu: [CP366 partial art study](LAM_THIEN_CP366_LEFT_SLEEVE_SIX_VECTOR_ART_STUDY.md).

## CP367 — CANON-only QA và khóa quy tắc preview (2026-10-29)
- [x] Xác minh file gốc người dùng gửi, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`, 941×1672 RGBA.
- [x] QA hai mũi guốc xanh từ crop Front chính xác: trái 163/163, phải 146/146 pixel nguồn. Hai lỗi xóa alpha mũi guốc bị phát hiện, crop lệch kích thước bị chặn; **6/6 local test PASS**.
- [x] Cập nhật PROJECT_SPEC: mọi lần hiển thị nhân vật chỉ dùng ảnh CANON mới nhất đã duyệt của chính nhân vật hoặc crop đúng nguồn; ảnh draft phải ghi rõ draft và so với CANON, không dùng hình khác thay thế.
- [x] Công cụ và test kiểm chân tại `tools/art/cp367_canon_guard.py` và `tests/art/test_cp367_canon_guard.py`.
- [ ] **CP368 tiếp theo:** nâng chất lượng art tay/vai/tóc/vải CP366 theo CANON, kiểm khớp/underpaint qua dịch/rotation và vẽ tiếp các layer full-body; đòi hỏi preview nhận xét của người dùng trước khi rig thật.
- [ ] Spine/rig, art đã duyệt, APK vẫn **BLOCKED**. Chi tiết: [CP367 handoff](LAM_THIEN_CP367_CANON_ONLY_QA.md).


## CP368 — Localized left-sleeve SVG refinement (2026-10-29)

- [x] CANON V2.1 nguồn duy nhất: SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a` (941×1672 RGBA). Không dùng ảnh nhân vật thay thế; bản mới phải ghi rõ **DRAFT**.
- [x] Tinh chỉnh 6 SVG art thực từ CP366: tóc sau, bodice khuất, da vai khuất, tay/bàn tay, lụa tay áo, hoa văn vàng. Có 6 PNG alpha, ORA 7 lớp (1 guide CANON ẩn), ảnh đối chiếu CANON/CP366/CP368; không chỉnh sửa ảnh gốc.
- [x] **6/6 local tests PASS**, có QA vùng chồng lớp vai khi xoay 0/-8/-15/+8°; các vùng có pixel chồng nhưng **chưa chứng minh rig không hở hình**. ZIP CRC PASS, 25 files SHA256 `2a8ab1c8a5b22eac5a265ebfe07bcde592de501c9b98014aaa6c957f618009b8`, lưu Library `/Thanh Van Ky/Development/CP368_Refined_Sleeve_Study/`. [CP368 report](LAM_THIEN_CP368_REFINED_LEFT_SLEEVE_DRAFT.md).
- [ ] **ART VISUAL QA NOT_PASSED**: nét vẽ còn khác ảnh chuẩn, chưa native painted full body hoặc keyframe tay nâng do họa sĩ vẽ; chưa được phê duyệt để nhập game. Spine/APK vẫn BLOCK.
- [ ] **CP369 ưu tiên:** làm chi tiết nếp lụa/vải khuất và hair/ornament đúng CANON, phát triển các semantic layer full body, làm idle/raised-arm vẽ riêng và xin nghiệm thu hình trước khi tích hợp gameplay.



## CP369 — Fixed-shoulder gold, moving wrist và hidden-underpaint (2026-10-29)
- [x] Nguồn duy nhất là CANON V2.1 đã được chốt, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a` (941×1672 RGBA); chỉ dùng crop chính xác từ nguồn này để đối chiếu, art mới ghi rõ UNAPPROVED DRAFT.
- [x] Sửa lỗi logic CP368: tách vàng vai **cố định** khỏi vàng cổ tay **di chuyển cùng tay**; tạo 7 lớp SVG/PNG alpha độc lập + ORA 8 lớp (7 art và CANON guide ẩn). Thêm path vẽ da/vải lót bị khuất tại vai.
- [x] Local motion ở ROI source x=54..83, y=124..170: -8° có 3.192 pixel mới lộ / 0 thiếu lót; -15° có 5.905 / 0; +8° có 789 / 0. Test âm bỏ da/vải lót phải FAIL. **Chỉ là kiểm tra alpha cục bộ; không chứng minh toàn sprite hoặc rig không hở.**
- [x] 8/8 kiểm thử local PASS (SHA source, SVG, ORA CRC, một lớp guide ẩn, vai cố định/cổ tay chuyển động, phủ alpha ở khớp, test âm, release gate). Gói CP369 ZIP 29 file SHA256 `84a5b29e6618c0b4901707f045e44b9020febc768181b758748355c513917dfb`, ORA SHA256 `cf0b06461ae0c1aace0d3c5bc92691a066b0f2446df7bd617a9de4f4cabf54be`; lưu Library `/Thanh Van Ky/Development/CP369_Static_Shoulder_Moving_Wrist_Underpaint/`.
- [ ] **Visual QA NOT_PASSED**: nguồn vẽ còn quá đơn giản so với CANON, chuyển động vẫn là xoay bitmap kỹ thuật, chưa có 2 keyframe vẽ thật, chưa đủ full-body semantic layers. Spine/APK vẫn BLOCK.
- [ ] **CP370 tiếp tục:** vẽ/nâng chất lượng tay/vai và lụa so với CANON, triển khai các lớp thật của tay phải, thân, mặt và hai guốc xanh; sau đó vẽ riêng idle/raised-arm keyframes rồi xin duyệt art.
- [CP369 handoff](LAM_THIEN_CP369_STATIC_SHOULDER_MOVING_WRIST.md), code `tools/art/cp369_split_gold_and_underpaint.py`, QA `tests/art/test_cp369_split_gold_and_underpaint.py`.


## CP370 — Two independently drawn SVG arm key poses (2026-10-29)
- [x] Chỉ sử dụng Lâm Thiển **CANON V2.1** nguyên bản, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a` (941×1672 RGBA); preview có crop đúng nguồn + 2 DRAFT có nhãn, không dùng ảnh nhân vật khác.
- [x] **Vẽ riêng đường SVG** cho 3 phần moving ở key pose tay nâng (tay/bàn tay, lụa có nếp rủ mới, vòng vàng cổ tay); 4 phần khác vẫn cố định gồm tóc sau, bodice khuất, da vai khuất, phụ kiện vai. Khác CP369: không chỉ xoay bitmap của pose idle.
- [x] Xuất **2 bộ art / 2 ORA**, mỗi tư thế 7 art SVG/PNG độc lập + ORA 8 lớp (1 CANON guide ẩn), cùng canvas 1302×2748. Chỉ là canvas vector 6× crop 217×458; không được suy ra nguồn tranh đã HD.
- [x] Local **9/9 PASS** (8 có ảnh nguồn thật + 1 static contract). Trên GitHub CI không có CANON/ORA private thì bài kiểm tra cần asset skip; không được gọi đó là kiểm thử art đã đạt. Vai vàng fixed pixel-exact, vòng vàng cổ tay thay vị trí; ROI vai có 2.996 pixel lộ và 0 pixel thiếu lót theo alpha trong vùng nhỏ; không chứng minh mọi khớp an toàn.
- [x] ZIP 43 entries, CRC PASS, SHA256 `6845f2543befe36c7dabb19d2e097e0821b71485ca7d7835b6f7e8dd2bb18e9e` lưu Library `/Thanh Van Ky/Development/CP370_Independent_Arm_KeyPose_Study/`. [CP370 handoff](LAM_THIEN_CP370_INDEPENDENT_ARM_KEYPOSE_STUDY.md), script `tools/art/cp370_two_hand_authored_poses.py`, test `tests/art/test_cp370_two_hand_authored_poses.py`.
- [ ] **Visual QA NOT_PASSED**: bàn tay/nếp lụa còn sơ lược so CANON; chưa full-body native painted, không có in-betweens, rig, Spine, FPS hay APK. **Production release BLOCKED**.
- [ ] **CP371 tiếp tục:** vẽ lại chi tiết tay/lụa 2 pose, bảo vệ nhận diện CANON; xây các semantic layers còn thiếu (mặt/tóc trước/thân/tay phải/2 guốc xanh), gửi preview để duyệt rồi mới rig và build APK.



## CP371 — Two-pose silk fold and hem detail (2026-10-30)

- [x] Khóa nguồn Lâm Thiển CANON V2.1 (941×1672 RGBA, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`). Toàn bộ preview chỉ có đúng CANON của nhân vật và art draft từ đó, không có ảnh thay thế.
- [x] Thêm 2 mảng SVG vector **vẽ riêng cho idle/raised**: nếp lụa sáng và chỉ viền xanh/vàng; bổ sung nét bàn tay và giữ các phần đứng yên chính xác giữa 2 pose. Mỗi tư thế 9 art layers + CANON guide ẩn; 2 ORA 10 lớp, PNG alpha, preview đối chiếu.
- [x] **11/11 local tests PASS**, hai ORA CRC PASS. Khác CP370: idle 19.833 pixels, raised 35.436 pixels. Coverage mới (trong hoặc sát silhouette tay áo) folds/hem idle 100%/100%, raised 96,11%/100%. Chỉ QA kỹ thuật cục bộ, **không chứng nhận đạt thẩm mỹ**.
- [x] Đã sao lưu ZIP 52 files SHA256 `b0f1a18c36edc9e69a9a3e232e0b20cc633c647fe7173555a9b673a93831eb2c`, Library `/Thanh Van Ky/Development/CP371_Silk_Detail_Two_Poses/`. [CP371 handoff](LAM_THIEN_CP371_SILK_FOLD_HEM_TWO_POSES.md).
- [ ] **VISUAL QA NOT PASSED**: còn thô so CANON, thiếu nhiều lớp art nhân vật thực, chưa rig/Spine hoặc APK. Production blocked, sprite_paths empty.
- [ ] **CP372 next:** ưu tiên true native art fidelity tay/bàn tay, áo và trang sức; sau đó full-body, hai giày xanh và 5 expression / 4 damage, trước khi duyệt art/rig, test APK.

## CP372 — Finger, wrist and fixed-shoulder details (2026-10-30)
- [x] CANON source-locked: đúng `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, 941×1672 RGBA, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`; preview chỉ dùng CANON thật + các bản CP371/CP372 của chính Lâm Thiển có nhãn DRAFT.
- [x] Từ CP371 (9 lớp/tư thế), tạo thêm **3 lớp SVG/PNG có nét vẽ thật** mỗi tư thế: ngón tay/khớp, hoa văn cổ tay và hoa văn vàng vai cố định. Idle/raised có nét tay/cổ tay khác nhau; vai giữ nguyên pixel.
- [x] Tất cả nét mới được alpha-clip vào art cha tương ứng; tạo **2 ORA 13 lớp** (12 art hiển thị + CANON guide ẩn). Composite thay đổi so CP371: 2.598 pixel idle và 2.624 pixel raised, không phải chứng nhận đẹp hơn.
- [x] **11/11 local tests PASS**, đúng SHA source, từ chối nguồn sai trước output, path SVG, clip semantic, ORA CRC/13 lớp, static shoulder, mobile release gate. Khi thiếu ảnh và binary ORA trong GitHub CI, test art-dependent skip đúng. [Báo cáo CP372](LAM_THIEN_CP372_FINGER_GOLD_DETAIL_STUDY.md).
- [x] ZIP 64 tệp SHA256 `721a17c057cc3732c1c8b084a81046fd2b4d1d1e9b11a5a7b1fe4a61d4118249`, CRC PASS; Library `/Thanh Van Ky/Development/CP372_Finger_Gold_Detail_Study/`. Code `tools/art/cp372_finger_gold_detail.py`, tests `tests/art/test_cp372_finger_gold_detail.py`.
- [ ] **Visual QA NOT_PASSED**: vẫn là art mảng tay đơn giản, chưa có Front full-body native semantic, 5 expression, 4 damage, chân/giày 2 bên, Spine/physics, gameplay runtime hoặc Android APK.
- [ ] **CP373 next:** ưu tiên tạo *bộ art Front full-body thực* theo CANON, tách tóc, mặt, thân/áo, hai tay, vạt lụa, chân và hai guốc xanh; tạo underpaint và kiểm pose với art chất lượng cao hơn trước khi phê duyệt và rig. Không nối CP372 vector thử trực tiếp vào APK.

## CP373 — Full-body source-region guide (2026-10-30)
- [x] Khóa nguồn **CANON V2.1 đã duyệt**: đúng PNG 941×1672 RGBA, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`; chỉ dùng ảnh này và các phần cắt đúng từ ảnh này trong bảng preview, không tìm hình khác thay thế.
- [x] Dùng vùng Front gốc chính xác `(13,172,230,630)` = **217×458 pixel thật** để xây **19 source-region PNG/mask** phủ toàn bộ Front và một file ORA 20 lớp (19 lớp nguồn + 1 CANON guide ẩn). Composite tư thế đứng pixel-exact so với **alpha matte kỹ thuật**; không phải art redraw high-res, không có hidden anatomy.
- [x] Tách nền thử nghiệm bằng GrabCut + phục hồi vùng dải lụa xanh/tím; **vẫn có nền/bóng sàn lẫn ở dưới chân và mất một số mép vải sáng**, phải dọn bằng tay, không được dùng làm production sprite.
- [x] QA hai mũi guốc xanh theo CANON: bên trái **163/163** và bên phải **146/146 pixel nguồn** còn thấy. Khi dịch phần bàn tay (-6,+3) phát hiện **204 pixel hở** vì thiếu lớp da/vải khuất; rig gate **FAIL**.
- [x] **10/10 local tests PASS**: lock SHA, sai nguồn từ chối trước xuất, RGB giữ nguyên, 19 mask ghép tĩnh, ORA CRC/stack, mũi guốc, kiểm hở khi chuyển động và release gate. Không đánh đồng test kỹ thuật với Visual QA.
- [x] ZIP 54 files SHA256 `72f25fff04c64d5345ba8047de9aceb0c3713d8c3f45580341210b028f937662`, Library `/Thanh Van Ky/Development/CP373_FullBody_Canon_SourceGuide/`. [CP373 report](LAM_THIEN_CP373_FULL_BODY_SOURCE_GUIDE.md); công cụ `tools/art/cp373_fullbody_source_guide.py`, test `tests/art/test_cp373_fullbody_source_guide.py`.
- [ ] **VISUAL QA NOT PASSED / PRODUCTION BLOCKED:** source chỉ có 217×458 pixel, chưa phải 2D art vẽ thật đủ chi tiết, alpha còn dính bóng sàn và thiếu underpaint. Spine/Android APK chưa hoàn thành. `production_release.status=blocked_pending_art`, `sprite_paths={}`.
- [ ] **CP374:** artist redraw Front native HD theo đúng CANON thành tóc/mặt/cơ thể, thân áo, hai tay, váy/vạt, chân và hai mũi guốc xanh, bổ sung hidden underpaint; kiểm alpha/pose và xin duyệt trước khi rig/Spine.

---

## CP374 — Partial source-matte floor-shadow removal (2026-10-30)

- [x] CANON-only V2.1 SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`; nguồn Front thật 217×458, ảnh gốc 941×1672 RGBA. Giữ nguyên hình đã chốt, **không dùng image-search/nhân vật khác**.
- [x] Từ CP373, thử gỡ alpha **1.030 pixel** ứng viên bóng sàn trong ROI thận trọng dưới chân. RGB không đổi, alpha vùng chân/giày bảo vệ giữ nguyên; mũi guốc xanh trái 163/163, phải 146/146. Không tuyên bố bóng sàn đã sạch hoàn toàn.
- [x] Xuất 19 source-region PNG/mask và ORA **21 lớp** (19 visible, 2 hidden để hoàn tác/đối chiếu CANON), ảnh so sánh CANON/CP373/CP374, mask phần loại, JSON và script reproducible.
- [x] **10/10 local tests PASS** trên private CANON và CP373; simulated public CI **2 pass / 8 skip**, CRC PASS. ZIP 72 items SHA256 `824215ec6a2ae08321b8e895cc0c42dc68cae408f32b72473139b90df2ec8d41`, Library `/Thanh Van Ky/Development/CP374_Floor_Shadow_Partial_Cleanup/`. [CP374 handoff](LAM_THIEN_CP374_FLOOR_CANDIDATE_CLEANUP.md).
- [ ] **Visual QA NOT_PASSED**: còn viền lụa/bóng sàn, 204px underpaint missing theo CP373, chưa independent high-res art, 5 expression/integrity overlays, Spine/Android APK. Giữ `production_release.status=blocked_pending_art`, `sprite_paths={}`.
- [ ] **CP375:** vẽ bản native hi-res Front thực theo CANON với các semantic layers/body underpaint; không biến mask crop/phóng to thành “vẽ HD”. Làm hai pose thật và xin duyệt trước khi rig.

---

## CP375 — Partial drawn hidden-wrist study (2026-10-30)

- [x] Xác minh CANON V2.1 SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`, dùng crop Front 217×458 đúng nguồn và chỉ hiển thị CANON của Lâm Thiển + draft cùng nhân vật.
- [x] Tạo 4 SVG Bézier/gradient được vẽ mới thành 4 PNG art RGBA (canvas vector 1302×2748) + ORA 5 lớp có CANON guide ẩn. **Không được xem 6× là nâng chi tiết gốc lên HD**.
- [x] Test dịch tay (-6,+3), nguồn CP374: **204** pixel hở ban đầu, **114** pixel được alpha vector mới phủ, **90** còn hở. Đây chỉ QA cục bộ, không phải rig chuyển động hoàn chỉnh.
- [x] **9/9 local PASS**, mô phỏng public CI thiếu art **4 PASS / 5 SKIP**; ORA CRC PASS, hai giày xanh nguồn giữ 163/163 và 146/146. [Handoff CP375](LAM_THIEN_CP375_HIDDEN_WRIST_ART_STUDY.md), ZIP 21 entries SHA256 `c279ba8b9f24fd57fdd0fdc743cba7185474461fe6d2b57aedf871ee07c19ba7`, sao lưu Library `/Thanh Van Ky/Development/CP375_Hidden_Wrist_Native_Art_Study/`.
- [ ] **Visual QA NOT PASSED / release blocked**: art chỉ là một phần cẳng tay, chưa full-body native painting hay anatomy hợp lý khi di chuyển; 90 px hở, lụa sáng/matte/bóng sàn còn lỗi; chưa Spine/APK.
- [ ] **CP376:** vẽ lại *toàn bộ vai/tay trái/tay áo*, hoàn thiện underpaint và hai keyframes đúng CANON, rồi phát triển full-body semantic art / expression / clothing integrity trước kiểm thử Android.

---

## CP376 — Wrist cuff and rear-ribbon alpha diagnostic art (2026-10-30)

- [x] Giữ duy nhất Lâm Thiển CANON V2.1 `LAM_THIEN_CANON_V2_1_FINAL_20261029.png` SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`; không dùng hình nhân vật không liên quan.
- [x] Bổ sung **3 SVG vẽ mới**, tổng 7 art PNG/layers, ORA 8 lớp (7 art đang hiển thị + 1 CANON guide ẩn); vẫn chỉ là mảng cổ tay/lụa thử nghiệm.
- [x] Phân nhóm 90 pixel còn lại ở CP375 theo quan sát trực quan CANON: 35 vòng cổ tay, 40 mép lụa, 15 đầu ngón tay. Kết quả hướng (-6,+3): **90→18 pixel** sau CP376; còn 3 mép lụa và 15 đầu ngón tay. KHÔNG tự xóa điểm ngón tay vì thay silhouette không nhất thiết là alpha hole.
- [x] Thử thêm (-4,+2): 68→21; (+3,-2): 121→98; (-8,+5): 113→26. **11/11 local tests PASS**, public-mode 4 PASS/7 SKIP. Art chuyển động và quality gate **CHƯA ĐẠT**.
- [x] ZIP 32 tệp SHA256 `e110ed56c1d40c41450363d1d4cc40c60067f801c68ccfc510870ce666f775b8`, Library `/Thanh Van Ky/Development/CP376_Wrist_Ribbon_Underpaint_Draft/`. [CP376 handoff](LAM_THIEN_CP376_WRIST_RIBBON_UNDERPAINT_STUDY.md).
- [ ] **Visual QA NOT_PASSED / production blocked:** cổ tay/ribbon vẫn là vector sơ lược, chưa làm full-body art thật hay hai keyframe toàn diện, chưa Spine/APK.
- [ ] **CP377:** vẽ riêng hình đầu ngón, cổ tay, mép lụa cho keyframe; QA chuyển động nhiều hướng với CANON, rồi tiếp tục hoàn thành Front semantic body/face/hair/legs/shoes trước nghiệm thu và build.

