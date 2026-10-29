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
