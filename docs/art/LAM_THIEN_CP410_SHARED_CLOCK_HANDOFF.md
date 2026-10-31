# Thanh Vân Ký — CP410 / Đồng bộ body idle và chớp mắt trong một đồng hồ DEBUG

**Ngày:** 2026-10-30  
**Trạng thái:** DEMO KỸ THUẬT; chưa đạt nghiệm thu mỹ thuật, chưa có rig phân lớp, chưa có blink production.

## Nguồn và giới hạn bắt buộc

- CANON V2.1 `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`, kích thước 941×1672 RGBA, nguyên byte.
- Vùng đứng toàn thân: `(16,180,224,623)`, 208×443, **khác góc vẽ** với vùng mặt dùng ở CP409 `(25,684,193,881)`, 168×197.
- Atlas 15 khung CP409 (native 2520×197), SHA256 `d9234630eab9e13ec07527e2c7b6fbbacd849117bf2e4983bf35ac4bcf73a07e`; khung 0 bằng chính xác vùng mặt CANON.
- Do **khác tư thế/góc vẽ** nên **không được phủ ảnh mắt CP409 lên đầu của bản đứng**. CP410 xem đồng bộ ở hai vùng hiển thị khác nhau, ghi nhãn rõ. Đây là kết quả đúng về nguồn và thử đồng bộ, KHÔNG phải animation mắt gắn trên fullbody.

## Việc đã làm

1. `TVKPreviewClock.kt` sử dụng đồng hồ monotonic chung cho chuyển động fullbody và khung CP409. Khi pause giữ thời gian tại chỗ và resume tiếp tục, không reset ảnh về trạng thái đầu như CP408.
2. `TVKCombinedIdleMotionView.kt` vẫn là bitmap-mesh 5 kênh nhịp khác nhau (thở/đầu/tay/tóc/lụa), lấy thời gian từ đồng hồ chung. Nó **không** là xương/mesh rig phân lớp thật.
3. `TVKCombinedBlinkInsetView.kt` hiện hình mắt CP409 ở ô **tách biệt**, cùng timeline 2.4 giây/chu kỳ; dùng frame atlas gốc, không dựng ảnh nhắm mới.
4. `TVKCombinedIdlePreviewActivity.kt` yêu cầu chọn hai tệp từ Android picker, xác nhận raw SHA-256 trước khi decode, kích thước đúng, khung 0 atlas **pixel-identical** với CANON. Sai nguồn phải từ chối, không dùng legacy sprite fallback. Chỉ chạy ở `FLAG_DEBUGGABLE`, activity không exported, không đóng gói private CANON/atlas vào assets.
5. Tạo video CP410 body+face hai panel (4.8 giây, 30 FPS), bảng so sánh 6 trạng thái, và bộ QA kiểm tra 14 trường hợp khi có ảnh nguồn.

## Kiểm thử / release gate

- Trên máy tạo thử có hai ảnh chính xác: **14/14 local QA PASS** (9 source/static + 5 private exact-image).
- GitHub repo công khai không có private source: **9 PASS, 5 SKIP** là kết quả dự kiến, không tự coi SKIP là PASS.
- [CP410 public source QA](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/41061717703) **SUCCESS**: 9 PASS, 5 private-source SKIP.
- [Android build](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/41061708348) **SUCCESS**: `app-debug.apk` 8,810,643 bytes, SHA256 `a6ba38ee15f604a088827d0e327e57d17945786859d82c0c5904ef304ad79870`. This confirms compilation, not execution on a physical phone.
- CANON production lock succeeded. The APK has no original CANON bitmap or private CP409 atlas embedded in assets.
- Entry point: `CP410 | Body + chớp mắt đồng bộ (DEBUG)` in Lâm Thiển interaction screen.
- **Art QA NOT APPROVED; true rig NOT READY; exact same-pose eyelid master MISSING; physical phone QA NOT DONE; production sprite paths `{}`.**
- Không đưa CP409 vào mặt hình đứng chỉ để minh họa hiệu ứng; cần master mắt nhắm đúng pose body (hoặc bộ head rig phân lớp đúng nhận diện) rồi mới làm compositing thực.

## Hướng đi tiếp theo

**CP411** tập trung tạo **same-pose head/eyelid source**: vẽ hoặc phục hồi nguồn vùng đầu của fullbody ở độ phân giải cao theo đúng CANON, underpaint hợp lệ, phân lớp tóc/mặt/mí/mi và pivot xương đầu; kiểm tra phiến/màu dưới các tư thế thở/nghiêng đầu, đồng thời xem video và duyệt nét mắt. Chỉ sau đó mới ghép blink đúng lên head/body và test Android thật.

Mọi tệp art đang ở trạng thái DRAFT, không làm thay đổi CANON đã duyệt hoặc tỷ lệ cơ thể +17%.