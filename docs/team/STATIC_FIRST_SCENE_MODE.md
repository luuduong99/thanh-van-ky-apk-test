# TVK — Chế độ xem cảnh bằng ảnh tĩnh (Static-first / View-only)

**Quyết định sản phẩm được người dùng xác nhận: 2026-10-31.** Áp dụng cho toàn dự án, TVK-01/02/03/04. Đây là quy tắc gameplay đang hoạt động, có ưu tiên cao hơn các **hướng dẫn tương tác chạm body ở checkpoint cũ**. Không chỉnh sửa những CANON đã chốt.

## Trải nghiệm mong muốn

1. Nhân vật hiển thị bằng **ảnh tĩnh sắc nét đúng trạng thái đang chọn**, đúng nhận diện CANON. Thay cảnh bằng **nút cảnh / hội thoại / lựa chọn**, thay tư thế qua **nút tư thế**, trang phục qua **nút trang phục / thay đồ**; các nút và lưu state tiếp tục hoạt động.
2. **Tắt các hotspot / touch-zone trên body**: chạm, vuốt hoặc giữ vào bất kỳ vị trí nào trên ảnh nhân vật đều **không gọi phản ứng theo body-zone**, không phát hoạt ảnh phản ứng chạm, không tự thay expression, không tự nhận điểm thân thiết do body touch.
3. **Giữ chạm UI để điều khiển**: nút tương tác được ấn như cũ; chạm nền hội thoại để tiếp tục dòng (nếu thiết kế cảnh hỗ trợ); chạm điểm trên bản đồ chọn địa điểm/NPC vẫn hoạt động. Chỉ vô hiệu hóa touch-zone trên hình nhân vật.
4. Nếu chưa có sprite đúng `character × pose × wardrobe × integrity × expression`: hiển thị thông báo **thiếu asset** hoặc bản draft được đánh dấu, không thay lén bằng trang phục/tư thế/người khác.
5. Các mốc trang phục/hư hại 100/70/50/30 và trạng thái wardrobe / pose tiếp tục được lưu và có thể lựa chọn. **Quy tắc lựa chọn trạng thái không có nghĩa mọi hình đã đủ/đã duyệt.**

## Chuyển động nhẹ khi đủ asset đạt chất lượng

- Giai đoạn A (đang áp dụng): **ảnh tĩnh**, dùng `ImageView.ScaleType.FIT_CENTER`; không dùng lưới bitmap, toàn thân warp, scale vùng ngực hay kéo méo mắt/cổ/eo/tay áo.
- Giai đoạn B (tùy chọn, cần nghiệm thu): eyelid blink, thở vùng vai/thân trên rất nhẹ, chuyển động mềm vùng ngực theo hơi thở, tóc ngọn, tay áo, lụa; **chỉ animate các layer đã được vẽ/khép kín/underpaint và duyệt**, có điểm neo và kiểm seam. Không dùng mesh của CP419 như rig production.
- Nếu chưa có asset phù hợp hoặc bất kỳ khung nào méo mặt, cổ, vòng ngực/eo, trang phục, họa tiết, viền tóc hay đường silhouette: **tắt animation và dùng lại static**. Việc chuyển fallback không được reset wardrobe/pose/integrity.
- Mọi trạng thái phải được kiểm tra ở kích thước hiển thị thật trên Android; AI draft/CI PASS không đồng nghĩa visual approval.
- CANON Lâm Thiển V2.1 SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a` bất biến; chưa có sprite high-res/rig được duyệt.

## Thực thi Android đã thay đổi

- `app/src/main/java/vn/thanhvanky/prototype/CharacterInteractionActivity.kt`: heroine portrait ở cả normal và bed pose sử dụng **`ImageView(FIT_CENTER)` không có listener**, không gọi `TVKCharacterMotionView`, `touchPortrait`, `respondToTouch`. Nam chính cũng được render tĩnh.
- Các nút **chọn nhân vật, tư thế, biểu cảm, wardrobe, scene, trò chuyện, về bản đồ** giữ nguyên. `CharacterAppearanceState` tiếp tục lưu state, cũng giữ mã `character_interactions.json` làm nguồn scenes/poses; `touchZones` ở file JSON trở thành *legacy metadata, runtime không dùng* và chỉ dùng lại nếu người dùng phê duyệt lại.
- `MainActivity.kt`: tương tác bản đồ và tiến trình hội thoại bằng UI là luồng riêng, **không bị thay đổi**.
- CP402–CP419 animation *DEBUG* còn tồn tại ở các màn test được đánh dấu rõ. **Không đồng nghĩa chuyển động được bật ở chế độ xem cảnh thật**.
- Các điểm scene hiện có chưa chắc có đủ minh họa riêng. Giao diện vẫn có thể hiển thị lời thoại/cảnh hiện có; artwork nào thiếu phải báo thiếu, không giả là có ảnh tương ứng.

## Bảng nghiệm thu tối thiểu

| ID | Thao tác | Kết quả cần có |
|---|---|---|
| VIEW-01 | Chạm, vuốt, giữ lên ảnh body | Không `touch_reaction`, không tăng affinity do body-zone, không thay expression |
| VIEW-02 | Chọn nút đổi trang phục | Wardrobe đổi / giữ state; thiếu ảnh hiện cảnh báo |
| VIEW-03 | Chọn tư thế front/back/bed | Pose đổi, state khác không reset |
| VIEW-04 | Chọn cảnh/trò chuyện | Nội dung cảnh, hội thoại/điểm điều khiển còn hoạt động |
| VIEW-05 | Chạm vị trí map, nút hội thoại | Hệ điều khiển riêng vẫn hoạt động |
| VIEW-06 | Chọn pose/outfit chưa có sprite | Không tráo image không đúng CANON/wardrobe/damage |
| VIEW-07 | Bản static ở ảnh nguồn | Không `drawBitmapMesh`, source giữ tỷ lệ bằng `FIT_CENTER` |
| VIEW-08 | Chạy debug preview cũ | Không tự đánh dấu production animation ready |

**Trạng thái nghiệm thu:** đã thực thi thay đổi source, nhưng phải có Android CI build và test trên thiết bị thật để xác nhận runtime. Không nâng `production_release` hay `spine_ready` vì thay đổi này.

## Phân công bốn thread

- **TVK-01**: sản xuất ảnh static chính xác và layer micro-animation **không méo**, không phụ thuộc body hotspot.
- **TVK-02**: bản đồ/NPC/story/scene switching, nút đổi cảnh; không làm touch-zone trên nhân vật.
- **TVK-03**: battle với sprite static cho đội/địch, frame skill khi có; không buộc có rig.
- **TVK-04**: tích hợp viewer, pose/wardrobe controls, kiểm thử/static fallback, CI/APK và đảm bảo các thread không tái bật body hotspot.

Tài liệu cũ mô tả body touch chỉ mang tính **lịch sử**, không còn là hành vi mục tiêu hiện tại. Muốn bật lại phải có **quyết định mới của người dùng**, không tự động khôi phục vì JSON có `touchZones`.

## Bằng chứng tích hợp INT-002 (2026-10-31)

- [GitHub Actions Source Contract](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/41151380759): **SUCCESS — 7/7 PASS**. Chỉ kiểm source/luồng nút, chưa kiểm thao tác trên máy thật.
- [GitHub Actions Android Build](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/41151376829): **SUCCESS**. Artifact `13023586247`; APK debug `TVK_Static_First_View_Only_Debug_20261031.apk` **8,824,258 bytes**, SHA256 `4842812c72ce3d8fcc35a1e600e2c0cc1f7417c42f381918494090946bf18fcd`.
- Kiểm ZIP CRC và DEX thấy `STATIC-FIRST`, `FIT_CENTER`; không nhúng các file riêng tư `LAM_THIEN_CANON_V2_1_FINAL_20261029.png` hay atlas CP417.
- Đã lưu APK + workflow artifact trong Library `/Thanh Van Ky/Development/INT002_Static_First_View_Only_20261031/`.
- **Giới hạn chưa nghiệm thu:** chưa thử trực tiếp chạm/đổi cảnh/pose/wardrobe trên điện thoại; scene-specific art và micro-animation phân lớp chưa hoàn thiện. `production_release.status=blocked_pending_art`.

## ART REVIEW — phản hồi trực tiếp của người dùng (2026-10-31): PHƯƠNG PHÁP KÉO ẢNH BỊ LOẠI

Các demo thử dựng nhiều phương án và video `TVK_LamThien_NaturalMotion_PriorityChest.mp4` **KHÔNG ĐƯỢC DUYỆT**: cảm giác hình bị kéo, co dãn và dịch chuyển để giả chuyển động, khác chất lượng chuyển động thực mà người dùng mong muốn ở video tham chiếu.

**Tiêu chuẩn sửa đổi (ưu tiên cao hơn mô tả chuyển động thử trước đó):**
- Cấm **cả warp toàn ảnh lẫn warp/scale/stretch một phần thân trên, vòng ngực, vai, tay, tóc** từ một ảnh phẳng. Không được che giấu việc biến dạng bằng từ "local micro-animation" hoặc "mức rất nhẹ".
- Chuyển động vòng ngực ưu tiên số một, nhưng phải là **nhịp thở/chuyển động vải được vẽ riêng theo thời điểm**, có underpaint, nếp áo, viền trang phục, sắc độ và trọng tâm thống nhất. Không thể tuyên bố có "chuyển động ngực thật" nếu mới dùng 1 sprite phẳng.
- Chớp mắt: các frame mặt/mí được **vẽ lại thực sự cùng pose**, duyệt chi tiết mặt và màu da; CP417 là DRAFT không được tự nâng thành production.
- Tay/tóc: cần asset tách lớp và underpaint chất lượng; có thể dùng khớp nối, chuyển động rất chậm, không xé mép, lặp nét hoặc tạo cảm giác bị kéo.
- Ứng dụng màu ửng đỏ được phép nếu là overlay sắc độ đồng bộ da, **không bóp hình mặt**.
- Chuyển động ưu tiên chậm, không rung, không biểu diễn quá mức. Cần kiểm video ở mức phóng to 100% và tốc độ bình thường, so sánh liên tục với ảnh CANON; chặn nếu có méo, ghosting, viền trắng, khớp gãy, ánh sáng/vải không đồng nhất.
- **Nếu không có frame/layer được vẽ đúng CANON để animate, phải thành thật hiển thị ảnh tĩnh + môi trường / blink DRAFT có nhãn**, không tự chế animation cơ thể bằng deform.
- Video demo bị chê được giữ lại chỉ để audit kỹ thuật, **không phải tham chiếu chất lượng nghệ thuật**. Không dùng làm tiêu chí chốt cho TVK-01.

**Mốc nghiệm thu art cho demo mới:** (1) duyệt 2–4 keyframe nhịp thở/sắc độ/vải trên model CANON đúng pose trước; (2) kiểm ảnh đứng yên vẫn pixel-exact hoặc duy trì nhận diện; (3) chỉ nội suy bằng frame đã được họa sĩ dựng và kiểm viền, không scale patch; (4) xuất video ngắn chứng minh động tác nhìn tự nhiên; (5) người dùng duyệt mới được tích hợp game. **Hiện ở trạng thái ART_REWORK_REQUIRED**.
