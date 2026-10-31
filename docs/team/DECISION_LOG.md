# TVK — Sổ quyết định dùng chung (DECISION LOG)

**Khởi tạo:** 2026-10-31. **Owner tích hợp:** TVK-04. **Nhánh nguồn chung:** `map-2d-prototype`.
**Mục đích:** các quyết định đã chốt trong TVK-01/02/03/04 phải đọc được từ GitHub; chat, bộ nhớ hoặc ảnh preview không thay thế commit.
**Nguồn ưu tiên:** `docs/PROJECT_SPEC.md` và [STATIC_FIRST_SCENE_MODE.md](STATIC_FIRST_SCENE_MODE.md); sổ này ghi quyết định liên nhóm và trạng thái triển khai. Nếu có mâu thuẫn, khóa thực thi, báo TVK-04; không tự chọn một phiên bản.

## Quy trình bắt buộc

1. Khi người dùng **chốt** một yêu cầu, nhóm đang làm ghi một dòng quyết định có ID, ngày, người yêu cầu, phạm vi, tiêu chí kiểm chứng, các team chịu ảnh hưởng và link handoff. Ghi trên **branch của nhóm** và commit ngay khi có thể; không cần đợi ảnh/code xong.
2. Quyết định cần chia sẻ được chuyển bằng **PR tài liệu nhỏ** tới `map-2d-prototype`, ưu tiên ngay; TVK-04 rà xung đột, độ chính xác và merge. **Không merge asset DRAFT** chỉ vì quyết định thiết kế đã được chốt.
3. Sau khi TVK-04 merge, cập nhật [DEPENDENCIES.md](DEPENDENCIES.md), [STATUS_BOARD.md](STATUS_BOARD.md) và tài liệu đặc tả nếu thay đổi hành vi. Các nhóm khác **đọc phiên bản trên nhánh tích hợp trước mỗi task** rồi sync nhánh làm việc an toàn.
4. Khi người dùng đổi quyết định, tạo **dòng thay thế (supersedes)**, giữ lại lịch sử; không âm thầm sửa chuẩn cũ hoặc tuyên bố asset đạt.
5. Nếu không thể commit/PR, ghi `NOT_SYNCED` và báo rõ: nhóm khác chưa có thông tin đáng tin cậy trên GitHub.
6. **ChatGPT không tự chạy nền, không tự đọc chat khác hoặc tự gửi tin giữa các chat.** Việc đồng bộ chỉ xảy ra qua commit/PR/merge được thực hiện thật.

### Trạng thái quyết định

- `CONFIRMED`: người dùng đã chốt yêu cầu; chưa khẳng định code/ảnh có.
- `PROPOSED`: phương án chưa được người dùng chốt; không coi là chuẩn bắt buộc.
- `SUPERSEDED`: đã có quyết định mới thay thế.
- `BLOCKED`: thiếu điều kiện/đối chiếu để áp dụng an toàn.

**Trạng thái thực hiện tách riêng:** `NOT_STARTED`, `IN_PROGRESS`, `PENDING_USER_APPROVAL`, `VERIFIED`; quyết định CONFIRMED ≠ triển khai VERIFIED.

## Bảng quyết định liên nhóm

| ID | Ngày | Quyết định | Trạng thái quyết định | Trạng thái triển khai | Owner | Team liên quan | Kiểm chứng / nguồn |
|---|---|---|---|---|---|---|---|
| TVK-DEC-001 | 2026-10-29 | Lâm Thiển dùng đúng CANON V2.1 (+17%) `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`; file gốc bất biến, private. | CONFIRMED | Art HD production BLOCKED | 01 | 03,04 | SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a` |
| TVK-DEC-002 | 2026-10-31 | Static-first/view-only: chọn scene, pose, wardrobe, biểu cảm bằng UI; không body touch zone, không warp ảnh phẳng. | CONFIRMED | Source/build INT-002 pass; device QA pending | 04 | 01,02,03 | [Quy chuẩn](STATIC_FIRST_SCENE_MODE.md) |
| TVK-DEC-003 | 2026-10-31 | Mỗi tổ hợp cần **một file PNG sprite riêng** dùng cho game; ảnh sheet/crop/upscale proxy không phải art production. Master nhiều lớp có thể được tái sử dụng để xuất sprite. | CONFIRMED | Production art pending | 01 | 02,03,04 | Kiểm PNG/alpha/canvas, người dùng duyệt |
| TVK-DEC-004 | 2026-10-31 | Trạng thái trang phục hư hại: 100/70/50/30, phải nhất quán toàn cơ thể và không tự đổi model/pose. | CONFIRMED | Registry + ảnh cần triển khai | 01 | 03,04 | [ASSET_CONTRACTS](ASSET_CONTRACTS.md) |
| TVK-DEC-005 | 2026-10-31 | **Yêu cầu biến thể thiết kế**: tóc/đầu theo ảnh 1 người dùng chỉ định, các phần còn lại theo ảnh 2; giảm tua rua, dây vàng và phụ kiện rườm rà. **Chưa có master dẫn xuất được nghiệm thu**, không được tự thay CANON V2.1 gốc. | CONFIRMED (yêu cầu), không phải CANON mới | PENDING_USER_APPROVAL cho master | 01 | 04 | So preview mẫu gốc/biến thể; ghi mã master sau khi duyệt |
| TVK-DEC-006 | 2026-10-31 | Ảnh tham khảo khác được người dùng bảo lưu để tạo **nhân vật tương lai**, không đưa vào nguồn Lâm Thiển hoặc coi là CANON mới. | CONFIRMED | REFERENCE_ONLY | 01 | 04 | Dán nhãn và lưu provenance rõ |
| TVK-DEC-007 | 2026-10-30 | 4 nhóm: 01 Art, 02 World/Story, 03 Combat, 04 Integration; các nhóm riêng commit branch của mình, TVK-04 quản lý nhánh tích hợp. | CONFIRMED | Tài liệu/branch có; triển khai theo task | 04 | 01,02,03 | [WORKSTREAMS](WORKSTREAMS.md) |
| TVK-DEC-008 | 2026-10-31 | Quyết định được chốt phải **đồng bộ sớm qua Git**; không chờ code/ảnh hoàn tất. TVK-04 merge hợp đồng/tài liệu trước khi PR triển khai đủ điều kiện. | CONFIRMED | Quy trình tài liệu được thiết lập; chưa có chứng cứ nhóm đã đồng bộ nhánh | 04 | 01,02,03 | [SYNC_AND_MERGE](SYNC_AND_MERGE.md) |

## Mẫu ghi quyết định mới

```markdown
### TVK-DEC-XXX — <tên ngắn>
- Date / requested by / confirmed in: YYYY-MM-DD / user / TVK-0X
- Status: PROPOSED | CONFIRMED | SUPERSEDED | BLOCKED
- Implementation: NOT_STARTED | IN_PROGRESS | PENDING_USER_APPROVAL | VERIFIED
- Owner + impacted: TVK-0X → TVK-0Y, TVK-0Z
- Exact decision: ...
- CANON / asset / gameplay boundaries: ...
- Acceptance checks: ...
- Dependencies: TVK-DEP-...
- Source evidence: user-approved preview/commit/PR/CI/Android QA (chỉ link có thật)
- Supersedes: none | TVK-DEC-...
```
