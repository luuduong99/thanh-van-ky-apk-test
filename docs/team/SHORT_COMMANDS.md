# TVK — Lệnh ngắn tiếp tục 4 thread

**Bản quy ước 2026-10-31 — dùng trong Project ChatGPT "Thanh Vân Ký".**

Mỗi thread có thể bắt đầu từ **một câu duy nhất** (không cần dán lại prompt dài):

| Lệnh gửi vào chat mới | Thread | Nhánh viết code |
|---|---|---|
| `TVK-01 tiếp tục` | Nhân vật & Animation | `tvk/characters` |
| `TVK-02 tiếp tục` | Bản đồ, NPC & Cốt truyện | `tvk/world-story` |
| `TVK-03 tiếp tục` | Chiến đấu & Gameplay | `tvk/combat` |
| `TVK-04 tiếp tục` | Tích hợp, Build & APK | `map-2d-prototype` |

## Ý nghĩa chung của lệnh "tiếp tục"

Dù nhận lệnh từ chat cũ hay chat hoàn toàn mới, trợ lý cần:

1. Nhận diện đúng thread từ mã `TVK-01`…`TVK-04` và repo `luuduong99/thanh-van-ky-apk-test`. Không chuyển thread chỉ vì một cuộc trò chuyện trước có chủ đề khác.
2. **Đọc bản mới nhất trên GitHub** và bắt buộc áp dụng [quy chuẩn static-first / view-only](STATIC_FIRST_SCENE_MODE.md): **tắt body hotspots, giữ nút chọn cảnh/tư thế/trang phục, không warp ảnh**. : `docs/PROJECT_SPEC.md`, `docs/team/README.md`, `docs/team/WORKSTREAMS.md`, `docs/team/STATUS_BOARD.md`, `docs/team/SYNC_AND_MERGE.md`, rồi tài liệu riêng ở [START_THREADS.md](START_THREADS.md).
3. Đọc commit, checkpoint, thay đổi mới trên nhánh **được giao**; đối chiếu nhánh tích hợp `map-2d-prototype`. Phát hiện việc đang làm/đã làm để không lặp hay tự cho rằng đã hoàn thành.
4. Chọn **một bước thực sự cần thiết và có thể thực hiện trong lượt hiện tại** trong phạm vi team; dùng static-first, không warp/kéo méo hình, giữ CANON V2.1 và các trạng thái `DRAFT/BLOCKED` nếu chưa được duyệt.
5. Chỉ commit vào nhánh đã giao, và nếu cần sửa file shared, đưa đề xuất hoặc PR để TVK-04 tích hợp. Không tự sửa chéo nhánh, thay ảnh CANON hoặc công bố production khi chưa có nghiệm thu.
6. Kiểm thử điều thực sự có thể kiểm; cập nhật checkpoint/handoff, báo **đã làm / còn thiếu / nguồn bằng chứng**. Không nói đã chạy trên Android thật nếu chỉ build CI.
7. Nếu GitHub không truy cập được hoặc chưa đủ dữ liệu, **nói rõ giới hạn**, không suy diễn tiến độ hoặc bịa commit; dùng bối cảnh đã xác minh và chỉ hỏi người dùng khi thật sự cần.

## Cách làm cho chat mới nhận diện lệnh ổn định

Tên chat **không** phải khóa tự động bảo đảm. Đây là **quy ước prompt**; ChatGPT cũng không tự kích hoạt công việc nền hay tự đồng bộ bốn cửa sổ.

Để khỏi phải dán prompt dài ở các chat mới, người dùng nên **dán một lần** đoạn sau vào **hướng dẫn của ChatGPT Project "Thanh Vân Ký"**, hoặc gửi đoạn này một lần ở chat mới nếu không chỉnh được Project instructions:

```text
Dự án: Thanh Vân Ký, GitHub luuduong99/thanh-van-ky-apk-test.
Khi tôi gửi "TVK-01 tiếp tục", "TVK-02 tiếp tục", "TVK-03 tiếp tục" hoặc "TVK-04 tiếp tục",
hãy thực thi quy ước tại docs/team/SHORT_COMMANDS.md trên nhánh map-2d-prototype.
Đọc docs/PROJECT_SPEC.md và docs/team/STATUS_BOARD.md từ GitHub,
xác minh commit/checkpoint mới nhất rồi tiếp tục đúng phần và đúng nhánh.
Giữ static-first, không làm méo ảnh hoặc tự thay CANON, không bịa tình trạng build/art.
```

Sau khi thiết lập chỉ dẫn chung **một lần**, các chat mới chỉ cần một câu lệnh ngắn như `TVK-04 tiếp tục`.

## Bàn giao trước khi thay chat (khuyến nghị, không bắt buộc)

Gửi `TVK-04 bàn giao` (hoặc đúng số thread) để yêu cầu ghi checkpoint, commit và việc kế tiếp vào nhánh được giao. Nếu chat cũ đã hết hạn, chat mới vẫn có thể tiếp tục từ GitHub và `STATUS_BOARD.md`; không cần truy xuất nguyên văn toàn bộ lịch sử chat.

## Không nhầm lẫn

- `TVK-01 tiếp tục` **không** tự chuyển sang `map-2d-prototype` để commit art.
- `TVK-04 tiếp tục` **không** đồng nghĩa tự tạo PR/merge tất cả nhánh bất kể CI, xung đột hay quyền hạn.
- Các lệnh ngắn **không** thay thế chính sách về private CANON, xét duyệt hình ảnh và kiểm thử thiết bị thật.

## Bổ sung bắt buộc cho mọi lệnh TVK-01/02/03/04 (2026-10-31)

Sau `Read PROJECT_SPEC.md first`, luôn đọc từ branch `map-2d-prototype`:
- `docs/team/DECISION_LOG.md` — quyết định đã chốt và quyết định bị thay thế.
- `docs/team/DEPENDENCIES.md` — cần gì từ nhóm khác và ai phụ trách.
- `docs/team/ASSET_CONTRACTS.md` — schema ảnh / trạng thái / điều kiện phê duyệt.

Khi người dùng chốt thay đổi ảnh, gameplay, story hay API: **ghi quyết định, commit branch nhóm, đề xuất PR tài liệu dùng chung sớm**; không chờ viết xong feature. Báo trong chat `DECISION_READY` khi có commit/PR thật; chỉ TVK-04 xác nhận đã merge. Khi phần code/ảnh đủ điều kiện, báo `READY_FOR_REVIEW` riêng. Nếu chưa có thao tác GitHub, nói rõ `NOT_SYNCED`.
