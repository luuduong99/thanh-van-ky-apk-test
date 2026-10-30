# TVK — Quy trình phối hợp khi mở 4 thread cùng lúc

## Trước mỗi lượt làm việc (tất cả thread)

1. Đọc `docs/PROJECT_SPEC.md` **từ nhánh tích hợp `map-2d-prototype`** để nắm luật mới nhất; đọc tài liệu riêng trên nhánh được giao.
2. Xác định đúng branch, file owner và `docs/team/STATUS_BOARD.md`. Nếu GitHub đã đổi từ lần trước, **không dùng bản cũ trong ngữ cảnh chat**.
3. Chỉ chọn một thay đổi độc lập, có tiêu chí kiểm chứng. Không sửa cùng một file shared khi chưa giao tiếp qua checkpoint/PR.
4. Đánh dấu dự kiến file sẽ thay và interface cần team khác tại đầu handoff.

## Quy trình từ code đến APK

1. **TVK-01/02/03:** làm trên nhánh của mình, commit các thay đổi thật, chạy test liên quan. Không tự push vào `map-2d-prototype`/`main`.
2. **Bàn giao:** lập báo cáo theo `CHECKPOINT_TEMPLATE.md` trong folder sở hữu hoặc mô tả PR; cung cấp commit SHA + file thay đổi + pass/fail/skip + nguồn ảnh, trạng thái duyệt, rủi ro.
3. **Pull Request:** nhánh `tvk/...` → base `map-2d-prototype`. PR nên nhỏ theo từng thay đổi, dùng `.github/PULL_REQUEST_TEMPLATE.md`. Không tự merge khi chưa review.
4. **TVK-04:** đọc diff thực tế, đảm bảo luật CANON/state/contracts, xử lý xung đột, chạy test CI, build APK khi cần. Nếu thay đổi shared, TVK-04 thực hiện sau khi các bên đồng ý.
5. **Hợp nhất:** chỉ merge khi CI cần thiết thành công; `SKIP` private art ≠ `PASS`; visual/phone QA riêng. Không tự động promote CANON, Spine hay APK chính thức.
6. **Sau merge:** cập nhật `docs/team/STATUS_BOARD.md`, `docs/PROJECT_SPEC.md` (không xóa lịch sử), `TVK_LESSONS_LEARNED.md` với bằng chứng; thông báo commit tích hợp.
7. **Đồng bộ nhánh:** trước task mới, TVK-01/02/03 lấy cập nhật từ `map-2d-prototype` bằng merge/rebase cẩn thận; không force-push hoặc reset làm mất công việc. Nếu môi trường không hỗ trợ merge an toàn, TVK-04 sẽ phối hợp bằng PR và branch mới.

## Quy tắc khi có xung đột

- 2 PR cùng sửa `MainActivity.kt`? Chặn PR thứ hai; TVK-04 tách entry point hoặc tích hợp tuần tự.
- MAP cần đổi `CharacterAppearanceState.kt`? Gửi mô tả interface, không sửa file đó trực tiếp.
- COMBAT cần event `onIntegrityThreshold(70/50/30)`? Chỉ gửi payload; TVK-01 xác nhận semantics và art; TVK-04 nối logic.
- Các thread cùng muốn sửa `PROJECT_SPEC.md`? TVK-04 là người cập nhật sau merge; những thread khác chỉ ghi handoff riêng.
- Có ảnh mới khác nhận diện CANON? Giữ DRAFT, **không dùng làm production**, hỏi user duyệt đúng ảnh.

## Quy ước checkpoint

- Nhân vật: `CHAR-CP420` rồi tăng (`CP419` là mốc lịch sử cuối trước khi tách).
- Bản đồ: `WORLD-001`, `WORLD-002`, v.v. — bắt đầu từ audit hiện trạng, **không giả định chưa có source**.
- Chiến đấu: `COMBAT-001`, ... — bắt đầu từ audit hiện trạng.
- Tích hợp: `INT-001`, ...; tổng checkpoint `CP419` giữ nguyên cho tới khi có checkpoint tích hợp mới có bằng chứng.
- Không xem số bước, test PASS hay tỉ lệ ước tính là bằng chứng art hoàn thiện.

## Sự thật và giới hạn

- Có thể mở bốn chat trong **cùng một tài khoản**, nhưng lịch sử tin nhắn không đồng bộ tự động; GitHub là nguồn phối hợp.
- Mỗi chat chỉ xử lý tác vụ khi bạn giao việc; không giả định các thread đang tự chạy ngầm.
- Không có thư mục chat con thật; tổ chức bằng tên chat có tiền tố `[TVK-XX]` và tài liệu trong GitHub.
- Nếu có plugin/runner không truy cập được, ghi rõ **BLOCKED**, không tự tuyên bố đã merge, đã chạy APK/điện thoại, hay đã nghiệm thu.