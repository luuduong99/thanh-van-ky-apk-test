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
