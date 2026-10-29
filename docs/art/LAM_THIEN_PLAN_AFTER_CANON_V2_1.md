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