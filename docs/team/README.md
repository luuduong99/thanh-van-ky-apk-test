# Thanh Vân Ký — Bộ điều phối bốn thread ChatGPT

**Phiên bản:** 1.0 · **Ngày:** 2026-10-30 · **Phạm vi:** Quy trình và tài liệu, không thay đổi gameplay, CANON hay điều kiện release.

## Quyết định gameplay mới — static-first / view-only (31-10-2026)

**[Đọc quy chuẩn đã chốt](STATIC_FIRST_SCENE_MODE.md):** Trong cảnh nhân vật, **tạm tắt body touch-zone** và mọi warp/bitmap-mesh ở màn thường; chọn cảnh, pose, wardrobe, biểu cảm, hội thoại bằng nút **vẫn hoạt động**. Ảnh tĩnh là fallback an toàn. 4 thread không được tự tái bật touch-zone hoặc thay CANON. Chuyển động nhẹ chỉ qua layer có nghiệm thu, không kéo méo ảnh.

## Đọc trước khi bắt đầu

1. [Quy định chung của dự án](../PROJECT_SPEC.md) — nguồn sự thật về gameplay, các quyết định CANON và điều kiện phát hành. **Đọc `PROJECT_SPEC.md` trước**.
2. [Phân công và quyền sở hữu file](WORKSTREAMS.md) — việc của bốn thread và các vùng xung đột.
3. [4 mẫu tin nhắn khởi động](START_THREADS.md) — sao chép đúng tin nhắn vào mỗi cuộc trò chuyện trong cùng ChatGPT Project.
4. [Quy trình bàn giao, PR và merge](SYNC_AND_MERGE.md) — quy tắc giữ an toàn khi các thread chạy đồng thời.
5. [Bảng tình trạng công việc](STATUS_BOARD.md) — thread tích hợp cập nhật sau khi **xác minh**, không phải dựa trên lời hứa.
6. [Mẫu bàn giao checkpoint](CHECKPOINT_TEMPLATE.md) — để một thread khác tiếp tục không cần đoán trạng thái.

## Lệnh ngắn khi mở lại thread

**Bạn chỉ cần gửi `TVK-01 tiếp tục`, `TVK-02 tiếp tục`, `TVK-03 tiếp tục` hoặc `TVK-04 tiếp tục`** trong chat mới. Quy ước và đoạn hướng dẫn Project một lần nằm tại **[SHORT_COMMANDS.md](SHORT_COMMANDS.md)**. Trợ lý phải đọc checkpoint GitHub mới nhất trước khi tiếp tục; tên chat đơn thuần không bảo đảm đồng bộ.

## Cách sử dụng với một tài khoản ChatGPT

- Trong ChatGPT Project **Thanh Vân Ký**, tạo bốn cuộc trò chuyện có tên:
  - `[TVK-01] Nhân vật & Animation`
  - `[TVK-02] Bản đồ & Cốt truyện`
  - `[TVK-03] Chiến đấu & Gameplay`
  - `[TVK-04] Tích hợp & APK`
- **Không có folder con thật bên trong ChatGPT Project**: đây là quy ước đặt tên. Thư mục `docs/team/` chỉ tồn tại **trong GitHub**.
- Đối với từng thread, dán prompt tương ứng ở [START_THREADS.md](START_THREADS.md).
- Mỗi thread chỉ làm việc khi bạn đưa yêu cầu; **không tự chạy nền, không tự đọc tin nhắn thread khác, không tự merge**.
- Tất cả ghi kết quả vào GitHub **trên nhánh được phân công**. Bằng chứng review/CI quan trọng hơn số checkpoint; không tăng % giả.

## Nhánh GitHub (thiết lập ban đầu)

| Thread | Nhánh | Vai trò |
|---|---|---|
| TVK-01 | `tvk/characters` | Art, animation, nhân vật |
| TVK-02 | `tvk/world-story` | Bản đồ, NPC, cốt truyện, nhiệm vụ |
| TVK-03 | `tvk/combat` | Chiến đấu theo lượt, kỹ năng, AI |
| TVK-04 | `map-2d-prototype` | Nhánh tích hợp; PR, CI, APK, tài liệu chung |

`main` là nhánh mặc định của repository **không tự động ghi hoặc merge tới đây**. Tên nhánh và tài liệu không có nghĩa feature đã hoàn thành. Luôn đọc checkpoint mới nhất trên nhánh của mình.

## Nguyên tắc không thể thương lượng

1. Tôn trọng ảnh CANON đã duyệt; không tự tạo/đổi danh tính nhân vật bằng artwork khác.
2. Mọi sản phẩm thiếu nghiệm thu phải ghi `DRAFT` / `PENDING_USER_APPROVAL` / `BLOCKED` rõ ràng. Android build `SUCCESS` ≠ test máy thật ≠ art đạt.
3. Không nhúng nguồn CANON riêng tư vào GitHub public hoặc APK public; giữ trong Library/nguồn được phép.
4. Các file shared như `MainActivity.kt`, `AndroidManifest.xml`, Gradle, CI build, `docs/PROJECT_SPEC.md` do TVK-04 tích hợp. Thread khác gửi đề xuất API/PR thay vì sửa trực tiếp vào nhánh tích hợp.
5. Không tạo nhiều PR cùng sửa một file rồi merge tùy ý. Dùng `SYNC_AND_MERGE.md`.