# Lâm Thiển — CP317 / Back reconstruction (PROXY, not original)

**Ngày:** 2026-10-28. **Trạng thái:** BẢN PHỤC DỰNG KỸ THUẬT, chưa duyệt, chưa vào APK/Spine.

## Quy chuẩn canon

- Giữ nguyên ảnh Back của Lâm Thiển từ Google Drive, màu trắng–xanh–vàng, tóc bạc và tư thế đã duyệt.
- Giữ mốc **+17%** từ thiết kế đã chốt. CP317 không tự tăng hoặc giảm tỷ lệ nhân vật; ảnh phục dựng lấy nguyên pixel của PNG Back hiện có. Mọi thay đổi chiều cao/tỷ lệ phải có preview và duyệt.
- File gốc CP313 ORA 10 lớp **chưa tìm được**. File ORA CP317 là bản thay thế kỹ thuật từ ảnh phẳng, **không phải CP313, không là rig**.

## Những gì đã tạo

- `CP317_LamThien_Back_10Layer_RECONSTRUCTION_NOT_ORIGINAL.ora`: **ORA 10 lớp không rỗng**, giữ nguyên composite tĩnh từ `lin_qian_back.png` (207×656), sai lệch 0 pixel (toàn ảnh). Đây là bản dựng lại bằng các vùng cắt ước lượng, **không phải ảnh phân lớp nguyên bản**.
- Các lớp từ trên xuống: `hair_jewelry_top`, `hair_front_highlights`, `hair_outer_strands`, `shoulder_skin_right`, `shoulder_skin_left`, `sleeve_right`, `sleeve_left`, `sash_bow`, `sash_hanging_panels`, `underpaint_estimated_NOT_SOURCE`.
- `underpaint_estimated_NOT_SOURCE` được suy đoán bằng OpenCV inpaint phía sau vùng bị che, không có bảo đảm giải phẫu/cổ áo/dây trang sức chính xác. Khi dịch tóc ±5 px, đường biên polygon lộ rõ; đây là **QC FAILED về mỹ thuật chuyển động**, chưa đủ để rig.
- Metadata `data/CP317_PROVENANCE.json` gắn nhãn `PROXY_RECONSTRUCTION_NOT_ORIGINAL`; `tools/art/source_inventory.py` từ chối nguồn phục dựng làm ứng viên CP313. Không được xóa nhãn xuất xứ để tránh nhầm lẫn.
- `preview/CP317_static_composite.png`, `preview/CP317_proxy_mask_overlay.png`, bốn hình kiểm tra dịch chuyển tóc và báo cáo JSON/ảnh layer riêng.
- 12/12 unit tests PASS trên fixture giả lập và thử nghiệm composite CP317; CP315 audit báo `INSPECTION_READY` về mặt cấu trúc. **Không đồng nghĩa phân lớp mỹ thuật đúng**.

## Bước sửa thật sau CP317

1. Ưu tiên phục hồi file CP313 ORA 10 lớp (hoặc CP312 ORA 8 lớp) từ lịch sử cũ, vì có các phần gốc không thể khôi phục từ ảnh phẳng.
2. Nếu không tìm được, người vẽ cần redrawing lớp tóc/scalp/gáy–vai/tay áo trên bản proxy; cắt lại theo viền thật, vẽ phần da–trang phục bị che, kiểm tra seam khi tóc dịch ±5 px. Không tự gắn nhãn 10 lớp gốc.
3. Khi có ảnh lớp thật, chạy `python tools/art/audit_ora.py ...` với `--baseline`, `--motion-roi`, `--allowed-roi`. Chỉ nghiệm thu nếu static không lệch ngoài ROI và chuyển động không tạo seam lỗi.
4. Tạo preview full-body, crop gáy–vai và tay áo, trình người dùng duyệt trước khi bắt đầu rig/physics/Android APK.

## Lệnh dựng lại proxy (không ghi đè file gốc)

```
python -m pip install 'Pillow>=10,<14' 'opencv-python-headless>=4.8,<5' numpy
python tools/art/reconstruct_back_ora.py lin_qian_back.png --out CP317_LamThien_Back_10Layer_RECONSTRUCTION_NOT_ORIGINAL.ora
python tools/art/source_inventory.py CP317_LamThien_Back_10Layer_RECONSTRUCTION_NOT_ORIGINAL.ora --out reports/cp317_provenance
python -m unittest discover -s tests/art -v
```

**Điểm tiếp tục CP318:** sửa seam thực tế trên các lớp phục dựng hoặc file gốc phục hồi, không lặp lại QA source inventory; preview trước khi chốt.

## Bổ sung quyết định thiết kế đã duyệt — 2026-10-28

**LƯU Ý NGHIỆM THU: PNG Back cũ dùng trong CP317 KHÔNG được coi là bản thiết kế trang phục Back cuối cùng.** Bản CP317 giữ nguyên pixel ảnh cũ và chỉ thử tách lớp; kiểm thử 0px không thể chứng minh trang phục đúng với thiết kế canon.

**ĐÃ CHỐT trước đó (2026-10-27):**
- Trang phục mặc định Lâm Thiển giữ trắng–xanh–vàng, tóc bạc dài và nhận diện gốc.
- **Khoét cân đối hai bên hông**, thấy được phom dáng tại hai sườn/hông; không tự bịt kín bằng tà áo nguyên khối.
- **Phần mông/phía sau đầy đặn, nổi khối rõ và tôn dáng** theo ảnh Back đã được người dùng duyệt; các lớp trang phục/vải phải thể hiện silhouette và độ nổi khối này. Không làm phẳng/che khuất hết chi tiết đã chốt.
- Áp dụng đồng bộ thiết kế đó vào các tư thế, không chỉ góc Back.

**ĐÃ CHỐT sau đó (2026-10-28):** lấy mốc +17% cho phần thân trên theo mẫu; bản preview điều chỉnh chiều cao hình 947→971px và vai–eo 144→168px, **không kéo giãn hông/chân**, giữ tổng thể thanh thoát. Mốc +17% là riêng Lâm Thiển, quy trình trình preview mới có thể dùng cho các nhân vật khác.

**YÊU CẦU CHO CP318:** Trước khi tách lớp hoặc nghiệm thu rig mới, phục hồi ảnh Back canon thực tế hoặc vẽ lại tạo hình Back theo các tiêu chí trên. So sánh bản đầy đủ cả người với ảnh canon được duyệt, gồm vùng hông, mông và tỷ lệ thân trên. Không sửa proxy kỹ thuật hiện tại và gọi đó là asset cuối, cũng không coi test 0px trên proxy là pass về trang phục. Gửi preview người dùng duyệt trước khi xác nhận asset chính thức.
