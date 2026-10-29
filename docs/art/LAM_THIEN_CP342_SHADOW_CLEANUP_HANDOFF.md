# Lâm Thiển — CP342: Làm sạch bóng nền Front alpha (29/10/2026)

**Checkpoint:** CP342 technical matte cleanup **DONE**; Front artist-painted semantic layers, Spine and APK **NOT DONE**.

## Bất biến CANON V2.1

- `LT_CANON_V2_1_FINAL_USER_APPROVED_2026_10_29`; PNG user-approved 941×1672 RGBA, SHA-256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- Toàn bộ vóc dáng và tỷ lệ +17% **đã nằm sẵn** trên CANON; không tự tăng thêm. Giữ áo, màu tóc bạc, phụ kiện hoa trắng–xanh–vàng, 5 biểu cảm đã chốt và damage 100/70/50/30 (đặc biệt **30% không được làm rách/bẩn quá mức**).
- CP337/CP338/CP339 và các bản CP340/CP341 chỉ làm lịch sử/nguồn R&D. **Không thay CANON V2.1**.

## File art thực đã chỉnh

- Đọc đúng crop Front pixel gốc `(13,177)-(228,626)` → **215×449**, và `FRONT_CP341` RGBA. **RGB của toàn bộ crop không đổi**; chỉ chỉnh alpha ở **39 dòng cuối, y≥410** để giảm nền sàn màu xanh-xám bị dính dưới giày và vạt lụa.
- Xuất `FRONT_CP342_FLOOR_CLEAN_ALPHA_NOT_RIG.png`, `FRONT_CP342_EDITABLE_ALPHA_MASK.png`, `FRONT_CP342_REMOVED_ALPHA_DIAGNOSTIC.png`. Giữ cả bản CP341 trước chỉnh để rollback.
- `CP342_MATTE_VARIANTS_NOT_RIG.ora` gồm **4 raster comparison layers**, chỉ 1 visible; không phải 4 lớp body/tóc/áo có thể rig. Xuất bảng đối chiếu `CP342_THREE_WAY_CANON_ALPHA_QA.png` và close-up `CP342_SHADOW_BEFORE_AFTER_DETAIL.png`.
- So sánh thực: **2.364 pixel alpha bị chỉnh**, **1.506 pixel giảm dưới ngưỡng alpha 128**, tích lũy giảm **360.784 đơn vị alpha**; vùng floor QA giảm 209.000 đơn vị alpha; vùng giày giữa **0 delta**; tất cả **88.150 pixel ở 410 hàng trên** không thay đổi. Màu RGB vẫn nguyên, kể cả áo và khuôn mặt.
- **13/13 local binary tests PASS**: SHA nguồn user-approved, crop khớp byte, RGB bất biến, 410 dòng không đổi alpha, floor reduction, vùng giày/tua giữ lại, PNG mask và delta, 9 hash output, ORA ZIP/CRC/merged, production gate vẫn tắt.
- ZIP `TVK_LamThien_CP342_Front_Alpha_Shadow_Cleanup_NOT_SPINE_READY.zip` **15 entries / ZIP CRC PASS**, SHA-256 `76d8fd962688dde6356d4853b5e522b5ce78567a1e08ae3739668851ec5ebf66`. Lưu Library `/Thanh Van Ky/Development/CP342_Canon_V2_1_Alpha_Shadow_Cleanup/`.

## Giới hạn còn tồn tại

- Màu pale drapes trùng nền, vẫn có white halo/viền vải và chút shadow. Thuật toán alpha có thể xóa nhầm vùng vải bán trong suốt và **không** tự tái tạo pixel bị che. Bản này không nên tự chốt nghiệm thu mỹ thuật.
- **215×449 là native crop của poster**, không phải ảnh vẽ rig-ready high-res. Chưa có semantic layer `body/hair_front/hair_back/face_underpaint/bodice/arms/sleeves/ribbons`; chưa có mesh/Spine/Android APK.
- `production_release.status=blocked_pending_art` và `sprite_paths={}`. Cấm đưa R&D matte vào game.

## Next: CP343

1. Dừng thêm vòng tự chỉnh mask khi chưa có đột phá; chuyển sang **vẽ thật một Front native high-resolution theo CANON V2.1** có các lớp độc lập **và vùng underpaint ẩn** dưới tóc/áo/tay, không đổi body/bodice đã chốt.
2. Test một pose Front ở góc quay/động tác nhẹ để xác minh không thủng da/vải, occlusion, draw order và alpha. Review full body side-by-side với CANON V2.1.
3. Sau artist + user asset acceptance riêng mới làm 5 biểu cảm độc lập, 100/70/50/30 overlays, các góc nhìn, và chạy CP335 release gate, Spine/Android APK.

**CP342 chỉ hoàn thành thử nghiệm xử lý alpha; P1 semantic artist art, P2 rig, P3 APK chưa nghiệm thu.**

- [Manifest](LAM_THIEN_CP342_SHADOW_CLEANUP_MANIFEST.json)
- [Artist handoff](LAM_THIEN_CP342_ARTIST_HANDOFF.md)
