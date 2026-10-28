# Lâm Thiển — CP315: kiểm thử ORA / seam / alpha

**Ngày:** 2026-10-28  
**Trạng thái:** Đã hoàn thành **công cụ QA + unit tests**, **chưa chỉnh xong model** vì chưa có file CP313 ORA 10 lớp.

## Quy chuẩn không thay đổi

- Model Lâm Thiển gốc giữ nguyên nhận diện và màu trang phục trắng–xanh–vàng.
- Tỷ lệ hình thể tăng **+17%** là nền chốt. Chỉ được tinh chỉnh nhẹ chiều cao và tỷ lệ tổng thể, phải gửi preview để duyệt. Áp dụng nguyên tắc preview này cho các nhân vật tương lai.
- Không đánh dấu model/rig Spine/Unity hoặc APK đã hoàn thành nếu chưa kiểm chứng asset tương ứng.

## Những gì đã thực hiện tại CP315

1. Nâng cấp script audit ORA từ gói CP314: đọc 10 lớp, render composite và ảnh layer isolation, ROI crop, so `mergedimage.png`.
2. Thêm so sánh ảnh **trước/sau trong vùng được phép chỉnh**: 
   - `--baseline` để cung cấp composite CP313 trước sửa;
   - `--allowed-roi` một hoặc nhiều vùng thay đổi hợp lệ;
   - phát hiện pixel bị sửa ngoài vùng (mặc định phải bằng 0).
3. Thêm mô phỏng dịch chuyển riêng lớp tóc được chọn `±5px` theo bốn hướng. Dò pixel alpha mới bị thủng bên trong vùng an toàn quanh gáy/vai `--motion-roi`. Có mask riêng để kiểm tra.
4. Thêm unit tests dùng **ORA tổng hợp 10 lớp**; 5/5 test PASS ở môi trường chạy hiện tại:
   - full underpaint khi dịch tóc: pass, 0 holes;
   - thiếu underpaint: phát hiện **70 holes** và fail;
   - thay đúng trong ROI: pass;
   - sửa lệch ROI: phát hiện **9 pixels** và fail;
   - ROI ngoài khung: reject.
5. Không thay file tham chiếu PNG; không sinh giả một ORA 10 lớp từ ảnh phẳng.

> **Quan trọng:** các con số 70 và 9 ở trên là kết quả từ **fixture giả lập**, không phải số liệu pixel thật của CP313.

## Nguồn có thể xác minh

- Google Drive hiện có `lin_qian_back.png` (207×656 RGB) và `lin_qian_sheet.png` (1448×1086 RGB). Cả hai là ảnh phẳng, không có thông tin lớp.
- Tệp `TVK_CP314_LamThien_Handoff.zip` đã kiểm tra: có preview, PNG tham chiếu, script CP314 và tài liệu; **không chứa ORA 10 lớp**.
- Tên gói nguồn mong đợi theo handoff trước: `TVK_CP313_LamThien_Back_10Layer.ora` hoặc ZIP có ORA tương ứng; chưa xác minh tên tệp tồn tại.

## Lệnh chạy sau khi lấy được ORA nguồn

```
python -m pip install Pillow
python -m unittest discover -s tests/art -v
python tools/art/audit_ora.py CP313.ora --expect-layers 10 --out reports/cp313
python tools/art/audit_ora.py CP315_edit.ora --expect-layers 10 \
  --baseline reports/cp313/composite_rgba.png \
  --allowed-roi x,y,width,height --roi x,y,width,height \
  --motion-layer hair --motion-roi x,y,width,height \
  --motion-px 5 --max-holes 0 --out reports/cp315
```

Trong lệnh cuối, `hair` là ví dụ; thay bằng tên lớp tóc thực tế trong ORA. `x,y,width,height` phải xác định trên **canvas ORA gốc**, không được mặc định lấy theo ảnh PNG 207×656. Nếu nhiều lớp tóc cùng chuyển động, truyền `--motion-layer` nhiều lần. Công cụ chỉ đọc bản gốc, không chỉnh pixel.

## Điểm tiếp tục CP316

1. Lấy đúng CP313 ORA 10 lớp (và baseline/composite trước chỉnh). Kiểm tra hash, kích thước canvas, tên và thứ tự lớp.
2. Phân định ROI gáy/tóc/vai trên canvas ORA (không đoán từ thumbnail).
3. Sửa underpainting tóc–gáy và da vai trên các lớp thật. Kiểm tra dây trang sức xanh–vàng. Làm tiếp 2 tay áo.
4. Chạy QA CP315; xử lý mọi pixel ngoài ROI và alpha hole trong ROI.
5. Xuất ảnh so sánh, các layer isolation, preview trước/sau để người dùng duyệt; **sau đó** mới nghiệm thu và tích hợp rig/physics.