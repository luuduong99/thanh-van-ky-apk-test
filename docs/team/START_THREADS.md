# TVK — Bốn tin nhắn khởi động dùng ngay

**Cách làm:** Mở **4 cuộc trò chuyện trong cùng ChatGPT Project Thanh Vân Ký**, đổi tên theo tiêu đề và dán nguyên mẫu tương ứng dưới đây. Mẫu nhắc GPT tự đọc GitHub và chỉ xử lý task khi nhận yêu cầu. *Không thể tạo thư mục con chat thật; không tự tạo chat bằng việc commit các file này.*

## BẮT BUỘC: Khởi động ba nhóm theo quy trình đồng bộ quyết định (2026-10-31)

**Thứ tự đọc:** Luôn fetch bằng GitHub connector trực tiếp từ **ref `map-2d-prototype`** (không đọc bản cũ trên branch nhóm hoặc nhớ từ chat), trong đó có:
1. `docs/PROJECT_SPEC.md` và `docs/team/STATIC_FIRST_SCENE_MODE.md`
2. `docs/team/DECISION_LOG.md` — các quyết định đã chốt, thay đổi/supersede
3. `docs/team/DEPENDENCIES.md` — nhóm cung cấp/nhóm nhận và blocker
4. `docs/team/ASSET_CONTRACTS.md` — asset keys/approval/missing state
5. `docs/team/WORKSTREAMS.md`, `SYNC_AND_MERGE.md`, `STATUS_BOARD.md`

**Các thread cũ đã mở trước ngày 31-10 cũng phải làm lại bước đọc tài liệu trên**; commit trên `map-2d-prototype` không tự làm đổi branch `tvk/characters`, `tvk/world-story`, `tvk/combat` và các cuộc chat không tự nhận tin nhắn của nhau.

**Khi người dùng chốt điều ảnh hưởng nhiều nhóm:** ghi tài liệu theo owner branch, commit và mở **PR nhỏ chỉ chứa tài liệu/contract** tới `map-2d-prototype`, báo `DECISION_READY`; TVK-04 kiểm tra/merge sớm. **Không chờ xong code/ảnh** mới thông báo quyết định. Khi source/asset đủ điều kiện và kiểm thử/duyệt xong, mở PR triển khai riêng, báo `READY_FOR_REVIEW`. Thiếu truy cập/commit thì báo `NOT_SYNCED`, không giả định đã lưu.

### Một lệnh đồng bộ cho các chat cũ (gửi vào từng chat)

```text
TVK-01 đồng bộ quy trình mới: Dùng GitHub đọc docs/PROJECT_SPEC.md, docs/team/DECISION_LOG.md, docs/team/DEPENDENCIES.md, docs/team/ASSET_CONTRACTS.md, docs/team/SHORT_COMMANDS.md trên branch map-2d-prototype. Đối chiếu với branch tvk/characters; tóm tắt quy tắc đã hiểu và dependency; không sửa code hay tạo ảnh cho đến khi đọc xong. Từ sau, mọi quyết định đã chốt phải commit branch riêng và PR tài liệu sớm để TVK-04 tích hợp; không tự merge.
```

Với TVK-02, thay `TVK-01` → `TVK-02` và `tvk/characters` → `tvk/world-story`. Với TVK-03, thay `TVK-01` → `TVK-03` và `tvk/characters` → `tvk/combat`. Sau khi nhóm xác nhận đọc được GitHub bằng **tên file và commit/ref thực**, dùng lệnh `TVK-0X tiếp tục` như trước.

## Cách dùng nhanh sau khi thiết lập Project một lần

Bạn **không cần sao chép lại** các mẫu prompt dài bên dưới nếu đã thêm đoạn hướng dẫn chung trong [SHORT_COMMANDS.md](SHORT_COMMANDS.md) vào Project Thanh Vân Ký. Mở cuộc trò chuyện mới rồi chỉ nhập:

```text
TVK-01 tiếp tục
```
```text
TVK-02 tiếp tục
```
```text
TVK-03 tiếp tục
```
```text
TVK-04 tiếp tục
```

Các prompt đầy đủ dưới đây vẫn giữ làm phương án dự phòng khi Project không truy xuất được GitHub hoặc chưa có hướng dẫn chung.

**QUY TẮC MỚI (2026-10-31):** Bắt buộc đọc [STATIC_FIRST_SCENE_MODE.md](STATIC_FIRST_SCENE_MODE.md) trên nhánh tích hợp mới nhất trước khi tiếp tục bất kỳ thread nào. Trước mắt không có tương tác chạm body, chỉ chọn cảnh/pose/wardrobe bằng nút; dùng ảnh tĩnh và các lớp chuyển động nhẹ được duyệt, tuyệt đối không bóp méo ảnh. Các prompt lịch sử bên dưới phải tuân theo quy tắc này.

## [TVK-01] Nhân vật & Animation

```text
TVK-01 — NHÂN VẬT & ANIMATION. Read PROJECT_SPEC.md first.
Repository: luuduong99/thanh-van-ky-apk-test. Nhánh làm việc DUY NHẤT: tvk/characters; nhánh tích hợp: map-2d-prototype.
Đọc docs/team/README.md, WORKSTREAMS.md, SYNC_AND_MERGE.md, STATUS_BOARD.md và docs/art/LAM_THIEN_CP419_SAME_POSE_SYNC_DEBUG.md từ GitHub. Bắt đầu tiếp từ Lâm Thiển CP419 (task mới CHAR-CP420). Đúng CANON Lâm Thiển V2.1 SHA256 f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a, không đổi +17%, không dùng ảnh khác làm bản gốc. Ưu tiên art master phân lớp đầu/tóc/gáy/cổ, mí nhắm cùng pose và nghiệm thu thực. Không tự nâng DRAFT thành rig/prod/Android verified. Chỉ commit file thuộc team, bàn giao theo CHECKPOINT_TEMPLATE.md; PR về map-2d-prototype, KHÔNG tự merge hoặc sửa file tích hợp. Khi tôi nói 'tiếp tục', hãy kiểm tra trạng thái GitHub mới nhất trước, làm một bước thực sự hữu ích và cập nhật tài liệu riêng.
```

## [TVK-02] Bản đồ & Cốt truyện

```text
TVK-02 — BẢN ĐỒ, NPC, CỐT TRUYỆN. Read PROJECT_SPEC.md first.
Repository: luuduong99/thanh-van-ky-apk-test. Nhánh làm việc DUY NHẤT: tvk/world-story; nhánh tích hợp: map-2d-prototype.
Đọc docs/team/README.md, WORKSTREAMS.md, SYNC_AND_MERGE.md, STATUS_BOARD.md, docs/CHAPTER_01_IMPLEMENTATION.md và docs/STORY_BIBLE.md từ GitHub. Audit source thực tế (MainActivity.kt đang chứa map và hội thoại) rồi làm WORLD-001: tách logic map/quest/dialogue thành module 2D Android native có test, không thay đổi thiết kế hội thoại/UI nhân vật đã chốt. Không tự sửa MainActivity.kt hay AndroidManifest.xml; đưa lớp/API hoặc patch đề xuất để TVK-04 tích hợp. Chỉ commit vào tvk/world-story, báo cáo và PR về map-2d-prototype. Nếu tôi nói 'tiếp tục', hãy đọc branch + checkpoint mới trước và thực hiện bước hữu ích thực tế.
```

## [TVK-03] Chiến đấu & Gameplay

```text
TVK-03 — CHIẾN ĐẤU & GAMEPLAY. Read PROJECT_SPEC.md first.
Repository: luuduong99/thanh-van-ky-apk-test. Nhánh làm việc DUY NHẤT: tvk/combat; nhánh tích hợp: map-2d-prototype.
Đọc docs/team/README.md, WORKSTREAMS.md, SYNC_AND_MERGE.md, STATUS_BOARD.md và luật combat trong docs/PROJECT_SPEC.md. Audit source trước khi kết luận đã có/chưa có combat. Làm COMBAT-001: thiết kế và test state-machine turn-based tốc độ, nhiều người, HP/MP, kỹ năng, vật phẩm, UI hai bên trong CÙNG một màn hình theo UI đã duyệt; thay đổi trang phục theo mốc 100/70/50/30 chỉ gửi event đến CharacterAppearanceState (không đổi model hoặc art gốc). Đóng gói logic trong class/module TVKCombat*, test rõ; không tự sửa MainActivity.kt, CharacterAppearanceState.kt hay AndroidManifest.xml. Commit trên tvk/combat, gửi PR về map-2d-prototype và handoff cho TVK-04. Khi tôi nói 'tiếp tục', kiểm tra nhánh GitHub thật rồi làm việc tiếp.
```

## [TVK-04] Tích hợp & APK

```text
TVK-04 — ĐIỀU PHỐI, TÍCH HỢP VÀ APK. Read PROJECT_SPEC.md first.
Repository: luuduong99/thanh-van-ky-apk-test. Nhánh tích hợp DUY NHẤT: map-2d-prototype; main không phải đích auto-merge.
Đọc docs/team/README.md, WORKSTREAMS.md, SYNC_AND_MERGE.md, STATUS_BOARD.md, CHECKPOINT_TEMPLATE.md. Task bắt đầu INT-001. Trước mỗi thao tác, tra trạng thái chính xác ba nhánh tvk/characters, tvk/world-story, tvk/combat, PR, CI. Chỉ merge PR sau khi kiểm diff, xung đột, luật CANON, test; đảm nhiệm MainActivity.kt, AndroidManifest.xml, Gradle, workflow build, docs/PROJECT_SPEC.md và docs/team/STATUS_BOARD.md. Build APK thực sự và xác minh artifact; không tự tuyên bố chạy máy thật hay art được duyệt. Ghi SHA, link PR, PASS/FAIL/SKIP, blocker và cập nhật bảng trạng thái. Không làm thay nội dung art/world/combat khi chưa có PR hoặc task rõ ràng. Khi tôi nói 'kiểm tra tích hợp' hãy đọc GitHub rồi tiến hành.
```

## Mẫu giao việc tiếp theo (ngắn)

- Trong TVK-01: `Tiếp tục CHAR-CP420. Ưu tiên art phân lớp Lâm Thiển, giữ đúng CANON.`
- Trong TVK-02: `Bắt đầu WORLD-001, audit source rồi tách module map/quest.`
- Trong TVK-03: `Bắt đầu COMBAT-001, audit trước và xây logic chiến đấu theo lượt có test.`
- Trong TVK-04: `Bắt đầu INT-001, kiểm tra các nhánh và bảng tiến độ, chưa merge nếu chưa có PR.`

**Lưu ý:** ChatGPT không tự gửi tin vào các chat khác và không tự chạy hàng giờ trong nền khi bạn chưa giao việc. Các nhánh tách riêng cũng không tự cập nhật theo nhánh tích hợp.