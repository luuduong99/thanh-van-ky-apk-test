> **MẪU NGOẠI HÌNH LÂM THIỂN HIỆN HÀNH (28/10/2026):** [CANON BODY V2](LAM_THIEN_CANON_BODY_V2_2026_10_28.md) ([ảnh nguồn](https://drive.google.com/file/d/1mEsyn2wMo-MVQqhtbmdUiFfO8AaYhzUR/view?usp=drivesdk)). Quy tắc toàn game vẫn dùng chung, không sao chép body V2 sang nhân vật khác. Những tham chiếu V1 bên dưới là lịch sử.

# Thanh Vân Ký — GLOBAL CHARACTER APPEARANCE CONTRACT v1

**Ngày chốt:** 2026-10-28. **Phạm vi:** TẤT CẢ nhân vật hiện có và nhân vật mới của dự án (bao gồm Tô Nguyệt Ly, Lâm Thiển). Đây là quy tắc runtime/art bắt buộc, không phải thiết kế riêng của Lâm Thiển.

## Quy tắc toàn cục

Trạng thái **theo ID nhân vật** phải gồm 5 phần tách biệt:

| Key | Ví dụ | Đổi tư thế có reset? |
| --- | --- | --- |
| wardrobe | default / outer_removed / private_fantasy / outfit riêng | **Không** |
| integrity | 100 / 70 / 50 / 30 | **Không** |
| pose | front / back / side / 3/4 / bed / chair / wall | Chỉ thay khi người chơi chọn |
| expression | normal / smile / surprised / troubled / tired ... | Thay theo tình huống, không làm biến dạng nhân vật |
| action | idle / move / hit / adjust_outfit / relax ... | Thay theo ngữ cảnh/animation |

- **Tất cả các mức cởi**, từ mặc đủ đến tháo áo ngoài và mức cuối, đều được giữ khi đổi góc nhìn, chuyển tư thế, đổi cảnh, chuyển battle → tương tác/hội thoại. Không chỉ áp dụng mức cuối.
- Trạng thái hư hại trang phục **khác** mức cởi: 100/70/50/30 là độ nguyên vẹn, **không phải % da lộ ra hoặc ngưỡng HP**. Hồi HP không làm hồi phục đồ. Ở 30%, lớp vải còn che phủ cũng có mép rách/sờn nhưng vẫn đảm bảo che phủ phù hợp; không tăng cố định +20% lượng rách.
- Thay trang phục/cởi đồ được kích hoạt riêng theo điều khiển trong game, không tự kích hoạt từ hành động đổi tư thế.
- **Cấm fallback sai hình**: Khi thiếu ảnh của `wardrobe × integrity × pose`, vẫn lưu state nguyên vẹn nhưng hiển thị thông báo thiếu tài nguyên, không tự đổi sang trạng thái mặc đủ/không rách hoặc dùng ảnh sai tư thế.
- Mọi vết rách phải theo **cùng vị trí trên cấu trúc trang phục** khi đổi góc, nhưng hình dạng/nếp vải có thể biến thiên theo trọng lực, chuyển động và tư thế. Không được phát sinh rách ngẫu nhiên do chuyển pose.
- Biểu cảm và hành động tùy bối cảnh: chiến đấu (trúng đòn, giữ thăng bằng, điều chỉnh đồ, mệt), nội thất (đứng, nằm/ngồi giường, ngồi ghế, dựa tường, tự nhiên/thư giãn), hội thoại (biểu cảm theo tình tiết). Cảnh tình cảm: nhân vật trưởng thành, có đồng thuận.
- **Bản ngoại hình gốc riêng:** mọi nhân vật có face, tóc, màu, vóc dáng, trang phục canon riêng; chỉ lấy ảnh đã chốt đúng nhân vật. Mốc thay đổi hình thể +17% là riêng của Lâm Thiển, **không** dùng cho người khác.

## Asset resolution & trạng thái thực tế

1. Bộ dữ liệu hiện tại: `app/src/main/assets/character_interactions.json` (appearanceSystem + wardrobeStates + poses + plannedPoses).
2. Một ảnh chỉ hợp lệ khi đồng thời đúng `characterId`, `poseId`, `wardrobeId`, `integrity` và **file tồn tại thực tế**; không dùng poster phẳng như texture layer nếu chưa dựng asset.
3. Với `integrity=100`: ảnh pose mặc đủ dùng `poses[].image`; biến thể khác dùng `wardrobeStates[].images[poseId]`.
4. Với `integrity=70/50/30`: dùng `wardrobeStates[].integrityImages["70"/"50"/"30"][poseId]`. Nếu thiếu, giữ state và hiển thị placeholder rõ lý do.
5. `plannedPoses` chỉ đăng ký mục tiêu thiết kế còn thiếu; **không** được đánh dấu sẵn sàng hoặc bật hotspot theo ảnh chưa có. Tài nguyên cho Back/Side/Front 3/4/Back 3/4, `bed_kneel_forward`, `bed_recline`, `bed_side_lying`, `bed_sit`, `chair_sit`, `wall_lean` phải là hình đúng góc và bối cảnh.
6. Các thuộc tính lớp, alpha, underpaint, rig/physics, build/APK và kiểm thử thực tế là **các cổng nghiệm thu riêng**, không suy ra từ việc có metadata/PNG concept.
7. Nếu thêm nhân vật mới, phải thêm đủ định danh, pose, outfit variants, độ bền và trạng thái thiếu/sẵn sàng asset theo cùng schema; kiểm tra tự động cấm bỏ qua yêu cầu này.

## Luồng hiển thị tối thiểu

Người chơi chọn nhân vật → đọc `State(characterId)` → khi chọn mức trang phục hoặc pose chỉ ghi **một key tương ứng** → renderer tìm `image(characterId, wardrobe, integrity, pose)` → nếu có thì render đúng hình; nếu không có thì hiện placeholder + thông báo thiếu asset → các state khác không đổi.

Ví dụ: `to_nguyet_ly / outer_removed / 50 / chair_sit` → chuyển sang `wall_lean` thành `to_nguyet_ly / outer_removed / 50 / wall_lean`, không tự chuyển về mặc đủ hay 100%.

## Kiểm thử bắt buộc

- Đổi ít nhất 3 pose với **mọi** mức wardrobe; kiểm tra state và integrity không đổi.
- Đổi pose khi integrity 70/50/30: đúng art từng mức hoặc báo thiếu art; không hiển thị ảnh 100%.
- Thoát/vào ứng dụng, đổi nhân vật, từ battle sang hội thoại: state vẫn theo **đúng characterId**.
- Sửa đồ reset integrity về 100 nhưng **không reset wardrobe/pose**; hồi HP không reset integrity.
- Chọn pose chưa có art: không crash, không dùng art nhân vật khác; hotspot không hoạt động khi không có ảnh.
- Art QA: khuôn mặt/tỷ lệ, draw order, seam, alpha, vật lý tóc/vải, cấu trúc rách hợp lý và che phủ phù hợp; QA 2D trên thiết bị Android trước khi nhận là đã hoàn tất.

## Nguồn được duyệt

- [Lâm Thiển — ảnh ngoại hình chính thức](https://drive.google.com/file/d/10jKNq-VL62sv1gez5PHlVT9QKyJp_Cvd/view?usp=drivesdk).
- [Bảng biểu cảm, tư thế, biến thể trang phục](https://drive.google.com/file/d/1M-6KIEeon7HX4Qn56UlhGMfV76Lr-sN5/view?usp=drivesdk).
- [Bảng lộ trình triển khai](https://drive.google.com/file/d/1ZgMB8nkRlkar3-MYCrH32uQaYxO29S5Q/view?usp=drivesdk).

**Quy tắc chung về cách làm** dùng để thiết kế nhân vật tương lai; không sao chép hình thể và chi tiết nhân vật này sang nhân vật khác.

## Trạng thái triển khai 2026-10-28

- **Đã làm ở mức code:** có `CharacterAppearanceState.kt` lưu trạng thái theo nhân vật, resolver tìm ảnh đúng tích hợp tại màn tương tác; độ nguyên vẹn màn Nhân vật Tô Nguyệt Ly chia sẻ với màn tương tác, không fallback sai costume. App catalogue khai báo wardrobe và integrity matrix cho hai nữ chính.
- **Chưa làm:** hình từng mức/pose, rig/secondary motion, hình combat thật, trạng thái battle cuối cùng toàn bộ đội hình, thử APK trên máy thực; chọn pose mới đã đăng ký trong `plannedPoses` nhưng chưa có artwork.
- **Kiểm chứng:** `tools/validate_global_appearance.py`, `tests/art/test_global_appearance.py` và GitHub Actions CI cần xem kết quả chạy thực tế, không gọi hoàn thành chỉ vì đã tạo test.
