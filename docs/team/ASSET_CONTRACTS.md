# TVK — Hợp đồng tên ảnh / trạng thái nhân vật dùng chung

**Ngày:** 2026-10-31 · **Owner hợp đồng:** TVK-04, phối hợp TVK-01 (art) và TVK-03 (combat).
**Đây là SPEC/CONTRACT ĐỀ XUẤT, không phải code đã tích hợp.** Quan sát từ source hiện tại: `CharacterAppearanceState.State` lưu đủ `wardrobe, integrity, pose, expression, action`, nhưng `resolveArt` hiện **chưa dùng expression/action khi chọn file**. Không đánh dấu contract implemented khi chưa sửa resolver và test.

## 1. Key xác định đúng một sprite

```text
character_id × wardrobe_id × integrity × pose_id × expression_id × action_id
    => {asset_path, crop, master_id, source_sha256, approval_status, resolution}
```

- ID chuỗi dạng `[a-z0-9_]{1,64}` để khớp định dạng hiện tại.
- `integrity` thuộc `{100,70,50,30}`, độc lập với wardrobe; combat phát **sự kiện**, không sửa source art.
- Mỗi kết hợp thực sự dùng trong game có **một PNG sprite độc lập**, chỉ một tư thế/biểu cảm, nền alpha sạch, canvas/pivot và ánh sáng được kiểm. Có thể chia sẻ cùng master PSD/ORA nhiều lớp để sản xuất hàng loạt nhưng **không dùng sheet/crop/upscale proxy thay art**.
- `expression` và `action` phải được tính trong lookup. Không tự thay `70%` bằng ảnh `100%`, không đổi nhân vật/pose/wardrobe/biểu cảm sai chỉ vì thiếu ảnh.
- Khi thiếu tổ hợp được yêu cầu: giữ nguyên game state, trả lỗi thiếu asset/cảnh báo hoặc fallback DRAFT **có nhãn rõ** (chỉ debug), không lén tráo art đã duyệt.

## 2. Ví dụ manifest (chưa được đưa vào game)

```json
{
  "schema_version": 1,
  "character_id": "lam_thien",
  "wardrobe_id": "default",
  "integrity": 70,
  "pose_id": "front",
  "expression_id": "shy",
  "action_id": "idle",
  "asset_path": "characters/lam_thien/lt_default_70_front_shy_idle.png",
  "crop": "full",
  "master_id": "lt_front_master_pending",
  "source_sha256": null,
  "approval_status": "DRAFT",
  "resolution": null
}
```

**Đây là mã ví dụ, không phải tệp đã tồn tại.** TVK-01 phải đề xuất danh sách mã pose/biểu cảm/action từ kịch bản; TVK-04 khóa schema và thực thi migration để không phá game save hiện có.

## 3. Trạng thái một asset

| Trạng thái | Ý nghĩa | Có được đưa vào APK production? |
|---|---|---|
| REFERENCE_ONLY | CANON board/crop, ảnh V2, ảnh mẫu tham khảo khác, không phải sprite cuối | Không |
| DRAFT | Art mới nhưng sai/chưa kiểm CANON, thiếu alpha hoặc chưa đủ chi tiết | Không |
| PENDING_USER_APPROVAL | Art đạt QA kỹ thuật nhưng chờ người dùng so với CANON | Không |
| APPROVED | Đúng CANON/thiết kế dẫn xuất đã chốt và được người dùng duyệt, có provenance & QA | Có thể sau kiểm runtime |
| REJECTED | Sai model, bàn tay, giày, trang phục, tỷ lệ, v.v. | Không |

`APPROVED` không tự đồng nghĩa `ANDROID_VERIFIED`. CI/build thành công không thay được kiểm art và thiết bị.

## 4. CANON và yêu cầu thay đổi Lâm Thiển

- Nguồn chuẩn bất biến: `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, **941×1672 RGBA**, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`, tỷ lệ body +17%.
- Nguồn art Front đứng thực trong sheet CANON là crop cỡ 208×443; phóng lớn không tạo detail native HD.
- Người dùng yêu cầu **tóc/đầu theo ảnh 1, phần còn lại theo ảnh 2, tinh giản dây vàng, tua rua/phụ kiện**: đây là yêu cầu cho một **master dẫn xuất cần duyệt**; chưa tự đổi CANON gốc và chưa được gọi `APPROVED`.
- Hình tham khảo do người dùng dành cho các nhân vật tương lai = `REFERENCE_ONLY`; không áp vào Lâm Thiển.
- 4 mức trang phục gồm cả thân dưới, mức rách/bụi/xước hợp lý; giữ nguyên nhận diện và tỷ lệ; cần preview theo cùng pose.
- Bản sprite production là PNG riêng, không bảng ghép; nguồn gốc, alpha, checksum, master, pivot và độ phân giải phải lưu trong manifest. Kích thước xuất game được đo theo device; không ép mọi sprite thành 4K nếu gây tốn bộ nhớ.

## 5. Giao tiếp với World và Combat

- TVK-02 cung cấp `scene_id, character_id, wardrobe_id, integrity, pose_id, expression_id, action_id` cho mỗi beat hội thoại/sự kiện cần ảnh. Nếu chưa có art, đánh dấu `REQUIRED_MISSING` và có thể dùng placeholder ghi DRAFT cho debug.
- TVK-03 cung cấp sự kiện trạng thái như `IntegrityThresholdReached(character_id, new_integrity, battle_id)`; payload cụ thể phải được TVK-03/01/04 rà trước khi khóa. Event không chứa đường dẫn asset và không được reset các trường state khác.
- TVK-04 sở hữu resolver + asset manifest migration + test hiện có/thiếu/missing 70/50/30/expression/action. Kiểm state persistence, không tự bịa asset.
- TVK-01 sở hữu art production và danh sách combo/metadata; các nhóm khác **không tự sinh ảnh mới hoặc thay CANON** để vá missing sprites.

## 6. Checklist nghiệm thu

1. Đúng nhân vật CANON hoặc master dẫn xuất được người dùng duyệt.
2. Full-body hai tay/hai chân/hai guốc và trang phục đúng; không chi tiết thừa, không mất mũi guốc.
3. Một PNG RGBA riêng, alpha sạch, không dính ảnh bên cạnh, không watermark/chữ, canvas/pivot cố định.
4. Đạt mức nét hiển thị game thật; nguồn nhiều lớp chất lượng cao nếu cần đổi pose/cảm xúc; không gọi upscale proxy là HD.
5. Metadata chỉ tới nguồn thật, checksum, kích thước và quyền lưu trữ; không đăng private CANON vào repo public.
6. Các biến thể 100/70/50/30 có vết hư hại nhất quán, không đổi hình thể hoặc họa tiết chính.
7. Duyệt art riêng với kiểm code, Android QA riêng với build CI. Thiếu điều kiện phải báo `BLOCKED`.

## 7. Tác vụ tiếp theo

- `CHAR-421`: TVK-01 cung cấp danh mục ID, manifest của pilot 12 ảnh; artwork chỉ khi master được duyệt.
- `INT-004`: TVK-04 cập nhật `resolveArt` để hỗ trợ expression/action bằng manifest; migration + test; không triển khai tự phát trên nhánh của TVK-01/03.
- `COMBAT-001` và `WORLD-001`: thống nhất events/scene requirements qua [DEPENDENCIES](DEPENDENCIES.md).
