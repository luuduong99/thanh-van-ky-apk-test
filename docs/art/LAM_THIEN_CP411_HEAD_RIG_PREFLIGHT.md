# Thanh Vân Ký — CP411 | Chuẩn bị đầu và mặt đúng pose toàn thân

**Ngày:** 2026-10-30 · **Nhân vật:** Lâm Thiển · **Nhánh:** `map-2d-prototype` · **Trạng thái:** TECHNICAL DRAFT, **KHÔNG** phải rig/sprite/animation hoàn chỉnh.

## Vì sao cần checkpoint này

Hai asset đang dùng ở CP410 cùng thuộc bảng ảnh CANON V2.1, nhưng **khác ô và khác tư thế**:

- Front standing: tọa độ sheet `(16,180,224,623)` → **208×443 px**.
- Expression portrait: `(25,684,193,881)` → **168×197 px**.
- Mắt trên dáng đứng chỉ có hai ROI nghiên cứu khoảng **13×10 và 15×10 px**, quá ít chi tiết để chuyển nguyên atlas CP409 từ khuôn mặt biểu cảm sang mà vẫn đẹp.

Nguồn CANON: `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, **941×1672**, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.

## Những gì đã tạo thật

1. Trích đúng crop đứng và khóa SHA riêng của crop: `c5505f4ca8eb541e364cd1b9bc239be2c95695b4ebb829cbb3be647d8899219d`.
2. Đo vùng mặt, hai mắt, điểm xoay đầu (104,77), giao điểm cổ và một **rough head capsule mask**. Các điểm này ở hệ tọa độ **208×443** của ảnh đứng, không phải hệ 168×197 của ảnh biểu cảm.
3. Tạo ảnh đầu tách lớp có alpha và **lớp inpaint bên dưới đầu chỉ để kiểm tra che khuất**. Ở trạng thái không di chuyển, ghép hai lớp trả về **100% pixel gốc CANON**. Khi xoay/di chuyển thật có thể thấy vết ghép; hiện **không** được dùng cho rig production.
4. Xuất `CP411_HEAD_SEPARATION_SOURCE_LOCKED_DRAFT.ora` ba lớp (nguồn CANON hiển thị, hai lớp nghiên cứu ẩn), PNG mặt nạ, ảnh kiểm tra và manifest.
5. Bổ sung `TVKFrontPoseRigAuditOverlay.kt` cho CP410 debug viewer: chỉ sau khi người dùng chọn PNG CANON có SHA đúng, có thể bật hướng dẫn mốc đầu/mắt/cổ. Overlay luôn **reset + pause** body về tư thế nguồn để các mốc không lệch theo mesh.
6. **14/14 unit tests PASS cục bộ** với nguồn CANON thật; repo public không có CANON dự kiến **7 PASS + 7 SKIP**. Bài kiểm tra kỹ thuật không xác nhận chất lượng mỹ thuật.

## Những phần KHÔNG được đánh dấu đã xong

- Không tìm thấy **master ORA thực sự đã vẽ lớp kín bên dưới tóc/gáy/cổ** trong thư mục Drive CANON đã kiểm tra; thư mục hiện có ZIP, PNG, README và MODEL_CARD. Gói ORA CP411 mới chỉ là **mặt nạ nghiên cứu**, không thay cho file master vẽ tay bị thiếu.
- Tóc dài vẫn nằm trên ảnh đứng phẳng, chưa được bóc tách từng phần trước/sau. Mặt nạ đầu mới **cắt ngang** phần tóc dài; inpaint tự động không thể tạo vùng da/cổ đúng mỹ thuật.
- Không có master mắt nhắm theo đúng pose đầu đứng. **Không overlay** CP409 expression-face lên fullbody CP408/CP410.
- Chưa dựng xương đầu/cổ, chưa thêm mesh physics, chưa ghép mắt vào rig toàn thân, chưa nghiệm thu trên Android vật lý.
- CANON V2.1, tỷ lệ +17%, trang phục và nhận diện **không thay đổi**. `sprite_paths = {}`, `apk_production = false`.

## Hướng tiếp theo thiết thực — CP412

- Khôi phục/vẽ **front-pose face/head master** độ phân giải phù hợp và underpaint gáy/cổ/tóc thật. Dùng CP411 guide để giữ nhận diện CANON, nhưng **không dùng bản phóng to từ sheet như master HD**.
- Tách tóc gần đầu/tóc dài, cổ, vai, tay, thân và lụa có underpaint thật; kiểm tra chồng ghép ở vị trí đầu nghiêng 0°, ±2°, ±4°, không để hở mép trắng.
- Vẽ mí mắt khép phù hợp riêng với góc đứng (không lấy trực tiếp crop biểu cảm CP409), thử chớp mắt trên **cùng đầu**, rồi ghép với đồng hồ chuyển động CP410.
- Nghiệm thu bằng hình ở kích thước game và APK trên thiết bị thực trước khi cấp quyền production.

## Tệp chính

- `output/CP411_HEAD_SEGMENTATION_QA_BOARD.png` — giải thích ảnh gốc, mặt nạ, underpaint tự động và ghép lại.
- `output/CP411_FRONT_HEAD_ANCHOR_GUIDE_4X.png` — các mốc và khung kiểm tra.
- `output/CP411_HEAD_SEPARATION_SOURCE_LOCKED_DRAFT.ora` — nguồn thô có thể mở bằng Krita/GIMP (một số công cụ hỗ trợ ORA).
- `cp411_front_head_preflight.py`, `tests/test_cp411_head_preflight.py` — tái tạo và kiểm định.
- `android/TVKFrontPoseRigAuditOverlay.kt` — lớp vẽ hướng dẫn ở debug APK.

**Mốc chất lượng quan trọng:** Neutral compositing PASS chỉ chứng minh ảnh gốc không bị sửa; hoàn toàn không chứng minh head mesh/animation trông tự nhiên khi chuyển động.