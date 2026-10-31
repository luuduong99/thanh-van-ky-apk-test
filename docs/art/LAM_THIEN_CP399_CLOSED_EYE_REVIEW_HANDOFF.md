# Thanh Vân Ký — CP399: Lâm Thiển closed-eye art review / decision gate

**Ngày:** 2026-10-30  
**Kết quả:** HOÀN TẤT GÓI REVIEW KỸ THUẬT — **MỸ THUẬT CHƯA ĐẠT/CHƯA DUYỆT**. Không có animation, Spine, APK hoặc sản phẩm nghệ thuật mới đạt chuẩn.

## Nguồn, khóa SHA-256

Nguồn hình là **duy nhất CANON V2.1** `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, 941×1672 RGBA, SHA-256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.

- Crop mặt `Ngại ngùng`: `(25,684,193,881)` (168×197 native), byte/pixel không sửa.
- CP397 (cũ): `0baf2ad9c2524ac355d106556dea0b506f12644dc99a1b3d77df3e522de3d554`.
- CP398 Natural: `6f36ba97e307f3c31c4166dd9a539ec945f12dde4a31370196e0c7497af391ea`.
- CP398 Soft: `5ce4ab198235a58905d8f867f53973d7d49d3e9686bb769675568d454c142c17`.

## Hoàn tất CP399 thực tế

1. Bộ bảng duyệt `CP399_CANON_NATURAL_SOFT_REVIEW_16x9.png`: 3 chân dung **CANON/Cp398 Natural/Cp398 Soft** cùng một nguồn; chỉ phóng to để người dùng thấy dễ hơn.
2. Bảng 8 vùng ảnh cho cả hai mắt `CP399_EYES_EXACT_NATIVE_ZOOM.png`: CANON/CP397/Natural/Soft, phóng nearest-neighbor ×8 để nhìn chính xác pixel. **Không tô lại pixel gốc.**
3. Bốn file ảnh crop nguồn ở 168×197, báo cáo JSON, bản ghi phê duyệt cố ý để **NOT_APPROVED**, mã kiểm thử và script tái tạo.
4. **13/13 local unit tests PASS**: source SHA, kích thước/mode, crop exact, 0 pixel ngoài ROI thay đổi, hai ứng viên khác nhau, phát hiện giả mạo source/draft, không tạo output sau khi fail, **không mở production dù JSON đặt phê duyệt giả**.
5. Repo public không có ảnh CANON riêng: kiểm thử trên public **dự kiến 4 PASS/9 SKIP**. Không đánh đồng SKIP với nghiệm thu.

## Kết quả thực tế của hai ứng viên

- Natural thay đổi **2.006** pixel trong hai vùng mắt so với CANON; Soft **2.012**; khác nhau **928** pixel; cả hai **0 pixel thay đổi bên ngoài hai ROI**.
- Natural có nét rõ hơn, nhưng đường mi bị băng xám, phần đầu/cuối chưa thon tự nhiên.
- Soft mượt/nhẹ hơn nhưng thiếu ranh giới mi tự nhiên, hơi phẳng khi phóng lớn.
- **CẢ HAI: NOT APPROVED.** Không thể quyết định chất lượng từ kiểm thử pixel hoặc báo cáo tự động.

## CP400 — việc cần làm thật, không thêm các patch nhỏ tùy tiện

1. Vẽ lại **mắt nhắm chất lượng họa sĩ**, đi từ ảnh CANON đúng nhân dạng; dựng nếp mí mềm, sắc độ da khớp ánh sáng gốc, vi cấu trúc và chân lông mi thon dần, xử lý cả hai khóe mắt.
2. Giữ toàn bộ khuôn mặt, tóc, cơ thể, trang phục ngoài hai ROI đúng CANON; nếu cần nới vùng sửa phải gửi QA trước. Tối ưu bản vẽ **168×197 gốc và bản vẽ nguồn chất lượng cao nếu có**, không tự gắn nhãn HD cho ảnh phóng lớn.
3. Gửi đối chiếu ở kích thước gốc và zoom, **nhận duyệt từ người dùng**. Chỉ sau bước này mới làm in-between mở → nhắm → mở và đưa sprite/rig vào APK.
4. Không dùng ảnh của mẫu nữ tóc đen/tóc bạc mới để thay ảnh Lâm Thiển. Định hướng áo quây B thuộc thư viện tham khảo **nhân vật khác**.

**Trạng thái release khóa:** `production_release.status=blocked_pending_approved_eye_art`, `sprite_paths={}`, `spine_ready=false`, `apk_ready=false`.

## Rebuild

```bash
PYTHONPATH=tools/art python tools/art/cp399_closed_eye_art_review.py \
  --canon /path/to/LAM_THIEN_CANON_V2_1_FINAL_20261029.png \
  --cp397 /path/to/CP397_PREVIOUS_CLOSED_EYE_DRAFT_NOT_APPROVED.png \
  --natural /path/to/CP398_CLOSED_EYE_NATURAL_DRAFT_NOT_APPROVED.png \
  --soft /path/to/CP398_CLOSED_EYE_SOFT_DRAFT_NOT_APPROVED.png \
  --out /path/to/CP399_OUTPUT
PYTHONPATH=tools/art python -m unittest discover -s tests/art -p 'test_cp399_closed_eye_art_review.py' -v
```

Bộ ZIP CP399 trong Library chỉ dùng cho bàn giao/QA, không có sprite game mới.