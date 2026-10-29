> **NGUỒN MỸ THUẬT LÂM THIỂN HIỆN HÀNH — CANON V2.1 ĐÃ CHỐT (2026-10-29)**: Chỉ dùng **file nguyên bản** `LAM_THIEN_CANON_V2_1_FINAL_20261029.png` (941×1672, 9:16, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`). Tài liệu [CANON V2.1](art/LAM_THIEN_CANON_V2_1_FINAL_2026_10_29.md) · [Model Card](art/LAM_THIEN_MODEL_CARD_V2_1_FINAL.json) · [Plan](art/LAM_THIEN_PLAN_AFTER_CANON_V2_1.md). **V2/CP337/CP338/CP339 là lịch sử, không được sử dụng làm mẫu chính.** Chỉ ảnh tham chiếu đã duyệt; layer/Spine/APK chưa hoàn thành.

# THANH VÂN KÝ — TÀI LIỆU MÔ TẢ DỰ ÁN

> **Mục đích:** Đây là nguồn thông tin chuẩn của dự án để tiếp tục công việc ở các thread khác mà không cần đọc lại toàn bộ lịch sử hội thoại. Khi có quyết định mới, hãy cập nhật tài liệu này trong cùng thay đổi/commit nếu phù hợp.
>
> **Quy tắc trạng thái:**  
> - **ĐÃ CHỐT**: người dùng đã xác nhận, không tự ý thay đổi.  
> - **ĐỊNH HƯỚNG**: mục tiêu mong muốn, có thể cần làm rõ chi tiết.  
> - **CHƯA CHỐT**: không tự coi là quyết định cuối cùng.  
> - **TRẠNG THÁI KỸ THUẬT**: phải kiểm tra trực tiếp repository/GitHub trước khi khẳng định vẫn đúng.

> **ẢNH NGOẠI HÌNH CANON LÂM THIỂN MỚI NHẤT (28/10/2026):** [V2 đã chốt](https://drive.google.com/file/d/1mEsyn2wMo-MVQqhtbmdUiFfO8AaYhzUR/view?usp=drivesdk) · mã `LT_CANON_BODY_REF_2026-10-28_V2` · SHA-256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711`. V2 **thay thế V1 về body/trang phục**, không thay quy tắc toàn game về pose/outfit/damage. [Hồ sơ canon V2](art/LAM_THIEN_CANON_BODY_V2_2026_10_28.md) và [plan thực hiện](art/LAM_THIEN_NEXT_TASKS_AFTER_CANON_V2.md). **Không tự đổi model theo poster cũ.**

**Cập nhật lần cuối:** 2026-10-28  
**Repository thử nghiệm:** https://github.com/luuduong99/thanh-van-ky-apk-test  
**Nhánh prototype:** `map-2d-prototype`  
**PR:** https://github.com/luuduong99/thanh-van-ky-apk-test/pull/1  
**GitHub Actions:** https://github.com/luuduong99/thanh-van-ky-apk-test/actions

---

## 1. Tầm nhìn và mục tiêu

- **ĐÃ CHỐT:** Xây dựng game/visual novel tiên hiệp 2D có thể chơi được trên điện thoại Android Xiaomi, ưu tiên tạo APK thử nghiệm và kiểm tra thực tế sớm.
- **ĐÃ CHỐT:** Ưu tiên bản 2D trước. Unity từng được cân nhắc cho hướng 3D trước đây, nhưng không phải lý do để tự chuyển dự án hiện tại sang 3D.
- **ĐÃ CHỐT:** Trọng tâm là sản phẩm có thể tương tác và chơi được, không chỉ tạo concept art hoặc tài liệu ý tưởng.
- **ĐỊNH HƯỚNG:** Có cốt truyện phân nhánh, hội thoại có lựa chọn, các quyết định tạo hậu quả, quan hệ nhân vật nhiều chiều, tu luyện, nhiệm vụ, mini-game và sưu tập trang phục.
- **ĐỊNH HƯỚNG:** Phong cách tiên hiệp đẹp, giàu không khí và có sức hút; có thể lấy cảm hứng ở mức phong cách tổng quát từ *Above the Immortality Realm*, nhưng thiết kế nhân vật, hình ảnh và nội dung phải nguyên bản.

## 2. Nền tảng và nguyên tắc kỹ thuật

- **ĐÃ CHỐT:** Ưu tiên APK Android có thể cài và chạy trên Xiaomi.
- **ĐÃ CHỐT:** Người dùng muốn build từ xa/cloud, không muốn phải tự cài bộ công cụ phát triển trên máy cá nhân nếu có thể tránh.
- **TRẠNG THÁI KỸ THUẬT tại 2026-10-23:** Repository hiện là dự án **Android native Kotlin**, không phải dự án Ren'Py.
  - Application ID/namespace: `vn.thanhvanky.prototype`
  - File màn hình chính: `app/src/main/java/vn/thanhvanky/prototype/MainActivity.kt`
  - Cấu hình Gradle Kotlin DSL; thông tin đã thấy trước đó: compileSdk 35, minSdk 23, Java 17.
- **ĐÃ CHỐT:** Tiếp tục trên nền tảng Kotlin Android hiện tại để thử nghiệm bản đồ; không tự đổi engine/framework. Nếu có bằng chứng kỹ thuật cho thấy cần chuyển engine, hãy giải thích ưu/nhược điểm và xin thống nhất trước khi thay đổi.
- Không tuyên bố build APK thành công nếu chưa có kết quả GitHub Actions hoặc APK thực tế xác nhận.
- Không merge PR, đổi nhánh chính hoặc xóa/thay thế công việc đã có nếu chưa được yêu cầu.
- Ưu tiên thay đổi nhỏ, kiểm tra được, có thể chạy thử; không làm lại kiến trúc rộng chỉ để tiện cho một tính năng.

## 3. Bản đồ 2D và cách di chuyển

### 3.1 Thiết kế đã thống nhất

- **ĐÃ CHỐT:** Bản đồ nhiều tầng:
  1. Bản đồ thế giới.
  2. Bản đồ khu vực/tông môn.
  3. Cảnh địa điểm cụ thể.
- **ĐÃ CHỐT:** Người chơi **chạm vào địa điểm trên bản đồ để di chuyển**; không dùng joystick và không yêu cầu điều khiển nhân vật chạy quanh bản đồ.
- **ĐÃ CHỐT:** Khi vào một địa điểm, hiển thị nền minh họa 2D. Người chơi chạm NPC, công trình hoặc vật thể/điểm tương tác để xem hội thoại hoặc kích hoạt hành động.
- **ĐÃ CHỐT:** Có thể quay lại bản đồ và không làm mất tiến trình đã đạt được.
- **ĐÃ CHỐT:** Địa điểm có thể bị khóa/mở theo cốt truyện, nhiệm vụ hoặc điều kiện tu luyện.
- **ĐỊNH HƯỚNG:** Giao diện có thể gồm bản đồ, nhân vật, túi đồ, nhiệm vụ và các mục phù hợp khác; không cần nhồi tất cả vào prototype đầu tiên.

### 3.2 Prototype bản đồ đầu tiên

Phạm vi thử nghiệm tối thiểu:
- Một bản đồ tông môn.
- Sân chính.
- Khoảng 2–3 NPC.
- Một công trình có thể tương tác.
- Ít nhất một địa điểm liên kết.
- Luồng bắt buộc: **bản đồ → vào địa điểm → chạm NPC/công trình → quay lại bản đồ**.

**Tiêu chí kiểm thử:** thao tác chạm dễ hiểu trên màn hình điện thoại, chuyển cảnh hoạt động, nút quay lại hoạt động, trạng thái mở/khóa hiển thị rõ ràng và ứng dụng không bị crash.

### 3.3 Prototype đã được ghi nhận trên GitHub

- Nhánh: `map-2d-prototype`.
- `MainActivity.kt` được thay bằng prototype Kotlin Canvas vẽ bản đồ 2D cách điệu và các vùng chạm.
- Các điểm hiện có trong prototype theo thay đổi đã thực hiện: Thanh Vân Tông, Trấn Thanh Hà, Rừng Trúc; chạm NPC/công trình để hiện Toast mẫu; nút quay lại bản đồ; Bí cảnh ở trạng thái khóa.
- Hình vẽ hiện tại là hình vẽ bằng code để chứng minh luồng tương tác, **chưa phải tranh nền hoặc art cuối cùng**.
- PR #1 là PR nháp, nhánh `map-2d-prototype` → `main`: https://github.com/luuduong99/thanh-van-ky-apk-test/pull/1
- Workflow build đã được sửa để chạy khi push lên `main`, `map-2d-prototype` hoặc chạy thủ công. **Kết quả build chưa được xác nhận trong tài liệu này.** Cần mở Actions và đọc kết quả mới nhất.
- Nếu workflow thành công, artifact dự kiến tên `thanh-van-ky-debug-apk`, APK nằm tại `app/build/outputs/apk/debug/app-debug.apk`. Chỉ báo thành công sau khi xác nhận artifact thực sự được tạo.

## 4. Nhân vật và cốt truyện

- **ĐỊNH HƯỚNG:** Một nhân vật nam chính.
- **ĐỊNH HƯỚNG:** Khoảng 10 nhân vật nữ chính/đối tượng tình cảm, cộng thêm nhân vật phụ. Con số này là quy mô mục tiêu, chưa phải danh sách nhân vật đã chốt tên hoặc hồ sơ.
- **ĐỊNH HƯỚNG:** Hội thoại phân nhánh; lựa chọn ảnh hưởng đến quan hệ và diễn biến truyện.
- **ĐỊNH HƯỚNG:** Hệ thống quan hệ nhiều chiều, không chỉ một thanh điểm duy nhất; chi tiết các chỉ số và quy tắc chưa chốt.
- **ĐÃ CHỐT:** Tất cả nhân vật trong tuyến tình cảm đều từ **18 tuổi trở lên theo tuổi thực**. Nữ chính không bị giới hạn ở tuổi đời ngắn: trong bối cảnh tu tiên, có thể có nhân vật sống vài trăm hoặc vài nghìn năm nhưng vẫn giữ ngoại hình trẻ trung do tu vi, công pháp hoặc đặc tính chủng tộc.
- **ĐÃ CHỐT:** Tuổi thực, tuổi biểu hiện bên ngoài và tuổi tu luyện phải là các thông tin riêng trong hồ sơ nhân vật; không suy ra tuổi thực chỉ từ ngoại hình.
- **ĐÃ CHỐT:** Mức thể hiện thân mật kết hợp lãng mạn/gợi cảm với cách **chuyển cảnh (fade-to-black)** khi quan hệ tình dục diễn ra; lựa chọn cách thể hiện tùy tình huống và tuyến nhân vật.
- **ĐỊNH HƯỚNG:** Tính cách đa dạng; chỉ một vài nhân vật có thể mang nét tsundere, không áp dụng cho toàn bộ dàn nữ chính.
- **ĐỊNH HƯỚNG:** Xem nội dung người trưởng thành, sức hút nhân vật và tiến triển quan hệ là các yếu tố cần được chú ý khi thiết kế nhân vật, hội thoại, sự kiện và tuyến truyện. Các tương tác tình dục phải có sự đồng thuận; có thể khai thác xung đột, chiếm hữu hoặc đối đầu trong cốt truyện mà không coi sự phản kháng là đồng thuận.
- Chưa có danh sách hồ sơ nhân vật đầy đủ được xác nhận trong tài liệu này. Không tự bịa tên, quá khứ, tính cách cốt lõi hoặc quan hệ gia tộc rồi xem đó là canon. Đề xuất mới cần được người dùng duyệt trước khi chuyển sang phần **ĐÃ CHỐT**.

## 5. Phong cách hình ảnh và thiết kế nhân vật

- **ĐỊNH HƯỚNG:** Mỹ thuật tiên hiệp/fantasy 2D, đẹp, giàu chi tiết và nhất quán giữa bản đồ, chân dung, cảnh hội thoại và các phân cảnh.
- **ĐỊNH HƯỚNG:** Khoảng 7/10 nhân vật nữ có trang phục tiên hiệp quyến rũ/hở hơn; khoảng 3/10 kín đáo hơn. Đây là tỷ lệ phong cách tổng thể, không phải hồ sơ chi tiết cho từng nhân vật.
- **ĐỊNH HƯỚNG:** Một số nhân vật có dáng đồng hồ cát/vòng một lớn, các nhân vật còn lại có vóc dáng đa dạng; tránh để tất cả nhân vật giống hệt nhau.
- **ĐÃ CHỐT:** Tất cả nhân vật trong tuyến tình cảm đều từ **18 tuổi trở lên theo tuổi thực**. Nhân vật có thể sống hàng trăm hoặc hàng nghìn năm và vẫn giữ ngoại hình trẻ trung trong bối cảnh tu tiên.
- **ĐỊNH HƯỚNG:** Có thể có nhân vật trưởng thành có vóc dáng thấp bé/nhỏ nhắn, gương mặt dễ thương và vòng một rất đầy đặn. Nếu nhân vật tham gia tuyến thân mật trưởng thành, thiết kế cần thể hiện rõ họ là người trưởng thành qua đường nét khuôn mặt, tỷ lệ cơ thể, khí chất và cách tạo hình; tránh tạo hình mang đặc điểm cơ thể trẻ em rồi tình dục hóa.
- **ĐÃ CHỐT:** Định hướng cảnh thân mật là kết hợp lãng mạn/gợi cảm với chuyển cảnh khi quan hệ tình dục diễn ra, tùy tình huống; không mô tả hành vi tình dục trực diện, chi tiết và cần có sự đồng thuận.
- **ĐỊNH HƯỚNG:** Cần chú trọng sức hút nhân vật trưởng thành qua thiết kế hình thể, biểu cảm, ngôn ngữ cơ thể, trang phục, ánh sáng, góc máy và tiến triển quan hệ; giữ khác biệt về ngoại hình, tính cách và ranh giới của từng nhân vật.
- Tạo thiết kế nguyên bản; hình tham khảo chỉ định hướng phong cách, không sao chép nhân vật/tác phẩm có bản quyền.

## 5.1 Nhân vật nữ chính — định hướng đã chốt ngày 2026-10-23

Các mô tả dưới đây là quyết định tạo hình và vai trò đã được người dùng xác nhận. Những chi tiết chưa nêu rõ (ví dụ quá khứ hoàn chỉnh, chỉ số gameplay, cảnh giới cuối cùng) vẫn có thể tiếp tục phát triển sau.

### Tô Nguyệt Ly — người đồng hành từ đầu

- **TRẠNG THÁI:** ĐÃ CHỐT định hướng nhân vật và mẫu mỹ thuật tham chiếu.
- Vai trò: nữ chính đồng hành cùng nam chính ngay từ đầu; tạo cảm giác thân thuộc, là người để trò chuyện, khám phá, chiến đấu và phát triển quan hệ.
- Tính cách: dịu dàng, trung thành, chu đáo, chân thành; chủ động quan tâm và thể hiện tình cảm; có thể hơi ghen nhưng không cố tình tạo hiểu lầm để kéo dài cốt truyện.
- Ngoại hình/mỹ thuật: lấy **ảnh AI Tô Nguyệt Ly đã tạo trong cuộc trò chuyện ngày 2026-10-23** làm mẫu tham chiếu ưu tiên. Tóc bạc/trắng, tông trắng-xanh nhạt phối vàng, trang sức hoa tinh xảo, gương mặt dịu dàng.
- Vóc dáng: rất đầy đặn, vòng một nổi bật và đường cong rõ theo mẫu người dùng yêu thích; thiết kế nhất quán với ảnh tham chiếu.
- Trang phục: tiên hiệp quyến rũ, có thể hở táo bạo; vẫn giữ thẩm mỹ fantasy và phụ kiện tinh xảo.
- Tuổi: hồ sơ trước đây đề xuất tuổi thực 126 và ngoại hình khoảng 22; **các con số tuổi này chưa được người dùng xác nhận riêng, nên vẫn là đề xuất, không phải dữ kiện canon**.

### Lạc Huyền Sương — nữ cường giả Ma đạo chiếm hữu

- **TRẠNG THÁI:** ĐÃ CHỐT định hướng tạo hình, tính cách cốt lõi và vai trò; các chi tiết tiểu sử/cảnh giới vẫn là đề xuất.
- Vai trò: nữ cường giả Ma đạo, địa vị cao, là tuyến tình cảm có xung đột và sức hút mạnh.
- Tính cách: chiếm hữu mạnh, kiêu ngạo, quyến rũ, có khí chất áp đảo; không bắt buộc luôn lạnh lùng, có thể chủ động trêu chọc và thể hiện ham muốn tình cảm.
- Ngoại hình/mỹ thuật: tóc đen dài, điểm đỏ sẫm; trang phục đen-đỏ, phụ kiện ma đạo và phong thái tự tin, nguy hiểm. Phong cách lấy cảm hứng tổng quát từ hình tham khảo do người dùng cung cấp, không sao chép nguyên xi nhân vật có sẵn.
- Vóc dáng: **dùng cùng chuẩn vóc dáng rất đầy đặn, vòng một nổi bật và đường cong rõ như mẫu Tô Nguyệt Ly**; không dùng lại kiểu tạo hình ban đầu mà người dùng không thích.
- Trang phục: hở táo bạo hơn, cổ áo sâu và đường cắt tôn dáng, nhưng vẫn giữ nhận diện fantasy/tiên hiệp.
- Tên, thân phận Ma đạo là định hướng được chốt; tuổi thực 428, ngoại hình khoảng 25, Huyền Sương Điện chủ và tu vi Nguyên Anh hậu kỳ từng là đề xuất của trợ lý, chưa được xác nhận riêng nên **không xem các chi tiết đó là canon đã chốt**.

### Nhân vật nữ hồ ly — ý tưởng cần phát triển sau

- **TRẠNG THÁI:** ĐỊNH HƯỚNG, chưa chốt hồ sơ cụ thể.
- Người dùng muốn có một nhân vật hồ ly, lấy cảm hứng phong cách fantasy/anime hiện đại như *Wuthering Waves*, nhưng thiết kế phải nguyên bản.
- Có thể có tai hồ ly và đuôi lớn, trang phục fantasy quyến rũ và vóc dáng theo chuẩn tham chiếu Tô Nguyệt Ly; cần tạo diện mạo, tính cách và vai trò riêng, không trùng Lạc Huyền Sương.



### Chuẩn tham chiếu trang phục — ĐÃ CHỐT ngày 2026-10-23

Người dùng đã cung cấp hai ảnh tham khảo để thống nhất **phong cách trang phục**, không phải để thay đổi hồ sơ hay tạo hình cốt lõi của các nhân vật đã chốt.

- **Phong cách tổng thể:** Tiên hiệp/fantasy anime hiện đại, cách điệu tự do; không bắt buộc bám sát Hán phục truyền thống.
- **Phom dáng:** Có thể dùng cổ áo sâu, hở vai/lưng, tay áo rời, tà áo xẻ, vải quấn, các lớp lụa/voan buông mềm và đường cắt tôn dáng, tùy hình tượng từng nhân vật.
- **Mức độ quyến rũ:** Có thể táo bạo và gợi cảm với các nhân vật trưởng thành phù hợp; không ép tất cả nhân vật mặc kín đáo hoặc cùng một kiểu.
- **Màu sắc:** Phối màu rõ ràng, tương phản và phù hợp nhận diện riêng của nhân vật. Tham chiếu gồm trắng/xanh nhạt/viền vàng và đen/đỏ/điểm vàng, nhưng không giới hạn toàn bộ dàn nhân vật vào hai bảng màu này.
- **Phụ kiện:** Có thể dùng trâm cài, trang sức, dây buộc, hoa văn hoặc chi tiết fantasy; ưu tiên một số điểm nhấn dễ nhận diện thay vì nhồi quá nhiều chi tiết nhỏ.
- **Độ phức tạp:** Có thể đơn giản hóa trang phục so với ảnh tham khảo nếu điều đó giúp tạo ảnh nhất quán hơn. Ưu tiên giữ phom dáng, màu sắc, chất liệu và chi tiết nhận diện; không cần sao chép mọi đường thêu/phụ kiện.
- **Khác biệt giữa nhân vật:** Mỗi nhân vật có thiết kế trang phục riêng phù hợp với hồ sơ đã chốt. Không chỉ thay màu trên cùng một bộ trang phục.
- **Nguyên tắc sử dụng ảnh:** Hai ảnh người dùng cung cấp là tham chiếu cho ngôn ngữ thiết kế trang phục. Ảnh AI Tô Nguyệt Ly đã tạo trước đó vẫn là tham chiếu ưu tiên riêng cho tỷ lệ cơ thể và mức độ quyến rũ mà người dùng yêu thích. Không coi ảnh minh họa tìm thêm trên mạng trong câu trả lời của trợ lý là ảnh gốc hoặc asset chính thức của game.
- **Phạm vi quyết định:** Đây là quy chuẩn thẩm mỹ trang phục dùng cho ba nhân vật mẫu và các nhân vật phát triển sau này; không tự ý sửa tên, tính cách, vai trò hoặc các chi tiết nhân vật đã chốt. Các mẫu hình vẫn cần được tạo/chuẩn bị thành asset riêng trước khi tích hợp vào game.

### Ảnh tham chiếu ba nữ chính — người dùng cung cấp lại ngày 2026-10-23

- **ĐÃ CHỐT:** Người dùng đã tải lại ảnh triptych (1536 × 1024 px) gồm ba nhân vật, dùng làm **mẫu hình ảnh ưu tiên** cho các bản thử nghiệm. Ảnh được đính kèm trực tiếp trong cuộc trò chuyện dự án ngày 2026-10-23, tên file khi tải lên: `image.png` (file đính kèm, không phải URL blob bền vững).
- **Bên trái:** **Tô Nguyệt Ly**, tóc bạc/trắng, mắt xanh nhạt, trang phục trắng/xanh nhạt/viền vàng, hoa cài tóc; đây là hình cần dùng cho màn tương tác thử với Tô Nguyệt Ly.
- **Ở giữa:** **Lạc Huyền Sương**, tóc đen, phục sức đen/đỏ/vàng.
- **Bên phải:** **Nữ hồ ly**, tóc hồng, tai hồ ly, trang phục hồng/trắng.
- **Lưu ý kỹ thuật:** Đây là **một ảnh ghép ba nhân vật**, chưa phải ba sprite độc lập hoặc bộ ảnh phân lớp để animate. Cần tách ảnh và xử lý asset trước khi đưa vào APK.
- **Trạng thái lưu trữ:** Ảnh đã được người dùng tải lên cuộc trò chuyện; **đã được lưu trong repository tại `app/src/main/assets/characters/heroines_reference.png`**. Mục ghi chú này giúp nhận diện và không phải hỏi lại mẫu thiết kế, nhưng nếu cần lấy đúng bytes cho build tự động thì vẫn phải có asset ảnh được lưu vào repo hoặc kho tài nguyên ổn định. Không dùng đường dẫn `blob:https://chatgpt.com/...` làm URL asset.

### Chuẩn mỹ thuật chung đã chốt

- Dùng ảnh AI Tô Nguyệt Ly được tạo ngày 2026-10-23 làm **mẫu tham chiếu ưu tiên** cho vóc dáng và mức độ quyến rũ mà người dùng yêu thích. Không thay bằng ảnh tìm từ mạng làm mẫu chính.
- Với nhóm nữ chính hở bạo: vòng một rất đầy đặn, đường cong nổi bật, trang phục táo bạo hơn (ví dụ cổ khoét sâu, để lộ vai/lưng, xẻ tà, lớp lụa/voan phủ ngoài) theo phong cách anime tiên hiệp.
- Mục tiêu sơ bộ: khoảng 7/10 nữ chính quyến rũ/hở bạo và 3/10 kín đáo hơn; đây là tỷ lệ định hướng chung, có thể phân bổ khi chốt toàn bộ dàn nhân vật.
- Mỗi nhân vật phải có khuôn mặt, tóc, bảng màu, trang phục, vóc dáng/khí chất và tính cách đủ khác biệt; không chỉ đổi màu của cùng một mẫu.
- Ảnh tham khảo từ người dùng dùng để xác định gu thẩm mỹ; ảnh AI tạo riêng dùng làm mẫu thiết kế. Khi tạo ảnh mới, nên dùng trực tiếp ảnh tham chiếu được tải lên lại nếu ảnh cũ/đường dẫn blob không còn truy cập được.
- Tất cả nhân vật trong tuyến tình cảm là người trưởng thành, từ 18 tuổi trở lên theo tuổi thực; tuổi thực và ngoại hình có thể khác nhau trong bối cảnh tu tiên.
- Các quyết định trên được chốt cho **định hướng nhân vật trong hội thoại và tài liệu dự án**, không đồng nghĩa các ảnh đã trở thành asset trong game. Cần tạo/chuẩn bị asset riêng trước khi tích hợp vào Android.

## 6. Trang phục và sưu tập

- **ĐỊNH HƯỚNG:** Có trang phục mặc định, trang phục mua bằng tiền tệ trong game, phần thưởng nhiệm vụ, sự kiện, hẹn hò, điểm quan hệ và thành tựu.
- **ĐỊNH HƯỚNG:** Có thể có trang phục cao cấp/sự kiện; tránh cơ chế mua trùng một bộ trang phục đã sở hữu.
- **ĐỊNH HƯỚNG:** Trang phục đã chọn cần đồng bộ với hình nhân vật trong cảnh, hội thoại và hoạt ảnh liên quan; không chỉ thay đổi một biểu tượng trong túi đồ.
- Chưa chốt danh sách trang phục, giá, độ hiếm, tiền tệ hoặc cách mở khóa cho từng bộ.

## 7. Gameplay và hệ thống dự kiến

Các hệ thống mong muốn, cần ưu tiên theo từng giai đoạn:
- Hội thoại và lựa chọn phân nhánh.
- Nhiệm vụ và cờ trạng thái cốt truyện.
- Quan hệ/độ thân thiết với nhân vật.
- Tu luyện và điều kiện mở khóa khu vực.
- Mini-game cho tu luyện, trận pháp hoặc tặng quà.
- Túi đồ và vật phẩm.
- Sưu tập/trang phục.
- Biểu cảm và hoạt ảnh nhân vật.
- Bản đồ tương tác, điểm nóng và các địa điểm có thể khám phá.

Không triển khai tất cả cùng lúc. Ưu tiên hoàn thiện một lát cắt nhỏ nhưng chơi được, sau đó mở rộng.

## 8. Lộ trình ưu tiên

1. Kiểm tra trạng thái nhánh `map-2d-prototype`, PR #1 và GitHub Actions.
2. Sửa lỗi build dựa trên log thực tế nếu có; lấy APK từ artifact khi build đã được xác nhận.
3. Cài và thử APK trên Xiaomi; ghi nhận lỗi thao tác, hiển thị và crash.
4. Hoàn thiện luồng bản đồ → địa điểm → tương tác → quay lại.
5. Chốt phong cách và danh sách nhân vật chính; xây hồ sơ từng nhân vật sau khi người dùng duyệt.
6. Thay hình vẽ placeholder bằng asset 2D nguyên bản theo từng phần.
7. Thêm lưu tiến trình, nhiệm vụ và điều kiện mở khóa.
8. Mở rộng hội thoại, quan hệ, tu luyện và trang phục.

## 9. Quy tắc quản lý quyết định

### Quy tắc ưu tiên thiết kế mới nhất đã được duyệt — ĐÃ CHỐT (2026-10-28)

**THAM CHIẾU HIỆN HÀNH — Lâm Thiển (đã chốt 2026-10-28):** [mở bảng thiết kế đã duyệt](https://drive.google.com/file/d/10jKNq-VL62sv1gez5PHlVT9QKyJp_Cvd/view?usp=drivesdk) · [hồ sơ chuẩn](art/LAM_THIEN_APPROVED_REFERENCE_2026_10_28.md) · [quy chuẩn mỹ thuật các nhân vật sau](art/CHARACTER_ART_DIRECTION_REFERENCE.md). Đây là **ảnh chuẩn thay thế bản preview CP318/319**, không thay thế quyết định riêng về pose/hệ thống kỹ thuật; chỉ thay khi người dùng duyệt bản mới hơn.

1. **Nguồn chuẩn triển khai (canon):** Với mỗi nhân vật, trang phục, tư thế, UI, cảnh và asset, **luôn dùng phiên bản mới nhất đã được người dùng xác nhận/chốt** làm cơ sở tạo ảnh, sửa art, phân lớp, rig, hoạt ảnh, tích hợp APK và preview. Khi một phần (ví dụ hông/trang phục) được duyệt mới, chỉ thay phần đó; giữ các quyết định đã chốt khác (gương mặt, màu sắc, tỷ lệ…) nếu chưa bị thay thế.
2. **Không quay về thiết kế cũ:** Bản cũ, PNG phẳng, proxy, fixture test, concept và bản chưa duyệt chỉ được dùng để tham khảo lịch sử/kỹ thuật, **không dùng làm mẫu sản xuất hoặc ảnh preview chính**. Ghi nhãn `DEPRECATED / HISTORICAL / TECHNICAL PROXY` rõ ràng; không xóa dữ liệu gốc.
3. **Phân biệt trạng thái:** Thiết kế mới được đề xuất hoặc mới tạo preview **chưa tự động thành bản chốt**. Chỉ sau khi người dùng xác nhận mới thay bản chuẩn. Nếu cùng lúc có nhiều bản chưa rõ trạng thái hoặc có mâu thuẫn không được giải quyết, đối chiếu lịch sử và hỏi xác nhận, không tự chọn tùy tiện.
4. **Đồng bộ đầu ra:** Sau mỗi lần chốt, cập nhật `docs/PROJECT_SPEC.md`, tài liệu nhân vật và bảng tên/đường dẫn asset chuẩn nếu có; mọi lần dựng mới phải đối chiếu với bản chốt trước khi bắt đầu. Không được lấy sự trùng khớp pixel với một proxy cũ làm bằng chứng thiết kế mới đã đúng.
5. **Trường hợp thiếu asset gốc mới nhất:** Có thể làm việc bằng một bản phục dựng/tạm để thử kỹ thuật nhưng **phải đánh dấu không phải bản chuẩn**; ưu tiên tạo lại art theo thiết kế mới được chốt, không biến thiết kế cũ thành sản phẩm cuối.

- Tài liệu này là nguồn tham chiếu chuẩn; thread cũ chỉ là lịch sử bổ sung.
- Sau mỗi quyết định được người dùng chốt, cập nhật mục liên quan, ngày cập nhật và trạng thái.
- Không nâng một ý tưởng do trợ lý đề xuất thành quyết định đã chốt nếu người dùng chưa đồng ý.
- Nếu quyết định mới mâu thuẫn với quyết định cũ, nêu rõ mâu thuẫn và hỏi xác nhận; sau khi xác nhận, cập nhật tài liệu và ghi quyết định cũ vào lịch sử thay đổi.
- Giữ riêng thông tin **đã xác nhận**, **định hướng**, **chưa chốt** và **trạng thái kỹ thuật**.
- Khi bắt đầu thread mới, đọc file này trước; sau đó kiểm tra trạng thái GitHub hiện tại nếu công việc liên quan đến code/build. Không dựa vào mô tả trạng thái kỹ thuật cũ nếu cần thông tin mới nhất.

## 10. Lịch sử cập nhật

- **2026-10-28 (chốt hình mới):** Người dùng duyệt bảng tạo hình Lâm Thiển mới nhất; lưu ảnh nguyên gốc, checksum và link trong mục 20; dùng làm chuẩn tạo hình Lâm Thiển và mẫu trình bày mỹ thuật cho nhân vật khác, không sao chép hình thể cá nhân.
- **2026-10-28:** Người dùng chốt quy tắc dự án: luôn dùng **thiết kế mới nhất đã duyệt** cho việc triển khai và preview; mẫu cũ/proxy chỉ lưu làm tài liệu đối chiếu kỹ thuật, không tự lấy làm bản chính. Áp dụng cho mọi asset và giữ lại các quyết định thành phần không thay đổi.
- **2026-10-23:** Tạo tài liệu tổng hợp đầu tiên từ các yêu cầu đã thống nhất và trạng thái repository được ghi nhận. Ghi rõ bản đồ 2D, cách di chuyển bằng chạm, phạm vi prototype, định hướng nhân vật/trang phục, nguyên tắc kỹ thuật và lộ trình APK. Trạng thái build vẫn cần kiểm tra trực tiếp.
- **2026-10-23:** Người dùng xác nhận định hướng nội dung người trưởng thành: mọi nhân vật trong tuyến tình cảm từ 18 tuổi trở lên theo tuổi thực; cảnh thân mật kết hợp lãng mạn và chuyển cảnh khi quan hệ tình dục diễn ra, tùy tình huống. Hồ sơ nhân vật và chi tiết hệ thống quan hệ vẫn là định hướng/chưa chốt.
- **2026-10-23:** Người dùng xác nhận bối cảnh tu tiên cho phép nữ chính có tuổi đời hàng trăm hoặc hàng nghìn năm nhưng vẫn giữ ngoại hình trẻ trung. Bổ sung hướng tạo hình nhân vật trưởng thành có vóc dáng nhỏ nhắn, dễ thương và có thể có vòng một rất đầy đặn; cần thể hiện rõ đặc điểm trưởng thành trong thiết kế.

- **2026-10-23:** Người dùng chốt định hướng nhân vật Tô Nguyệt Ly (đồng hành từ đầu, dịu dàng/trung thành; ảnh AI đã tạo là mẫu mỹ thuật ưu tiên) và Lạc Huyền Sương (Ma đạo, chiếm hữu, tóc đen/đen-đỏ, trang phục hở táo bạo; vóc dáng theo mẫu Tô Nguyệt Ly). Ghi nhận thêm ý tưởng nữ hồ ly lấy cảm hứng phong cách fantasy/anime hiện đại như Wuthering Waves nhưng phải có thiết kế nguyên bản. Phân biệt rõ các chi tiết tiểu sử/cảnh giới/tuổi từng do trợ lý đề xuất nhưng chưa được người dùng xác nhận riêng.

- **2026-10-23:** Người dùng xác nhận hai ảnh vừa cung cấp là tham chiếu **về trang phục בלבד**, không thay đổi các hồ sơ nhân vật đã chốt. Chốt ngôn ngữ trang phục tiên hiệp/fantasy anime hiện đại, có thể hở vai/cổ/tà áo và tôn dáng tùy nhân vật; phối màu rõ, phụ kiện vừa đủ và được phép giản lược chi tiết để tăng tính nhất quán khi tạo ảnh. Ảnh AI Tô Nguyệt Ly vẫn là tham chiếu ưu tiên cho tỷ lệ cơ thể/mức độ quyến rũ; không coi ảnh minh họa bổ sung do trợ lý tìm là asset chính thức.

- **2026-10-23:** Người dùng tải lại ảnh ghép ba nữ chính (Tô Nguyệt Ly trái, Lạc Huyền Sương giữa, nữ hồ ly phải) để dùng làm tham chiếu chuẩn. Ghi rõ ảnh được đính kèm trong hội thoại, chưa được lưu dưới dạng asset GitHub.


## 11. Ảnh nhân vật trong APK — 2026-10-23

- **ĐÃ CHỐT:** Dùng đúng ảnh Tô Nguyệt Ly bên trái ảnh ghép, không thay bằng hình Canvas. File gốc: `app/src/main/assets/characters/heroines_reference.png` (1536 × 1024). Ứng dụng giải mã vùng bên trái 512 × 1024 khi chạy; không sửa ảnh nguồn.
- **ĐÃ CHỐT:** Người dùng chọn ảnh nam chính “Lãng khách dưới trăng hoa rơi”: nam trưởng thành, không quá gầy, hơi phong trần/trải đời, không phải khỏa thân. Asset: `app/src/main/assets/characters/main_portrait.png`.
- Màn Tô Nguyệt Ly và thử chuyển động dùng ảnh đã chọn; màn hẹn hò hiển thị cả hai chân dung. Ảnh được đóng gói trong APK, không cần mạng để tải.
- **GIỚI HẠN BẢN THỬ:** Hai ảnh tĩnh có nền riêng; màn hẹn hò dùng bố cục hai chân dung, không phải tranh cặp đôi mới. Chuyển động chỉ dịch chuyển nhẹ ảnh tĩnh. Các hành động nắm tay/ôm/hôn nhẹ/vuốt tóc hiện phản hồi bằng hội thoại/biểu tượng, chưa có hoạt ảnh tư thế tương ứng. Chưa có ảnh trang phục khác nên không giả lập đổi trang phục bằng đổi màu.
- **KIỂM THỬ:** Cần xác nhận build GitHub Actions của commit mới và thử trên Xiaomi; chưa xác nhận chuyển động nhân vật phân lớp.

- **2026-10-23 (lịch sử):** Người dùng chốt ảnh nam chính và yêu cầu tích hợp ảnh thật đã chọn của cả hai nhân vật vào APK thử. Lưu asset cố định trong source để các lần sau không phải yêu cầu gửi lại ảnh.


## 12. Bổ sung đã thống nhất — tương tác, tạo hình và trang phục (2026-10-23)

### 12.1 Ba mẫu nhân vật đã được duyệt

- **ĐÃ CHỐT:** Người dùng xác nhận cả ba mẫu trong ảnh `app/src/main/assets/characters/heroines_reference.png` đều đúng gu: Tô Nguyệt Ly, Lạc Huyền Sương và nữ hồ ly. Giữ thiết kế khuôn mặt, tóc, vóc dáng, bảng màu và trang phục của ba mẫu làm chuẩn; khi tạo biểu cảm, tư thế hoặc hoạt ảnh mới phải bám đúng mẫu.
- Xác nhận này chốt **mẫu tạo hình nữ hồ ly**, thay cho trạng thái tạo hình mới chỉ là ý tưởng ở mục 5.1. Tên riêng, tính cách cốt lõi, tiểu sử, tuổi cụ thể và vai trò truyện chưa được xác nhận vẫn là **CHƯA CHỐT**.
- Không coi việc duyệt ngoại hình là duyệt toàn bộ tiểu sử hoặc mọi ý tưởng từng được đề xuất.

### 12.2 Tham khảo cho những nhân vật tiếp theo

- **ĐÃ CHỐT hướng thực hiện:** Các nhân vật khác phát triển theo ngôn ngữ tạo hình, trang phục và cách thể hiện tương tác tham khảo từ *Above the Immortality Realm*, kết hợp chuẩn thẩm mỹ của ba mẫu đã duyệt. Người dùng cho phép chủ động phát triển thiết kế theo hướng này.
- Nguồn đã xem: bản game `Above_the_Immortality_Realm_v0.7.0-VH by VoThien` trên máy người dùng. Đã trích đọc kịch bản và bảng hội thoại tiếng Việt, bước đầu xem kỹ chương 1–2; đã khảo sát cấu trúc kịch bản các chương 1–9. Chưa trực tiếp chơi hoặc kiểm tra toàn bộ hoạt ảnh của game.
- Tham khảo cách phân biệt khí chất, biểu cảm, trang phục và thái độ giữa từng nhân vật. Thiết kế TVK phải nguyên bản; không đưa trực tiếp tranh, sprite, hội thoại hay hoạt ảnh trích từ game tham khảo vào APK.
- Mỗi nhân vật mới cần hồ sơ tạo hình gồm: gương mặt, vóc dáng trưởng thành, màu/kiểu tóc, mắt, bảng màu chủ đạo, dáng đứng, phụ kiện nhận diện, trang phục mặc định và bộ biểu cảm. Tránh dùng cùng một khuôn mặt hoặc chỉ đổi màu trang phục.
- Giữ phong cách fantasy/anime tiên hiệp hiện đại, đường cong và mức độ quyến rũ theo ba mẫu đã duyệt; phân bổ khác biệt theo tính cách, vai trò và định hướng khoảng 7/10 táo bạo, 3/10 kín đáo hơn đã ghi.
- Có thể phát triển các hướng như kiếm tu thanh nhã, y tu dịu dàng, nữ cường giả uy nghi hoặc nữ tu hoạt bát. Đây là **ví dụ thiết kế**, chưa phải danh sách nhân vật, tên hoặc quan hệ đã chốt.

### 12.3 Quy chuẩn trang phục để triển khai

- **ĐÃ CHỐT hướng mỹ thuật:** Trang phục tôn dáng, có nhận diện tiên hiệp/fantasy; có thể dùng cổ sâu, hở vai/lưng, tay áo rời, tà xẻ, lụa/voan và phụ kiện tinh xảo theo từng nhân vật. Không tự giảm mức độ quyến rũ của ba mẫu đã duyệt.
- Tô Nguyệt Ly giữ trắng/xanh nhạt/vàng và chi tiết hoa; Lạc Huyền Sương giữ đen/đỏ/vàng cùng khí chất Ma đạo; nữ hồ ly giữ tóc hồng, tai hồ ly và phối hồng/trắng theo ảnh chuẩn.
- Trang phục mới phải khác biệt bằng phom cắt, chất liệu, lớp áo và phụ kiện, không chỉ phủ màu lên cùng một ảnh. Cân nhắc độ rõ trên điện thoại và khả năng giữ nhất quán qua các tư thế.
- **ĐỊNH HƯỚNG triển khai:** Mỗi nhân vật ưu tiên một bộ mặc định hoàn chỉnh; sau đó phát triển bộ thường ngày, lịch luyện/chiến đấu và lễ hội/hẹn hò phù hợp. Chưa chốt số lượng, giá hoặc điều kiện mở khóa.
- Khi đổi trang phục, chân dung, hình hội thoại và hoạt ảnh phải dùng cùng bộ đã chọn. Nếu thiếu tư thế/hoạt ảnh của bộ đó, dùng hình tĩnh tương ứng và ghi rõ giới hạn; không tự chuyển về bộ khác.

### 12.4 Tương tác nhân vật và phản ứng theo quan hệ

- **ĐÃ CHỐT hướng thiết kế:** Hướng tới tương tác có phản ứng biểu cảm, tư thế, hội thoại và quan hệ, tham khảo cách dàn cảnh của game mẫu.
- Khi trò chuyện: nhân vật có thể chớp mắt, thở nhẹ, chuyển hướng nhìn, nghiêng đầu, cử động môi và đổi biểu cảm theo câu thoại; tóc, tay áo, phụ kiện có chuyển động nhẹ khi có tài nguyên phù hợp.
- Khi đối thoại nhiều người: đổi nhân vật đang nói, vị trí, ánh nhìn và phản ứng của người nghe; phối hợp nền, âm thanh và chuyển cảnh để thể hiện tình huống.
- Cùng một nhân vật có thể dịu dàng với người thân, dè chừng người lạ hoặc đối đầu với đối thủ. Phản ứng phải dựa trên tính cách, quan hệ và điều đã xảy ra, không dùng cùng một câu trả lời cho mọi người.
- Các lựa chọn hội thoại cần có hậu quả hợp lý: mở lời tâm sự, tạo tin tưởng, gây hiểu lầm hoặc mở sự kiện. Ghi nhớ lời hứa, quà đã tặng, nhiệm vụ chung và mốc quan hệ để lần gặp sau có phản hồi liên quan.
- **ĐỊNH HƯỚNG hệ thống:** Theo dõi thiện cảm, tin tưởng và các cờ sự kiện; có thể thêm đố kỵ/đối địch khi tuyến truyện cần. Công thức, ngưỡng điểm và tốc độ tiến triển chưa chốt.
- Nhóm tương tác mong muốn: trò chuyện, tặng quà, mời đồng hành, khám phá địa điểm, luyện công/đấu tập, nhiệm vụ chung và hẹn hò. Những hành động gần gũi như nắm tay, vuốt tóc, ôm hoặc hôn nhẹ cần phù hợp mức quan hệ, tình huống và phản ứng riêng của nhân vật.
- Chạm nhân vật hoặc điểm tương tác sẽ kích hoạt hành động có chủ đích. Không dùng một động tác chạm tùy ý để tự động suy ra sự đồng thuận cho mọi hành động thân mật. Giữ quy tắc nhân vật trưởng thành và chuyển cảnh đã chốt ở mục 4–5.
- **ĐỊNH HƯỚNG mini-game:** Có thể xen đấu kiếm, đỡ/né, kết ấn, trận pháp hoặc tìm vật trong cảnh, gắn với mục đích truyện và quan hệ; không sao chép nguyên nội dung từ game tham khảo.

### 12.5 Tài nguyên và tiêu chí nghiệm thu

- **ĐỊNH HƯỚNG triển khai:** Ưu tiên Tô Nguyệt Ly trước: một cảnh có hội thoại lựa chọn, thay biểu cảm, một tương tác gần gũi phù hợp và phản hồi ở lần gặp sau. Sau đó mở rộng sang hai mẫu còn lại.
- Bộ biểu cảm đề xuất: bình thường, vui, ngượng, buồn, giận, ngạc nhiên và lo lắng; điều chỉnh theo tính cách. Bộ chuyển động đề xuất: nghỉ, nói, phản ứng vui/ngượng và tư thế hành động cần cho cảnh.
- Với tương tác nắm tay/ôm/hôn nhẹ, cần ảnh tư thế, chuỗi khung hình hoặc hoạt ảnh riêng và có hình nam chính khi cảnh cần. Một ảnh tĩnh chỉ dịch chuyển lên xuống không đủ thể hiện các động tác này.
- Chọn ảnh nhiều biểu cảm, sprite/chuỗi khung hình hoặc rig phân lớp tùy nguồn tài nguyên và độ phức tạp. Chưa chốt công cụ hoạt ảnh mới và không tự đổi nền tảng Kotlin Android hiện tại.
- Tiêu chí: giữ đúng khuôn mặt và trang phục qua các trạng thái; chuyển động không biến dạng; phản ứng phù hợp tính cách; kết thúc tương tác quay về trạng thái nghỉ; tiến trình quan hệ được lưu; thao tác rõ và chạy ổn trên điện thoại.
- **TRẠNG THÁI:** Phần này cập nhật yêu cầu thiết kế, không xác nhận các hoạt ảnh hay hệ thống quan hệ đã có trong APK. Giới hạn ảnh tĩnh ở mục 11 vẫn áp dụng cho tới khi có tài nguyên và bản build được kiểm tra.

**Lịch sử cập nhật — 2026-10-23:** Người dùng duyệt cả ba mẫu nhân vật hiện tại và yêu cầu bổ sung tương tác, tạo hình, trang phục vào tài liệu chuẩn. Chốt hướng dùng game tham khảo cho những nhân vật tiếp theo; bổ sung quy tắc phản ứng theo quan hệ, biểu cảm/tư thế, tài nguyên hoạt ảnh và tiêu chí nghiệm thu. Tiểu sử và thông số mới chưa được duyệt vẫn giữ trạng thái đề xuất.


## 13. Chốt phạm vi khởi động phát triển — 2026-10-23

### 13.1 Trạng thái quyết định

- **ĐÃ CHỐT:** Kiến trúc hoạt ảnh **Hybrid 2D**: nhân vật phân lớp cho trạng thái nghỉ/hội thoại (chớp mắt, thở, tóc/tay áo chuyển động), sprite/tư thế hoặc chuỗi khung hình cho hành động, và CG động nguyên bản cho những phân cảnh đặc biệt. Không coi dịch chuyển nguyên ảnh lên xuống là hoạt ảnh nhân vật hoàn chỉnh.
- **ĐÃ CHỐT:** Ưu tiên tạo một lát cắt có thể chơi được với nam chính và Tô Nguyệt Ly, giữ nguyên mẫu tạo hình đã duyệt, trước khi nhân rộng sang Lạc Huyền Sương, nữ hồ ly và dàn nhân vật sau này.
- **ĐÃ CHỐT:** Các tương tác gần gũi như nắm tay, ôm, hôn nhẹ phải có tư thế/khung hình phù hợp của cả hai nhân vật, thay vì chỉ đổi lời thoại hoặc biểu tượng.
- **ĐÃ CHỐT:** Tập trung trước vào gameplay, hình ảnh, tương tác, trang phục, giao diện và chiến đấu. **Chi tiết hệ thống quan hệ/nội dung 18+ để giai đoạn sau**; không để chúng chặn tiến độ APK đầu tiên.
- **ĐÃ CHỐT về tông thể hiện:** Giữ thẩm mỹ trưởng thành, lãng mạn, gợi cảm và táo bạo nhất quán với các mẫu đã duyệt, nhưng không tự ý biến yêu cầu này thành mô tả hoặc hoạt ảnh tình dục trực diện. Các nhân vật liên quan đều trưởng thành, mọi tiếp xúc thân mật có đồng thuận; các cảnh vượt mức lãng mạn/gợi cảm dùng chuyển cảnh theo quyết định trước đó.
- **CHƯA CHỐT:** Kịch bản, nhánh lựa chọn, chỉ số, ngưỡng mở khóa và bộ cảnh 18+ chi tiết; chỉ thiết kế kiến trúc có thể mở rộng về sau, chưa triển khai nội dung này.

### 13.2 Bộ khung tính năng và màn hình cần có

- **ĐÃ CHỐT từ trao đổi gameplay:** Màn **Nhân vật** để xem thông tin, chọn trang phục và trang bị vũ khí; màn **Túi đồ** quản lý vật phẩm. Trang phục đang chọn phải nhất quán trong cảnh và hoạt ảnh có tài nguyên tương ứng.
- **ĐÃ CHỐT từ trao đổi chiến đấu:** Hỗ trợ **nhiều nhân vật cùng tham chiến** thay vì chỉ một nhân vật; **HP của từng nhân vật tách riêng**. Không thêm cơ chế chia vị trí/cấu hình **công–thủ** phức tạp.
- **ĐÃ CHỐT yêu cầu nội dung:** Có cơ chế **trang phục hư hại/mất dần theo tiến trình chiến đấu**, chia **3 mốc hư hại** (không tính trạng thái nguyên vẹn): mốc 1 rách nhẹ; mốc 2 rách nhiều; mốc 3 **rách gần như toàn bộ trang phục**. Cần chuẩn bị asset nhất quán theo nhân vật và bộ đồ, không biến đổi ngẫu nhiên. Ở mốc cuối vẫn dùng tạo hình che phủ phù hợp, không mặc định hiển thị khỏa thân hay chi tiết nhạy cảm trực diện. Ngưỡng kích hoạt, cách phục hồi và điều kiện áp dụng sẽ xác định khi triển khai.
- **ĐÃ CHỐT:** Đội hình chiến đấu có **tối đa 4 nhân vật** cùng tham gia; mỗi nhân vật có HP độc lập. Cơ chế lượt/điều khiển chi tiết vẫn cần xác định khi triển khai.
- **CHƯA XÁC NHẬN TRIỂN KHAI:** Các mục trên là yêu cầu thiết kế, không đồng nghĩa màn hình hoặc hệ thống đã có trong APK.

### 13.3 Kiến trúc tài nguyên và hoạt ảnh

- Mỗi nhân vật có mã định danh và hồ sơ asset riêng: ảnh đứng, lớp biểu cảm, bộ phận có thể chuyển động, tư thế hành động, trang phục/biến thể, và CG sự kiện nếu có.
- Animation Controller dùng chung với các trạng thái **idle → transition → action → hold → recovery → idle**, có thể phát hoạt ảnh phối hợp hai nhân vật, ngắt/chuyển cảnh an toàn và khôi phục đúng trang phục/biểu cảm.
- Giữ khuôn mặt, vóc dáng, tóc, phụ kiện và trang phục nhất quán giữa các khung; không ghép cứng hai ảnh chân dung có nền riêng rồi gọi là tư thế ôm/hôn.
- Tối ưu cho Android: tải asset theo cảnh, tránh giữ toàn bộ ảnh độ phân giải cao trong RAM; kiểm thử bộ nhớ, độ mượt và kích thước APK trên máy thật.
- Dùng hình, sprite, kịch bản và hoạt ảnh **nguyên bản** của TVK. *Above the Immortality Realm* chỉ là tài liệu tham khảo cách dàn cảnh, thiết kế và tổ chức kỹ thuật; không sao chép asset có bản quyền.
- **TRẠNG THÁI KỸ THUẬT:** Prototype Kotlin Canvas hiện chỉ dịch chuyển ảnh tĩnh và đổi hội thoại; chưa có rig phân lớp, bộ tư thế cặp đôi hay CG động. Không tuyên bố các hạng mục trên đã hoàn thành trước khi code, build và thử APK.

### 13.4 Thứ tự triển khai để bắt đầu

1. Kiểm tra trạng thái repo, nhánh, source và workflow Actions mới nhất; xác nhận APK hiện có.
2. Chuẩn hóa danh mục asset và dữ liệu nhân vật, trang phục, biểu cảm, animation clip; giữ ảnh đã duyệt làm tham chiếu.
3. Làm mẫu hoạt ảnh **idle + biểu cảm** của Tô Nguyệt Ly, sau đó một tương tác hai nhân vật có tư thế thật (ưu tiên **nắm tay hoặc ôm**).
4. Tạo bộ khung điều hướng **Bản đồ / Nhân vật / Túi đồ / Đội hình**, chọn trang phục/trang bị và lưu trạng thái.
5. Hoàn thiện bản thử chiến đấu nhiều nhân vật, HP độc lập, và một trạng thái hư hại trang phục có kiểm soát.
6. Kiểm tra build Actions, cài trên Android, đo tính ổn định, sửa lỗi; sau đó mới mở rộng nhân vật/cảnh và hệ thống quan hệ.

**Tiêu chí nghiệm thu lát cắt đầu tiên:** APK cài và mở được; vào cảnh từ bản đồ; xem đúng ảnh nam chính/Tô Nguyệt Ly; có ít nhất một hoạt ảnh không chỉ tịnh tiến toàn bộ ảnh và một tương tác có tư thế phù hợp; có điều hướng Nhân vật/Túi đồ; chiến đấu mẫu có nhiều nhân vật với HP riêng khi giai đoạn chiến đấu được triển khai. Các tính năng chưa làm phải ghi rõ là TODO, không dùng nút giả khiến người chơi hiểu nhầm.

**Lịch sử cập nhật — 2026-10-23:** Người dùng yêu cầu tổng kết để bắt đầu triển khai, chốt Hybrid 2D, ưu tiên hệ thống chơi/hoạt ảnh trước và hoãn thiết kế chi tiết quan hệ 18+. Ghi rõ phạm vi, thứ tự triển khai, giới hạn prototype và các điểm cần xác minh trước khi code.

**Lịch sử cập nhật — 2026-10-23 (bổ sung):** Người dùng xác nhận tối đa 4 nhân vật cùng chiến đấu và 3 mốc hư hại trang phục, trong đó mốc cuối rách gần như hết. Các ngưỡng HP và cách phục hồi chưa chốt.


## 14. Ngôn ngữ, hội thoại và giọng nhân vật — 2026-10-23

- **ĐÃ CHỐT:** Ngôn ngữ giao diện, nhiệm vụ, lựa chọn và phụ đề/hội thoại hiển thị trong game là **tiếng Việt**. Font phải hỗ trợ đầy đủ dấu tiếng Việt, xuống dòng tự nhiên và đọc rõ trên Android.
- **ĐÃ CHỐT:** Hộp thoại và thao tác tham khảo cảm giác sử dụng của *Above the Immortality Realm* (bố cục dễ đọc, nhịp tương tác nhanh), nhưng thiết kế giao diện, hình ảnh, văn bản và âm thanh phải nguyên bản.
- **ĐÃ CHỐT:** Chữ hiện theo hiệu ứng gõ **tốc độ nhanh vừa phải/bình thường**, không kéo dài thời gian chờ. **Chạm màn hình** trong lúc chữ đang hiện để hiển thị ngay toàn bộ câu; **chạm tiếp** để chuyển sang câu tiếp theo. Không để thao tác chạm liên tục vô tình bỏ qua nhiều câu; khi có lựa chọn thì chạm lựa chọn thay vì tự động nhảy.
- **ĐỊNH HƯỚNG triển khai:** Có thể cho người chơi tùy chỉnh tốc độ chữ, bật/tắt hiệu ứng gõ, xem lịch sử hội thoại và bật/tắt tự động phát về sau. Chưa chốt vị trí các nút phụ.
- **ĐỊNH HƯỚNG được người dùng yêu thích:** Giọng nhân vật **tiếng Trung phổ thông (Mandarin)** để phù hợp không khí tiên hiệp, trong khi phụ đề vẫn là tiếng Việt. Chưa chốt công nghệ tổng hợp/thu âm, giọng từng nhân vật, phạm vi lồng tiếng, chi phí hoặc quyền sử dụng; không coi voice đã có trong APK.
- **Khuyến nghị kỹ thuật:** Dùng tệp âm thanh riêng gắn với ID câu thoại và nhân vật; có chế độ chơi không cần giọng, cho phép bật/tắt âm lượng thoại. Ưu tiên lồng tiếng một số câu chào, phản ứng và cảnh trọng điểm ở bản thử; không bắt buộc thu âm toàn bộ lời thoại ngay. Chỉ dùng giọng tổng hợp có quyền sử dụng hoặc diễn viên lồng tiếng được cấp phép; không sao chép giọng của game tham khảo.
- **Tiêu chí nghiệm thu hội thoại:** Hiển thị đúng tiếng Việt có dấu, không tràn khung; chạm lần một hoàn tất câu đang gõ, lần sau sang câu mới; lựa chọn không bị bỏ qua; nếu thiếu file thoại tiếng Trung thì game vẫn chạy và hiển thị phụ đề.

**Lịch sử cập nhật — 2026-10-23:** Chốt tiếng Việt và tương tác hộp thoại chạm để hiện hết câu/chuyển câu, tốc độ chữ nhanh vừa phải. Ghi nhận ưu tiên giọng nhân vật tiếng Trung phổ thông là định hướng cần triển khai và kiểm thử.


## 15. Chuyển từ prototype sang sản xuất game chính thức — 2026-10-23

- **ĐÃ CHỐT:** Không còn coi mục tiêu là APK thử giao diện đơn lẻ. Từ nay phát triển **Thanh Vân Ký thành game hoàn chỉnh theo từng bản chơi được**, ưu tiên chất lượng mỹ thuật, hoạt ảnh, nội dung và trải nghiệm trên Android.
- **ĐÃ CHỐT:** Người dùng ủy quyền chủ động viết cốt truyện, bổ sung tài nguyên còn thiếu và cải thiện chi tiết triển khai để tăng chất lượng. Những thay đổi ảnh hưởng các quyết định cốt lõi đã chốt (nhân vật, nền tảng, gameplay, giới hạn nội dung) vẫn phải ghi rõ lý do, không tự âm thầm ghi đè.
- **ĐÃ CHỐT:** Lấy *Above the Immortality Realm* làm chuẩn tham khảo **mức độ trau chuốt, nhịp hội thoại và cảm giác tương tác mượt**, không sao chép ảnh, code, âm thanh, kịch bản hoặc nhân vật của trò chơi đó.
- **ĐÃ CHỐT:** Cốt truyện do dự án tự phát triển. Tài liệu khởi đầu: [docs/STORY_BIBLE.md](STORY_BIBLE.md). Đây là **bản thảo sáng tác v0.1** để bắt đầu xây nội dung; chi tiết mới không mặc nhiên thay thế hồ sơ nhân vật đã duyệt.
- **ĐÃ CHỐT:** Ngôn ngữ game tiếng Việt, định hướng thoại tiếng Trung phổ thông; bốn nhân vật tối đa khi chiến đấu, HP độc lập; trang phục có ba mức hư hại sau trạng thái nguyên vẹn.
- **ƯU TIÊN SẢN XUẤT:** (1) khung dữ liệu và lưu game; (2) hội thoại/chạm/biểu cảm; (3) asset nhân vật, cảnh và hoạt ảnh thực; (4) bản đồ/cảnh/nhiệm vụ; (5) nhân vật/túi đồ/trang phục; (6) chiến đấu đội bốn người; (7) giọng thoại và âm thanh; (8) mở rộng chương truyện.
- **CHẤT LƯỢNG:** Không sử dụng hình vẽ Canvas placeholder làm mỹ thuật cuối; asset mới phải đồng bộ mẫu đã duyệt, đủ quyền sử dụng, rõ trên màn hình điện thoại. Nếu asset chưa hoàn thành, ghi trạng thái TODO thay vì gọi bản thử là bản hoàn chỉnh.
- **PHẠM VI NỘI DUNG TRƯỞNG THÀNH:** Giữ không khí lãng mạn, quyến rũ, các tuyến tình cảm giữa người trưởng thành có đồng thuận; hệ thống quan hệ và nội dung thân mật chi tiết phát triển sau. Không yêu cầu cảnh tình dục trực diện để hoàn thành mốc sản xuất đầu tiên.
- **KỶ LUẬT TRIỂN KHAI:** Mỗi đợt thay đổi cập nhật tài liệu/changelog, kiểm tra GitHub Actions và trạng thái APK thực tế, ghi rõ tính năng hoàn thành/chưa hoàn thành. Không coi một tài liệu kế hoạch là đã triển khai tính năng.

**Lịch sử cập nhật — 2026-10-23:** Người dùng chính thức yêu cầu bắt đầu sản xuất game trau chuốt, giao quyền chủ động xây cốt truyện và cải thiện thiết kế. Tạo STORY_BIBLE.md với tiền đề Thất Tinh Mạch, khung năm hồi và bản thảo chương mở đầu; chuyển mục tiêu từ thử nghiệm sang phát triển từng phiên bản có thể chơi được.


### Quy tắc hư hại trang phục toàn bộ — ĐÃ CHỐT (2026-10-23)

- Có đúng **bốn mức độ nguyên vẹn: 100%, 70%, 50%, 30%** (nguyên vẹn cộng ba mốc hư hại).
- Hư hại áp dụng cho **toàn bộ các lớp trang phục**: áo ngoài, áo trong, váy, tay áo và phụ kiện; không giữ nguyên một lớp áo trong ở các mức thấp. Các vùng nhạy cảm vẫn được che kín bằng phần trang phục còn lại.
- Hư hại là trạng thái riêng, **không tự hồi phục khi hồi HP**; có thể sửa trang phục bằng thao tác riêng.
- Tỷ lệ là **quy ước độ nguyên vẹn của trang phục**, không phải tỷ lệ da lộ ra.
- **TRẠNG THÁI KỸ THUẬT (2026-10-23):** Đã thêm mã Kotlin lưu bốn mức qua SharedPreferences, màn xem mức trang phục, nút mô phỏng hư hại và sửa trang phục. **Chưa nối sát thương chiến đấu thật, chưa có bộ ảnh 4 mức mới tương ứng, chưa xác minh build APK hoặc kiểm thử Xiaomi.** Màn trang phục hiện dùng ảnh nhân vật đã có và ghi rõ mô phỏng chỉ số, không coi là hình ảnh cuối.


### Chuẩn hình ảnh nữ chính và ngoại trang — ĐÃ CHỐT (2026-10-23)

- **Ảnh do người dùng cung cấp là chuẩn ưu tiên cao nhất:** bảng nhân vật Tô Nguyệt Ly tóc bạc, mắt xanh ngọc, trang phục trắng–xanh–vàng và ảnh ba nữ chính đứng cạnh nhau (Tô Nguyệt Ly tóc bạc, nữ chính tóc đen–đỏ, nữ chính hồ ly tóc hồng có tai cáo). Các ảnh áo cổ cao tạo sau chỉ là **ngoại trang thay thế**, không phải mặc định.
- **Tô Nguyệt Ly mặc định:** dáng trưởng thành, tóc bạc dài, mắt xanh, hoa cài tóc trắng–vàng; trang phục tiên hiệp trắng–xanh–vàng, đường nét tôn dáng, có khoảng hở thiết kế nhưng không phơi bày bộ phận nhạy cảm.
- **Các ngoại trang mua thêm:** giữ phong cách tiên hiệp quyến rũ, nhận diện riêng theo từng nhân vật; không được sao chép nguyên một thiết kế cho cả ba. Chưa có cửa hàng/thanh toán thì phải hiển thị trạng thái chưa sở hữu, không tự mở khóa.
- **Hư hại:** 100% / 70% / 50% / 30%, tác động tất cả lớp áo; phần còn lại vẫn che chắn vùng nhạy cảm. Cần bộ hình riêng cho từng mẫu × từng cấp hư hại và rig phù hợp.
- **TRẠNG THÁI KỸ THUẬT:** Kotlin đã thêm lựa chọn mẫu Bạch Nguyệt (mặc định), Huyền Hỏa (khóa), Hồ Tiên (khóa), Áo du hành (có), lưu lựa chọn và giữ trạng thái hư hại độc lập. Đây là **catalog giao diện và logic**, chưa phải cửa hàng thật; hình ảnh chính xác theo các ảnh tham chiếu chưa được nhập vào APK, chưa kiểm tra build sau commit. Không gọi phần mỹ thuật là đã xong.


### Tương tác động lặp liên tục và ảnh gốc — ĐÃ CHỐT (2026-10-23)

- Mỗi tương tác có thể gồm **Start → Loop (lặp vô hạn cho đến khi người chơi chủ động dừng hoặc chọn tương tác khác) → End**. Không tự kết thúc sau một vòng.
- Hôn là chuỗi chuyển động liên tục, không phải một ảnh tĩnh hay một hiệu ứng lắc ảnh. Cần khung chuyển tiếp/rig thật, chớp mắt, tóc, cơ thể và tương tác giữa hai nhân vật; sau khi bấm dừng mới chạy hoạt ảnh tách ra.
- **Bắt buộc giữ đúng khuôn mặt, tóc, vóc dáng và trang phục từ ảnh gốc người dùng gửi**; không dùng hình khác trông tương tự để thay thế. Ảnh tham chiếu hiện có trong cuộc hội thoại chưa đồng nghĩa với asset đã được thêm vào repo.
- **TRẠNG THÁI THỰC TẾ:** Đã có state controller Start/Loop/End trong Kotlin và thao tác dừng thủ công, nhưng renderer hiện chỉ di chuyển hai ảnh chân dung đã có bằng hiệu ứng sway; **chưa có chuỗi frame hôn thật, rig phân lớp, ảnh gốc mới trong assets hoặc kiểm thử build**. Không được đánh dấu là hoàn thiện tương tác động.


### Đội hình khởi đầu và định hướng nhân vật Above — ĐÃ CHỐT (2026-10-24)

- Đội hình khởi đầu gồm **nam chính (nhân vật người chơi)** và **hai nữ chính Tô Nguyệt Ly, Lâm Thiên (Lin Qian)**. Lâm Thiên **không phải** tên nam chính.
- Lâm Thiên dùng ảnh nhân vật từ *Above the Immortality Realm* do người dùng gửi ngày 2026-10-24 làm tham chiếu tạo hình chính thức; không thay bằng ảnh tìm kiếm tương tự. Chưa xác minh/nhập model Live2D/Spine hoàn chỉnh.
- Tính cách Lâm Thiên: **ngoài lạnh trong nóng**, ban đầu kiêu kỳ, kín đáo; khi phát triển tình cảm và có sự thân mật đồng thuận giữa người trưởng thành, trở nên dịu dàng, tin tưởng, chiều chuộng nam chính trong quan hệ riêng tư, vẫn giữ cá tính và năng lực chiến đấu.
- Giữ nguyên nam chính và ba tạo hình nữ đã được chọn trước đó; nhân vật mới về sau ưu tiên **phong cách mỹ thuật Above**, có thể sử dụng tài nguyên gốc chỉ khi có quyền và tương thích kỹ thuật. Không tự ý xóa mục tiêu 10 nữ chính trước đó; cho phép mở rộng thêm.
- **TRẠNG THÁI KỸ THUẬT:** đây là quyết định thiết kế, chưa phải tính năng APK đã hoàn thiện. Tài nguyên Above hiện ở giai đoạn kiểm kê bundle và trích xuất node thô.


### Thư viện cảnh tương tác dùng chung — TRẠNG THÁI KỸ THUẬT (2026-10-24)

- **ĐÃ CHỐT về kiến trúc:** Dùng một hệ thống phát cảnh có thể lựa chọn theo ID nhân vật và ID cảnh, phối hợp chuyển động, biểu cảm, hình ảnh, âm thanh; mỗi nhân vật có model, texture và rig riêng. Không mặc định rằng animation của rig này có thể gán ngay cho rig khác.
- **TRẠNG THÁI KỸ THUẬT:** Đã thêm `CharacterSceneLibrary.cs`, `CharacterScenePlayer.cs` và cập nhật `InteractionMenuController.cs` trong repo [thanh-van-ky-unity](https://github.com/luuduong99/thanh-van-ky-unity). Module hỗ trợ Unity Timeline/Animator, sprite và audio cho các cảnh không tường minh; có mã kiểm tra dạng Unity Editor test và [tài liệu thiết lập](https://github.com/luuduong99/thanh-van-ky-unity/blob/main/docs/CHARACTER_SCENE_PLAYER.md).
- **CHƯA HOÀN THÀNH:** Chưa chạy compile/test trên Unity Editor; chưa kết nối prefab và asset Spine Lâm Thiển vào ScenePlayer; chưa triển khai Start → Loop → End hoàn chỉnh theo yêu cầu tương tác trước đó; chưa chuyển tính năng sang APK hiện hành (đang là dự án Kotlin Android); chưa có bản APK tích hợp.
- **PHẠM VI TÀI NGUYÊN:** ZIP model hội thoại Spine Lâm Thiển có skeleton, texture, atlas và 7 biểu cảm đã được ghi nhận, nhưng không phải toàn bộ cảnh trong Above. Không ghi nhận đã có hoạt ảnh cảnh riêng hoặc tích hợp nội dung tình dục tường minh. Cần quyền phù hợp nếu sử dụng tài nguyên gốc của game khác.
- **LỊCH SỬ CẬP NHẬT 2026-10-24:** Thêm module Unity dùng chung cho cảnh dựng sẵn, giữ trạng thái là code chưa kiểm thử; không thay đổi kiến trúc Android/Kotlin của APK hiện tại.


### Tương tác nhân vật theo vùng chạm — ĐÃ CHỐT thiết kế (2026-10-24)

- **ĐÃ CHỐT:** Ở màn tương tác từng nữ chính, người chơi chạm **trực tiếp lên ảnh nhân vật**, không hiển thị 8 nút chọn vùng cơ thể. Phản ứng phụ thuộc nhân vật và vùng được chạm: **đầu, mặt, ngực, bụng, tay, đùi, chân, mông**. Nhân vật nam chính hiện bên cạnh nữ chính, không dùng chung một ảnh giả với nhân vật nữ.
- **ĐÃ CHỐT:** Nút **Lột đồ / Trang phục** và nút **Cảnh 18+** là **hai nút riêng**, không kích hoạt khi chạm vùng cơ thể. Trạng thái thay đồ/hoạt cảnh chỉ được hiển thị là đã có nếu tài nguyên, quyền sử dụng và kiểm thử thực sự đầy đủ.
- **YÊU CẦU HÌNH ẢNH:** Chạm mông cần góc nhìn phía sau hoặc nghiêng có asset tương ứng; không gán sai vào vùng mặt trước. Vùng chạm trên ảnh phải hiệu chỉnh theo tọa độ và kiểu crop thật của từng nhân vật. Cảnh nhạy cảm chỉ kích hoạt khi có sự đồng thuận rõ ràng của các nhân vật trưởng thành.
- **ĐÃ TRIỂN KHAI Ở MỨC KHUNG (2026-10-24):** Bản thử Kotlin `CharacterInteractionActivity.kt` sử dụng `character_interactions.json` (v2) để ánh xạ 8 vùng, lời thoại riêng cho Tô Nguyệt Ly và Lâm Thiển, phản ứng không tường minh, cùng hai nút độc lập. Vùng phía sau chỉ có metadata, chưa khả dụng do chưa có ảnh từ phía sau; các vùng nhạy cảm đưa ra phản ứng giữ ranh giới, không tự tăng thiện cảm. Tọa độ chỉ là mẫu, chưa hiệu chỉnh theo nhân vật thật.
- **TRẠNG THÁI ASSET:** Ảnh nam chính và Tô Nguyệt Ly đã có trong assets APK; ảnh `characters/lin_qian.png` chưa nhập vào repo APK nên không thể chạm xác định vùng trên Lâm Thiển khi chưa có ảnh. Bộ model thoại Spine Lâm Thiển ở thư viện ngoài, **chưa tích hợp** renderer Android. Chưa có các file MP4 riêng cho nhân vật; nút 18+ chỉ cung cấp chuyển cảnh kín đáo, không có hoạt cảnh tình dục trực diện. Nút trang phục chưa thay đổi hình nhân vật.
- **TRẠNG THÁI BUILD:** Mọi kết luận build/APK phải dựa trên GitHub Actions của commit hiện tại. Không đánh dấu đã phát hành APK hay đã test Xiaomi nếu chưa có kết quả.
- **LỊCH SỬ CẬP NHẬT 2026-10-24:** Điều chỉnh tương tác theo yêu cầu người dùng: thay nút vùng cơ thể bằng thao tác chạm trực tiếp, tách trang phục và cảnh 18+ thành hai nút riêng; giữ nam chính bên cạnh từng nữ chính.


### Đổi tư thế mặt trước / phía sau trong tương tác — ĐÃ CHỐT (2026-10-24)

- **ĐÃ CHỐT:** Màn tương tác của Tô Nguyệt Ly và Lâm Thiển có thêm hai trạng thái **Mặt trước** và **Quay ra sau**, chuyển bằng nút ngay dưới ảnh nhân vật. Chỉ bật vùng chạm đúng với góc nhìn đang hiển thị; **vùng mông thuộc tư thế phía sau**, không nhận chạm trên ảnh chính diện.
- **ĐÃ TRIỂN KHAI Ở MỨC KHUNG:** `CharacterInteractionActivity.kt` đã có chuyển tư thế theo từng nhân vật, lưu lựa chọn tư thế riêng bằng SharedPreferences; `character_interactions.json` v3 đăng ký slot `backPortrait` độc lập. Khi đổi nhân vật, tư thế của nhân vật đó được phục hồi. Vùng chạm lấy tọa độ dựa trên ảnh FIT_CENTER và loại trừ phần khoảng trống letterbox.
- **TÀI NGUYÊN CHƯA CÓ:** Hiện repo Android chưa chứa `characters/to_nguyet_ly_back.png` và `characters/lin_qian_back.png`, do đó màn phía sau hiển thị thông báo thiếu ảnh, không giả mạo tư thế bằng cách lật ảnh mặt trước và **không kích hoạt vùng mông** cho đến khi có hình chính xác. Ảnh mặt trước của Lâm Thiển cũng chưa tích hợp vào Android. Các tọa độ vùng chạm hiện vẫn là nguyên mẫu, phải hiệu chỉnh theo hình gốc trước khi kết luận hoàn thành trải nghiệm.
- Hai nút **Lột đồ / Trang phục** và **Cảnh 18+** vẫn tách riêng hoàn toàn với thao tác chạm trực tiếp. Những cảnh không có asset không được giả là đã có animation.
- **LỊCH SỬ CẬP NHẬT 2026-10-24:** Thêm lựa chọn tư thế nhằm hỗ trợ tương tác vùng phía sau đúng vị trí. Tiếp tục ưu tiên asset thật, không tự nhận đã hoàn thành artwork hoặc phát hành APK nếu chưa xác minh GitHub Actions.


### Tư thế trên giường và chuyển động phụ của nhân vật — ĐÃ CHỐT yêu cầu (2026-10-24)

- **ĐÃ CHỐT:** Bổ sung hai tư thế cho giao diện tương tác của **Tô Nguyệt Ly** và **Lâm Thiển**:
  1. `bed_kneel_forward` — **Quỳ trên giường, thân trên hạ thấp**, dựa trên ảnh thứ nhất người dùng đưa; góc nhìn có thể chếch từ sau, biểu cảm tùy nhân vật, khi cần có thể ngoảnh đầu nhìn lại.
  2. `bed_recline` — **Nằm ngửa nghỉ ngơi trên giường**, dựa trên dáng nằm của ảnh thứ hai. Ảnh tham khảo thứ hai chụp trên sofa nhưng bối cảnh trong game **phải là giường**.
- **ĐÃ CHỐT:** Tư thế cần có biểu cảm phù hợp cá tính (Lâm Thiển có thể ngại, đỏ mặt và tránh mắt; Tô Nguyệt Ly dịu dàng, thoải mái), đồng thời cần **chuyển động thở lên/xuống ở thân trên và dao động phụ tự nhiên của vùng ngực, tóc và trang phục** khi có rig phân lớp. Không tạo hiệu ứng giật lắc cả ảnh để giả chuyển động riêng của từng bộ phận. Chuyển động phải vừa phải, có tính vật lý, loop mượt, tùy chỉnh mức độ theo nhân vật và tư thế.
- **QUY TẮC TƯƠNG TÁC:** Từng tư thế có bố cục và vùng chạm riêng; không dùng trực tiếp tọa độ của hình đứng cho hình nằm. Không mở tương tác khi thiếu ảnh/model của đúng tư thế. Các nút **Lột đồ / Trang phục** và **Cảnh 18+** tiếp tục tách biệt với bộ chọn tư thế. Nhân vật trong tuyến tình cảm đều là người trưởng thành và mọi tương tác thân mật đều cần đồng thuận.
- **TRẠNG THÁI KỸ THUẬT:** Đã đăng ký bốn tư thế `front`, `back`, `bed_kneel_forward`, `bed_recline` cho hai nữ chính trong `character_interactions.json` v4; màn Android có bộ chọn tư thế cuộn ngang, lưu tư thế riêng từng nhân vật, sử dụng ảnh đúng theo mỗi tư thế và hiển thị rõ khi thiếu asset. `motionProfile` khai báo yêu cầu animation, **không phải bằng chứng đã có animation hoặc chuyển động vòng một thực sự trong APK**.
- **ASSET CÒN THIẾU:** Chưa có ảnh gốc đúng các tư thế mới trong repository Android; ảnh đính kèm từ nguồn tham khảo chỉ dùng để mô tả pose, không sao chép làm mỹ thuật nhân vật. Chưa có rig phân lớp, secondary motion thực tế, hoặc vùng chạm hiệu chỉnh cho hai tư thế mới. Mô hình 2D nguyên bản cần được dựng và nhập riêng cho mỗi nhân vật.
- **LỊCH SỬ CẬP NHẬT 2026-10-24:** Chốt thêm hai kiểu nằm/quỳ trên giường theo ảnh người dùng gửi; ưu tiên nét mặt quay lại và chuyển động tự nhiên, ghi rõ phần mới là cấu trúc dữ liệu và UI chứ chưa có asset hoặc animation.


## 16. Kiểm kê nghiệm thu Chương I, tư thế và tương tác — 2026-10-24

> **TRẠNG THÁI HIỆN HÀNH; ưu tiên hơn các ghi chú "thiếu ảnh/chưa build" ở mục 11–15 đã viết trước đó.** Đối chiếu trực tiếp branch `map-2d-prototype` commit `196e77fa3ad77edc3fad54452d0cb373bdf01fa6`, tree GitHub, `MainActivity.kt`, `CharacterInteractionActivity.kt`, `TVKCharacterMotionView.kt` và `character_interactions.json` phiên bản **6**. Workflow [GitHub Actions #40062868665](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/40062868665) kết thúc **success**, có artifact `thanh-van-ky-debug-apk`. Thành công biên dịch **không tương đương** kiểm thử trên thiết bị hay xác nhận chất lượng hoạt ảnh.

### 16.1 Đã đưa vào source và build được

| Hạng mục | Trạng thái thực tế |
|---|---|
| Bản đồ Thanh Vân Sơn → Chương I → hội thoại sáu đoạn → lựa chọn Rừng Trúc/đại điện, lưu `complete` và `choice` | **ĐÃ CÓ BẢN CHƠI THỬ** trong `MainActivity.kt`; chưa hoàn thiện nhiệm vụ nối tiếp. |
| Nam chính và Tô Nguyệt Ly trong màn tương tác | **ĐÃ CÓ** ảnh và luồng điều hướng; ảnh nam chính `characters/main_portrait.png`, Tô Nguyệt Ly từ phần bên trái `characters/heroines_reference.png`. |
| Lâm Thiển và các tư thế mới | **ĐÃ CÓ FILE ẢNH** `characters/lin_qian.png`, `lin_qian_back.png`, `lin_qian_bed_kneel_forward.png`, `lin_qian_bed_recline.png`; Tô Nguyệt Ly có ảnh `to_nguyet_ly_back.png`, `to_nguyet_ly_bed_kneel_forward.png`, `to_nguyet_ly_bed_recline.png`. Không còn ghi "chưa nhập ảnh Lâm Thiển" cho trạng thái hiện tại. |
| Bộ chọn tư thế theo nhân vật | **ĐÃ CÓ UI + LƯU TRẠNG THÁI**: `front`, `back`, `bed_kneel_forward`, `bed_recline`. Nam chính được trình bày cạnh/inset ảnh nữ chính tùy khung hình. |
| Chạm trực tiếp lên từng vùng nhân vật | **ĐÃ CÓ BẢN THỬ**: JSON v6 khai báo 7 vùng khi nhìn trước, 1 vùng khi nhìn sau và 7 vùng riêng cho mỗi tư thế giường, **mỗi nhân vật có phản hồi văn bản riêng**. Không phải 7 động tác rig độc lập. |
| Hiệu ứng chạm và idle | **ĐÃ CÓ RENDERER THỬ** `TVKCharacterMotionView.kt`: biến dạng mesh ảnh phẳng cục bộ theo nhịp thở, tóc và khi chạm. **KHÔNG** phải rig Spine/Live2D thật, animation hành động cặp đôi, hay chuyển động tách riêng các lớp trang phục/cơ thể. |
| Nút riêng **Lột đồ / Trang phục** và **Cảnh 18+** | **ĐÃ CÓ NÚT, CHƯA CÓ ĐẦY ĐỦ NỘI DUNG**: `wardrobeStates` có `default` và slot `outer_removed`, chỉ đổi khi có ảnh trạng thái thực. `Cảnh 18+` hiện là fade-to-black, **không có video/cảnh tình dục trực diện**. |
| Ảnh tư thế đã thêm vào APK | **ĐÃ ĐÓNG GÓI CÁC CROP CONCEPT**; ảnh lấy từ bảng tham khảo mới của hai nhân vật, hiện kích thước nhỏ (xấp xỉ 200–430 px chiều ngang), có thể mang chi tiết nền/chữ của concept; **chưa nghiệm thu art sản xuất, độ nhất quán trang phục và vùng chạm chính xác**. |

### 16.2 Các yêu cầu trước đó vẫn CHƯA HOÀN THÀNH

1. **Đúng mẫu art nhân vật ở mọi tư thế:** cần bộ ảnh từng tư thế chất lượng đủ dùng trên điện thoại, cùng gương mặt/trang phục mặc định đã chốt, loại bỏ mọi khung chữ/đường viền còn dính từ ảnh concept. Các ảnh crop hiện tại chỉ đủ để thử luồng.
2. **Hoạt ảnh thực tế:** cần rig phân lớp/Spine/Live2D hoặc chuỗi frame được vẽ riêng để chớp mắt, xoay đầu nhìn lại, đổi nét mặt (bình thường, ngượng, đỏ mặt), chuyển động thở/tóc/tay áo hợp lý từng tư thế. Chưa có hoạt ảnh quỳ/nằm chuyển động thật; mesh-deform trên PNG chỉ là bản thử. Các tương tác **nắm tay, ôm, hôn nhẹ** với nam chính chưa có frame/rig cặp đôi đúng tư thế hay state Start → Loop → End thực sự.
3. **Hiệu chỉnh tương tác chạm:** tọa độ vùng trong JSON v6 được khai báo **theo ước lượng**, chưa đo theo bản sprite cuối cùng ở nhiều tỉ lệ màn hình; cần kiểm tra/điều chỉnh hotspot, quy tắc ưu tiên vùng chồng nhau, ngưỡng quan hệ và phản ứng biểu cảm/hoạt ảnh đúng nơi chạm. Vùng nhạy cảm chỉ phản hồi ranh giới, không tự tăng thiện cảm khi chưa có đồng thuận.
4. **Cởi/thay trang phục nhìn thấy được:** còn thiếu ảnh và lớp thay trang phục hợp lệ cho `outer_removed` ở **từng nhân vật × từng tư thế**; nút hiện có nhưng sẽ giữ nguyên trang phục khi thiếu ảnh. Danh mục trang phục ở `MainActivity.kt` còn là mô phỏng, chưa đồng bộ hoàn toàn với màn nhân vật.
5. **Tư thế người dùng từng yêu cầu ngoài bốn tư thế đã tích hợp:** tựa/chống tay vào tường, ngồi/ghế hoặc mép giường, nằm sấp/nghiêng và các biến thể góc camera; những tư thế này **chưa có asset, hotspot hay nút chọn**. Không tự đánh dấu đã hoàn thành tất cả tư thế chỉ vì hai ví dụ trên giường đã được tạo.
6. **Màn nhân vật, túi đồ, trang bị:** chưa có luồng đầy đủ xem nhân vật/chọn vũ khí/túi đồ mà người dùng yêu cầu; màn trang phục hiện còn là trang demo.
7. **Chiến đấu và hư hại đồ:** chưa có chiến đấu thử với tối đa **4 thành viên**, **HP riêng từng người** trên một màn chung, giao diện theo mẫu và thanh biểu tượng bên phải đã duyệt. Bốn mức trạng thái quần áo đã có biến số/nút mô phỏng trong `MainActivity.kt`, nhưng **chưa nối sát thương thật**, chưa có hình 2D rách đồ tại 3 ngưỡng và cảnh hiển thị ở lượt nhân vật theo yêu cầu.
8. **Chương I / kịch bản:** màn truyện có sáu dòng và hai lựa chọn, nhưng chưa hoàn thiện chuỗi nhiệm vụ hậu lựa chọn, NPC/địa điểm thật, tài sản nền/map chất lượng sản xuất, biểu cảm nhân vật đổi theo lời thoại, hội thoại nhiều người/cảnh động, và hành vi của NPC sau lần gặp tiếp theo. UI hội thoại/trận chiến chưa được nghiệm thu đúng các ảnh mẫu trước đó.
9. **Kiểm thử:** dù Actions thành công và có artifact, **chưa có bằng chứng kiểm thử trực tiếp APK trên điện thoại Xiaomi** (cảm ứng hotspot, hiệu suất, bộ nhớ, hiển thị cảnh nằm rộng, cảnh dọc và kiểm tra crash). Không ghi "Chương I hoàn thành" trước khi qua kiểm thử này.

### 16.3 Kết luận trạng thái và phạm vi thực hiện tiếp

- **CHƯA CHỐT HOÀN THÀNH CHƯƠNG I.** Hiện có **bản build APK thành công với luồng truyện cơ bản và thư viện tương tác tư thế dùng được ở mức thử nghiệm**.
- Các mục **đã chốt thiết kế** (4 nhân vật chiến đấu tối đa, HP riêng, 3 ngưỡng rách đồ, túi đồ/vũ khí, UI chuẩn, bốn tư thế cơ bản, nút trang phục và cảnh riêng, phản ứng chạm) không được suy ra là đã lập trình xong. Các tư thế/cảnh bổ sung chưa có ảnh và động tác được xếp vào danh sách chờ.
- **Ưu tiên tiếp:** (a) nâng chất lượng sprite/ảnh tư thế và nhận diện nhân vật; (b) kết nối chuyển động rig/khung hình thực cùng hiệu chỉnh hotspot; (c) hoàn thiện trang phục theo tư thế; (d) thêm nhân vật/túi đồ và chiến đấu nhiều nhân vật với HP riêng/hư hại 2D; (e) hoàn thiện nhiệm vụ Chương I và thử APK trên thiết bị thật. Nội dung tương tác lãng mạn/tình cảm bảo đảm nhân vật trưởng thành và có đồng thuận.
- **LỊCH SỬ CẬP NHẬT 2026-10-24:** Kiểm tra nguồn và kết quả GitHub Actions sau đợt nhập ảnh pose. Cập nhật trạng thái ảnh từ "chưa có" thành "đã có bản crop concept", phân biệt **asset**, **code**, **build**, **runtime trên máy**, **nghiệm thu nghệ thuật** và **tính năng chưa làm**, tránh khẳng định sai rằng đã hoàn thành toàn bộ Chương I.



---

## 13. Lâm Thiển — chuẩn +17% và trạng thái CP314 (2026-10-28)

- **ĐÃ CHỐT:** Giữ tạo hình/reference riêng của Lâm Thiển. Mốc tỷ lệ +17% là nền chốt; cho phép điều chỉnh nhẹ chiều cao/tỷ lệ tổng thể để thanh, cân đối hơn, tránh cảm giác thấp/lùn. Mọi điều chỉnh phải có preview để duyệt trước. Dùng quy trình này làm chuẩn tham khảo cho nhân vật mới, không tự ý đồng nhất vóc dáng.
- **TRẠNG THÁI KỸ THUẬT từ phiên trước:** CP312 ORA 8 lớp; CP313 ORA 10 lớp, báo cáo chuyển 365 pixel gán sai từ da sang chân tóc, thêm dây trang sức xanh–vàng và bốn test PASS. Cần kiểm tra trực tiếp nguồn trước khi coi là xác nhận kỹ thuật.
- **CHƯA NGHIỆM THU:** Ranh giới tóc/scalp–gáy–da vai và hai tay áo chưa hoàn tất, chưa có Spine rig/physics được chốt, chưa xác nhận vào APK.
- **TIẾP TỤC:** CP314 sửa tóc/scalp–gáy–vai, rồi tay áo; pixel diff và alpha ở ±5px, preview duyệt. Xem [hồ sơ CP314](art/LAM_THIEN_CP314.md). Đã tìm được PNG Back và sheet ở Drive, chưa tìm được ORA 10 lớp CP313 trong nguồn hiện truy cập.

### Cập nhật lịch sử ngày 2026-10-28
Ghi nhận chuẩn +17% và mốc giao việc CP314; không coi các bước sửa ảnh chưa chạy trên ORA là hoàn thành.


---

## 14. Lâm Thiển — CP315 QA và điểm tiếp tục CP316 (2026-10-28)

- **ĐÃ CHỐT — KHÔNG ĐỔI:** Model Lâm Thiển giữ reference và mốc +17%; chỉ tinh chỉnh nhẹ chiều cao/tỷ lệ tổng thể sau preview và duyệt. Đây là quy trình chung cho nhân vật sau, không phải tỷ lệ cơ thể bắt buộc giống hệt nhau.
- **ĐÃ THỰC HIỆN CP315:** Tạo script `tools/art/audit_ora.py` kiểm tra ORA theo layer, so pixel thay đổi với `--baseline` và ROI cho phép, mô phỏng dịch chuyển layer tóc ±5px, xuất alpha-hole mask. Tạo `tests/art/test_audit_ora.py` với **5/5 bài kiểm thử tổng hợp PASS** tại môi trường làm việc. Đã thêm workflow `.github/workflows/art-qa.yml`, nhưng cần kiểm chứng workflow GitHub thực tế sau khi push.
- **GIỚI HẠN:** 70 alpha holes và 9 pixel ngoài ROI được phát hiện trên fixture giả lập, không phải ảnh Lâm Thiển. Chưa có CP313 ORA 10 lớp nguồn trong repo/Drive đã truy cập nên không thể nghiệm thu artwork và rig.
- **TIẾP TỤC CP316:** Xác minh ORA 10 lớp CP313; sửa tóc/scalp–gáy–vai và phụ kiện; tiếp hai tay áo; chạy kiểm thử với ROI canvas thật; preview người dùng duyệt trước khi tích hợp Spine/physics/APK.
- Xem tài liệu chi tiết `docs/art/LAM_THIEN_CP315_QA.md`.

### Cập nhật lịch sử ngày 2026-10-28
Bổ sung công cụ QA CP315 và unit tests; phân biệt rõ kiểm thử công cụ thành công với hoàn tất asset/rig thực tế.


---

## 15. Lâm Thiển — CP316 kiểm kê nguồn ORA (2026-10-28)

- **ĐÃ CHỐT – KHÔNG THAY:** Mốc Lâm Thiển +17%, giữ nhận diện tóc bạc và trang phục trắng–xanh–vàng. Được tinh chỉnh nhẹ chiều cao/tỷ lệ tổng thể để thanh thoát, **chỉ sau khi có preview và người dùng duyệt**. Đây là quy trình tham khảo cho nhân vật khác, không dùng làm khuôn giống nhau.
- **HOÀN THÀNH CP316 (QA/nghiệp vụ kiểm kê):** Đã thêm `tools/art/source_inventory.py` để quét ORA trong các ZIP lồng nhau, kiểm tra cấu trúc 10 lớp, lớp alpha trống/placeholder và ghi sha256; thêm 5 test ở `tests/art/test_source_inventory.py`. Tổng cộng **10/10 unit tests PASS** trên fixture giả lập (5 CP315 + 5 CP316). Có ảnh khoanh vùng bốn điểm kiểm tra Back trong gói CP316.
- **ĐÃ KIỂM CHỨNG NGUỒN HIỆN CÓ:** Hai gói CP314/CP315 được rà soát trong phiên này không có ORA; ảnh Back 207×656 và sheet là PNG RGB phẳng. Tool trả `NO_QUALIFYING_ORA_SOURCE` (2 archives, 0 ORA). Tên `CP312`, `CP313`, `linqian`, `.ora` không có kết quả phù hợp từ tìm kiếm Drive phiên này; có thể tồn tại ở nguồn chưa truy cập.
- **CHƯA LÀM:** Chưa sửa art chân tóc–gáy–vai trên ORA thật, chưa sửa hai tay áo, chưa nghiệm thu rig/physics/Android APK. 10 test đạt **không đồng nghĩa model đạt**.
- **TIẾP TỤC CP317:** Phục hồi CP313 ORA 10 lớp hoặc CP312 8 lớp, kiểm tra hash và composite/layer, sửa gáy–vai/dây trang sức/hai tay áo; thử dịch ±5px và so pixel ngoài ROI; preview trước khi duyệt. Xem `docs/art/LAM_THIEN_CP316_SOURCE_RECOVERY.md`.

### Lịch sử cập nhật ngày 2026-10-28
CP316 hoàn thành bước khôi phục nguồn dưới dạng rà soát/đối soát và xây công cụ, nguồn ORA vẫn thiếu. Không đánh dấu art thực tế hoàn thành.



---

## 16. Lâm Thiển — CP317 bản ORA phục dựng từ PNG (2026-10-28)

- **ĐÃ CHỐT — KHÔNG ĐỔI:** Lâm Thiển theo màu trắng–xanh–vàng, tóc bạc và nhận diện người dùng đã duyệt. Mốc tỷ lệ +17% vẫn giữ, mọi tinh chỉnh chiều cao/tỷ lệ mới phải có preview và xác nhận; CP317 không tự thay đổi tỷ lệ.
- **ĐÃ TẠO CP317, nhưng KHÔNG PHẢI FILE NGUỒN:** Một file `CP317_LamThien_Back_10Layer_RECONSTRUCTION_NOT_ORIGINAL.ora` phục dựng từ PNG Back 207×656, gồm 10 lớp nhìn thấy và phần nền dưới tóc/tay áo được **ước lượng**. Composite đứng yên so với PNG gốc: 0 pixel khác biệt. Không được ghi đè, thay thế hoặc gọi file này là CP313 ORA gốc.
- **KIỂM THỬ:** 12/12 bài unit test chạy thành công trong môi trường cục bộ (CP315/CP316/CP317). Công cụ `source_inventory.py` đã được sửa để loại ORA phục dựng khỏi danh sách ứng viên nguồn CP313 dựa trên metadata/tên lớp. File kỹ thuật cấu trúc hợp lệ nhưng **đường mép chuyển động còn thô, chưa nghiệm thu mỹ thuật**.
- **CHƯA HOÀN THÀNH:** ORA CP313 gốc chưa phục hồi. Vùng tóc/scalp–gáy–vai và tay áo chưa có art layer chính xác; rig/physics/APK của Lâm Thiển chưa kiểm chứng.
- **TIẾP TỤC CP318:** Ưu tiên tìm CP313 gốc; nếu không có, vẽ lại chính xác viền phân lớp và phần dưới tóc trên bản proxy, sửa gáy–vai, dây trang sức, hai tay áo. Chạy motion ±5px và so với ảnh reference. Chỉ sau preview được duyệt mới rig/physics.
- Chi tiết: `docs/art/LAM_THIEN_CP317_RECONSTRUCTION.md`. File ORA proxy đã tạo trong phiên làm việc, cung cấp qua gói bàn giao; không ghi nhận đã upload binary asset vào GitHub.

### Lịch sử bổ sung (2026-10-28)
CP317 tạo bản phục dựng có thể chỉnh, không thay thế ORA nguồn; bổ sung kiểm soát xuất xứ và kiểm thử trong khi giữ nguyên quyết định +17%.


---

## 17. Lâm Thiển — sửa sai lệch tham chiếu trang phục Back (2026-10-28)

- **ĐÃ CHỐT 2026-10-27:** Lâm Thiển mặc định trắng–xanh–vàng; **khoét hai bên hông cân đối** và **vùng mông/phía sau đầy đặn, nổi khối rõ, tôn dáng** theo ảnh đã duyệt. Áp dụng đồng bộ sang mọi tư thế. Không tự che kín hai bên hông hoặc làm phẳng/giảm nét tạo hình đã chốt.
- **ĐÃ CHỐT 2026-10-28:** Điều chỉnh thân trên +17%; chiều cao bản preview 947→971px, vai–eo 144→168px, không kéo giãn vùng hông/chân. Giữ cảm giác thanh, cân đối, tránh thấp/lùn; phải có preview trước mọi tinh chỉnh tiếp theo. Mốc +17% dành riêng cho Lâm Thiển.
- **PHÂN BIỆT KỸ THUẬT:** CP317 dùng ảnh Back PNG cũ 207×656 để làm **proxy tách lớp**, vì vậy **không phản ánh đầy đủ thiết kế trang phục canon**; dù static composite khớp 0px cũng không được nghiệm thu mỹ thuật. Không dùng bản này để thay thế model cuối cùng hoặc dựa vào đó để bỏ phần khoét hông / tạo hình phía sau.
- **TIẾP TỤC CP318:** đối chiếu đúng ảnh Back canon đã duyệt trước khi vẽ lại trang phục, tách các phần hông–váy–mông phù hợp cho hoạt ảnh và giữ các chi tiết gáy–vai–tay áo. Preview full-body/Back cho người dùng xem trước khi duyệt, sau đó mới rig, physics và APK.

### Lịch sử 2026-10-28
Làm rõ sai lệch của proxy CP317 để bảo toàn thiết kế Back Lâm Thiển đã duyệt ngày 2026-10-27.


---

## 18. Lâm Thiển — CP318 preview mới chờ duyệt (2026-10-28)

- **ĐÃ THỰC HIỆN:** Tạo concept Back Lâm Thiển mới dựa trên các yêu cầu đã chốt: tóc bạc/trắng–xanh–vàng, hông hai bên khoét cân đối, silhouette phía sau rõ, dáng thanh hơn; ảnh preview lưu tại Library `/Thanh Van Ky/CP318_LamThien_Back_NEW_DESIGN_REVIEW_NOT_APPROVED.png`.
- **TRẠNG THÁI CHƯA DUYỆT:** Concept mới là hình xem trước, KHÔNG phải tệp CP251 canon gốc hay sprite phân lớp; không có phép đo pixel xác minh +17%, không có thử alpha/hair physics trên concept mới.
- **NGUYÊN TẮC:** Không dùng hình Back PNG cũ và CP317 proxy làm preview chính; chỉ dùng mẫu đã được người dùng duyệt làm canon. CP318 preview vẫn chờ người dùng xác nhận trước khi thay thế.
- **TIẾP TỤC CP319:** tiếp thu nhận xét/duyệt CP318; đồng bộ các góc/tư thế; tạo layer thực và kiểm thử trước rig/physics/APK. Chi tiết: `docs/art/LAM_THIEN_CP318_PREVIEW.md`.

### Lịch sử 2026-10-28
Tạo preview Back dựa thiết kế mới; tách trạng thái đề xuất khỏi bản chốt, tránh hiểu nhầm thành asset game hoàn thiện.


---

## 19. Lâm Thiển — CP319 clean review và kiểm soát thiết kế (2026-10-28)

- **ĐÃ THỰC HIỆN:** Tách/crop nguyên pixel thiết kế Back CP318 mới thành ảnh toàn thân góc sau và các vùng tóc–gáy–vai, khoét hông, tay áo/phụ kiện. Bảng xem sạch `CP319_LamThien_Clean_Primary_Back_Review.png` đã lưu trong Library `/Thanh Van Ky/`; gói bàn giao `TVK_CP319_LamThien_Clean_Review_Design_Gates.zip` ở cùng thư mục.
- **NGUỒN:** Ảnh CP318 725×981 RGB với SHA-256 `29bca1bb136394bcca3b31f05b0c4f43e8dbe15766f921436d2a27649e729e26`. Các hình chi tiết là crop từ cùng ảnh nguồn, KHÔNG phải sprite tách lớp. Hình tóc bay là concept riêng trong poster, KHÔNG phải frame từ rig.
- **QUẢN LÝ CANON:** Thêm `docs/art/LAM_THIEN_DESIGN_REGISTRY.json` để phân biệt **đặc điểm đã được người dùng chốt** (2026-10-27) với **ảnh concept CP318 chưa được duyệt riêng**. CP317 proxy và PNG Back cũ bị hạn chế chỉ cho lịch sử/kỹ thuật, không dùng làm preview sản xuất.
- **CÔNG CỤ:** Thêm `tools/art/validate_design_registry.py` và `tests/art/test_design_registry.py`; 5/5 bài kiểm thử trạng thái trong môi trường cục bộ PASS. Ba kiểm tra crop/sha nguồn trên file CP318 cũng PASS tại máy làm việc; GitHub CI chưa xác nhận.
- **KHÔNG ĐƯỢC TUYÊN BỐ:** CP318/CP319 chưa có art layer, phép đo +17% chính xác, alpha/Spine rig/physics hay APK; không tự chuyển CP318 thành bản canon đã được duyệt.
- **TIẾP TỤC CP320:** Sau khi người dùng duyệt/điều chỉnh ảnh Back, phát triển bộ hình nhất quán Front/Back/3/4, vẽ layer có alpha và underpaint; kiểm tra tóc–gáy–vai, khoét hông, tay áo, trang sức và chuyển động trước rig/physics. Chi tiết tại `docs/art/LAM_THIEN_CP319_DESIGN_REVIEW.md`.

### Lịch sử cập nhật 2026-10-28
Tạo ảnh review Back sạch và bổ sung gate không cho concept chưa duyệt/proxy lỗi thời đi vào asset sản xuất.



---

## 20. Lâm Thiển — ảnh mẫu đã chốt & chuẩn tham khảo nhân vật sau (2026-10-28)

- **ĐÃ CHỐT CHÍNH THỨC:** Người dùng xác nhận “ok chốt như này nha” với bảng ảnh Lâm Thiển cuối cùng trong cuộc trò chuyện. Đặt `lam_thien_visual_reference_approved_2026_10_28` làm bản hình ảnh chính thức (canon art reference) hiện hành; **không dùng lại CP317 proxy, CP318 và CP319 preview cũ** làm chuẩn ngoại hình.
- **ẢNH GỐC:** `TVK_LamThien_Approved_Reference_20261028.png` — 1672×941 px RGB, SHA-256 `4b6cbf29ee8aef6aa2d927e7bb89428a9fda5bca1bb67a3f1c7b08e3a94129fd`. [Mở file trên Google Drive (đã xác minh)](https://drive.google.com/file/d/10jKNq-VL62sv1gez5PHlVT9QKyJp_Cvd/view?usp=drivesdk). Sao lưu ChatGPT Library: `/Thanh Van Ky/Approved References/TVK_LamThien_Approved_Reference_20261028.png`.
- **THÀNH PHẦN ĐÃ CHỐT CHO LÂM THIỂN:** tóc bạc dài, phụ kiện hoa, tông trắng–xanh nhạt–vàng, **dây/trang sức vàng vừa đủ**, dáng thanh thoát, tỷ lệ cơ thể/đường cong nhất quán giữa front/side/back/3/4, phần hông khoét theo mẫu, bảng biểu cảm và phụ kiện. Tiếp tục giữ quyết định tăng +17% dành **riêng cho Lâm Thiển** trong lịch sử; **không suy ra số đo pixel chính xác** từ poster.
- **POSE/BỐI CẢNH ĐÃ DUYỆT:** các cảnh tương tác trong phòng với giường, ghế/sofa, mép giường, tường; pose nằm, quỳ ngoảnh lại, ngồi giường, ngồi ghế và dựa tường. Vẫn phân biệt `bed_recline` (nằm ngửa nghỉ ngơi theo đặc tả trước đó) và `bed_kneel_forward` (quỳ/ngoảnh lại), không đánh đồng chỉ vì ảnh poster vẽ các góc khác nhau.
- **ÁP DỤNG CHO NHÂN VẬT SAU:** dùng ảnh làm **chuẩn chất lượng art, bố cục bảng turnaround, biểu cảm, chi tiết trang phục vừa phải, cách thể hiện pose indoor và danh sách phân lớp**. Không sao chép gương mặt, màu tóc, trang phục, tỷ lệ hình thể hoặc +17% của Lâm Thiển sang nhân vật khác.
- **PHÂN BIỆT TRẠNG THÁI:** ảnh là **concept phẳng đã duyệt**, chưa phải ORA/Spine rig, physics, animation thật hoặc APK. Các số đo/chiều cao/ngày sinh trên poster do hình minh họa thể hiện **chưa được chốt riêng**, không tự nhập thành canon game.
- **TÀI LIỆU CHUẨN:** `docs/art/LAM_THIEN_APPROVED_REFERENCE_2026_10_28.md`, `docs/art/CHARACTER_ART_DIRECTION_REFERENCE.md` và `docs/art/LAM_THIEN_DESIGN_REGISTRY.json` (đã chuyển từ CP318 pending sang approved mới). Chỉ sau khi tách lớp/hình pose, QA và duyệt từng bước mới tích hợp rig/physics/APK.

### Lịch sử cập nhật 2026-10-28
Chốt ảnh tạo hình Lâm Thiển mới nhất, lưu ảnh nguyên bản trên Drive và Library; ghi quy trình tham khảo dùng chung và khóa chống hồi quy ảnh cũ.


---

## 21. Lâm Thiển — lộ trình thay đồ và hư hại trang phục khi chiến đấu (2026-10-28)

- **Đã chốt trước:** Có nút thay/cởi lớp ngoài trong màn Nhân vật và hư hại trang phục trong chiến đấu. Mức nguyên vẹn **100% / 70% / 50% / 30%**, tác động toàn bộ nhóm trang phục; ở mức cuối vẫn che phủ phù hợp. Độ nguyên vẹn quần áo khác lượng da lộ và không tự hồi khi hồi HP.
- **Nên làm cùng lúc với tách lớp:** Lấy [ảnh Lâm Thiển đã chốt 28/10/2026](https://drive.google.com/file/d/10jKNq-VL62sv1gez5PHlVT9QKyJp_Cvd/view?usp=drivesdk) làm chuẩn tạo layer áo, tay áo, váy/vạt, phụ kiện, underpaint; chuẩn bị bốn bộ texture tương ứng và biến thể tháo lớp áo ngoài để không phải sửa lại rig.
- **Tương tác/gameplay:** Artwork 2D hiển thị lần đầu chạm mốc hư hại mới và có trạng thái tiếp nối qua màn Nhân vật/hội thoại/tương tác khi có asset. Việc cởi/thay trang phục khác với bị rách do chiến đấu. **Ánh xạ chính xác sát thương/HP sang độ bền chưa chốt riêng**, không tự áp 70% HP = 70% quần áo.
- **Trạng thái:** Mới có ảnh concept và bộ khung nút/trạng thái, chưa có sprite bốn mức, rig, animation hay APK được nghiệm thu. Không ghi đã hoàn thành.
- **Chi tiết triển khai:** [Kế hoạch trang phục và hư hại Lâm Thiển](art/LAM_THIEN_OUTFIT_DAMAGE_IMPLEMENTATION_PLAN.md). Không dùng mẫu CP317/318 cũ để tạo biến thể.

### Lịch sử 2026-10-28
Ghi kế hoạch xử lý trang phục cùng giai đoạn phân lớp theo đề nghị của người dùng, giữ nguyên các quyết định đã chốt trước.


### Bổ sung thiết kế 30% & đề xuất trang phục riêng tư (2026-10-28)

- **ĐÃ CHỐT:** Khi trang phục hư hại xuống mức **30%**, ngay cả các mảnh vải còn lại để che phủ cũng phải **có dấu hư hại rõ** (rách mép, sờn, chỉ bung, vải xô lệch) chứ không giữ nguyên như mới. Không làm lộ trực diện vùng nhạy cảm; phần che phủ vẫn sử dụng cấu trúc nhiều lớp có chủ đích. Mốc 30% vẫn chỉ là **độ nguyên vẹn trang phục**, không phải % da lộ ra.
- **ĐỀ XUẤT / CHƯA CHỐT:** Cởi/thay trang phục có thể chia ba trạng thái: trang phục đầy đủ → tháo áo ngoài → nội y fantasy có lớp voan/lưới mỏng phủ ngoài và lớp lót không xuyên thấu tại vùng cần che phủ. Người dùng đang cân nhắc nội y trong suốt; **chưa coi đã duyệt ba mức hoặc mẫu nội y cuối cùng**.
- **QUY TẮC CẤU TRÚC:** Trạng thái tháo/thay đồ là trục riêng, không đồng nhất 4 cấp độ hư hại 100/70/50/30. Ghi quy chuẩn và ma trận art ở [LAM_THIEN_OUTFIT_DAMAGE_IMPLEMENTATION_PLAN.md](art/LAM_THIEN_OUTFIT_DAMAGE_IMPLEMENTATION_PLAN.md). Chưa có sprite/rig/animation đã hoàn tất cho biến thể mới.


---

## 22. Lâm Thiển — chốt phương án hư hại/trang phục & đồng bộ tư thế (2026-10-28)

- **ĐÃ CHỐT PHƯƠNG ÁN THAM CHIẾU MỚI:** Người dùng chọn một ảnh qua `blob:https://chatgpt.com/8d8b9f33-3a9b-47c6-a677-c31dd0dcfccc`, đồng thời yêu cầu ghi làm chuẩn tham khảo và **áp dụng cả khi đổi tư thế**. Đây là URL tạm trong trình duyệt, **chưa lấy được file bytes**, không thể gọi là ảnh đã upload hay kiểm chứng. Không thay bằng ảnh cũ mà gắn nhãn mới.
- **MỨC RÁCH:** Điều chỉnh khỏi phương án tăng +20% cố định; ưu tiên **giảm bớt độ rách cho hợp lý** theo lựa chọn mới. Giữ các mức độ nguyên vẹn **100/70/50/30**, kể cả vải che phủ còn lại ở 30% vẫn có dấu hư hại nhưng giữ che phủ phù hợp.
- **TƯ THẾ / TƯƠNG TÁC:** Mọi biến thể trang phục và độ hư hại **giữ cùng trạng thái** khi đổi Front/Back/Side/3/4, quỳ/nằm trên giường, ngồi giường/ghế/sofa, tựa tường, hội thoại và chiến đấu. Vết rách bám đúng cấu trúc lớp vải, thay đổi theo trọng lực/tư thế; biểu cảm, hành động phù hợp từng hoàn cảnh.
- **THAY/CỞI ĐỒ:** Trạng thái riêng với hư hại chiến đấu; phương án voan/lưới chỉ được khóa chi tiết chính xác sau khi nhận tệp ảnh nguồn. Giữ lớp che phủ phù hợp.
- **NGUỒN CHUẨN:** Ngoại hình gốc Lâm Thiển vẫn tham chiếu [ảnh đã lưu chính thức](https://drive.google.com/file/d/10jKNq-VL62sv1gez5PHlVT9QKyJp_Cvd/view?usp=drivesdk). Ảnh biến thể trang phục vừa chốt cần **tải lên lại dạng PNG/JPG** để lưu và xác minh. Xem [hồ sơ quyết định mới](art/LAM_THIEN_CLOTHING_VARIANT_APPROVAL_2026_10_28.md).
- **TRẠNG THÁI KỸ THUẬT:** Chốt yêu cầu bằng chữ, **chưa xác minh ảnh blob mới**, chưa có sprite từng tư thế/mức và rig/APK cho các biến thể này. Không đánh dấu sản xuất hoàn tất.

### Lịch sử cập nhật 2026-10-28
Bổ sung quyết định chọn biến thể trang phục mới và quy tắc đồng bộ trạng thái qua tư thế; bỏ yêu cầu tăng mức rách +20% cố định, giữ ràng buộc nguồn ảnh chưa thể truy xuất.


---

## 23. Lâm Thiển — lưu ảnh tham khảo biểu cảm/pose và giữ mức cởi cuối khi đổi tư thế (2026-10-28)

- **ẢNH ĐÃ TẢI LÊN THÀNH CÔNG, THAY THẾ TRẠNG THÁI `blob:` CHƯA TRUY CẬP Ở MỤC 22:** [Bảng biểu cảm, hành động, trạng thái đồ và tư thế](https://drive.google.com/file/d/1M-6KIEeon7HX4Qn56UlhGMfV76Lr-sN5/view?usp=drivesdk) (1672×941, SHA-256 `96caa07b59abd998f905dc19da732a3ebe455ab50863d934865da9a4eace94b2`), [Bảng kế hoạch art/rig/gameplay](https://drive.google.com/file/d/1ZgMB8nkRlkar3-MYCrH32uQaYxO29S5Q/view?usp=drivesdk) (1672×941, SHA-256 `380d21c2b8f6e862ce7b7a9f4b751e8625716a9c02b06b3bb672e4d0dc49b31a`). Hai ảnh do người dùng đính kèm trực tiếp; đã lưu cả nguyên bản trong Google Drive và ChatGPT Library. Xem [hồ sơ nguồn ảnh và quy tắc](art/LAM_THIEN_EXPRESSION_ACTION_REFERENCE_2026_10_28.md).
- **ĐÃ CHỐT BỔ SUNG:** Biến thể thay/cởi đồ ở **mức cuối** phải giữ nguyên khi đổi pose và góc nhìn, từ mặt trước/sau/3-4 tới nằm/quỳ/ngồi giường, ngồi ghế/sofa, dựa tường, cả chuyển giữa tương tác/hội thoại/chiến đấu. Không tự động mặc lại hoặc giảm mức cởi. Mỗi pose phải dùng asset `wardrobe_state × pose` phù hợp, đồng bộ biểu cảm/hành động, tóc và vải. **Nếu chưa có ảnh đúng pose thì giữ trạng thái lựa chọn nhưng báo thiếu ảnh, không dùng ảnh mặc đủ thay thế gây hiểu nhầm**.
- **STATE ĐỘC LẬP:** `wardrobe_state` và `clothing_integrity` 100/70/50/30 là hai trục độc lập. Bốn mức hư hại đã chốt, điều chỉnh độ rách tự nhiên, không tăng cứng +20%; cấp 30% cả vải che phủ còn lại cũng có dấu hao mòn. Hồi HP không tự phục hồi vải.
- **PHÂN BIỆT THAM CHIẾU VỚI TRIỂN KHAI:** Bảng ảnh mới là nguồn thiết kế biểu cảm/hành động/trang phục, không thay thế ảnh Lâm Thiển canon về hình thể được chốt riêng tại mục 20. Số liệu nhân vật xuất hiện trong poster AI không được tự gán thành thông số game; ảnh layer trong poster không phải sprite layer thật. Chưa có bộ art từng pose/wardrobe/damage, rig hay APK hoàn chỉnh.

### Lịch sử 2026-10-28
Đã nhận 2 PNG thật, lưu kiểm chứng hash; xác nhận mức cởi cuối vẫn áp dụng qua mọi tư thế.


---

## 24. QUY CHUẨN CHUNG — trang phục, hư hại và trạng thái khi đổi tư thế (2026-10-28)

- **ĐÃ CHỐT CHUNG CHO TOÀN BỘ NHÂN VẬT HIỆN TẠI VÀ SAU NÀY**: Khi đổi tư thế/góc nhìn/chuyển cảnh, **TẤT CẢ mức trang phục** (`default`, `outer_removed`, mức cuối `private_fantasy` nếu nhân vật có, hoặc biến thể riêng) **phải giữ nguyên**. Không chỉ riêng mức cởi cuối của Lâm Thiển. Mọi nhân vật cũng giữ `integrity` (100/70/50/30) độc lập với `wardrobe`, và đổi biểu cảm/hành động theo bối cảnh.
- **ĐÃ THÊM BỘ QUẢN LÝ CHUNG:** `CharacterAppearanceState.kt` lưu 5 key theo ID nhân vật: wardrobe, integrity, pose, expression, action. `CharacterInteractionActivity.kt` dùng resolver tìm đúng asset; thiếu ảnh thì không tự hiển thị lại trang phục đầy đủ. Màn Nhân vật của Tô Nguyệt Ly chia sẻ độ nguyên vẹn, không còn sử dụng riêng chỉ số demo cho hiệu ứng này. Thư viện asset khai báo tổ hợp các mức hư hại cho cả Tô Nguyệt Ly và Lâm Thiển, cùng danh sách pose bổ sung ở trạng thái chờ asset.
- **ĐÃ CHỐT KHI THIẾU ẢNH:** Phải giữ giá trị state đã chọn và báo thiếu tệp thật, tắt hotspot phụ thuộc art; không giả mạo bằng crop, flip hay ảnh khác. Vết rách nằm đúng cấu trúc vải ở mọi góc nhìn; các lớp che phủ còn lại ở 30% cũng hư hại nhưng vẫn che kín phù hợp.
- **CHƯA HOÀN THÀNH MỸ THUẬT:** Khai báo đường dẫn và placeholder không đồng nghĩa đã có texture pose × wardrobe × damage. Chưa có bộ sprite tất cả trạng thái, rig Spine hoặc APK được nghiệm thu.
- **ĐẶC TẢ CHUNG BẮT BUỘC:** [GLOBAL_CHARACTER_APPEARANCE_SPEC.md](art/GLOBAL_CHARACTER_APPEARANCE_SPEC.md) và quy chuẩn art [CHARACTER_ART_DIRECTION_REFERENCE.md](art/CHARACTER_ART_DIRECTION_REFERENCE.md). Kiểm tra metadata qua `tools/validate_global_appearance.py` và `tests/art/test_global_appearance.py`; build pipeline cũng chạy kiểm tra global. Rule dùng cho **mọi nhân vật mới**, không chép số đo/hình thể của Lâm Thiển sang nhân vật khác.

### Lịch sử cập nhật 2026-10-28
Nâng yêu cầu giữ mức cởi khi đổi pose từ nhân vật Lâm Thiển thành **luật toàn dự án cho mọi mức**. Thêm code lưu trạng thái toàn nhân vật, data placeholder và gate kiểm tra asset.


---

## 25. Lâm Thiển — CHỐT MẪU NGOẠI HÌNH GỐC CANON BODY V2 (2026-10-28)

**ĐÃ CHỐT:** Người dùng chốt chính ảnh Lâm Thiển mới nhất đính kèm ngày 28/10/2026 làm **model gốc trực quan CANON V2**. Ảnh PNG RGBA 1672×941 / 3,747,713 bytes, [đã xác minh trên Drive](https://drive.google.com/file/d/1mEsyn2wMo-MVQqhtbmdUiFfO8AaYhzUR/view?usp=drivesdk); SHA-256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711`. ChatGPT Library: `/Thanh Van Ky/Approved References/Lam_Thien_Canon_V2_20261028/`. Trạng thái là **ảnh tạo hình đã duyệt**, chưa phải layered sprite/Spine rig hay APK.

- **Body đã chốt qua hình ảnh V2:** hình thể, khuôn mặt, chiều cao cảm nhận, đường nét ngực/eo/hông giữ như ảnh chuẩn qua mọi góc. Không tự nhân đôi kích thước hay cộng lại phần +17% đã quyết định trong lịch sử khi làm từ V2.
- **Trang phục đã chốt:** tông trắng–xanh nhạt, chất liệu **lụa mềm, voan rủ**, phụ kiện vàng ít và tinh tế; loại bỏ viền phụ kiện kim loại vàng dày, đặc biệt vùng viền áo thân trên. Các trạng thái trang phục trong game phát triển trên mẫu V2 này và phù hợp bối cảnh.
- **THẺ SỐ DỄ NHỚ:** `LT_CANON_BODY_REF_2026-10-28_V2`; chỉ số **chuẩn hóa trực quan** của bốn nhóm (bust/waist/hips/height) được lấy **100% = chính V2**, giúp so các pose mới với ảnh mẫu. Gợi ý B/W/H 102/60/110 từ trao đổi cũ chỉ là ký hiệu minh họa chưa đo hoặc chốt theo cm, **không** dùng làm thông số vật lý, rig hay lore. Ảnh gốc + SHA luôn ưu tiên hơn mọi số đề xuất.
- **TỪ V1 SANG V2:** Registry `docs/art/LAM_THIEN_DESIGN_REGISTRY.json` đã đưa V1 vào `archived_approved_designs`. CP317/318/319 và các preview khác là lịch sử. Bộ ảnh biểu cảm/pose đã chốt trước dùng bổ trợ về **hành động**, không tự áp lại body/trang phục V1.
- **TOÀN GAME:** Các mức wardrobe (default / outer_removed / private_fantasy hoặc mức khác), độ bền 100/70/50/30 và biểu cảm/hành động giữ trạng thái theo ID nhân vật khi đổi pose; áp dụng cho tất cả nhân vật, nhưng **không sao chép body Lâm Thiển sang nhân vật khác**.
- **PLAN / NGHIỆM THU:** [LAM_THIEN_NEXT_TASKS_AFTER_CANON_V2.md](art/LAM_THIEN_NEXT_TASKS_AFTER_CANON_V2.md): P0 kiểm chứng art nguồn và tách layer/sửa tám pose, P1 texture trạng thái/Spine/animation, P2 gameplay QA/build APK và đóng gói template dùng chung. **Mỗi bước chỉ đánh dấu hoàn thành khi có artifact thật + kiểm thử.**
- **THẺ DỮ LIỆU:** [LAM_THIEN_MODEL_CARD_V2.json](art/LAM_THIEN_MODEL_CARD_V2.json), [tài liệu model gốc](art/LAM_THIEN_CANON_BODY_V2_2026_10_28.md).

### Lịch sử cập nhật 2026-10-28 (Canon V2)
Đã nhận/chốt PNG V2, lưu nguyên bản Drive/Library, lập model card và checklist, chuyển V1 sang lịch sử và khóa quy tắc tránh đoán số đo từ poster.


---

## 26. Toàn bộ nhân vật — bổ sung bẩn, xước và rách trang phục theo hư hại (2026-10-28)

**ĐÃ CHỐT từ người dùng:** Các tình trạng trang phục sau chiến đấu phải thể hiện phối hợp **vết bẩn**, **vết xước/sờn trên chất liệu**, và **vết rách**. Mức tăng phù hợp với độ tổn hại: `100%` nguyên vẹn; `70%` nhẹ; `50%` trung bình; `30%` nặng, kể cả các mảnh vải còn đảm nhiệm che phủ cũng mang dấu sờn/rách nhưng vẫn che phủ phù hợp. Không đặt mức tăng cố định +20% hoặc nhầm con số này với tỷ lệ da lộ ra.

- **PHÂN BỐ THEO NGUYÊN NHÂN:** Các hình thức hư hại có thể khác nhau theo va chạm/môi trường/chất vải: có tình huống thiên về bụi bẩn, có tình huống thiên về cọ xát/sờn, có tình huống làm rách đường may. Không bắt buộc mỗi lần trúng đòn tạo cả ba vết với cùng độ nặng.
- **TRẠNG THÁI VÀ TƯ THẾ:** Tổn hại phải bám cùng cấu trúc quần áo khi đổi Front/Back/Side/3⁄4, nằm, quỳ, ngồi, dựa tường; không tự xóa hoặc thêm dấu vết chỉ do đổi pose. `wardrobe` và `integrity` vẫn độc lập, giữ theo nhân vật khi chuyển cảnh/hội thoại/chiến đấu. Hồi HP không tự giặt/sửa đồ.
- **PHẠM VI:** Áp dụng cho **tất cả nhân vật hiện tại và tương lai**; Lâm Thiển làm mẫu triển khai đầu tiên theo **CANON BODY V2**.
- **NGUỒN KỸ THUẬT:** [GLOBAL_CLOTHING_DAMAGE_VISUAL_STANDARD.md](art/GLOBAL_CLOTHING_DAMAGE_VISUAL_STANDARD.md) là chuẩn art; `app/src/main/assets/character_interactions.json` có `appearanceSystem.damageVisualProfile` và `tools/validate_global_appearance.py` có kiểm tra metadata tương ứng; [kế hoạch Lâm Thiển V2](art/LAM_THIEN_NEXT_TASKS_AFTER_CANON_V2.md) đã có việc tạo/dò preview.
- **PHÂN BIỆT HOÀN THÀNH:** Đã lưu quyết định và lập profile metadata, **chưa có hình texture/animation thực** cho vết bẩn, xước hay rách; cần duyệt preview rồi mới tách layer/rig và xác minh APK.

### Lịch sử 2026-10-28
Bổ sung quy tắc đa dạng dấu hư hại theo mức độ và nguyên nhân, thống nhất xuyên tư thế/nhân vật. Không thay ảnh canon V2 hiện tại.


---

## 27. Lâm Thiển — CHỐT PREVIEW 4 MỨC HƯ HẠI (2026-10-28)

**ĐÃ CHỐT BẰNG HÌNH ẢNH:** Người dùng duyệt preview bốn cột 100% / 70% / 50% / 30%, ngày 28/10/2026. 100% sạch nguyên vẹn; 70% bụi/xước/rách rất nhẹ; 50% bẩn rõ và sờn/rách vừa; 30% bẩn/xước/rách nhiều **kể cả vùng vải còn che phủ**, vẫn giữ che phủ phù hợp. Không tự sửa mức độ tổn hại khác preview đã duyệt.

- **Nguồn đối chiếu:** PNG 1672×941 RGB trong cuộc trò chuyện, SHA-256 `03251b5ec9b020b325687b530c98e026622ba7b3334466ab5d2323a0a89c9e23`. Chưa xác minh lưu bền vững lên Drive/GitHub; cần upload PNG nguồn trước khi triển khai art.
- **TOÀN BỘ NHÂN VẬT:** áp dụng 4 cấp và quy tắc chuyển pose/cảnh, giữ nguyên `wardrobe_state` và `clothing_integrity` độc lập; không sao chép body Lâm Thiển sang các nhân vật khác.
- **Triển khai:** dựng texture riêng cho từng mức/góc/pose, kiểm rig, alpha và hiệu ứng lần đầu tụt ngưỡng; hồi HP không tự sửa quần áo, thiếu asset không lấy nhầm ảnh lành thay thế.
- **TRẠNG THÁI:** preview/cấp độ **APPROVED**; sprite, rig, physics, animation và APK **PENDING**.
- **TÀI LIỆU CHI TIẾT:** [LAM_THIEN_DAMAGE_PREVIEW_APPROVED_2026_10_28.md](art/LAM_THIEN_DAMAGE_PREVIEW_APPROVED_2026_10_28.md).

### Lịch sử 2026-10-28
Ghi xác nhận chính thức của người dùng cho preview hư hại bốn mức, đóng băng mức độ trực quan và bổ sung checklist nghiệm thu.


---

## 28. CP320 — khởi động P0-02/P0-03 sau khi chốt damage preview (2026-10-28)

- **ĐÃ LÀM:** xác minh Drive vẫn có mẫu ngoại hình `LT_CANON_BODY_REF_2026-10-28_V2`, tạo bản sao lưu nguyên byte của PNG hư hại bốn mức đã duyệt vào ChatGPT Library và thêm ma trận view/pose/layer, validator, unit tests.
- **HỒ SƠ CP320:** [LAM_THIEN_CP320_HANDOFF.md](art/LAM_THIEN_CP320_HANDOFF.md); [LAM_THIEN_CP320_VIEW_CALIBRATION.json](art/LAM_THIEN_CP320_VIEW_CALIBRATION.json); `tools/check_lam_thien_cp320.py`; `tests/art/test_lam_thien_cp320.py`.
- **CHƯA HOÀN THÀNH:** ảnh full-body thống nhất Front/Back/Side/3⁄4, landmark đo trực tiếp, layer PNG alpha/ORA/PSD và phép thử Spine/physics. Bản V2 trên Drive là **ảnh phẳng**, không được đánh dấu đã rig hoặc đã có art nhiều trạng thái.
- **ƯU TIÊN:** Front–Back → Side/3⁄4 → bảy landmark mỗi view → chia layer → kiểm seam/underpaint/draw order → mới triển khai texture hư hại. Chốt 100/70/50/30 giữ nguyên.
- **QUY TẮC:** Mẫu +17% đã nằm trong V2, không cộng lại. View/pose/wardrobe/integrity giữ riêng; preview damage là hướng hình ảnh, chưa là asset game.

### Lịch sử 2026-10-28
Thực hiện bàn giao CP320 và lưu PNG preview; cập nhật trạng thái kỹ thuật minh bạch, chưa đóng P0.


---

## 29. CP321 — đã chuẩn bị ORA Front/Back, art tách lớp vẫn CHỜ (2026-10-28)

- **ĐÃ TẠO CÓ FILE THẬT:** bộ `TVK_LamThien_CP321_Empty_ORA_Templates.zip` (checksum trong [CP321 handoff](art/LAM_THIEN_CP321_HANDOFF.md)), gồm 2 file ORA Front/Back kích thước 2048×3072, mỗi file 15 layer art RGBA rỗng + guide. Đã sao lưu ChatGPT Library. Đây là **editable scaffold**, không phải sprite chia lớp.
- **QA THỰC TẾ:** cả hai ORA CRC PASS, canvas đúng, alpha có nội dung **0/15 layer** mỗi file; do đó **P0-02/P0-03/P1/rig/APK chưa được nghiệm thu**.
- **CODE KIỂM TRA:** `tools/validate_lam_thien_cp321_ora.py` và `tests/art/test_lam_thien_cp321_ora.py`, bổ sung kiểm kích thước và loại PNG RGBA, gate strict để ngăn template rỗng được nhận là production art. Kiểm thử CI GitHub chưa xác minh.
- **TIẾP TỤC:** hoàn thiện hình full-body Front/Back chất lượng đủ, đo 7 landmark, vẽ và kiểm các lớp, sau đó mới rig Spine; ảnh V2 chính thức và mức hư hại đã chốt không thay đổi.
- **TÀI LIỆU BÀN GIAO:** [LAM_THIEN_CP321_HANDOFF.md](art/LAM_THIEN_CP321_HANDOFF.md).

### Lịch sử 2026-10-28
Đối chiếu nguồn và kiểm tra artifact ORA thật; ghi trạng thái đúng, chưa tự đánh dấu hoàn thành art hoặc rig.


---

## 30. CP322 — thử nghiệm pipeline PNG alpha, CANON V2 vẫn bất biến (2026-10-28)

- **ĐÃ LÀM KỸ THUẬT:** tạo 5 PNG RGBA native-resolution từ *preview chưa duyệt* để thử alpha/export, ZIP backup Library, manifest checksum, validator PNG IDAT/CRC/alpha và unit test 4/4 PASS trong container.
- **TUYỆT ĐỐI KHÔNG NHẬP CANON:** tạo hình bản thử có khác biệt so với V2. Không sử dụng nó để thay ngoại hình Lâm Thiển, tự đổi tỷ lệ +17%, tạo sprite/Spine production hoặc thay bốn mức hư hại đã duyệt.
- **CHƯA ĐẠT P0-02/P0-03:** cần art full-body đạt chuẩn riêng cho Front/Back/Side/3/4, 7 mốc đo và 15 lớp art thực trong ORA; không suy từ crop poster/PNG alpha demo. Rig, physics và APK vẫn chờ.
- **TÀI LIỆU:** [CP322 handoff](art/LAM_THIEN_CP322_ALPHA_TRIAL_HANDOFF.md), [manifest nguồn nháp](art/LAM_THIEN_CP322_ALPHA_TRIAL_MANIFEST.json), `tools/validate_lam_thien_cp322_proxy.py`, `tests/art/test_lam_thien_cp322_proxy.py`.
- **ĐIỂM TIẾP TỤC:** tạo art Front/Back mới **theo V2 gốc** và gửi duyệt, rồi chỉnh các lớp ORA/tay áo/tóc/underpaint. Không đánh dấu đã rig/APK.

### Lịch sử 2026-10-28
Cập nhật bản thử alpha có ảnh thật, lưu audit và phân biệt nghiêm với art đã được duyệt; giữ nguyên P0/P1/P2.


### Bổ sung CP322 — kiểm chứng test và nguồn art (2026-10-28)
Đã lưu bản dự thảo khác CANON V2 tại **Library Development** (không đẩy vào Approved References); hoàn tất kiểm tra 5 PNG alpha/IDAT/CRC và 4 unit test local PASS. CI workflow `.github/workflows/cp322-art-alpha-validation.yml` đã được tạo nhưng **chưa có bằng chứng kết quả GitHub Actions**. Source draft SHA256 `f171a06f9d67cb510cd46067a30d12763850620970e3d724c93d5c8a681c2d60`, ZIP SHA256 `bf73215eaa09baa27d024c0aeaf864137a90d1d06d3291bc5e2975790062a437`. Hình ảnh này **KHÔNG ĐƯỢC DUYỆT, KHÔNG THAY CANON V2**, P0-02/P0-03 chưa đóng.


---

## 31. CP323 — OpenRaster pixel-level QA (2026-10-29)

**ĐÃ LÀM THỰC:** Tạo công cụ `tools/validate_lam_thien_cp323_layers.py`, 5 bài kiểm thử PNG/ORA thực và workflow `.github/workflows/cp323-openraster-art-gate.yml`. Test local 5/5 PASS. Giải mã PNG alpha thực và kiểm tra hai ORA Front/Back từ CP321: cấu trúc hợp lệ nhưng **0/15 lớp art có pixel ở cả hai**, chế độ `--strict` chặn sản xuất như kỳ vọng. Gói kết quả và ảnh kiểm tra sao lưu vào ChatGPT Library Development.

- **CANON GIỮ NGUYÊN:** `LT_CANON_BODY_REF_2026-10-28_V2`, PNG SHA256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711`, +17% đã nằm trong V2. Các ảnh tạo mới chưa khớp V2 **không được duyệt và không thay thế** mẫu chính thức. Bốn mức độ nguyên vẹn 100/70/50/30 đã duyệt vẫn giữ nguyên.
- **CHƯA HOÀN TẤT:** chưa có ảnh Front/Back toàn thân độ phân giải sản xuất theo V2, chưa đo 7 landmarks trên ảnh fullbody, chưa có bộ art 15 lớp thật / rig Spine / physics hoặc APK mới nghiệm thu. P0-02, P0-03, P1, P2 giữ trạng thái đang chờ.
- **NEXT:** dựng Front/Back full-body đúng V2 và gửi preview → đo anchor → nhập artwork từng layer/kiểm underpaint, alpha và draw order → nghiệm thu mỹ thuật **riêng** với gate kỹ thuật → rig → gameplay/APK.
- **HỒ SƠ:** [LAM_THIEN_CP323_HANDOFF.md](art/LAM_THIEN_CP323_HANDOFF.md), `tools/validate_lam_thien_cp323_layers.py`, `tests/art/test_lam_thien_cp323_layers.py`. Kết quả GitHub Actions chưa được xác minh; test local không có nghĩa CI đã PASS.

### Lịch sử cập nhật 2026-10-29
Bổ sung bằng chứng QA file thật để chặn template trống bị nhận là sprite; giữ nguyên thiết kế đã duyệt và ranh giới công việc còn thiếu.


---

## 32. Lâm Thiển — phân biệt rõ 5 biểu cảm (2026-10-29, CHỜ DUYỆT PREVIEW)

Theo đề nghị của người dùng, cần điều chỉnh **cả 5 biểu cảm**: `shy` (Ngại ngùng), `angry` (Tức giận), `pain` (Đau đớn), `embarrassed` (Xấu hổ), `alluring` (Quyến rũ), không chỉ hai biểu cảm đầu/cuối. Khóa quy tắc phân biệt qua ánh mắt/lông mày/miệng/độ ửng má/hướng đầu: `shy` tránh ánh nhìn nhẹ, `embarrassed` né mạnh và đỏ mặt rõ; `angry` mắt sắc/mày ép, `pain` mắt co/mày nhíu cong; `alluring` giao tiếp mắt chủ động, cười mỉm tinh tế.

- **ĐÃ TẠO:** preview 1536×1024 PNG RGB và đặc tả 5 biểu cảm. File preview được sao lưu tại ChatGPT Library Development: `/Thanh Van Ky/Development/Lam_Thien_Expression_5_20261029/LAM_THIEN_5_EXPRESSIONS_PREVIEW_PENDING_20261029.png` (SHA256 `ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7`).
- **CHỜ DUYỆT:** ảnh preview mới và độ nhấn cụ thể; không tự coi ảnh này là model canon hoặc sprite production. **CANON BODY/FACE V2** `LT_CANON_BODY_REF_2026-10-28_V2` và mẫu hư hại 100/70/50/30 đã chốt giữ nguyên.
- **SAU KHI DUYỆT:** dựng lại các biểu cảm đúng V2 trên mặt thật, tách mắt/lông mày/miệng/ửng má/giọt lệ tùy cần, rig/animation/QA ở UI hội thoại và góc Front/3-4, đồng bộ `expression` mà không reset wardrobe/integrity/pose.
- **TÀI LIỆU:** [Đặc tả biểu cảm 5 loại](art/LAM_THIEN_FIVE_EXPRESSIONS_REVIEW_2026_10_29.md), [metadata JSON](art/LAM_THIEN_FIVE_EXPRESSIONS_REVIEW_2026_10_29.json). Chưa có file tách lớp/rig/APK đã nghiệm thu cho biểu cảm mới.

### Lịch sử 2026-10-29
Lập preview và tiêu chuẩn phân biệt năm nét mặt để người dùng duyệt trước khi cập nhật asset chính thức.


---

## 33. CHỐT 5 BIỂU CẢM LÂM THIỂN & ÁP DỤNG CHUNG NHÂN VẬT (2026-10-29)

**ĐÃ CHỐT** theo xác nhận trực tiếp của người dùng sau khi xem preview 5 biểu cảm: “tôi thích như này, chốt biểu cảm này nha. Note vào cho tôi để tránh bị quên và làm sai hoặc nhầm khi hoàn thiện nhân vật. Các nhân vật khác cũng nên như này nhưng tinh chỉnh lại xíu cho các nhân vật khác”.

- **LÂM THIỂN — MẪU CHÍNH THỨC CHO NÉT MẶT:** 5 biểu cảm `shy` (Ngại ngùng), `angry` (Tức giận), `pain` (Đau đớn), `embarrassed` (Xấu hổ), `alluring` (Quyến rũ). Ảnh đã duyệt `TVK_LamThien_5_Expressions_APPROVED_20261029.png`, SHA256 `ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7`, 1536×1024 RGB. Đã sao lưu trong ChatGPT Library `/Thanh Van Ky/Approved References/Lam_Thien_Expressions_20261029/`.
- **KHÔNG ĐỔI BODY CANON V2:** `LT_CANON_BODY_REF_2026-10-28_V2` tiếp tục là model chính thức duy nhất cho khuôn mặt/cơ thể/tóc/trang phục/tỷ lệ. Preview biểu cảm chỉ chốt **cách diễn đạt cảm xúc**, không thay ngoại hình nền. Mốc +17% đã nằm trong V2.
- **KHÔNG ĐƯỢC NHẦM NĂM NÉT MẶT:** `shy` né mắt nhẹ/hồng má nhẹ, `embarrassed` cúi đầu/né mắt nhiều hơn/đỏ má rõ; `angry` mắt sắc/mày ép, `pain` mắt co/mày nhíu cong; `alluring` mí hạ nhẹ và nụ cười chủ động. Phải nhận diện được cả 5 trong chân dung hội thoại, không chỉ lúc zoom.
- **MỌI NHÂN VẬT CHÍNH TRƯỞNG THÀNH PHÙ HỢP:** cùng hệ thống năm sắc thái rõ ràng và cách nghiệm thu, nhưng điều chỉnh mắt/mày/miệng/má/góc đầu/theo tính cách riêng; **không copy hình thể, mặt, tóc, trang phục, tỷ lệ hoặc sprite của Lâm Thiển**. Tô Nguyệt Ly và nhân vật tiếp theo phải có preview biểu cảm **riêng** trước khi chốt.
- **TRẠNG THÁI GAME:** `expression` độc lập với `wardrobe`, `integrity`, `pose`, `action`; không reset trang phục/hư hại khi đổi cảm xúc. Không sử dụng biểu cảm tình cảm/quyến rũ ở nhân vật chưa trưởng thành hay bối cảnh không thích hợp.
- **NGHIỆM THU:** hình preview của 5 biểu cảm Lâm Thiển **APPROVED**, còn PNG alpha tách nét mặt, Spine rig/animation và tích hợp APK **PENDING**. Những nhân vật khác mới **APPROVED về nguyên tắc tùy biến**, chưa duyệt art từng người.
- **TÀI LIỆU CHÍNH:** [5 biểu cảm Lâm Thiển đã duyệt](art/LAM_THIEN_FIVE_EXPRESSIONS_APPROVED_2026_10_29.md) và [JSON](art/LAM_THIEN_FIVE_EXPRESSIONS_APPROVED_2026_10_29.json); [quy chuẩn chung](art/GLOBAL_CHARACTER_EXPRESSION_STANDARD_2026_10_29.md); `LAM_THIEN_DESIGN_REGISTRY.json` lưu riêng approved expression profile.

### Lịch sử 2026-10-29
Người dùng xác nhận preview 5 biểu cảm đã đạt yêu cầu; chuyển từ review sang Approved, lưu checksum + bản sao ảnh, chuẩn hóa quy tắc riêng từng nhân vật, không sửa body canon hoặc tự nhận đã rig.


---

## 34. CP324 — kết nối 5 biểu cảm Lâm Thiển đã chốt vào Android (2026-10-29)

**ĐÃ THỰC HIỆN CODE, CHƯA NGHIỆM THU ART/ANDROID APK:**

- **KHÔNG THAY CANON:** body/face/costume vẫn `LT_CANON_BODY_REF_2026-10-28_V2` (+17% đã có). Ảnh năm biểu cảm `LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED` là chuẩn **cách thể hiện cảm xúc**, chưa phải ảnh face tách lớp.
- Bổ sung `app/src/main/assets/character_expression_profiles.json` ghi đúng năm ID đã duyệt `shy, angry, pain, embarrassed, alluring` của Lâm Thiển, `sprite_paths={}` vì chưa có sprite. Tô Nguyệt Ly vẫn `individual_preview_required`, không dùng mặt của Lâm Thiển.
- Bổ sung `CharacterExpressionCatalog.kt` giải quyết sprite theo bộ khóa **characterId × expression × wardrobe × integrity × pose**, chỉ chấp nhận file `characters/{characterId}/...` có thật. Nếu thiếu thì trả null/hiển thị thiếu ảnh, **không fallback sang biểu cảm hoặc trang phục khác**.
- Bổ sung bộ chọn năm biểu cảm trong `CharacterInteractionActivity.kt`, cùng nút trở về `normal` (nút reset, **không phải loại cảm xúc mới**). **Đã sửa lỗi đổi pose tự đặt lại expression normal/relaxed; mở wardrobe không xóa biểu cảm đang lưu.** `expression` vẫn độc lập với `wardrobe/integrity/pose/action`.
- Đã cắt nguyên pixel từ ảnh đã duyệt thành 5 ảnh chân dung và 5 ảnh cận mắt/miệng (**REFERENCE ONLY**), ZIP SHA256 `d12dfa89ac0ae002095effd4d2e789d31bbcb09c23a1f4b857da29e4b906ca1a`, backup Library Approved References tại `/Thanh Van Ky/Approved References/Lam_Thien_Expressions_20261029/CP324_Reference_Handoff/`. Không nhận crop làm PNG alpha/rig thật.
- **Kiểm thử:** Kotlin resolver chạy local với mock Android JSON/State **11/11 PASS**; thêm Python contract tests và GitHub Actions workflow `cp324-expression-runtime.yml`, **CI trên GitHub và APK chưa xác minh**. Chưa thay P0-02/P0-03 và P1-03 từ pending thành done.
- **TÀI LIỆU:** [CP324 handoff](art/LAM_THIEN_CP324_EXPRESSION_RUNTIME_HANDOFF.md), [manifest crop](art/LAM_THIEN_CP324_APPROVED_EXPRESSION_CROPS_MANIFEST.json), [hồ sơ 5 biểu cảm APPROVED](art/LAM_THIEN_FIVE_EXPRESSIONS_APPROVED_2026_10_29.md).

### Lịch sử 2026-10-29
Tiến hành tích hợp metadata, chọn và lưu expression trong Android; sửa pose reset, kiểm strict missing-art; giữ ranh giới art/rig/APK chưa hoàn thành.


---

## 35. CP325 — 5 ORA vùng mặt biểu cảm; chưa là sprite game (2026-10-29)

- **THỰC HIỆN:** dùng đúng ảnh năm biểu cảm Lâm Thiển được duyệt (`LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED`, SHA256 `ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7`), tạo **5 file ORA**, mỗi file 7 lớp pixel patch alpha RGBA và 1 ảnh hướng dẫn ẩn (**35 vùng alpha thật**). Tạo annotation sheet, bảng so biểu cảm kích thước 132px/64px, manifest + SHA/CRC.
- **CHỈ LÀ REFERENCE:** đây là các phần vùng ảnh nhỏ cắt/matte từ poster phẳng, **chứa da/tóc nền lẫn trong patch**, không phải mắt/mày/miệng tách độc lập/underpaint, không phải art được vẽ lại từ CANON V2 và **không được coi là rig/Spine-ready**. Kích thước ảnh native 285–303×385; không khai báo vào `sprite_paths`.
- **KẾT QUẢ QA:** local test 5/5 PASS cho hợp lệ ORA/CRC/alpha/nguồn pixel, chế độ `--strict` FAIL đúng kỳ vọng (chưa có art thật). `tools/cp325/validate_cp325_face_proxies.py`, `tests/art/test_cp325_face_proxy_contract.py`, workflow `.github/workflows/cp325-face-proxy-contract.yml` (GitHub Actions chưa xác minh). Gói ZIP SHA256 `8cc9bac61fb843c84444cae57668318f9d5c40a3538d7e8262ae585493aacf3e`.
- **LƯU TRỮ:** gói `TVK_LamThien_CP325_Face_Region_Prototypes_NOT_SPINE_READY.zip` và ảnh kiểm tra đã sao lưu ChatGPT Library tại `/Thanh Van Ky/Development/CP325_Face_Region_Prototypes/`.
- **CANON BẤT BIẾN:** body/mặt/trang phục theo `LT_CANON_BODY_REF_2026-10-28_V2` (tỷ lệ +17% đã có); năm biểu cảm `shy/angry/pain/embarrassed/alluring` đã chốt, không hỏi duyệt lại concept; giữ damage 100/70/50/30. Với nhân vật khác chỉ dùng **quy chuẩn phân biệt cảm xúc**, không copy face/body.
- **CHƯA HOÀN TẤT:** P0-02/P0-03, P1-03 sprite/rig thật, Android APK build, CI chưa nghiệm thu.
- **BƯỚC TIẾP THEO CP326:** trên mặt thật CANON V2 vẽ layer mắt/mày/miệng/má độc lập với underpaint/alpha; QA 132px/64px và pose/wardrobe/integrity, rồi mới khai báo asset/Spine và build/test APK.
- **BÀN GIAO:** [LAM_THIEN_CP325_FACE_ART_HANDOFF.md](art/LAM_THIEN_CP325_FACE_ART_HANDOFF.md) và [manifest](art/LAM_THIEN_CP325_FACE_REGION_PROXY_MANIFEST.json).

### Lịch sử 2026-10-29
Có thêm ORA alpha tham chiếu *thực* và QA; không đánh tráo trạng thái bản reference thành sản phẩm art/canon/rig.


### Bổ sung CP325 — GitHub CI đã xác minh (2026-10-29)

Kiểm tra thực tế GitHub Actions trên commit `4cab946f91efdaf5c08988df85f76bb2d0b88929`: CP325 metadata contract run `40804686901` **SUCCESS**, CP324 runtime contract run `40804686882` **SUCCESS**, approved-expression consistency run `40804686885` **SUCCESS**. Đây là các kiểm tra code/metadata, **không phải Gradle APK**, không kiểm trực tiếp file ORA Library và không thay P0/P1 thành DONE. Kiểm tra ORA 5/5 PASS là kết quả local riêng. Xem [CP325 handoff](art/LAM_THIEN_CP325_FACE_ART_HANDOFF.md).


---

## 36. CP326 — 5 biểu cảm dùng chung một nền mặt CANON V2, layer alpha vẽ độc lập (2026-10-29)

**ĐÃ TẠO ART THỬ/ĐÃ QA KỸ THUẬT; CHƯA ĐƯỢC DUYỆT LÀ SPRITE GAME:**

- Trích nguồn face từ đúng `LT_CANON_BODY_REF_2026-10-28_V2`, SHA256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711`, bbox `[1160,0,1390,114]`. **Native 230×114 px**; làm việc trên canvas 920×456 chỉ là phóng 4×, KHÔNG gọi là ảnh HD.
- Dựng 5 bộ biểu cảm `shy, angry, pain, embarrassed, alluring` từ đúng bộ được duyệt (`LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED`) bằng **35 layer RGBA độc lập vẽ mới** (mắt/mày/miệng/má); 5 file ORA, mỗi file kèm base underpaint **inpaint tự động tạm thời** và guide canon gốc ẩn. Khác pixel patch CP325 ở chỗ các layer không chứa da/tóc cắt từ poster.
- **Kiểm thử LOCAL:** 6/6 unittest PASS; 5 ORA đều có alpha, khớp ảnh composite, CRC/stack hợp lệ; `--strict` FAIL đúng dự kiến do prototype chưa được duyệt.
- **CHƯA ĐẠT ART:** nét vẽ độc lập hiện chưa khớp mức tinh tế của mẫu được duyệt; nền inpaint là bản tạm; full-body/face nguồn đủ phân giải và ORA 15 layer của CANON V2 vẫn thiếu. **Không** dùng làm `sprite_paths`, không rig, không APK.
- **LƯU TRỮ:** ZIP `TVK_LamThien_CP326_Vector_Face_Prototype_NOT_GAME_READY.zip`, SHA256 `377086143ce7a85449e9ade18d1de02f64431ba15e8c8024b2ce5bc86f37f4f6`, Library Development `/Thanh Van Ky/Development/CP326_Vector_Face_Prototype/`. Mã tái tạo `tools/cp326/create_cp326_face_vectors.py`, QA `tools/cp326/validate_cp326_face.py`, JSON `LAM_THIEN_CP326_VECTOR_FACE_MANIFEST.json`.
- **P0/P1-03/P2 CHƯA ĐÓNG:** đã duyệt CANON V2 và 5 biểu cảm nhưng chưa có production face art, Spine runtime hoặc APK mới được kiểm thử. Không gọi 35 layer demo là asset hoàn tất.
- **ĐIỂM TIẾP TỤC CP327:** nguồn V2 layer/fullbody thực hoặc vẽ lại đúng canon ở độ phân giải đủ → underpaint thật/face attachments → QA cỡ thoại và các góc → rig/Spine → APK.
- **TÀI LIỆU:** [LAM_THIEN_CP326_FACE_VECTOR_HANDOFF.md](art/LAM_THIEN_CP326_FACE_VECTOR_HANDOFF.md).

### Lịch sử 2026-10-29
Đã chuyển từ pixel-patch CP325 sang *layer vector riêng* CP326 và ghi rõ mức trung thực của hình ảnh; chuẩn canon/5 cảm xúc bất biến.


---

## 37. CP327 — kiểm atlas 35 lớp nét mặt và đối chiếu CANON V2 (2026-10-29)

**ĐÃ LÀM BẰNG FILE THẬT (TECH PIPELINE):** xuất **35 thành phần RGBA** từ năm ORA CP326 chưa được duyệt thành atlas thử `2048×2048` và manifest `expression × part × atlas bbox × original offset`. Có nguồn ZIP/PNG và checksum, **5/5 local unit tests PASS**; từng vùng atlas đã so trực tiếp byte RGBA với source ORA, không overlap. Sửa lỗi alpha-composite làm đổi RGB má: phiên bản cuối dùng direct copy `paste`, SHA atlas **`2ef4e619e6d496598db835093e1be5f72ca8b7385ee3bfdc84f24188d7ea9739`**, ZIP cuối **`69be3de41b2e33dd15dd67899b27bb2b7a4ef86813afe3e91443f7b51e1b14db`**.

- **ART MỚI CHƯA CHỐT:** poster CP327 mới có mắt thiên xanh và chi tiết mặt/phụ kiện khác CANON V2; chỉ làm ví dụ nghiên cứu, **không thay ảnh body V2, không dùng sprite mới**, bất kể text trên poster có nhắc Spine/2048. Ảnh chuẩn V2 mắt hổ phách vẫn là mẫu chính thức. Năm biểu cảm APPROVED chỉ quyết định nét cảm xúc.
- **KHÔNG PHẢI SPINE ATLAS:** export ở đây là PNG + JSON **engine-neutral** từ CP326 vector demo, không có skeleton/mesh/underpaint production, không có APK. Strict gate FAIL theo thiết kế, `sprite_paths` không thay.
- **LƯU TRỮ:** Library Development `/Thanh Van Ky/Development/CP327_Rig_Atlas_Preflight/` chứa ZIP, PNG atlas, contact sheet so sánh, mã export/validate/test. GitHub có `tools/cp327/export_cp327_atlas.py`, `tools/cp327/validate_cp327_atlas.py`, `tests/art/test_cp327_atlas_contract.py` và CI metadata `.github/workflows/cp327-face-atlas-preflight.yml`.
- **CHƯA HOÀN THÀNH:** P0-02/P0-03, face art production P1-03, Spine rig/animation, Android APK. Nguồn khuôn mặt V2 hiện chỉ 230×114 px; phải phục hồi/vẽ lại master độ phân giải thật và underpaint before production.
- **NEXT CP328:** vẽ face master đúng CANON V2 → tách lớp độc lập mỹ thuật → QA kích thước hội thoại/góc → rig Spine/Android → APK; không hỏi chốt lại các mẫu đã duyệt.
- **BÀN GIAO:** [LAM_THIEN_CP327_RIG_ATLAS_HANDOFF.md](art/LAM_THIEN_CP327_RIG_ATLAS_HANDOFF.md), [CP327 manifest](art/LAM_THIEN_CP327_ART_GATE_MANIFEST.json).

### Lịch sử 2026-10-29
Đóng gói atlas PNG/JSON và khắc phục lỗi giữ nguyên pixel alpha, lưu các mẫu art nháp ở Development (không làm canon), chỉ tăng mốc kỹ thuật.


---

## 38. CP328 — Color Lock cho face master Lâm Thiển (2026-10-29)

**ĐÃ HOÀN THÀNH QA NGUỒN V2; CHƯA HOÀN THÀNH ART MỚI/SPRITE/SPINE/APK.**

- Đọc chính PNG body `LT_CANON_BODY_REF_2026-10-28_V2` đã duyệt (SHA256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711`). Crop mặt gốc từ poster bbox `[1160,0,1390,114]` có **230×114 px native**, không có art nguồn HD. Mắt hổ phách/vàng ấm là chuẩn; tóc bạc, cấu trúc mặt/hoa/phụ kiện/trang phục giữ nguyên.
- Năm biểu cảm `LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED` `shy/angry/pain/embarrassed/alluring` tiếp tục là chuẩn sắc thái **không thay mặt V2**. Mức hư hại 100/70/50/30 giữ nguyên, độc lập với expression/wardrobe/pose.
- **Kết quả pixel local:** hai vùng mắt trên native V2 có 124 và 105 pixel khớp dải HSV amber, 0 pixel khớp dải blue. Đây là heuristic trên vùng mắt **có cả da/lông mi**, nên chỉ là cảnh báo sai màu rõ rệt, không thay visual review hay phân đoạn mống mắt chuẩn.
- Đã tạo `tools/cp328/cp328_face_color_gate.py`: kiểm SHA nguồn V2, cho phép kiểm thêm ảnh vẽ mới bằng hai ROI mống mắt do artist đánh dấu; **9/9 local tests PASS** gồm trường hợp cố ý đổi một hoặc hai mắt sang xanh và ROI không hợp lệ. Có bảng QA đối chiếu V2/5 biểu cảm và ZIP backup Library Development SHA256 `4fe87b2ce4610da81919215ed3395d01f0a4a699fe472d6ba965c433755a360e`.
- **KHÔNG DUYỆT ART MỚI:** Các poster CP328 mới do công cụ tạo ảnh có mắt xanh và chữ “production ready” trang trí, **không phải source sản xuất** và không thể làm bằng chứng sprite/Spine. Không nhập các hình đó vào Approved References hoặc `sprite_paths`.
- **CI:** thêm `tests/art/test_cp328_color_contract.py` và workflow `.github/workflows/cp328-face-color-lock.yml` chạy synthetic và metadata; riêng binary V2 chỉ được kiểm local vì chưa có trên GitHub. Chưa có nghiệm thu Android APK.
- **CP329 TIẾP THEO:** khôi phục/vẽ lại *native high-res* face master khớp V2 (mắt hổ phách), underpaint chuẩn, vẽ 5 biến thể nét mặt có alpha thật → preview & art QA ở 132px/64px, Front/3⁄4 → mới rig/Spine/Android APK.
- **BÀN GIAO:** [LAM_THIEN_CP328_FACE_IDENTITY_HANDOFF.md](art/LAM_THIEN_CP328_FACE_IDENTITY_HANDOFF.md), [CP328 gate JSON](art/LAM_THIEN_CP328_FACE_MASTER_GATE.json).

### Lịch sử 2026-10-29
Đã đo từ CANON V2 và bổ sung regression test chống sai màu mắt; khóa nguồn thiết kế, **không đánh dấu P0/P1/P2 đã xong**.


---

## 39. CP329 — khung tách khuôn mặt đúng CANON V2 (2026-10-29)

**ĐÃ CÓ FILE THẬT ĐỂ TIẾP TỤC VẼ, KHÔNG PHẢI ART SẢN XUẤT ĐÃ XONG:**

- **CANON V2 BẤT BIẾN:** `LT_CANON_BODY_REF_2026-10-28_V2` SHA256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711` (mặt/mắt hổ phách/tóc/phụ kiện/trang phục/tỷ lệ +17% đã có). **5 BIỂU CẢM BẤT BIẾN:** `LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED` SHA256 `ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7`. Damage `100/70/50/30` giữ nguyên.
- Tạo *artist intake studio* gồm `CP329_FACE_MASTER_EMPTY.ora` (11 layer art để vẽ), **5 ORA biểu cảm × 7 layer** (các lớp mắt/mày/miệng/má), một ảnh nguồn thật 230×114 và bảng đối chiếu với đúng 5 nét đã duyệt. Canvas 2048×2048 là **canvas làm việc; guide ảnh gốc được phóng ×8 chỉ để căn chỉnh, không phải HD mới**.
- **Kết quả QA:** 6/6 OpenRaster hợp lệ, 8/8 bài test file thật local PASS; **0/46 layer art có nội dung mới**, `--strict` FAIL đúng kỳ vọng. Không xem việc tạo khung ORA là P0-02/P0-03/P1-03 hoàn thành.
- **GitHub:** `tools/cp329/create_cp329_intake.py`, `tools/cp329/validate_cp329_intake.py`, `tests/art/test_cp329_face_contract.py`, CI workflow `cp329-face-art-intake.yml` và `LAM_THIEN_CP329_FACE_INTAKE_MANIFEST.json`. CI CP329 trên commit tạo workflow, run `40812464457` đã **SUCCESS** (metadata/synthetic), không kiểm binary ORA trong Library. CI CP328 đã sửa lỗi manifest và xác nhận SUCCESS.
- **LƯU FILE:** ZIP `TVK_LamThien_CP329_Face_Master_Intake_NOT_GAME_READY.zip` SHA256 `e6b8e952b2a7028ac2314cf95d5fb0c94d008b9c0baf6c2064dc2b7130c91b9d`, sao lưu ChatGPT Library Development `/Thanh Van Ky/Development/CP329_Face_Master_Intake/`. Không đưa ảnh phóng to hoặc poster nháp mắt xanh vào production.
- **CP330 TIẾP TỤC:** vẽ lại face master có chất lượng native đủ pixel + clean underpaint, 35 attachment nét mặt thật theo biểu cảm duyệt, kiểm CP328 màu mắt, cỡ thoại 256/132/64, Front/3⁄4, sprite art QA riêng → Spine/runtime → APK. Không hỏi chốt lại những mẫu người dùng đã duyệt.
- **BÀN GIAO:** [LAM_THIEN_CP329_FACE_MASTER_HANDOFF.md](art/LAM_THIEN_CP329_FACE_MASTER_HANDOFF.md), [CP329 manifest](art/LAM_THIEN_CP329_FACE_INTAKE_MANIFEST.json).

### Lịch sử 2026-10-29
Hoàn thành gói ORA và regression tests để bàn giao redraw; vẫn xác nhận production art và Android APK chưa nghiệm thu.


---

## 40. CP330 — 5 khuôn mặt bản thử có 35 layer alpha ảnh thật (2026-10-29)

**CP330 QA KỸ THUẬT HOÀN THÀNH, CHƯA HOÀN THÀNH FACE MASTER SẢN XUẤT:**

- **CANON không đổi:** `LT_CANON_BODY_REF_2026-10-28_V2` (SHA256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711`, tỷ lệ +17% đã có, mắt hổ phách). 5 biểu cảm đã chốt `LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED` (SHA256 `ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7`). Mức hư hại 100/70/50/30 không đổi.
- Từ **một bảng minh họa AI MỚI chưa duyệt** đã xuất 5 chân dung ứng viên native **251–260×370 px**, tách **5 ORA × 7 layer alpha vùng nét mặt = 35 layer có pixel thật**, với `face_base_cutout` khuyết đúng vị trí và **underpaint OpenCV tự động**. Ghép bình thường **khớp pixel với bản nháp mới**; thử dịch mắt/miệng không tạo lỗ alpha.
- **KHÔNG NHẬN LÀ production art:** năm chân dung vẫn khác hình mặt canon và chưa cùng một face master; các patch là pixel vùng ảnh, có thể dính da/tóc; underpaint thuật toán chưa được artist duyệt; độ phân giải native không đủ cho sprite master. Những chữ *Final Art/Spine Ready* trên tranh sinh tự động **không chứng minh art được phân lớp/rig**.
- **Test local:** 9/9 PASS, SHA/CRC/7 lớp mỗi biểu cảm/alpha cutout/composite; `--strict` cố ý **FAIL**. Không khai báo vào `sprite_paths`, không coi P0-02/P0-03/P1-03 hoặc APK đã DONE.
- **ZIP Library Development** `/Thanh Van Ky/Development/CP330_Face_Painted_Region_Trial/TVK_LamThien_CP330_Face_Art_Decomposition_NOT_APPROVED.zip`, SHA256 `a1e1f4ec14d89263ff6797a445cc93c4e7140a1e08f1930bfee27d2560842172`. GitHub có builder, ORA validator, JSON source, metadata tests và workflow CI `cp330-face-art-trial.yml`.
- **CP331 NEXT:** vẽ **một master mặt high-res đúng V2** + underpaint được hoàn thiện thủ công; 35 attachment độc lập được vẽ lại cho 5 biểu cảm; preview ở 256/132/64, kiểm pose Front/3⁄4 và damage state, nghiệm thu mỹ thuật sprite; sau đó mới Spine và APK.
- **BÀN GIAO:** [LAM_THIEN_CP330_FACE_TRIAL_HANDOFF.md](art/LAM_THIEN_CP330_FACE_TRIAL_HANDOFF.md).

### Lịch sử 2026-10-29
Từ ORA CP329 trống chuyển sang thí nghiệm CP330 có các lớp mặt thật từ bản nháp riêng, không nâng nhầm lên canon hoặc rig.


---

## 41. CP331 — dùng chung một nền khuôn mặt cho năm biểu cảm (2026-10-29)

**KẾT QUẢ KỸ THUẬT THỰC, CHƯA PHẢI ART GAME ĐÃ DUYỆT:**

- **Hai quyết định bất biến:** BODY/FACE `LT_CANON_BODY_REF_2026-10-28_V2` (SHA256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711`, mắt hổ phách, +17% đã có), 5 biểu cảm `LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED` (SHA256 `ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7`); mức damage 100/70/50/30 và wardrobe/pose độc lập.
- CP330 dùng năm nguồn ảnh mặt khác nhau; CP331 thử **một base FLAT duy nhất** (258×364 native từ poster **mới chưa duyệt**), lắp 7 vùng cảm xúc × 5 thành **35 alpha patch thật/5 file ORA**. Tóc, phụ kiện, trang phục, vùng ngoài ROI nét mặt không thay pixel khi chuyển expression. Có ảnh đối chiếu V2 và preview 132/64px, GIF mô phỏng chuyển hình.
- **9/9 unit tests local PASS**, audit ORA thật (CRC, 7 alpha layers mỗi file, compositor preview, cùng layer base, bất biến pixel ngoài ROI). `--strict` **FAIL có chủ đích** để ngăn dùng production. Đây là kiểm thử kỹ thuật, không phải nghiệm thu hình.
- **CHƯA ĐẠT MỸ THUẬT:** Bản tạo mới CP331 SHA `a923f2125fbac40bd3a5975cc50d22ff12926d4f69b6d461d76f6be647c8a729` chưa được duyệt và không tự thay CANON V2; các mảnh vẫn chứa da/tóc, base còn **mắt/mày/miệng baked**, underpaint OpenCV chỉ ở lớp ẩn, native 258×364 không phải master HD. Poster sinh tự động có chữ *Production Ready* không đáng tin về tình trạng sprite.
- **LƯU TRỮ:** ZIP `TVK_LamThien_CP331_Shared_Face_Technical_Trial_NOT_APPROVED.zip`, SHA256 `e48174f1b0831942cc03f0ff5a0f98d51ae83ee01540135f24b6ffa9b2232578`, ChatGPT Library `/Thanh Van Ky/Development/CP331_Shared_Face_Technical_Trial/`. GitHub lưu manifest, code tạo/audit, công cụ QA, tài liệu art work-order và workflow chỉ kiểm metadata.
- **P0-02/P0-03/P1-03/P2 KHÔNG ĐỔI DONE:** art khuôn mặt master chất lượng native, underpaint họa sĩ, 35 attachment semantic, Spine rig và APK vẫn chưa có nghiệm thu.
- **CP332 TIẾP THEO:** dựng art highres thật từ nhận diện CANON V2, vẽ underpaint sạch không baked mắt/môi, làm 5 biểu cảm trên cùng master rồi QA 256/132/64px và Art Preview duyệt riêng; sau đó mới rig/Spine/Android.
- **HỒ SƠ:** [CP331 handoff](art/LAM_THIEN_CP331_SHARED_FACE_HANDOFF.md), [manifest](art/LAM_THIEN_CP331_SHARED_FACE_TRIAL_MANIFEST.json), [artist work order](art/LAM_THIEN_CP331_ARTIST_WORK_ORDER.md).

### Lịch sử 2026-10-29
Giảm sai lệch nhận dạng giữa năm bản face nháp bằng thử nghiệm dùng chung một nền; không thay bản đã chốt và không đánh dấu các patch là sprite game.


---

## 42. CP332 — master vector sạch và 65 layer biểu cảm ngữ nghĩa (2026-10-29)

**ĐÃ CÓ ART VECTOR PHÂN LỚP THẬT ĐỂ THỬ KỸ THUẬT, CHƯA ĐẠT MỸ THUẬT CANON HOẶC SPINE/APK.**

- **Hai nguồn đã duyệt không đổi:** CANON `LT_CANON_BODY_REF_2026-10-28_V2` SHA256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711`; mẫu 5 biểu cảm `LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED` SHA256 `ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7`. Tỷ lệ +17% đã có trong V2, mắt hổ phách, tóc/phụ kiện/trang phục và damage `100/70/50/30` bất biến.
- **Tiến bộ so với CP331:** CP331 có một raster master chứa mắt/miệng baked và dùng ảnh crop có lẫn da/tóc. CP332 vẽ **SVG vector mới ở canvas 1024×1024**: 1 OpenRaster face master với **10 lớp nền** gồm **da underpaint sạch (không có mắt/mày/miệng cũ)**, và **5 ORA biểu cảm** dùng **10 lớp nền cùng byte/hash** nhưng thêm **13 lớp RGBA ngữ nghĩa riêng mỗi trạng thái**, **65 attachment alpha thật**: sclera, iris hổ phách, lông mi, mí, chân mày, má, môi.
- **Kết quả kiểm:** 6 ORA binary mở được/ZIP CRC/stack đúng, lớp alpha có pixel, recomposite từ layer trùng mergedimage, skin đầy đủ dưới mắt/môi, 5 expression khác nhau; **10/10 bài test local PASS**. `--strict` cố ý **BLOCK** vì chưa có duyệt art.
- **LƯU:** `TVK_LamThien_CP332_Semantic_Face_Study_NOT_APPROVED.zip`, SHA256 `a70a383076592c986bd887bd4477c71b6c60f9bf13a3e711b9c20b1376dbeb01`, 173 tệp/CRC PASS, Library Development `/Thanh Van Ky/Development/CP332_Semantic_Face_Study/`. GitHub `tools/cp332/build_cp332.py`, `tools/cp332/validate_cp332.py`, `tests/art/test_cp332_semantic_source_contract.py`, workflow `cp332-semantic-face-contract.yml` chỉ kiểm source/metadata; ORA binary được QA local riêng.
- **KHÔNG TỰ NHẬN art production:** bản vector CP332 có nét khá đơn giản, không đủ giống anime face CANON V2, cần tinh chỉnh lại tỷ lệ/anatomy và nghệ thuật; canvas 1024 vector chỉ là kỹ thuật, không phải chứng minh art đúng canon, không đủ Front/3⁄4/Side hoặc animation. **Không đăng ký `sprite_paths`**, không đánh dấu P0-02/P0-03/P1-03/P2 DONE.
- **CP333 tiếp theo:** họa sĩ redraw/phát triển lớp nét mặt **trên cùng cấu trúc semantic** để khớp V2, hoàn thiện skin/hair underpaint, test 256/132/64px, Front/3⁄4 và biến dạng, gửi preview nghiệm thu asset mới → mới Spine/Android/APK.
- **Tài liệu:** [CP332 handoff](art/LAM_THIEN_CP332_SEMANTIC_FACE_HANDOFF.md), [manifest](art/LAM_THIEN_CP332_SEMANTIC_STUDY_MANIFEST.json).

### Lịch sử cập nhật 2026-10-29
Đã nâng từ patch R&D CP331 sang SVG art thật tách theo bộ phận CP332, vẫn trung thực trạng thái NOT APPROVED để các bước sau không sử dụng nhầm.


### Bổ sung CP332 — xác minh GitHub CI (2026-10-29)

Đã kiểm tra trực tiếp GitHub Actions CP332: run `40819544556` / job `123268528135` **SUCCESS**. CI xác minh mã vector, metadata và một số layer RGBA tổng hợp, **không đọc sáu ORA nhị phân** trong Library. Các bài kiểm ORA thật **10/10 PASS local** vẫn là chứng cứ riêng; trạng thái mỹ thuật `NOT APPROVED`, Spine/APK `NOT DONE` không thay đổi.


---

## 43. CP333 — tinh chỉnh 65 layer nét mặt độc lập trên cùng master (2026-10-29)

- **Hai chuẩn đã duyệt vẫn là nguồn duy nhất:** CANON BODY/FACE `LT_CANON_BODY_REF_2026-10-28_V2` (SHA256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711`), năm biểu cảm `LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED` (SHA256 `ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7`). Mắt hổ phách, tóc bạc, trang phục trắng-xanh-vàng, tỷ lệ +17% đã trong V2, damage 100/70/50/30 **không thay đổi**.
- **ĐÃ LÀM ART VECTOR R&D THỰC:** trên CP332 chỉnh các nét SVG tóc, hoa/châu vàng, vân/hắt sáng mống mắt hổ phách, mi/đường chân mày/miệng; xuất **6 OpenRaster có art thật** (1 base 10 lớp + 5 expression cùng base và mỗi expression 13 attachment RGBA, **65 lớp nét mặt**). Face base không baked mắt/mày/miệng; các layer base giữ nguyên byte giữa năm trạng thái. Có ảnh so trước/sau và QA hội thoại.
- **QA LOCAL:** 13/13 test trên file ORA thật PASS, ZIP CRC/alpha/composite/ảnh khác nhau và khóa SHA nguồn PASS; production `--strict` FAIL đúng thiết kế; source-only 9/9 test PASS. GitHub workflow `cp333-refined-face-contract.yml` kiểm mã nguồn và metadata, **không có ORA nhị phân trên runner**. Chưa xác minh kết quả CI mới khi ghi phần này.
- **GÓI ART:** `TVK_LamThien_CP333_Refined_Vector_Study_NOT_APPROVED.zip`, SHA256 `1f8aa806758332194e258f941530b18b54e00991c877c3397a274d7c134517ad`, 179 file/ZIP CRC PASS, sao lưu ChatGPT Library Development `/Thanh Van Ky/Development/CP333_Refined_Vector_Study/`. Không chuyển sang Approved References hoặc Android `sprite_paths`.
- **CHƯA ĐẠT MỸ THUẬT:** hình vector còn đơn giản và khác tỷ lệ/độ tinh tế CANON V2; chưa có Front 3/4, underpaint tóc khi deformation hoặc bone/mesh Spine thực; APK chưa build/test. Các chữ “Production Ready” trên infographic AI mới không phải bằng chứng nghiệm thu.
- **CP334 NEXT:** ưu tiên redraw theo chuẩn anime CANON V2 trên các semantic layer đang có, rồi gửi preview **art thành phẩm**; kiểm nét mắt/mày/miệng cả 5 emotion ở 256/132/64px, tạo Front/3⁄4, sửa hair occlusion/underpaint, chỉ sau QA art mới Spine/Android APK.
- **HỒ SƠ:** [CP333 handoff](art/LAM_THIEN_CP333_FACE_POLISH_HANDOFF.md), [manifest](art/LAM_THIEN_CP333_ART_HANDOFF_MANIFEST.json). P0-02/P0-03/P1-03/P2 vẫn chưa nghiệm thu.

### Lịch sử 2026-10-29
Có cải tiến pixel thực trên SVG semantic, xác minh bằng ORA 6 file và regression tests; vẫn giữ ranh giới technical R&D và production art chưa được duyệt.


### CP333 — GitHub Actions verification (2026-10-29)

Workflow `CP333 refined semantic face contract` run `40820930195`, job `123272972666` **SUCCESS**. CI validates repository source/metadata and synthetic SVG alpha, **not the six OpenRaster binaries in Library**. Real binary ORAs were tested locally (13/13 PASS). **Art remains NOT APPROVED; Spine and Android APK remain unverified.** See [CP333 handoff](art/LAM_THIEN_CP333_FACE_POLISH_HANDOFF.md).


---

## 44. CP334 — art direction preview năm biểu cảm Lâm Thiển (2026-10-29)

**ĐÃ TẠO CANDIDATE PREVIEW / CHƯA DUYỆT THÀNH ART GAME:**
- **CANON BODY V2 vẫn là thiết kế đã chốt** `LT_CANON_BODY_REF_2026-10-28_V2` SHA256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711` (+17% đã áp dụng). **5 biểu cảm đã chốt** `LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED` SHA256 `ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7`. Tóc bạc, mắt hổ phách, trang phục trắng–xanh–vàng và mức hư hại 100/70/50/30 không đổi.
- Bản tạo mới CP334: PNG phẳng `1536×1024`, SHA256 `1286237fd958990ffaf69f3b57c6997b00fbcd756d93887c351bb6ee84dda9ee`. Trích đúng 5 chân dung, làm bảng đối chiếu với V2, hướng biểu cảm và thumbnail 256/132/64. Có ORA review **7 lớp chứa các chân dung flat**, **KHÔNG phải semantic face rig**. Chữ *Production Ready* trên ảnh chỉ là text do trình tạo ảnh vẽ.
- Kiểm file thật local: **8/8 tests PASS**, 5 crop khớp byte gốc, ORA ZIP/CRC/7 lớp và nguồn SHA đúng. ZIP `TVK_LamThien_CP334_Art_Direction_Review_NOT_GAME_READY.zip` SHA256 `8602b28f6df43952b6f70adcdffd4c0945bd0463ba6144c449a0a5b192a5dc8b`, Library Development `/Thanh Van Ky/Development/CP334_Art_Direction_Review/`.
- **Chưa đúng mỹ thuật V2:** mới có chi tiết tóc/mắt hổ phách tốt hơn CP333, nhưng trang sức vàng/hoa, neckline và tỷ lệ chi tiết mặt vẫn khác; năm chân dung không chứng minh một master chung. **KHÔNG đăng ký `sprite_paths`**, không gắn vào Spine/APK, không thay ảnh đã được duyệt.
- **CP335 tiếp theo:** redraw một face master high-fidelity từ V2, underpaint thật và attachment mắt/mày/miệng/má semantic tách sạch, art Front/3⁄4, preview QA 256/132/64 và nghiệm thu art riêng rồi mới rig/Spine và APK.
- Tài liệu: [CP334 handoff](art/LAM_THIEN_CP334_ART_DIRECTION_HANDOFF.md), [manifest](art/LAM_THIEN_CP334_ART_REVIEW_MANIFEST.json). CP334 = preview kỹ thuật/mỹ thuật R&D, không đóng các công việc P0-02/P0-03/P1-03/P2.

### Lịch sử 2026-10-29
Tạo preview mỹ thuật chất lượng cao hơn CP333, nhưng tách biệt tình trạng art concept với production rig; ưu tiên sửa tương đồng CANON V2 thay vì thêm pixel patches.


---

## 45. CP335 — khóa art biểu cảm chưa duyệt trước khi dùng trong Android (2026-10-29)

**ĐÃ THỰC HIỆN BUG FIX/TEST TRÊN CODE, KHÔNG PHẢI ĐÃ HOÀN THÀNH ART LÂM THIỂN.**

- **CANON BẤT BIẾN:** ngoại hình V2 `LT_CANON_BODY_REF_2026-10-28_V2`, SHA `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711`; bộ 5 sắc thái `LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED`, SHA `ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7`. Body và màu mắt theo V2, nét cảm xúc theo sheet đã duyệt, tỷ lệ +17% đã nằm trong V2, damage 100/70/50/30 độc lập.
- **CP335 flat candidate:** PNG mới 1536×1024, SHA `7935e04f5fa04c3bd9d772577ad7ddbc806a9e5723629d8b963bb0611d7315d1`, có năm nét mặt nhưng **chưa được người dùng duyệt thành art sản xuất**, phụ kiện/neckline khác V2, thiếu một face master và layer alpha thật. Bảng QA so chuẩn và thumbnail 132/64px đã sao lưu Library Development. Chữ “Production Ready/Spine” bên trong ảnh không phải bằng chứng kỹ thuật.
- **ĐÃ SỬA LỖI ANDROID:** trước đó chỉ cần `sprite_paths` trỏ tới file tồn tại và emotion direction được duyệt là `CharacterExpressionCatalog.resolveSprite` có thể hiển thị; chưa đòi nghiệm thu riêng **sprite art**. Sau CP335 phải có `production_release.status=approved_for_runtime`, QA artist+runtime, **user asset approval riêng**, đúng nguồn ID/SHA, manifest và hash của từng PNG. Nếu thiếu, không trả ảnh và không fallback mức nguyên vẹn/outfit/pose.
- **HAI LOẠI APPROVAL KHÁC NHAU:** 5 biểu cảm **APPROVED REFERENCE**, nhưng mặt/layer/sprite **NOT ART ACCEPTED**. `character_expression_profiles.json` giữ `sprite_paths={}`, `production_release.status=blocked_pending_art` cho Lâm Thiển; Tô Nguyệt Ly chưa được auto-approve.
- **KIỂM THỬ:** `17/17` kịch bản Kotlin compiled local PASS (stub, không phải build Android), `14/14` Python unit test trên ảnh PNG tổng hợp thực PASS. Công cụ `tools/verify_expression_art_release.py` kiểm SHA256 file, alpha RGBA, kích thước native, manifest và chặn đường dẫn thiếu approval. GitHub Actions `CP335 facial art release gate` run `40823727298` **SUCCESS**; CI không có asset CP335 production/Spine/APK.
- **BACKUP:** `TVK_LamThien_CP335_Art_Release_Gate_NOT_APPROVED.zip`, SHA256 `d656146585681ce1a5b05d322fdab3a12eccb2c5f21b2afd6cc9e9d773dcf2df`, Library Development `/Thanh Van Ky/Development/CP335_Art_Release_Gate/`.
- **CP336 TIẾP:** redraw thực một face master Front/3⁄4 đúng CANON V2, clean underpaint, semantic eye/brow/lid/mouth/blush alpha, năm sắc thái dùng cùng base, QA mỹ thuật ở 256/132/64, nghiệm thu sprite thành phẩm → mở release manifest mới → rig/Spine, build APK, test thiết bị. **Không lặp checkpoint từ poster flat hay đổi thiết kế đã chốt.**
- [Hồ sơ CP335](art/LAM_THIEN_CP335_ART_RELEASE_HANDOFF.md), [manifest nguồn](art/LAM_THIEN_CP335_VISUAL_GATE_MANIFEST.json).

### Lịch sử 2026-10-29
Thêm cổng bảo vệ production art thực ở runtime và CI, tách riêng duyệt hướng biểu cảm với duyệt sprite thành phẩm. Giữ P0-02/P0-03/P1-03/P2 chưa nghiệm thu.


---

## 46. CP336 — kiểm 2 nguồn góc mặt CANON và QA 5 biểu cảm phân lớp (2026-10-29)

**ĐÃ XONG KIỂM NGUỒN/QA FRAMEWORK, CHƯA TẠO ART FACE MASTER SẢN XUẤT:**

- Ngoại hình **CANON BODY V2** `LT_CANON_BODY_REF_2026-10-28_V2`, SHA256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711`, và **năm sắc thái đã duyệt** `LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED`, SHA256 `ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7`, **giữ nguyên**. Ngoại hình V2 (mắt hổ phách, tóc bạc, phụ kiện tiết chế) ưu tiên hơn màu mắt/trang phục của sheet biểu cảm; tỷ lệ +17% đã có. Damage 100/70/50/30 độc lập với expression/pose/wardrobe.
- **Kiểm nguồn thực tế:** CANON V2 là poster flat 1672×941. Face crops native: Front-labeled [14,116,159,267] **145×151**, 3/4-labeled [321,116,464,267] **143×151**, closeup [1160,0,1390,114] **230×114**. Front hiện vẫn hơi nghiêng, hai góc gần giống nhau. Đây là **reference pixel thật**, KHÔNG phải 2 master art đủ phân giải. Google Drive folder Canon V2 hiện có PNG/flat ZIP/README/MODEL_CARD, không tìm được ORA/PSD/KRA trong nguồn có quyền truy cập.
- **CP336 mới:** bảng tham chiếu nguồn chính thức và 8 crop lossless; triển khai `tools/cp336/validate_head_layers.py` kiểm 2 góc `front/three_quarter` × 5 biểu cảm × 13 PNG alpha semantic/góc cộng 4 master/góc (138 file nếu xuất đầy đủ). Kiểm SHA, RGBA, canvas/ROI, alpha, underpaint, màu iris amber (heuristic), path traversal. **Không tạo 138 art thật**: số đó mới là PNG fixture tổng hợp.
- **16/16 local test PASS** gồm 12 kiểm thử PNG fixture 138 file và 4 kiểm pixel SHA/nguồn approved thật. `--strict` có chủ đích **FAIL** với fixture thiếu ảnh native ≥1024 và artist/user approval. GitHub Actions `CP336 two-angle facial layer contract` run **40829848852 SUCCESS**; CP335 release gate run **40829848868 SUCCESS**. CI chỉ kiểm nguồn code/metadata và fixture synthetic, không có source ảnh gốc/Spine/APK.
- Ảnh mới CP336 (dạng poster ghi “Production Ready v2.3”) **không phải source layered**, **chưa được user duyệt**, tuyệt đối không đưa vào game. `app/src/main/assets/character_expression_profiles.json` vẫn `production_release.status=blocked_pending_art`, `sprite_paths={}`.
- Gói ZIP `TVK_LamThien_CP336_Source_Master_Gate_NOT_SPINE_READY.zip` SHA256 `29d4f59402243a300357f6ab7e46440956e39bb1f7609cce988f8670daf8bde5` (161 entries, ZIP CRC PASS), Library Development `/Thanh Van Ky/Development/CP336_Face_Master_Source_And_QA/`. [CP336 handoff](art/LAM_THIEN_CP336_FACE_MASTER_HANDOFF.md), [manifest](art/LAM_THIEN_CP336_SOURCE_MASTER_MANIFEST.json).
- **CP337 ưu tiên:** artist vẽ thực native face master Front **nhìn thẳng** và 3/4 đủ khác góc, clean underpaint, tóc/hoa/mi/mày/miệng và bộ 5 cảm xúc alpha semantic trên cùng master mỗi góc. QA ảnh 256/132/64, blink/occlusion và duyệt **ART THÀNH PHẨM riêng**, rồi mới mở CP335 release gate, Spine/Android APK.
- P0-02/P0-03/P1-03/P2 **CHƯA NGHIỆM THU**. Không chốt lại các lựa chọn V2 hoặc 5 cảm xúc.

### Lịch sử 2026-10-29
Tách đúng nguồn Front/3⁄4 và phát hiện góc/nội dung pixel chưa đủ rig; có cổng QA đo được trước khi nhận art thật thay vì lặp thêm poster/crop rồi tự gọi “Production Ready”.


---

## 47. CP337 — thực hiện head artwork thật, Front + 3/4 (2026-10-29)

- **Đã kiểm chứng nguồn và mở quy trình redraw thực**: CANON V2/5 biểu cảm nguồn như mục 46; source Drive CANON hiện vẫn chỉ có ảnh phẳng, ZIP ảnh, README, MODEL_CARD, chưa có ORA/PSD/KRA tìm thấy trong quyền truy cập hiện tại.
- Đã gửi yêu cầu vẽ **một chân dung FRONT độc lập, không phải infographic** dựa trên hình CANON V2, task Runway `880ac92b-bf38-48ae-bd33-e7fde597efd8`. **Trạng thái khi ghi tài liệu: PENDING**; chưa quan sát và chưa duyệt ảnh hoàn chỉnh. Không tuyên bố đã có master production/native editable source; không có asset 3/4 được duyệt.
- **Tiêu chuẩn CP337:** Front nhìn trực diện thật và 3/4 khác góc thật, giống mặt V2, mắt hổ phách, tóc bạc, hoa trắng và vàng vừa phải; phải vẽ lại 2 face masters editable native thật, underpaint, layer semantic cho 5 emotion, QA thumbnail + biến dạng trước khi phát hành sprite.
- `production_release.status=blocked_pending_art`, `sprite_paths={}` vẫn nguyên. **Chưa DONE:** face art, mesh/Spine, APK. Chữ “Production Ready” trong tranh kỹ thuật không có giá trị nghiệm thu.
- Điểm nối: [CP337 work order](art/LAM_THIEN_CP337_FRONT_THREE_QUARTER_WORK_ORDER.md).


### CP337 — thất bại nghiệm thu nhận diện/body/trang phục (phản hồi người dùng 2026-10-29)

Hai ảnh **Front** (Runway task `880ac92b-bf38-48ae-bd33-e7fde597efd8`) và **3/4** (task `263c4531-2b33-4f2a-9ef5-5f5029a5b450`) đã được tạo ảnh phẳng nhưng **KHÔNG ĐẠT visual QA**: người dùng xác nhận lệch rõ **body và trang phục** so với mẫu chính thức. **Đánh dấu cả hai REJECTED/DEVELOPMENT ONLY**, không dùng làm model, không thêm `sprite_paths`, không rig/Spine/APK.

**Bài học quy trình bắt buộc:** prompting góc mặt mới bằng AI có thể tự thay body, tỉ lệ, áo, neckline, trang sức; lấy một bản sai làm tham chiếu cho bản tiếp theo sẽ nhân lỗi. Không có bảo đảm khớp tuyệt đối chỉ từ prompt. Bắt buộc lấy **CANON V2 làm nguồn body/costume bất biến**, chỉ chỉnh/vẽ vùng head cần thiết, kiểm đối chiếu đủ body/costume trong preview trước khi làm 5 biểu cảm/Spine. Tỷ lệ +17% trong V2, trang phục trắng–xanh–vàng, các trạng thái damage 100/70/50/30 và 5 biểu cảm vẫn giữ nguyên. **CP337 chưa nghiệm thu**.


### CP337 — Quy chuẩn nghiệm thu sai lệch hình ảnh (xác nhận người dùng 2026-10-29)

**Không yêu cầu trùng pixel tuyệt đối**, nhưng bản vẽ mới phải giữ **nhận diện và thiết kế tổng thể như CANON V2**. Phân loại trước khi đưa vào pipeline sản xuất:

- **P0 — Khóa đặc trưng (bắt buộc):** tỷ lệ cơ thể và mốc +17% đã có trong V2; vóc dáng/silhouette và tỷ lệ đầu–thân; đặc trưng khuôn mặt; màu mắt hổ phách; tóc bạc và kiểu tóc chính; kiểu cắt và cấu trúc trang phục, vị trí che phủ, viền/cổ áo, dải màu trắng–xanh–vàng; phụ kiện nhận diện và hoa cài nổi bật. **Không tự thay đổi**.
- **P1 — Sai lệch lớn / phải sửa:** thay khác vóc dáng, neckline/cutout, kiểu áo, mức che phủ, phối màu chính, hoa hoặc phụ kiện nổi bật; thay đổi khuôn mặt khiến nhìn như người khác; lặp sai lệch qua các góc nhìn. **Visual QA FAIL**, không cho vào game.
- **P2 — Chi tiết nhỏ có thể chấp nhận sau đối chiếu:** vài sợi tóc, nếp gấp vải và độ rủ tự nhiên, ánh sáng/đổ bóng, sắc độ hoặc hoa văn phụ rất nhỏ; biến đổi phối cảnh hợp lý khi quay góc 3/4. Chỉ chấp nhận nếu **tổng thể vẫn đúng CANON V2 và không tích lũy thành khác thiết kế**. Không tự đặt ngưỡng % tùy tiện.
- **Quy trình:** hiển thị **CANON V2 bên cạnh preview ở đủ phạm vi thân/trang phục liên quan**, đánh dấu sai khác và quyết định `PASS / PASS WITH MINOR NOTES / REVISE`. Với một thay đổi nhỏ còn phân vân hoặc làm thay đổi cảm giác tổng thể, gửi người dùng xem trước. **Phê duyệt concept V2 không đồng nghĩa phê duyệt file art mới**.
- **Bất biến:** 5 biểu cảm đã chốt, tủ trang phục và damage `100/70/50/30` vẫn theo tài liệu chính thức. CP337 và Spine/APK chưa hoàn thành.

Quy chuẩn này áp dụng cho các nhân vật tiếp theo với **CANON riêng của từng nhân vật**, không dùng body/mặt Lâm Thiển làm mẫu thay thế.


### CP338 — Quyền tinh giản tua rua phụ khi sản xuất art (2026-10-29)

**Người dùng xác nhận:** Nếu khó khăn khi vẽ/tách layer/rig, có thể **bỏ bớt những tua rua và đầu dây trang trí thừa thãi**, miễn là **Lâm Thiển vẫn giống CANON V2**. Đây là lựa chọn tinh giản phụ kiện nhỏ, **KHÔNG phải thay đổi body hay thiết kế trang phục**.

- **Bất biến:** vóc dáng và tỷ lệ +17% đã chốt, kết cấu/cắt may chính, vùng che phủ và cổ áo, các mảng trắng–xanh–vàng, tóc bạc/mắt hổ phách/hoa trắng, những dây buộc/vạt áo/tua chính tạo nên nhận diện. Bốn mức hư hại 100/70/50/30 và bộ 5 biểu cảm vẫn chốt.
- **Được lược có điều kiện:** một số *đầu tua rua nhỏ, sợi trang trí rời lặp thừa*, không có công năng buộc trang phục và không quyết định silhouette. Chỉ thực hiện nếu thực sự giúp rõ hình/rig dễ hơn; không phải bắt buộc phải cắt giảm.
- **Visual QA:** xem ảnh **toàn phần cơ thể/trang phục liên quan** cạnh CANON V2. Nếu giảm tua làm sai silhouette, đường buộc, độ che phủ, màu sắc, hoa hay nhận diện → `REVISE`. Nếu giữ đúng tổng thể nhưng giản lược ít chi tiết nhỏ → `PASS_WITH_MINOR_NOTES` và ghi chú. Không đặt ngưỡng % tùy tiện.
- **CP338 artifact thật:** tách **22 crop PNG native giữ nguyên pixel** từ nguồn đã duyệt (4 outfit, 4 damage, 4 pose, 4 view, 1 mặt closeup, 5 expression). Check SHA CANON V2/5 biểu cảm, 22 file hash PASS, 17 crop poster pixel-identical, ZIP CRC PASS. Gói `TVK_LamThien_CP338_Canon_Reference_And_Trim_Policy.zip`, SHA256 `a17de705436b5ad814507a8dc23135021d2ebd8ceb4d91027df8643df93d6757`, Library `/Thanh Van Ky/Development/CP338_Canon_Costume_Trim/`.
- **Giới hạn:** crop poster là nguồn đối chiếu, **không phải sprite đã tách lớp**; chưa chỉnh ảnh CANON V2, chưa có face master/underpaint artist-grade, Spine/APK chưa nghiệm thu. CP337 ảnh lệch đã REJECTED, CP335 `production_release=blocked_pending_art`.
- **Tài liệu:** [CP338 handoff](art/LAM_THIEN_CP338_CANON_PRESERVATION_HANDOFF.md), [reference manifest](art/LAM_THIEN_CP338_CANON_TRIM_MANIFEST.json).

### Lịch sử 2026-10-29 — CP338
Đã bổ sung ngoại lệ được người dùng cho phép tinh giản phụ kiện tua rua không quan trọng; giữ thiết kế chính thức V2 và mọi biểu cảm/độ hư hại; ưu tiên art trung thực thay vì giữ các đầu tua phức tạp mà không giúp nhân vật.


### CP339 — 3 ảnh tham chiếu cuối và đề xuất tinh chỉnh thân áo (2026-10-29)

Người dùng xác nhận lại rõ ràng **3 ảnh gốc phải được gán đúng vai trò**:

- **Ảnh 2 (SHA256 `3cd8977383ba2fd2563a8f3c07aa85e5a7af4572d37c0fdb80d0e52cba0a3501`): mẫu chính định hướng body/ngoại hình/trang phục, góc, tư thế, damage**. Khi khác nhau, nó ưu tiên về nhận diện toàn nhân vật.
- **Ảnh 3 (SHA256 `186ec1fef284d702229af9e10c6d27a7f3e27b664b22f204863a3f20469d6a50`): chuẩn năm biểu cảm**, chỉ dùng nét mặt/cảm xúc, không tự thay cấu trúc body/kiểu áo/màu mắt.
- **Ảnh 1 (SHA256 `5bd69fff139c4908d122786655babbf08301e345388f1fe6fa6d6b42e21e3d99`): tham chiếu có giới hạn cho kiểu thân áo phần ngực và tỷ lệ vòng một** khi chỉnh ảnh 2 và 3. Không dùng để thay toàn bộ model/trang phục hoặc cách biểu cảm.

**Ý định chỉnh sửa cần preview trước khi chốt art mới:** giữ form người và nhận diện ảnh 2, phối trang phục/góc/tóc/phụ kiện đặc trưng; chỉ tinh chỉnh **dáng phần ngực và cấu trúc áo khu vực đó** gần ảnh 1, hài hòa trên Front/3⁄4 và các biểu cảm ảnh 3. Không phát sinh khỏa thân, không tự đổi thiết kế ngoài vùng yêu cầu; giữ +17% đã chốt và các damage 100/70/50/30. Được giảm tua rua phụ theo CP338, không đổi phụ kiện nhận diện.

**Không thay thế nguồn gốc bằng ảnh sinh mới chưa được xem/duyệt; không xem dòng “Production Ready / Spine” in trong ảnh 3 là bằng chứng có layer.** Giữ `production_release=blocked_pending_art`, `sprite_paths={}` và Spine/APK chưa hoàn thành. Chi tiết vai trò nguồn, mã ảnh và bộ kiểm tra: [CP339 handoff](art/LAM_THIEN_CP339_REFERENCE_PRIORITY_AND_BODICE_ADJUSTMENT.md).

---

## 48. Lâm Thiển — CANON V2.1 9:16 là bản cuối người dùng đã chốt (2026-10-29)

**MỐC QUAN TRỌNG HƠN CÁC GHI CHÚ V2/CP339 TRƯỚC ĐÓ.** Người dùng chỉ định ảnh PNG 9:16 cuối cùng làm **mẫu chuẩn duy nhất** cho hình thể, quần áo, góc nhìn, tư thế, năm biểu cảm và mức hư hại. Những nguồn V2 cũ, CP339 ba ảnh tham khảo, CP337 ảnh lệch chỉ giữ lịch sử.

- Ảnh file nguyên bản không chỉnh sửa: `LAM_THIEN_CANON_V2_1_FINAL_20261029.png` 941×1672 RGBA, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`. Lưu `/Thanh Van Ky/Approved References/Lam_Thien_CANON_V2_1_FINAL_20261029/`.
- Form người +17% **đã có trong ảnh**, giữ nguyên; trang phục ngực và tổng thể theo đúng hình cuối. Tóc bạc/lavender, hoa trắng, phụ kiện và bảng màu trắng–xanh–vàng nhất quán. Có thể lược bớt tua rua phụ nếu không đổi nhận diện.
- Năm sắc thái chơi game: **ngại ngùng / tức giận / đau đớn / xấu hổ / quyến rũ**. Các góc Front, Side, Back, 3/4 và tám tư thế thể hiện trong sheet là chuẩn tham khảo. Khi cần vẽ lại native art nhiều góc, phải đối chiếu từng preview với nguồn này; không tự sinh thiết kế mới.
- Hư hại 100/70/50/30 theo **độ nặng của vết rách/bụi/vết xước trong bản đã chốt**. Đặc biệt mốc **30% không được bẩn, xước hoặc rách nhiều hơn ảnh chuẩn**, không thay độ che phủ/hình thể. Không sao chép mảng rách phẳng thành rig thật.
- Ảnh phẳng được **duyệt làm visual reference**, không xác nhận đã có ORA, PNG alpha riêng, 15 layer, Spine skeleton hoặc Android APK dù trên ảnh có chữ gợi ý. `production_release.status=blocked_pending_art`, `sprite_paths={}` vẫn phải giữ đến khi nghiệm thu asset thật.
- Bắt đầu lại việc triển khai theo [kế hoạch CANON V2.1](art/LAM_THIEN_PLAN_AFTER_CANON_V2_1.md): kiểm màu/góc nhìn → làm art native layer thật → damage/expression QA → rig/Spine → build/test APK. Mọi art phải giữ nguyên nhận diện theo file SHA mới.

**Điểm tiếp tục sau checkpoint:** P0 đã lưu & khóa nguồn; P1 art phân lớp chưa hoàn thành; P2 rig/gameplay chưa nghiệm thu; P3 APK chưa có build được kiểm chứng.


---

## 49. CP340 — triển khai CANON V2.1 từ nguồn pixel thật (2026-10-29)

**ĐÃ LÀM:** nguồn CANON V2.1 SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a` được đọc lại đúng hash; tách **14 ảnh native nguyên pixel** (5 góc nhìn, 5 biểu cảm, 4 mức damage) và một **Foreground Front RGB không đổi + alpha thật** được thử với OpenCV GrabCut ở kích thước gốc **215×449 px**. Có `ORA` 2 layer: một Front alpha visible, một flat crop gốc hidden; có preview QA source/alpha và bộ test **9/9 local PASS** trên ảnh/ORA thực.

**PHÂN BIỆT:** đây là `flat image with an experimental alpha matte` **không phải** tóc, mắt, cơ thể, trang phục tách semantic; nguồn nhỏ, mép vải/tóc còn xấu, mắt/môi in sẵn, không có underpaint. Không suy từ 2 layer ORA ra art production/Spine. File ZIP **26 entries** SHA256 `51cafc14800032712eeed7f0d1ff47edf6f486659ac38c28279298a1be0cb535`, Library Development `/Thanh Van Ky/Development/CP340_Canon_V2_1_Front_Alpha_Trial/`. GitHub có [CP340 handoff](art/LAM_THIEN_CP340_SOURCE_EXACT_FRONT_ALPHA_HANDOFF.md), [manifest](art/LAM_THIEN_CP340_ALPHA_TRIAL_MANIFEST.json), script tái tạo và CI metadata.

**Kết luận P0:** ảnh V2.1 đủ để kiểm nhận diện/màu/chính sách nhưng góc `3/4 Front` ở bảng trông khá chính diện; cần artist xác định góc nhìn thật khi redraw, tuyệt đối không đổi khuôn mặt, vóc dáng, phần áo ngực, hoa và các vật liệu/tỷ lệ đã chốt. Cả 4 mốc 100/70/50/30 giữ nguyên từ source, không làm bụi/xước/rách quá mức ở 30%.

**NEXT P1:** artist tạo **một Front native art đầy đủ** theo đúng V2.1 trên các layer *body, hair_back/front, face/skin_underpaint, eyes/mouth, main bodice, sleeve, ribbons/flowers/accessories* thật. Sau khi QA Front trên đúng silhouette mới làm 5 expressions và damage overlay, các góc còn lại. `production_release=blocked_pending_art`, `sprite_paths={}`; Spine/APK chưa nghiệm thu.


---

## 50. CP341 — Phục hồi mép tóc và vải alpha từ CANON V2.1 (2026-10-29)

- **CANON chính thức không đổi:** `LT_CANON_V2_1_FINAL_USER_APPROVED_2026_10_29`, file user-approved SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`, 941×1672 RGBA. Tỷ lệ +17%, thân áo, ngoại hình, năm biểu cảm và damage 100/70/50/30 đều lấy đúng ảnh đã chốt.
- **Tiến bộ ảnh có thật:** từ một crop Front native 215×449 CP340 bị mất nhiều tóc và dải vải sáng, CP341 tạo alpha mới từ mask lõi + ước lượng màu nền gốc. Tăng **19.983 pixel có alpha >128** (35.564 → 55.547 pixel) trong khi **RGB từng pixel giữ nguyên** CANON; cải thiện tóc dài, 2 tay áo và vạt vải ngoài hai bên. Có **PNG RGBA**, file **alpha mask grayscale**, **ORA 3 raster layer** để so CP341, CP340 và bản crop nguồn; không tự gọi chúng là 3 lớp ngữ nghĩa hay rig.
- **QA local thực:** **13/13 tests PASS**, kiểm SHA nguồn/crop, từng RGB pixel, alpha, vùng phục hồi, ZIP ORA/CRC/layer/mergedimage và cờ ngăn release. Có preview `CP341_BEFORE_AFTER_ALPHA_QA.png`. ZIP **12 file**, SHA256 `08d8aa08bc4b00163e092d056f1e067a5652b0f80b9462e5308277dbe8baacb1`, lưu Library Development `/Thanh Van Ky/Development/CP341_Canon_V2_1_Matte_Recovery/`.
- **Chưa nghiệm thu:** white halos, shadow ở chân/vạt, vùng vải bán trong suốt và các cạnh cắt chưa được sửa thủ công; nguồn chỉ 215×449 nên không phải high-res. Chưa có `face_underpaint`, phần tóc/tay/áo/đồ trang sức tách thật, không có Spine/APK. **CP335 `production_release=blocked_pending_art`, `sprite_paths={}` tiếp tục khóa.**
- **CP342 ưu tiên:** sửa alpha thủ công + shadow, rồi **vẽ thật** một Front native high-res theo V2.1, tách bộ phận có vùng ẩn để cử động, QA một pose đầu tiên; mới mở sang 5 biểu cảm, 4 damage, góc còn lại. Không tự thay trang phục, tỷ lệ +17% hoặc khuôn mặt.
- Hồ sơ [CP341 handoff](art/LAM_THIEN_CP341_MATTE_HANDOFF.md) · [manifest](art/LAM_THIEN_CP341_MATTE_MANIFEST.json).

**Đánh giá P1:** cải tiến matte kỹ thuật đã xong, **art riggable chưa xong**.


---

## 51. CP342 — xóa bóng nền bị giữ nhầm ở chân/vạt áo Front (2026-10-29)

- **Nguồn duy nhất vẫn là CANON V2.1 đã chốt:** `LT_CANON_V2_1_FINAL_USER_APPROVED_2026_10_29` SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`. Trang phục/vòng 1, tỷ lệ +17% đã có sẵn, tóc, phụ kiện, 5 biểu cảm và damage 100/70/50/30 (30% vừa phải) **không được thay**.
- **Art technical thực:** tiếp tục RGBA crop Front 215×449 của CP341, **chỉ sửa alpha 39 dòng dưới (y≥410)** để giảm bóng sàn xanh-xám bị trộn vào giày và hai dải vải rủ. **RGB mọi pixel bất biến**, alpha 410 hàng trên bất biến. Sửa 2.364 pixel alpha, giảm 1.506 pixel alpha >128, vùng floor giảm tổng 209.000 giá trị alpha; vùng giày giữa không đổi.
- Có PNG RGBA mới, mask grayscale, delta mask, **ORA 4 raster lớp để so sánh/rollback**, bảng QA toàn thân và zoom vùng bóng sàn. **Đây là flat cutout không có layer semantic hay underpaint để rig.**
- **QA local 13/13 thực đạt:** SHA source, crop exact, RGB toàn ảnh, 410 dòng trên không đổi, shadow/giày/vạt, các hash PNG, ZIP/CRC/merge ORA; ZIP package 15 file CRC PASS, SHA256 `76d8fd962688dde6356d4853b5e522b5ce78567a1e08ae3739668851ec5ebf66`. Library Development `/Thanh Van Ky/Development/CP342_Canon_V2_1_Alpha_Shadow_Cleanup/`. [Handoff CP342](art/LAM_THIEN_CP342_SHADOW_CLEANUP_HANDOFF.md), [manifest](art/LAM_THIEN_CP342_SHADOW_CLEANUP_MANIFEST.json).
- **Chưa xong** mép trắng của vài dải lụa, underpaint, body/hair/face/áo/tay tách thật, high-resolution painted art, Spine hoặc APK. `production_release.status=blocked_pending_art`, `sprite_paths={}`. Không đưa matte CP342 vào game.
- **CP343 next:** dừng tạo thêm vòng pixel-mask không giải quyết được bản vẽ gốc; làm **Front native high-resolution phân lớp artist-quality** đúng V2.1 với underpaint phần bị che để chuyển động. Kiểm tư thế/đường viền/bodice rồi mới mở năm nét mặt, bốn damage và các góc khác. Nghiệm thu sprite riêng trước Spine/Android.

**CP342 chỉ đóng một lỗi alpha kỹ thuật, không đóng P1 art/Spine/APK.**


---

## 52. CP343 — 10 vùng Front pixel-exact, kiểm nghiệm underpaint FAIL (2026-10-29)

- **CANON V2.1 vẫn khóa** (941×1672, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`): giữ body +17% đã chốt, kiểu thân áo/ngực, tóc bạc, hoa/phụ kiện, màu trắng–xanh–vàng, năm biểu cảm và mức hư hại 100/70/50/30 (30% vừa phải). **Không vẽ lại/chỉnh RGB thiết kế.**
- Từ ảnh Front foreground CP342 **215×449**, đã tách **10 nhóm PNG alpha có pixel thật, mask chỉnh được và OpenRaster 10 lớp**, gồm tóc/vải hai bên, chân trái/phải, dải vải eo, hai tay và tay áo, thân áo/cổ, đầu/phụ kiện và vùng đường nối khó phân chia. **Các mask là polygon phân vùng gần đúng, không phải anatomy đã vẽ đủ/riggable.**
- **Ghép ở vị trí nghỉ pixel-exact**: toàn bộ alpha và RGB tại các pixel có alpha đều đúng nguồn CP342; **12/12 test binary local PASS** trên các PNG/mask/ORA. Preview màu và nguồn đặt cạnh nhau. OpenRaster có layer raster thật, nhưng các bộ phận vẫn bị thiếu vùng ẩn và còn đường cắt thẳng.
- **Stress test thực:** dịch nhẹ hai nhóm tay ±10px/+5px → lộ **1.798 pixel bị trống** và 1.098 pixel nhô ra ngoài. Gate **FAIL_no_hidden_underpaint**. Đây là bằng chứng chưa đủ art để tạo motion, không phải một animation đã nghiệm thu.
- **Gói:** `TVK_LamThien_CP343_Source_Exact_Region_Layers_NOT_SPINE_READY.zip` (34 file, CRC PASS, SHA256 `b61169d5b3fdb04dbbbd38df3ab080b2662e9332fabcc9c6ecaf660691ce9519`), sao lưu `/Thanh Van Ky/Development/CP343_Canon_V2_1_Front_Region_Layers/`. [CP343 handoff](art/LAM_THIEN_CP343_REGION_LAYER_HANDOFF.md) · [manifest](art/LAM_THIEN_CP343_REGION_LAYER_MANIFEST.json).
- **CP344 next có mục tiêu cụ thể:** họa sĩ chỉnh một khớp tay–vai/trang phục Front và vẽ **vùng da/vải/tóc thực bị che phía sau**, làm 2 frame nghỉ→nhấc tay nhẹ, QA không hở vùng nào; sau đó mới tay còn lại và redraw native độ phân giải cao. Chưa sản xuất năm expression attachments, bốn overlay damage hay các góc còn lại.
- CP335 Android vẫn `production_release=blocked_pending_art`, `sprite_paths={}`. **P1 semantic movable art, Spine, APK vẫn CHƯA NGHIỆM THU.**


---

## 53. CP346 — Kiểm tra tay–vai trên nguồn thật (2026-10-29)

- Đã lấy đúng **CANON V2.1 user-approved** SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`, cùng gói **CP343 source-region 10 lớp** SHA256 `b61169d5b3fdb04dbbbd38df3ab080b2662e9332fabcc9c6ecaf660691ce9519` từ Library. Kiểm hash và ZIP PASS; composite CP343 ở trạng thái nghỉ pixel-exact PASS.
- Test dịch pixel ở chính ảnh nguồn 215×449: tay trái trên ảnh `(-10,+5)` thiếu **914 px**, xuất hiện thêm **500 px**; tay phải trên ảnh `(+10,+5)` thiếu **884 px**, thêm **598 px**; cả hai tay thiếu **1.798 px**, thêm **1.098 px**. Kết quả tổng khớp CP343. Đây là số vùng phủ alpha thay đổi, **không phải đã sửa/đã vẽ bù**.
- Tạo report JSON, preview khoanh lỗi thật, mask riêng mỗi tay và **mask hướng dẫn vùng cần underpaint** `underpaint_priority_mask_NOT_PAINT.png`. QA thực **5/5 local PASS** trên SHA, compositing, pixel counts, mask, release gate. Gói tải CP346 được tạo từ file thật; GitHub có [công cụ tái kiểm](../tools/art/cp346_joint_motion_audit.py) và [handoff](art/LAM_THIEN_CP346_REAL_SOURCE_JOINT_DIAGNOSIS.md).
- **Bất biến CANON V2.1:** tỷ lệ +17%, form thân áo/vòng 1, nhận diện, tóc, hoa, màu trắng–xanh–vàng, năm nét mặt, damage 100/70/50/30. Không thay nguồn đã chốt.
- **Cảnh báo:** sprite gốc hiện chỉ là **215×449 crop** và 10 nhóm vùng không có ảnh ẩn phía sau tay/vải/tóc. Không được nhận định mask QA là art cao cấp; chưa tạo native high-res painter art, chưa có frame chuyển động đạt chuẩn, rig Spine hoặc APK nghiệm thu. `production_release.status=blocked_pending_art`, `sprite_paths={}` vẫn giữ nguyên.
- **CP347 next:** họa sĩ vẽ thật Front độ phân giải cao với vùng ẩn tay-vai/thân áo/tóc, tách lớp ngữ nghĩa và thử động tác nhấc tay; so preview với CANON V2.1 trước khi mở rộng sang các biểu cảm và mức damage.
