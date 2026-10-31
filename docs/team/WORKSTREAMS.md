# TVK — Phân công và quyền sở hữu file

**Quy tắc:** Mỗi thread chỉnh sửa trên **nhánh riêng**, mỗi thay đổi phải được kiểm tra trước khi TVK-04 merge. Những đường dẫn dưới đây là **phân quyền khuyến nghị**, không phải khóa bảo vệ tự động của GitHub.

## Policy chung có hiệu lực từ 2026-10-31

Cả bốn thread phải theo [STATIC_FIRST_SCENE_MODE.md](STATIC_FIRST_SCENE_MODE.md): tạm tắt body touch-zone; vẫn giữ scene/pose/wardrobe/dialogue controls; không warp toàn bộ ảnh; chỉ thêm micro-animation bằng layer đã duyệt. Tài liệu và code body-touch trước ngày này là lịch sử, không được tái bật trong PR trừ khi có quyết định mới của người dùng.

## TVK-01 — Nhân vật & Animation

- **Nhánh:** `tvk/characters`. **Bối cảnh:** Lâm Thiển đã đến CP419 ở nhánh tích hợp trước khi tách thread; tiếp tục từ CP420/`CHAR-...`, không lặp CP396–CP419.
- **Mục tiêu:** CANON, trang phục 100/70/50/30, biểu cảm, rig/physics, animation và hệ thống hiển thị nhân vật. Sau Lâm Thiển mới tiếp Tô Nguyệt Ly theo thiết kế đã duyệt.
- **Ưu tiên file:** `docs/art/**`, `tools/art/**`, `tests/art/**`, `app/src/main/assets/characters/**`, các file Kotlin `Character*`, `TVK*` thuộc chuyển động/hiển thị nhân vật.
- **Không tự ý thay đổi:** nguồn CANON bất kỳ; bản art không được duyệt; `MainActivity.kt`, `AndroidManifest.xml`, build Gradle/CI chung, `PROJECT_SPEC.md`, `STATUS_BOARD.md` trên nhánh tích hợp.
- **Bàn giao:** tên asset + SHA/crop/pose, preview 1× và zoom, tests local/CI, `PENDING_USER_APPROVAL` khi còn chờ, API cần TVK-04 nối vào map/combat.

## TVK-02 — Bản đồ & Cốt truyện

- **Nhánh:** `tvk/world-story`. **Bối cảnh:** đã có prototype chương I/map trong `MainActivity.kt`; tài liệu `docs/CHAPTER_01_IMPLEMENTATION.md`, `docs/STORY_BIBLE.md`.
- **Mục tiêu:** map ngoài → khu vực trong, tọa độ chạm, NPC, hội thoại, lựa chọn, nhiệm vụ chương I; **Android native 2D không phải web**.
- **File ưu tiên:** `docs/STORY_BIBLE.md`, `docs/CHAPTER_01_IMPLEMENTATION.md`, thư mục mới `docs/world/**`, `tools/world/**`, `tests/world/**`, file Kotlin mới theo tiền tố `TVKWorld*`, `TVKQuest*`, `TVKDialogue*`.
- **Không tự ý sửa:** `MainActivity.kt` vì đây là điểm tích hợp hiện có; không đổi nhân vật CANON, appearance state, UI chiến đấu, màn hình debug nhân vật.
- **Bàn giao:** scene graph/điểm tương tác, điều kiện mở khóa, hợp đồng trạng thái save, UX native Android, test và API/Intent cho thread tích hợp.

## TVK-03 — Chiến đấu & Gameplay

- **Nhánh:** `tvk/combat`. **Bối cảnh:** đọc `PROJECT_SPEC.md`; không đoán đã có hệ chiến đấu hoàn chỉnh chỉ vì đã có reference UI.
- **Mục tiêu:** turn-based theo tốc độ, đội hình nhiều nhân vật, HP/MP, kỹ năng/vật phẩm, lượt địch, trạng thái hư hại trang phục; chiến đấu **một màn hình chung** (không chia hai ô), hiệu ứng 2D chỉ khi hành động/lần đầu chạm ngưỡng.
- **File ưu tiên:** thư mục mới `docs/combat/**`, `tools/combat/**`, `tests/combat/**`, Kotlin mới `TVKCombat*`, `TVKTurn*`, `TVKSkill*` và asset nội bộ của combat khi có phép sử dụng.
- **Không tự ý sửa:** `CharacterAppearanceState.kt`/asset CANON, `MainActivity.kt`, `AndroidManifest.xml`; nếu cần thay state thì đề xuất interface để TVK-04 phối hợp TVK-01.
- **Bàn giao:** mô hình combat thuần Kotlin dễ test, sự kiện combat → appearance (đề xuất), API, test determinism, demo screen và hợp đồng lưu/tải.

## TVK-04 — Tích hợp & APK

- **Nhánh:** `map-2d-prototype` (nhánh tích hợp chính của prototype; `main` **không** phải đích merge tự động).
- **Mục tiêu:** rà PR từ ba nhánh, tránh sửa trùng, điều phối API, build APK, kiểm nghiệm, QA thiết bị thật khi có bằng chứng, phát hành checkpoint tích hợp.
- **File quản lý chung:** `app/src/main/java/vn/thanhvanky/prototype/MainActivity.kt`, `app/src/main/AndroidManifest.xml`, `build.gradle.kts`, `settings.gradle.kts`, `app/build.gradle.kts`, `.github/workflows/build-apk.yml`, `docs/PROJECT_SPEC.md`, `docs/TVK_LESSONS_LEARNED.md`, `docs/team/STATUS_BOARD.md`, tài liệu hợp đồng chung.
- **Không tự nâng trạng thái:** rig/animation/canon/art approval, phone QA hoặc gameplay complete nếu chưa thấy bằng chứng.

## Điểm giao nhau — PHẢI có thỏa thuận trước

| File / interface có thật | Các thread liên quan | Cách xử lý |
|---|---|---|
| `MainActivity.kt` (map + hội thoại hiện tại) | TVK-02, 03, 04 | TVK-02/03 gửi class module/contract; TVK-04 nối entry point |
| `CharacterAppearanceState.kt` (wardrobe/integrity/state) | TVK-01, 03, 04 | TVK-01 làm chủ mô hình; TVK-03 đề xuất sự kiện; TVK-04 tích hợp |
| `CharacterInteractionActivity.kt` | TVK-01, 02, 04 | TVK-01 đề xuất UI nhân vật; TVK-04 ghép navigation liên hệ map |
| `AndroidManifest.xml`, Gradle, workflow build | Mọi thread | TVK-04 là người chỉnh trên nhánh tích hợp |
| `docs/PROJECT_SPEC.md` / `docs/TVK_LESSONS_LEARNED.md` | Mọi thread | Các thread gửi ghi chú trong nhánh riêng; TVK-04 tổng hợp, không ghi đè khối checkpoint |
| Art private, CANON Lâm Thiển V2.1 | TVK-01, 03, 04 | Chỉ dùng đúng ảnh đã duyệt, SHA nguồn, `blocked_pending_art` cho sản phẩm chưa duyệt |

Nếu file mới chưa xác định chủ sở hữu: **đừng tự nhận**. Ghi vào PR, để TVK-04 gán owner và đường tích hợp trước.

## Owner của tài liệu điều phối chung (31-10-2026)

- TVK-01/02/03 chịu trách nhiệm ghi **quyết định đã được người dùng chốt** và dependency trong handoff trên branch của mình, đề xuất PR tài liệu sớm tới `map-2d-prototype`.
- TVK-04 sở hữu bản tích hợp `docs/team/DECISION_LOG.md`, `DEPENDENCIES.md`, `ASSET_CONTRACTS.md`, `STATUS_BOARD.md`; xác minh trước khi merge hoặc bổ sung khi user giao trực tiếp.
- Mỗi nhóm đọc ba tài liệu trên ở nhánh tích hợp trước task mới; sync rõ ràng, không dựa vào chat khác hoặc branch chưa merge.
- [Quy trình](SYNC_AND_MERGE.md) phân biệt `DECISION_READY` (có thể merge docs) và `READY_FOR_REVIEW` (code/art hoàn chỉnh có test/duyệt).
