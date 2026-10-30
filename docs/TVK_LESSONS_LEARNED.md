# Thanh Vân Ký — Sổ kinh nghiệm & playbook cho mọi checkpoint

**Bắt đầu:** 2026-10-30. **Mục đích:** biến kinh nghiệm thực tế thành quy trình dùng lại được, tăng độ chính xác và giảm vòng lặp không cần thiết. Mục tiêu tối ưu là **chất lượng/tốc độ hoàn thành thực**, không phải số checkpoint hoặc số test PASS.

## 8 quy tắc bắt buộc

1. **Source/CANON lock:** đọc `docs/PROJECT_SPEC.md` trước; xác minh filename + kích thước + SHA-256 của CANON. Khi gửi preview phải dùng đúng ảnh CANON nhân vật hiện hành, hoặc crop đúng từ ảnh đó; ảnh mới là `DRAFT`, ảnh của người dùng bổ sung là `REFERENCE`.
2. **Không hòa trộn sai pose:** CP410/CP411 chứng minh crop biểu cảm 168×197 và crop body đứng 208×443 từ cùng nguồn không thể overlay trực tiếp. Cần master mặt ở đúng pose và underpaint tóc/cổ trước khi rig quay đầu/blink.
3. **Tách kiểm thử kỹ thuật và thẩm mỹ:** PASS hash, pixel, alpha, ROI không thay cho visual approval. Không suy diễn `CI SUCCESS` hoặc `assembleDebug SUCCESS` là đã test điện thoại thật.
4. **Không giả nguồn art:** upscale là viewing proxy, ORA với paint layer trống là artist handoff, biến dạng bitmap không phải rig phân lớp. Ghi đúng phần đã làm và phần chưa làm.
5. **Không thay CANON âm thầm:** trạng thái asset phải là `REFERENCE -> DRAFT -> REVIEWED -> APPROVED_CANON -> INTEGRATED -> DEVICE_VERIFIED`. Nâng trạng thái chỉ khi có bằng chứng tương ứng.
6. **Kiểm QA toàn hình:** ngoài cận cảnh mặt/trang phục còn phải xem whole-body, tay áo, tóc, phụ kiện, hai chân và mũi giày; áp dụng bài học từ lỗi mũi guốc bị khuyết trong các preview cũ.
7. **Batch có tiêu chí:** chỉ tạo vài phương án có khác biệt đáng đánh giá; so sánh native + zoom + full-image, chốt/loại theo bằng chứng, tránh thử cùng một bản vá nhỏ nhiều lần không cải thiện art.
8. **Không đánh dấu blocker là resolved quá sớm:** ghi `PASS/FAIL/SKIP` rõ ràng; thiếu file nguồn/private tests hoặc thiếu kiểm Android thực thì giữ `BLOCKED`/chưa nghiệm thu.

## Kinh nghiệm mới — hình thể, trang phục, rách/bẩn (2026-10-30)

Nguồn [4 ảnh tham khảo và SHA](art/TVK_COSTUME_DAMAGE_REFERENCES_20261030.md). Đây là nguồn **tham khảo**, không phải những model đã chốt.

- Tách lớp kỹ thuật theo vật liệu và chức năng (vải chính, vải lót, voan/thêu, phụ kiện, quần tất); nếu không có master layer thì đừng giả định có rig.
- Bốn mốc 100/70/50/30 phải **kế thừa nhau**: rách/đường chỉ/hoa văn phát triển có lý, không xuất hiện mất đi ngẫu nhiên giữa các frame.
- Chất liệu khác nhau có đường rách, căng và bóng khác nhau; bụi và vết xước đặt theo điểm ma sát, không phủ mất hoa văn hay che biểu cảm.
- Mức % **không** đồng nghĩa phần trăm diện tích vải bị xóa. Mức thấp vẫn bảo toàn silhouette, form, độ che phủ và tính nhất quán của nhân vật.
- Kiểm tra mặt trước/mặt sau: đường nối vai, lưng, eo và trang sức phải đối chiếu được. Bộ ảnh có nhiều góc nhìn không tự động là turnaround rig-ready.
- Logic gameplay: trạng thái trang phục đổi khi lần đầu xuống ngưỡng HP liên quan và được giữ trong các cảnh sau theo spec; art phải tách khỏi điều kiện logic để có thể đổi asset mà không sửa engine.

## Bảng workflow lặp

| Bước | Kiểm tra để chuyển bước |
|---|---|
| 1. Read | `PROJECT_SPEC`, checkpoint, CANON đúng SHA, blockers |
| 2. Define | asset ID, trạng thái `REFERENCE/DRAFT/CANON`, acceptance criteria |
| 3. Reuse | script/ORA/test đã xác minh; không sinh master giả |
| 4. Preview | fullbody + chi tiết + native/zoom, trước/sau, 100/70/50/30 nếu liên quan |
| 5. QA | hash/pixel/alpha/layer + art visual + Android thiết bị thật khi cần |
| 6. Commit | cập nhật artifact, SHA, GitHub/Library, liên kết ở spec |
| 7. Resume | chỉ ghi hoàn tất điều có chứng cứ; lưu rõ việc còn mắc để phiên sau đọc tiếp |

## Mẫu entry khi phát sinh bài học

```md
### YYYY-MM-DD — CPxxx — Tên vấn đề
- Input và nguồn lock (filename/SHA/branch/commit):
- Dấu hiệu lỗi / kiểm chứng:
- Cách làm hiệu quả và vì sao:
- Cách làm không hiệu quả / điều cần tránh:
- Kết quả kỹ thuật (PASS/FAIL/SKIP):
- Kết quả mỹ thuật và Android thực:
- Quy tắc có thể dùng lại:
- Blocker chưa xử lý / bước tiếp theo:
```

## Metrics hướng tới hiệu quả

- Lần dùng sai nguồn CANON (mục tiêu 0).
- Số lỗi tái xuất hiện sau khi đã ghi lessons (mục tiêu 0).
- Vòng tạo/sửa trước khi được duyệt mỹ thuật, phân biệt art và technical.
- Mức độ hoàn thành thực: `DRAFT`, `APPROVED_CANON`, `INTEGRATED`, `DEVICE_VERIFIED`.

**Trạng thái 2026-10-30:** `PROJECT_SPEC` đã đến CP411. Art master đầu/mí mắt đúng pose đứng, rig phân lớp và test điện thoại thật vẫn chưa hoàn tất. Không đổi các trạng thái đó vì cập nhật tài liệu.
