# Thanh Vân Ký — CP379 | Lâm Thiển Front full-body blocking pass

**Ngày:** 2026-10-30. **Trạng thái: nghiên cứu vector toàn thân, CHƯA DUYỆT MỸ THUẬT / NOT RIG READY / NO APK.**

## Nguồn chính thức, không được thay

- CANON: `LAM_THIEN_CANON_V2_1_FINAL_20261029.png` (941×1672 RGBA), **SHA-256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`**. Trong output, file này được sao chép byte-for-byte, không encode lại.
- Crop Front nguyên nguồn `(13,172,230,630)` = **217×458 pixel**; màu tóc bạc tím, bộ trắng–xanh–vàng, vóc dáng +17% đã được chốt và hai mũi guốc xanh luôn là chuẩn.
- Quy tắc CANON-only: ảnh review chỉ dùng chính CANON, crop từ CANON và bản DRAFT được gắn nhãn của đúng Lâm Thiển; không dùng ảnh mẫu nhân vật khác.

## Phần mới đã thực hiện

1. **21 SVG mới với đường Bézier/gradient chỉnh sửa độc lập** trên canvas tác nghiệp 1302×2748, gồm 2 vạt lụa dài phía sau, tóc sau trái/phải, da 2 chân, 2 guốc xanh, váy trước, thân da bị che, thân áo, 2 tay/bàn tay, 2 tay áo lụa, vòng cổ, mặt, mắt/miệng, tóc trước, hoa/ruy băng tóc và trang sức hông–vai. Mỗi SVG có PNG-alpha riêng. Các nét SVG được dựng độc lập; không nhúng bitmap CANON vào layer art vẽ mới.
2. OpenRaster **`CP379_21_AUTHORED_FULLBODY_BLOCKING_DRAFT_NOT_RIG.ora`**, 22 lớp (21 art visible + 1 CANON crop hidden), file mở chỉnh sửa trong Krita. Nguồn vector vẽ là các mảng color-block thô, **không phải art artist-grade hoặc master HD**. Kích thước canvas 6× không biến nguồn 217×458 thành nguồn ảnh chi tiết hơn.
3. Giữ một ORA tham chiếu nguồn riêng **`CP379_SOURCE_19_PARTS_NOT_RIG.ora`**, 20 lớp (19 source-pixel guide + 1 CANON guide ẩn). Khi ghép tư thế đứng, các phần nguồn khớp với matte CP374; bản source trace **chưa có underpaint** và vẫn có vấn đề matte ở viền lụa/bóng sàn.
4. Preview **`qa/CP379_CANON_FULLBODY_VECTOR_COMPARISON_NOT_APPROVED.png`** đối chiếu CANON, crop Front, vector draft và chi tiết chuẩn. Cột draft được đánh dấu NOT APPROVED, không thay thế bản CANON.

## Kiểm chứng

- **12/12 unit tests local PASS** với ảnh đúng và các lớp nguồn thật; mô phỏng môi trường công khai không có ảnh private: **4 PASS / 8 SKIP**. Không có đo FPS/máy Android hoặc nghiệm thu mỹ thuật.
- Nguồn được xác minh SHA và kích thước; script từ chối CANON sai trước khi tạo tệp đầu ra.
- Tách cả hai giày trong *source guide*, vùng xanh bên trái **163/163**, bên phải **146/146** (đây là chứng cứ từ nguồn gốc, không phải tuyên bố art vector hay runtime đã qua QA giày).
- Hai ORA ZIP CRC PASS, source-layer merge đúng ảnh matte CP374, 21 lớp vẽ có alpha và đường SVG khác nhau, luôn giữ `visual_qa=NOT_PASSED`, `production_release=blocked_pending_art`, `sprite_paths={}`.

## Giới hạn sản xuất / CP380

- **Bản vector còn khác CANON rõ rệt về mặt, tóc, thân áo, chi tiết vàng, lụa và giày.** Không tự chốt; không import vào game. Bản phác thảo 21 layer là nền để họa sĩ sửa/trace/paint thật.
- Chưa vẽ lớp da/vải/tóc bị che đầy đủ dưới khớp để motion an toàn; còn cần pose-specific keyframes, tách mặt (5 biểu cảm), 4 mức hư hại 100/70/50/30 và các góc nhìn khác.
- **CP380:** chọn một khu vực art Full Front (mặt–tóc–thân áo hoặc tay áo), **vẽ chi tiết chất lượng cao trên 21-layer master**, so trực tiếp CANON trước khi chốt; tiếp tục underpaint từng khớp, kiểm 2 guốc xanh và chuyển động. Chỉ sau nghiệm thu mới chuẩn bị Spine/rig, gameplay và Android APK.

## Cách chạy lại

```bash
python tools/art/cp379_fullbody_vector_blocking.py \
  --canon LAM_THIEN_CANON_V2_1_FINAL_20261029.png \
  --matte CP374_PARTIAL_FLOOR_REMOVAL_NOT_ART.png \
  --source-layers CP374_SOURCE_LAYERS \
  --out ./OUTPUT
python -m unittest tests/art/test_cp379_fullbody_vector_blocking.py -v
```

Lưu ý: `CP374_SOURCE_LAYERS` là 19 PNG từ CP374. Không đưa ảnh private vào GitHub công khai; bản handoff ZIP và Library giữ các byte nguồn và lớp ảnh để chạy lại.

## GitHub Actions sau khi đồng bộ

- Workflow **`CP379 full-body draft technical source guard`**, run ID `40994186046`: **completed / success** trên commit CP379 được kiểm tra. Đây là kiểm thử static public source; các test cần ảnh CANON/source-layer riêng tư không chạy trên GitHub.
- **Không suy ra Visual QA đã đạt, không mở khóa Spine hay APK** chỉ từ workflow xanh.
