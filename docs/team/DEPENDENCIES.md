# TVK — Phụ thuộc liên nhóm và bàn giao

**Ngày:** 2026-10-31 · **Owner:** TVK-04 · **Nguồn chuẩn:** [DECISION_LOG](DECISION_LOG.md), [ASSET_CONTRACTS](ASSET_CONTRACTS.md), [STATUS_BOARD](STATUS_BOARD.md).
Các dòng dưới đây là **việc cần phối hợp**, không phải lời khẳng định đã tạo PR/code/asset.

## Nguyên tắc

- Khi một nhóm cần thông tin từ nhóm khác, ghi `DEP-ID`, phía **cung cấp**, phía **tiêu thụ**, giao diện/tài liệu cụ thể, deadline nếu được người dùng giao, và trạng thái.
- Có thể bàn giao **hợp đồng/tài liệu đã chốt** trước sản phẩm cuối. PR tài liệu nhỏ, TVK-04 review/merge sớm; không cần đợi hoàn thành checkpoint lớn.
- Các nhóm chỉ coi thông tin là chuẩn chung sau khi đã có commit ở `map-2d-prototype` và đọc đúng phiên bản; commit branch riêng không tự lan sang branch khác.
- `BLOCKED_BY_TEAM` ghi rõ ai đang thiếu gì. Sau khi nguồn đã cập nhật: `CONTRACT_READY` (tài liệu), `IMPLEMENTATION_READY` (đã nghiệm thu code/art cần thiết), `INTEGRATED` (TVK-04 merge, có chứng cứ).
- `CONTRACT_READY` không đồng nghĩa `IMPLEMENTATION_READY`; ảnh chưa duyệt không được import production. Đối với hoạt ảnh, chỉ dùng asset/layer đã nghiệm thu, không warp.
- Mọi liên kết đến branch/PR dùng URL thật, không tự điền commit/PR chưa tồn tại.

## Bảng phụ thuộc

| DEP-ID | Bên cung cấp | Bên sử dụng | Cần chia sẻ | Trạng thái ban đầu | Bước kế |
|---|---|---|---|---|---|
| TVK-DEP-001 | TVK-01 | TVK-03, TVK-04 | Asset key 6 chiều: nhân vật, wardrobe, integrity, pose, expression, action và trạng thái duyệt | CONTRACT_DRAFT | TVK-01 xác nhận IDs, TVK-04 thiết kế resolver |
| TVK-DEP-002 | TVK-03 | TVK-01, TVK-04 | Event ngưỡng hư hại 70/50/30 và quy tắc không làm reset state | CONTRACT_DRAFT | TVK-03 đề xuất payload & test |
| TVK-DEP-003 | TVK-02 | TVK-01 | Scene IDs, pose/expression/wardrobe cần theo hội thoại và thân mật | CONTRACT_DRAFT | TVK-02 xuất scene→asset requirement list |
| TVK-DEP-004 | TVK-02 | TVK-03, TVK-04 | Quest → battle → battle result → quest/NPC state/save | CONTRACT_DRAFT | Hai nhóm thống nhất event ID/schema; TVK-04 nối |
| TVK-DEP-005 | TVK-01 | TVK-04 | Lâm Thiển front master HD + 4 integrity + pilot sprite được duyệt | BLOCKED_BY_ART | TVK-01 duyệt từng master; không dùng crop V2/ảnh AI sai model |
| TVK-DEP-006 | TVK-02 | TVK-04 | Chương 1 map/hội thoại/nhiệm vụ hai nhánh, API save/load | NEEDS_IMPLEMENTATION | Audit WORLD-001, module độc lập + test |
| TVK-DEP-007 | TVK-03 | TVK-04 | Engine chiến đấu, UI và battle-result event | NEEDS_IMPLEMENTATION | Audit COMBAT-001, module độc lập + test |
| TVK-DEP-008 | TVK-04 | TVK-01, 02, 03 | Resolver & UI theo static-first, cách báo missing art, giao diện shared | CONTRACT_DRAFT | TVK-04 cập nhật code và test, không tự khai đã xong |
| TVK-DEP-009 | TVK-01 / TVK-02 | TVK-04 | Tài nguyên nhân vật và scene Tô Nguyệt Ly dùng cho Chương 1 | NEEDS_ART_PLAN | Đối chiếu Story Bible/scene trước khi đặt hàng loạt asset |

## Khi nào báo sang TVK-04?

- **DECISION_READY:** yêu cầu người dùng đã chốt và ghi thành hợp đồng/tài liệu; đề nghị TVK-04 **merge docs** ngay, không cần đợi hoàn tất tính năng.
- **READY_FOR_REVIEW:** PR code/tài nguyên có đủ commit, kiểm thử phù hợp, art approval nếu là production; TVK-04 kiểm diff/CI rồi mới merge.
- **PENDING_APPROVAL:** thiếu duyệt hình/UI/decision, chỉ merge bản nháp có nhãn nếu không ảnh hưởng runtime.
- **NOT_READY / BLOCKED_BY_TEAM:** ghi rõ dependency ID, chủ sở hữu, điều kiện còn thiếu.

## Mẫu yêu cầu liên nhóm

```markdown
- Dependency ID: TVK-DEP-XXX
- Requesting team / providing team:
- Required contract / fields / values:
- Reason / receiving task ID:
- Deadline (only if actually agreed):
- Status: CONTRACT_DRAFT | BLOCKED_BY_TEAM | CONTRACT_READY | IMPLEMENTATION_READY | INTEGRATED
- Branch commit / PR / source link:
- Acceptance criteria and next owner:
```

TVK-04 cập nhật bảng này **sau khi kiểm tra bằng chứng GitHub**. Chỉ chốt theo nội dung chat khi có xác nhận, không bịa đã sync.
