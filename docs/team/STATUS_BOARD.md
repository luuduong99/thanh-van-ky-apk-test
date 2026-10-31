# TVK — Bảng trạng thái tích hợp (chỉ TVK-04 cập nhật)

**Khởi tạo:** 2026-10-30. **Chỉ ghi điều đã kiểm chứng từ repo/CI/handoff.** File này là điểm đọc nhanh của 4 thread, không thay cho `PROJECT_SPEC.md`.

| Thread | Nhánh | Mốc cơ sở đã xác minh | Việc tiếp theo | Trạng thái |
|---|---|---|---|---|
| TVK-01 Nhân vật | `tvk/characters` | Lâm Thiển CP419 đã có APK debug idle+blink; art CANON V2.1 vẫn blocked | `CHAR-CP420`: rà đầu/tóc/gáy/cổ high-res master và art production thật | READY, art production **BLOCKED** |
| TVK-02 Bản đồ/Cốt truyện | `tvk/world-story` | `MainActivity.kt` có prototype map + hội thoại chương I; `CHAPTER_01_IMPLEMENTATION.md` | `WORLD-001`: audit code hiện tại, tách map/quest thành module có test | NOT STARTED ở thread riêng |
| TVK-03 Chiến đấu | `tvk/combat` | Có luật turn-based/UI trong PROJECT_SPEC; chưa có chứng cứ game combat production hoàn thiện | `COMBAT-001`: audit thực trạng source và viết state-machine độc lập | NOT STARTED ở thread riêng |
| TVK-04 Tích hợp/APK | `map-2d-prototype` | CP419 GitHub source CI SUCCESS 7 PASS/3 SKIP, build APK debug SUCCESS | `INT-001`: kiểm tra PR từng thread, tránh file shared, ghép thành APK chương I | READY |

## Quyết định tích hợp INT-002 — đã triển khai nguồn, source CI 7 PASS + Android build SUCCESS; đang chờ nghiệm thu thiết bị

- 2026-10-31: **static-first, view-only** — body hotspots ngừng hoạt động trên màn nhân vật; nút chuyển cảnh, wardrobe, pose, expression, dialogue vẫn có. Android `CharacterInteractionActivity.kt` dùng `FIT_CENTER` thay bitmap mesh; CP419 chỉ còn debug. Chuẩn chi tiết: [STATIC_FIRST_SCENE_MODE.md](STATIC_FIRST_SCENE_MODE.md).
- Cần CI source-contract và Android build SUCCESS để xác nhận build; chưa xác minh thao tác thực trên thiết bị. Các thread khác phải đọc quyết định này từ nhánh tích hợp `map-2d-prototype` trước khi tiếp tục trên nhánh riêng; các nhánh **không tự cập nhật**.

## Release gate vẫn khóa

- Lâm Thiển đúng CANON V2.1: `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- `production_release.status=blocked_pending_art`, `sprite_paths={}`, `visual_approval=PENDING_USER`, `spine_ready=false`, `android_device_verified=false`.
- **Không biến `GitHub Actions SUCCESS` thành `visual art approved` hoặc `tested on real Android`.**

## Mẫu cập nhật một dòng (sau khi merge)

`YYYY-MM-DD | TEAM-ID | task-id | source commit | PR | integrated commit | tests PASS/FAIL/SKIP | user approval | build APK | blocker/next`

**Lưu ý:** các nhánh vừa được tạo không có nghĩa bốn công việc tự chạy đồng thời. Người dùng tạo chat và giao task cho từng thread qua `START_THREADS.md`.
### INT-002 — Bằng chứng CI/APK (2026-10-31)

- Source contract [41151380759](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/41151380759) **SUCCESS 7/7**.
- Android build [41151376829](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/41151376829) **SUCCESS**, APK `8,824,258` bytes SHA256 `4842812c72ce3d8fcc35a1e600e2c0cc1f7417c42f381918494090946bf18fcd`. Có thể lấy ở Library `/Thanh Van Ky/Development/INT002_Static_First_View_Only_20261031/`.
- Trạng thái: **SOURCE_AND_BUILD_PASSED, DEVICE_QA_PENDING, SCENE_ART_PARTIAL, ANIMATION_APPROVAL_PENDING**. Các thread khác phải nhận quy định từ `map-2d-prototype`, không tự bật lại body hotspots.

### 2026-10-31 — Phản hồi motion demo — ART REWORK REQUIRED

- Người dùng phản hồi `TVK_LamThien_NaturalMotion_PriorityChest.mp4` và các video thử trông như **kéo ảnh**, không phải chuyển động tự nhiên như video tham chiếu. **Không đạt nghiệm thu**; tuyệt đối không xem đây là animation chính thức.
- Quy tắc cập nhật tại [STATIC_FIRST_SCENE_MODE.md](STATIC_FIRST_SCENE_MODE.md): không scale/warp *cả cục bộ* ngực, torso, tóc, tay từ ảnh phẳng. Làm frame art/layer/underpaint thật rồi mới animate; ưu tiên nhịp thở/vòng một tự nhiên, chớp mắt/má ửng/tóc/tay nhẹ.
- **TVK-01 action:** kiểm tra nguồn master painter-quality, dựng 2–4 keyframe có duyệt CANON cùng pose; **không** lặp demo filter/mesh/pixel patch. **TVK-04:** giữ static fallback, chưa tích hợp motion draft.
- Source/build CI pass của viewer không xác nhận animation. `visual_approval=PENDING_USER`, `animation_ready=false`.

## DOC-SYNC-001 — Chuẩn hóa chia sẻ quyết định giữa 4 nhóm (2026-10-31)

- Đã thêm 3 tài liệu dùng chung trên nhánh `map-2d-prototype`: [DECISION_LOG.md](DECISION_LOG.md), [DEPENDENCIES.md](DEPENDENCIES.md), [ASSET_CONTRACTS.md](ASSET_CONTRACTS.md).
- Quyết định trong TVK-01/02/03 sẽ cần commit **trên nhánh riêng**, PR tài liệu sớm để TVK-04 merge, rồi các nhóm đọc bản trên nhánh tích hợp. **Không có cơ chế tự đồng bộ chat hoặc branch tự động**.
- Ghi rõ `DECISION_READY`, `READY_FOR_REVIEW`, `PENDING_APPROVAL`, `BLOCKED_BY_TEAM` và `NOT_SYNCED` để không nhầm quyết định đã chốt với asset/code production đã nghiệm thu.
- Không thay đổi gameplay, source code, CANON private hoặc APK trong DOC-SYNC-001. Art Lâm Thiển vẫn `PENDING_USER_APPROVAL`, Android device QA vẫn chưa xác minh; `production_release.status=blocked_pending_art`.
