# Thanh Vân Ký — Sổ kinh nghiệm & playbook cho mọi checkpoint

**Bắt đầu:** 2026-10-30. **Mục đích:** biến kinh nghiệm thực tế thành quy trình dùng lại được, tăng độ chính xác và giảm vòng lặp không cần thiết. Mục tiêu tối ưu là **chất lượng/tốc độ hoàn thành thực**, không phải số checkpoint hoặc số test PASS.

## 8 quy tắc bắt buộc

1. **Source/CANON lock:** đọc `docs/PROJECT_SPEC.md` trước; xác minh filename + kích thước + SHA-256 của CANON. Khi gửi preview phải dùng đúng ảnh CANON nhân vật hiện hành, hoặc crop đúng từ ảnh đó; ảnh mới là `DRAFT`, ảnh của người dùng bổ sung là `REFERENCE`.
2. **Không hòa trộn sai pose:** CP410/CP411 chứng minh crop biểu cảm 168×197 và crop body đứng 208×443 từ cùng nguồn không thể overlay trực tiếp. Cần master mặt ở đúng pose và underpaint tóc/cổ trước khi rig quay đầu/blink.
3. **Tách kiểm thử kỹ thuật và thẩm mỹ:** PASS hash, pixel, alpha, ROI không thay cho visual approval. Không suy diễn `CI SUCCESS` hoặc `assembleDebug SUCCESS` là đã test điện thoại thật.
4. **Không giả nguồn art:** upscale là viewing proxy, ORA với paint layer trống là artist handoff, biến dạng bitmap không phải rig phân lớp. Ghi đúng phần đã làm và phần chưa làm.
5. **Không thay CANON âm thầm:** trạng thái asset phải là `REFERENCE -> DRAFT -> REVIEWED -> APPROVED_CANON -> INTEGRATED -> DEVICE_VERIFIED`. Nâng trạng thái chỉ khi có bằng chứng tương ứng.
6. **Kiểm QA toàn hình:** ngoài cận cảnh mặt/trang phục còn phải xem whole-body, tay áo, tóc, phụ kiện, hai chân và mũi giày; áp dụng bài học từ lỗi mũi guốc bị khuyết trong các preview cũ.
7. **Batch có tiêu chí:** chỉ tạo vài phương án có khác biệt đáng đánh giá; so sánh native + zoom + full-image, chốt/loại theo bằng chứng, tránh thử cùng một bản vá nhỏ nhiều lần không cải thiện art.
8. **Không đánh dấu blocker là resolved quá sớm:** ghi `PASS/FAIL/SKIP` rõ ràng; thiếu file nguồn/private tests hoặc thiếu kiểm Android thực thì giữ `BLOCKED`/chưa nghiệm thu.

## Kinh nghiệm mới — hình thể, trang phục, rách/bẩn (2026-10-30)

Nguồn [4 ảnh tham khảo và SHA](art/TVK_COSTUME_DAMAGE_REFERENCES_20261030.md). Đây là nguồn **tham khảo**, không phải những model đã chốt.

- Tách lớp kỹ thuật theo vật liệu và chức năng (vải chính, vải lót, voan/thêu, phụ kiện, quần tất); nếu không có master layer thì đừng giả định có rig.
- Bốn mốc 100/70/50/30 phải **kế thừa nhau**: rách/đường chỉ/hoa văn phát triển có lý, không xuất hiện mất đi ngẫu nhiên giữa các frame.
- Chất liệu khác nhau có đường rách, căng và bóng khác nhau; bụi và vết xước đặt theo điểm ma sát, không phủ mất hoa văn hay che biểu cảm.
- Mức % **không** đồng nghĩa phần trăm diện tích vải bị xóa. Mức thấp vẫn bảo toàn silhouette, form, độ che phủ và tính nhất quán của nhân vật.
- Kiểm tra mặt trước/mặt sau: đường nối vai, lưng, eo và trang sức phải đối chiếu được. Bộ ảnh có nhiều góc nhìn không tự động là turnaround rig-ready.
- Logic gameplay: trạng thái trang phục đổi khi lần đầu xuống ngưỡng HP liên quan và được giữ trong các cảnh sau theo spec; art phải tách khỏi điều kiện logic để có thể đổi asset mà không sửa engine.

## Bảng workflow lặp

| Bước | Kiểm tra để chuyển bước |
|---|---|
| 1. Read | `PROJECT_SPEC`, checkpoint, CANON đúng SHA, blockers |
| 2. Define | asset ID, trạng thái `REFERENCE/DRAFT/CANON`, acceptance criteria |
| 3. Reuse | script/ORA/test đã xác minh; không sinh master giả |
| 4. Preview | fullbody + chi tiết + native/zoom, trước/sau, 100/70/50/30 nếu liên quan |
| 5. QA | hash/pixel/alpha/layer + art visual + Android thiết bị thật khi cần |
| 6. Commit | cập nhật artifact, SHA, GitHub/Library, liên kết ở spec |
| 7. Resume | chỉ ghi hoàn tất điều có chứng cứ; lưu rõ việc còn mắc để phiên sau đọc tiếp |

## Mẫu entry khi phát sinh bài học

```md
### YYYY-MM-DD — CPxxx — Tên vấn đề
- Input và nguồn lock (filename/SHA/branch/commit):
- Dấu hiệu lỗi / kiểm chứng:
- Cách làm hiệu quả và vì sao:
- Cách làm không hiệu quả / điều cần tránh:
- Kết quả kỹ thuật (PASS/FAIL/SKIP):
- Kết quả mỹ thuật và Android thực:
- Quy tắc có thể dùng lại:
- Blocker chưa xử lý / bước tiếp theo:
```

## Metrics hướng tới hiệu quả

- Lần dùng sai nguồn CANON (mục tiêu 0).
- Số lỗi tái xuất hiện sau khi đã ghi lessons (mục tiêu 0).
- Vòng tạo/sửa trước khi được duyệt mỹ thuật, phân biệt art và technical.
- Mức độ hoàn thành thực: `DRAFT`, `APPROVED_CANON`, `INTEGRATED`, `DEVICE_VERIFIED`.

**Trạng thái 2026-10-30:** `PROJECT_SPEC` đã đến CP411. Art master đầu/mí mắt đúng pose đứng, rig phân lớp và test điện thoại thật vẫn chưa hoàn tất. Không đổi các trạng thái đó vì cập nhật tài liệu.

## 2026-10-30 — CP412 — Bỏ vòng lặp giả master, đo khe hở khi đầu xoay

- **Input lock:** CANON Lâm Thiển V2.1 raw SHA `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`; crop dáng đứng `(16,180,224,623)` = 208×443. Không dùng expression portrait sai pose.
- **Vấn đề thật:** neutral head recompose đúng pixel vẫn không có nghĩa 2D rig khi chuyển động ổn. Khi nghiêng 2°–4°, rough mask cắt ngang tóc/underpaint giả sẽ lộ vùng chưa có art.
- **Cách phát hiện hiệu quả:** một board nguồn thật với 5 góc -4/-2/0/+2/+4; ghi số pixel phụ thuộc underpaint **271/174/0/174/276** (không diễn giải là chấm điểm mỹ thuật); soi luôn mặt cận và toàn thân. Cấm quảng bá debug rotation là hoạt ảnh đã đạt.
- **Cải tiến tăng tốc:** thay vì liên tục sửa vài pixel mí mắt, dùng một `ORA` có 8 lớp vẽ trống tên rõ ràng và source CANON hiển thị, chuyển giao trực tiếp phần cần vẽ. Test chặn nhầm CANON và chặn nâng trạng thái art nếu lớp vẫn trống.
- **Bằng chứng:** local **10/10 technical PASS** với CANON thật; [GitHub Actions CP412](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/41069360009) SUCCESS: 5 PASS / 5 SKIP vì thiếu private CANON. Đã tạo source tool/test và ZIP offline. Không có art mới được vẽ, rig thật hay test điện thoại thực.
- **Quy tắc tái dùng:** mỗi prototype động phải kiểm tra 0° nguyên bản + biên chuyển động và lớp hình bị khuất; định nghĩa rõ `DRAFT` vs `APPROVED_CANON`. Sau khi phát hiện thiếu underpaint, ưu tiên họa sĩ tạo master thực sự thay vì thêm vòng kiểm thử kỹ thuật.
- **Blocker:** `front-face/head master`, mắt nhắm đúng pose, vẽ cổ/tóc sau đầu, nhiều lớp tóc/phụ kiện vẫn thiếu; `sprite_paths={}`, `production_release.status=blocked_pending_art`. CP413 tập trung giải quyết blocker mỹ thuật.

Chi tiết: [CP412 handoff](art/LAM_THIEN_CP412_SAME_POSE_ART_INTAKE.md).

## 2026-10-30 — CP413 — Soi lỗi động trực tiếp trong APK thay vì chỉ xem ảnh tĩnh

- **Nguyên nhân:** kiểm tra PNG/ORA ở tư thế 0° không phát hiện khe ghép phát sinh khi đầu nghiêng. Ảnh crop biểu cảm khác pose không thể dùng làm patch cho hình đứng.
- **Đã làm tốt:** giữ SHA nguồn CANON cố định, dùng Android SAF picker kiểm raw byte + kích thước, giữ ảnh 0° đúng pixel, kiểm 5 góc ±4°/±2°/0°. Để trắng phần chưa vẽ có nhãn DEBUG, giúp nhìn rõ blocker thay vì che bằng inpaint giả.
- **Code dùng lại:** `TVKCP413HeadTurnDebugView.kt` + chế độ CP413 trong `TVKCombinedIdlePreviewActivity.kt`; không nhúng bitmap private vào APK, không ghép face portrait khác góc. Đầu vào sai SHA từ chối trước render.
- **Kiểm chứng:** [source CI](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/41071306636) **6/6 PASS**, [Android build](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/41071295753) **SUCCESS**. APK 8,817,067 bytes, SHA256 `5d2382090a2df082fed950096ac570c59cb1db61a55fdb623d3451fd95ee54c0`; đã xác minh dex chứa CP413, không đóng gói bitmap CANON.
- **Điều KHÔNG được suy ra:** static tests + assembleDebug không xác minh hiệu năng, độ đẹp, khe ghép thực khi chạy trên điện thoại, hay rig/Spine. Trạng thái vẫn **TECHNICAL_DEBUG**.
- **Tối ưu lần sau:** sau khi có công cụ soi lỗi động, **dừng thêm phiên test mặt nạ nếu chưa có art mới**. Ưu tiên vẽ thật underpaint gáy/cổ/tóc và mí nhắm đúng front đứng; nghiệm thu bằng art ở 0° và biên ±4°, rồi mới ghép production.
- **Tệp:** [CP413 Android debug handoff](art/LAM_THIEN_CP413_ANDROID_HEAD_TURN_DEBUG.md). Gói APK+CANON nguyên gốc được giữ riêng trong Library, không có trên GitHub công khai.

## 2026-10-30 — CP414 — Source-pixel extraction không phải art master mới

- **Source/CANON:** Chỉ sử dụng chính xác Lâm Thiển V2.1 SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`, crop đứng (16,180,224,623), 208×443; không mượn portrait khác pose.
- **Tiến triển thực:** tách **11 vùng RGBA chứa pixel màu nguyên bản** (tóc đỉnh, mặt, hai mắt, trang sức, tóc trên và dài, cổ), lưu đúng từng RGB gốc. ORA 14 lớp chứa 11 nguồn mẫu DRAFT ẩn, 2 lớp phải vẽ trống ẩn, 1 CANON visible; ảnh merged giữ đúng nguồn. **11/11 local source technical tests PASS; [public CI CP414](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/41073132107) SUCCESS 6 PASS / 5 SKIP**.
- **Bài học từ preview QA:** mặt nạ polygon vẫn cắt nhầm nền trắng và trang phục, chồng lấn và không có underpaint dưới tóc/cổ; vì vậy 11 file không rỗng không có nghĩa 11 bộ phận rig-ready, và phóng zoom sprite 208×443 không thể tạo mắt HD.
- **Phân biệt:** cắt/mask/số lượng layer chỉ là chuẩn bị dữ liệu. **Artist-painted underpaint, eyelashes/closed eyelid đúng pose, hair strands clean edge** mới là bước mang lại chất lượng production; chưa có thì `visual_approved=false` và `sprite_paths={}`.
- **Quy tắc tăng tốc:** Sau CP414 **đừng lặp thêm một phiên chỉ cắt mặt nạ**. Ưu tiên công việc vẽ thật và gửi trước/sau tại native/zoom để được người dùng nghiệm thu, rồi mới dùng công cụ kiểm tra CP413 ở ±4°.
- **Bàn giao:** [CP414 source layer extraction](art/LAM_THIEN_CP414_CANON_SOURCE_LAYER_EXTRACTION.md), ZIP private tại Library `/Thanh Van Ky/Development/CP414_Canon_SourcePixel_LayerDraft/`.

## 2026-10-30 — CP415 — Ngăn halo và phân biệt paint study với art hoàn chỉnh

- **Nguồn:** Lâm Thiển CANON V2.1 nguyên byte, raw SHA `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`; crop đứng 208×443, khác ảnh chân dung 168×197.
- **Đã thực hiện:** 3 layer RGBA có pigment/đường vẽ mới cho tóc sau đầu (969 px), da cổ khuất (545 px), shadow cổ áo (120 px). Tất cả dùng tọa độ trên đúng nguồn và clip vào vùng rough head matte; không hề đổi các pixel CANON nhìn thấy ở neutral.
- **Sai lầm được bắt bằng hình thay vì test tĩnh:** thử tô phủ tóc đến cả đỉnh đầu làm một **viền tím cực rõ khi nghiêng ±4°** mặc dù ảnh 0° nguyên vẹn và kiểm SHA PASS. Đã thu hẹp pigment vào vùng tóc nối cổ, so sánh bảng 5 góc trước/sau; đây là lý do cần visual QA động.
- **Chính sách:** backing kỹ thuật còn OpenCV inpaint, matte tóc còn thô. **Không được gọi đây là hand-painted master painter-grade** hoặc `rig_ready`. ORA mới chỉ là nghiên cứu có 3 layer vẽ bằng path + 1 layer mắt nhắm trống, không tự động lên CANON.
- **QA:** local 12/12 tests PASS có private image; [GitHub Actions](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/41075745315) SUCCESS 4 PASS / 8 SKIP, ORA merged nguyên pixel source, tamper rejection, layer alpha nằm trong matte và crown halo guard; kỹ thuật PASS không thay người dùng duyệt mỹ thuật hoặc test Android.
- **Bước tái sử dụng:** từ CP416 trở đi ưu tiên cải thiện nguồn ở độ phân giải phù hợp, phân tách tóc thật, vẽ kín gáy/cổ và mí mắt cùng pose; kiểm 0°/±2°/±4° trực quan trước khi tích hợp. Không lặp lại vòng cắt mask/đếm test mà không bổ sung asset art rõ rệt.
- **Bàn giao:** [CP415](art/LAM_THIEN_CP415_UNDERPAINT_PIGMENT_STUDY.md) · Library `/Thanh Van Ky/Development/CP415_Source_Locked_Underpaint_Study/`.

## 2026-10-30 — CP416 — Đầu tiên phải vẽ đúng pose, sau đó mới nói tới chớp mắt mượt

- **Nguồn:** chính xác CANON V2.1 SHA `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`, front crop 208×443; mắt gốc quá nhỏ (~13–15px) để tái tạo thành master HD chỉ bằng zoom.
- **Bước tiến art khác CP415:** vẽ **6 lớp pigment mới** (da, crease, mi cho mỗi biến thể nhắm) tạo hai trạng thái thực tế `RESTFUL` / `COMPLETE` trên **cùng front-pose**, thay vì tiếp tục cắt rough head mask. Atlas ba trạng thái có open frame pixel-exact. 12/12 private local source QA PASS; [GitHub Actions CP416](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/41078692596) SUCCESS 5 PASS / 7 SKIP; visual approval vẫn PENDING.
- **Sai lầm mỹ thuật phát hiện bằng mắt:** phiên thử đầu tiên có **2 dải mí và vệt ngang nhìn rất giả** dù mọi test ROI/hash đạt. Cải thiện bằng đặt màu da từ má của CANON tại row cố định, thu hẹp mask, bỏ bớt crease và làm mảnh mi. Bài học: **đếm pixel/CI không thay việc nhìn bản 1× lẫn phóng to**.
- **Không lẫn chức năng:** preview GIF 3 trạng thái chỉ là kiểm thử nhịp, không phải 15 keyframe eyelid motion, không chứng minh mượt, không gắn rig, không phải sprite production.
- **Quy tắc tiến độ:** sau khi có **ảnh thật** để so (không chỉ script/ROI), phải xin duyệt thẩm mỹ trước mọi animation in-between/Spine. Nếu ảnh 208×443 không đủ đẹp, cần minh họa lại đầu đúng pose ở độ phân giải cao *dựa đúng nhận diện CANON*, không tạo người khác hoặc phóng to giả HD.
- **Rào chắn:** lưu CANON private ngoài GitHub; `sprite_paths={}`, `visual_approval=PENDING_USER`, `production_release.status=blocked_pending_art`. Tóc, cổ, gáy phân lớp/underpaint họa sĩ còn thiếu, điện thoại Android thực chưa test.
- **Bàn giao:** [CP416 report](art/LAM_THIEN_CP416_SAME_POSE_EYELID_REVIEW.md) và ZIP tại Library `/Thanh Van Ky/Development/CP416_Same_Pose_Eyelid_Review/`.

## 2026-10-30 — CP417 — Giữ hàng mi thật, tránh vẽ chồng và kiểm APK cùng pose

- **Vấn đề CP416:** nét mi mới bị cộng thêm lên đường mi đậm vốn có của ảnh đứng, nên khi phóng to tạo cảm giác hai đường nhắm. Test ROI/hash vẫn PASS nhưng mỹ thuật chưa đạt.
- **Cách làm có tiến bộ:** giữ nguyên hàng pixel mi trên CANON (y50–51), di chuyển mask che đồng tử phía dưới qua 5 mức 0/25/50/75/100. Source CANON nguyên byte SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`; frame0 đúng source; mọi mức khác chỉ đổi hai ROI nhỏ, không mượn mặt biểu cảm khác pose.
- **Debug Android cụ thể:** thay vì tự coi GIF như chuyển động trong game, tạo `TVKCP417SamePoseBlinkActivity.kt` render atlas nguồn chính trên toàn thân, chu kỳ 2.4s, picker kiểm SHA và so từng pixel bên ngoài ROI; file private không nhúng APK công khai.
- **Kiểm chứng:** local 14/14 tests PASS có private CANON, bao gồm lash-row preservation, frame zero, ORA visible-source, atlas hash, gate không cấp quyền production. Public GitHub thiếu CANON cần để SKIP. APK CI chưa chứng minh chạy máy thật.
- **Giới hạn:** 5 frame ở sprite 208×443 chưa phải mượt HD; nếu người dùng thấy nhỏ/khó nhìn, hướng đi đúng là artist redraw head ở độ phân giải cao theo cùng nhận diện, không phải thêm vài màu mask. Mái tóc/gáy/cổ vẫn thiếu master đẹp thực sự; `visual_approval=PENDING_USER`, `sprite_paths={}`.
- **Tái sử dụng:** Khi có nét đường viền gốc đã tốt, ưu tiên **bảo toàn nét gốc** và vẽ phần bị che ở dưới, không sinh thêm nét trùng. Test QA kỹ thuật kết hợp nhìn 1× + 8× + xem chuyển động trong APK debug. [Báo cáo CP417](art/LAM_THIEN_CP417_SAME_POSE_SOURCE_LASH_BLINK.md).

- **Bằng chứng sau build CP417:** [public QA](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/41080652448) **5 PASS/9 private SKIP**; [Android build](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/41080652547) **SUCCESS**. APK đã kiểm tra có CP417 class, không chứa ảnh CANON trong assets, SHA256 `633d72189b1cef1f756865f816df296678539afd7d466c7667559ad820887680`. Không đồng nghĩa FPS/thiết bị thật/visual QA đã PASS.

## 2026-10-30 — CP418 — Review nhanh có giá trị hơn thêm vòng sửa mask

- **Vấn đề:** CP417 tạo được blink same-pose nhưng chỉ có GIF và tự chạy vòng lặp; người dùng khó dừng đúng frame để đánh giá, đặc biệt vì hai mắt nguyên bản chỉ 13–15px ngang.
- **Cải tiến cụ thể:** Android debug có nút 0/4–4/4 dừng đúng khung, chuyển toàn thân/cận mặt CANON và DRAFT đồng thời, vạch eye ROI; phóng NEAREST để xem pixel thật, không mô tả là bản HD.
- **Cải tiến hiệu năng/bảo mật:** thay ~370 nghìn lượt `getPixel` khi xác minh atlas bằng 2 lần `getPixels` vào `IntArray`; check frame0 đúng source, SHA-256 của CANON+atlas, không cho sửa ngoài 2 eye ROI. Chỉ bật điều khiển khi đã chọn hai ảnh hợp lệ.
- **QA:** 13/13 local tests trên private CANON và atlas, [public GitHub CI](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/41082343710) 7 PASS/6 private SKIP. Review board đã sửa lỗi che phần chân khi gắn crop zoom: phải luôn nhìn toàn thân trọn vẹn ở cùng lượt review.
- **Dữ liệu pixel có nghĩa giới hạn:** các khung 0/1/2/3/4 khác ảnh mở lần lượt 0/104/119/144/144 px, nhưng khung 3/4 khác nhau 46px. Không đánh giá vẻ tự nhiên, sắc nét hay FPS bằng số pixel.
- **Quy trình tái sử dụng:** ưu tiên cho người dùng duyệt 1× và zoom frame-by-frame trong app trước khi làm thêm paint; nếu art gốc không đủ resolution, cần source/painting mới đúng nhận diện chứ không tiếp tục sửa inpaint/mask. `visual_approval=PENDING_USER`, `spine_ready=false`, `android_device_verified=false`.
- **Tài liệu:** [CP418 Android Inspector](art/LAM_THIEN_CP418_ANDROID_FRAME_INSPECTOR.md).

- **Xác minh build CP418:** [Android debug workflow](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/41082343613) SUCCESS; APK 8.825.318 bytes SHA256 `29dcf40f65d05bb489331ef3b329eb026a854042f619448a0c479487fe3b59d9`, DEX có CP418, private CANON không nhúng trong APK. Chưa có kết quả kiểm thử thiết bị vật lý; không nâng `android_device_verified`.
