# Thanh Vân Ký — CP398 / Lâm Thiển mắt nhắm, refinement study

**Ngày:** 2026-10-30  
**Checkpoint:** CP398 — **TECHNICAL DRAFT ONLY; VISUAL QA / ART NOT YET APPROVED**.  
**Nguồn:** Lâm Thiển CANON V2.1 file chuẩn nguyên byte; **KHÔNG phải** mẫu tóc đen hay tóc bạc từ bộ reference trang phục mới.

## Nguồn đúng (khóa SHA)

- `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`: 941×1672 RGBA, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- Crop biểu cảm `Ngại ngùng`: `(25,684,193,881)`, **168×197** native pixel-exact.
- `CP397_CLOSED_EYE_PAINT_STUDY_DRAFT_NOT_APPROVED.png`: SHA256 `0baf2ad9c2524ac355d106556dea0b506f12644dc99a1b3d77df3e522de3d554`.
- Bản CP398 chỉ đọc đúng hai nguồn kể trên, từ chối SHA sai trước khi tạo file.

## Đã thực hiện

1. Tạo vùng chỉnh mí và ánh sáng da từ CANON, đường mi theo đường cong trái/phải riêng, có taper và vài sợi mi nhỏ. Đây là kỹ thuật retouch raster có giới hạn, KHÔNG phải họa sĩ vẽ khung HD mới.
2. Hai phương án **NATURAL** và **SOFT** để người dùng so sánh; đều là **DRAFT/NOT APPROVED**.
3. Tạo một OpenRaster `CP398_CANON_EYELID_REFINEMENT_13_LAYER_NOT_APPROVED.ora`: CANON thật là layer duy nhất hiện; CP397, 8 lớp retouch Natural, 2 composite variant và ROI guide đều ẩn. Các lớp phiên bản Soft là các PNG riêng trong `layers/` và đã bao gồm trong ZIP.
4. Bảng so sánh: `CP398_CANON_CP397_NATURAL_SOFT_COMPARE.png`; bảng phóng to mắt: `CP398_BOTH_EYES_NATIVE_ZOOM_COMPARE.png`.
5. 19/19 kiểm thử local PASS (4 public/static + 15 source-locked). Trong CI công khai không có tài nguyên nguồn: dự kiến 4 PASS, 15 SKIP; SKIP không phải kiểm định mỹ thuật.. Đây chỉ là **QA nguồn/độ toàn vẹn/vùng chỉnh**, không phải đánh giá vẻ đẹp.

## Kiểm tra giới hạn nguồn

- Tổng pixel thay đổi so với CP397: `natural` và `soft` ghi chính xác trong `CP398_REPORT.json`.
- **0 pixel ngoài hai mắt** thay đổi so với CANON ở cả hai lựa chọn.
- ROI LEFT `(29,93,71,124)`, RIGHT `(83,70,129,110)`.
- Nguồn gốc 168×197 là nhỏ; zoom x4/x6 là để kiểm tra pixel, không tự tạo chi tiết HD.
- Nét mắt vẫn có thể cần họa sĩ chỉnh trực tiếp thêm: các đường mí và chất liệu da vẫn có cảm giác vector/retouch ở bản phóng lớn. **Không đánh dấu aesthetic PASS**.

## Release gate

```json
{
  "checkpoint": "CP398",
  "visual_qa": "NOT_PASSED_PENDING_HUMAN_REVIEW",
  "source_canon_unchanged": true,
  "production_release": {
    "status": "blocked_pending_visual_art_approval",
    "sprite_paths": {},
    "spine_ready": false,
    "apk_ready": false
  }
}
```

## Bước tiếp theo

Người dùng chọn hoặc góp ý NATURAL/SOFT ở 168×197 và zoom; nếu vẫn chưa đạt chất lượng thì họa sĩ cần vẽ native/higher-detail master mí nhắm đồng nhất CANON. **Chỉ sau khi được duyệt trực quan** mới tạo các frame chớp mắt `mở → hé → nhắm → mở`, và sau đó mới kiểm nghiệm rig và APK riêng.

## Tái tạo local

```bash
python -m pip install pillow numpy
python cp398_eyelid_refinement.py \
  --canon LAM_THIEN_CANON_V2_1_FINAL_20261029.png \
  --cp397 CP397_CLOSED_EYE_PAINT_STUDY_DRAFT_NOT_APPROVED.png \
  --out OUTPUT
python -m unittest discover -s tests -v
```

Bản CP398 này độc lập với tham khảo trang phục A/B, KHÔNG thay đổi `app/src/main/assets` hoặc CANON đã chốt.