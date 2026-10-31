# Thanh Vân Ký — CP394: giữ nét mi CANON cho bản nhắm mắt Lâm Thiển

**Ngày:** 2026-10-30  
**Trạng thái:** Kỹ thuật hoàn thành ở mức thử nghiệm; **mỹ thuật NOT APPROVED**. Không phải animation, không phải sprite HD, không phải APK.

## 1. Nguồn được phép

- Duy nhất **Lâm Thiển CANON V2.1** `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, 941×1672 RGBA; SHA-256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- Biểu cảm **Ngại ngùng**: crop gốc `(25,684,193,881)` kích thước **168×197**. Ảnh trong gói được sao chép **nguyên byte** từ CANON.
- Bản CP393 trong gói chỉ làm đối chứng bản nháp. **Không dùng** ảnh tự sinh/ảnh Tô Nguyệt Ly để tạo Lâm Thiển.

## 2. Kết quả thực tế của CP394

- Đã thử kỹ thuật **giữ lại dải pixel mi mắt của ảnh CANON**, che bớt đồng tử bằng vùng màu và kết cấu da lấy trong cùng ảnh, thêm lớp bóng mí mềm. Hai mắt dùng đường cong riêng, không phản chiếu đối xứng.
- Tạo **6 lớp RGBA riêng** (`SKIN`, `CANON_LASH`, `CREASE` × 2) và **2 composite draft** (`closed`, `soft`). OpenRaster có **10 lớp**: duy nhất bản CANON mở mắt visible, 9 lớp kiểm tra hidden.
- Ảnh xem thử thật gồm CANON/CP393/CP394, tất cả đều từ một nguồn. Bản CP394 **giữ đường mi đậm tốt hơn**, nhưng **mắt trái vẫn có cảm giác hé**, vùng da che còn thiếu nét họa sĩ. Do đó **không** tuyên bố đã hoàn thành mắt nhắm.
- Ở canvas thật 168×197, bản `closed` khác CANON **1.766 pixel**, bản `soft` khác **1.481 pixel**; ở ngoài hai vùng mắt là **0 pixel**. Đây là kiểm thử giới hạn sửa, **không** phải số đo độ đẹp.
- Các lớp `CANON_LASH` là pixel gốc có alpha mask, còn lớp da là tái sử dụng màu nguồn; **không phải 6 lớp anatomy native HD được vẽ mới**.

## 3. Test và release gate

- **11/11 kiểm thử local PASS** trên CANON/CP393 thật: SHA, crop pixel-exact, lớp art, ORA/CRC, chỉ một lớp source visible, 0 thay đổi ngoài mắt, từ chối SHA sai trước khi ghi.
- **4 PASS / 7 SKIP** ở checkout công khai không có CANON/CP393, cần giữ đúng ý nghĩa này khi đọc GitHub Actions.
- `visual_qa=NOT_PASSED`; `production_release.status=blocked_pending_art`; `sprite_paths={}`; không bật rig/Spine/APK và không chép bản này vào `app/src/main/assets`.

## 4. CP395 — việc còn thiếu

1. **Chỉnh hình mắt trái**: loại phần iris hở mà không phá các sợi mi được giữ từ CANON.
2. **Vẽ mắt nhắm hoàn toàn thật**, có vùng da khuất, nếp mí, vi cấu trúc bóng và các sợi mi tinh xảo, phù hợp nhận diện và chất lượng CANON.
3. So ở **kích thước gốc 168×197 và phóng to**, gửi người dùng duyệt mẫu mắt nhắm trước khi làm blink in-between.
4. Chỉ sau nghiệm thu mới chuyển sang các biểu cảm còn lại, rig toàn thân, QA chuyển động và APK Android.

## 5. Tái tạo

```bash
python cp394_source_lash_underpaint.py \
  --canon /path/to/LAM_THIEN_CANON_V2_1_FINAL_20261029.png \
  --prior /path/to/CP393_FULL_CLOSED_PAINT_STUDY_NOT_APPROVED.png \
  --out /path/to/CP394_output
python -m unittest -v test_cp394_source_lash_underpaint.py
```

Ảnh minh họa tạo từ mô hình khác **không** phải nguồn hợp lệ của CP394. Không sử dụng các số PASS in trên ảnh minh họa làm kết quả kiểm thử.