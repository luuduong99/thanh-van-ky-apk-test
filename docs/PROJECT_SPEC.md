# THANH VÂN KÝ — TÀI LIỆU MÔ TẢ DỰ ÁN

> **Mục đích:** Đây là nguồn thông tin chuẩn của dự án để tiếp tục công việc ở các thread khác mà không cần đọc lại toàn bộ lịch sử hội thoại. Khi có quyết định mới, hãy cập nhật tài liệu này trong cùng thay đổi/commit nếu phù hợp.
>
> **Quy tắc trạng thái:**  
> - **ĐÃ CHỐT**: người dùng đã xác nhận, không tự ý thay đổi.  
> - **ĐỊNH HƯỚNG**: mục tiêu mong muốn, có thể cần làm rõ chi tiết.  
> - **CHƯA CHỐT**: không tự coi là quyết định cuối cùng.  
> - **TRẠNG THÁI KỸ THUẬT**: phải kiểm tra trực tiếp repository/GitHub trước khi khẳng định vẫn đúng.

**Cập nhật lần cuối:** 2026-10-23  
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

- Tài liệu này là nguồn tham chiếu chuẩn; thread cũ chỉ là lịch sử bổ sung.
- Sau mỗi quyết định được người dùng chốt, cập nhật mục liên quan, ngày cập nhật và trạng thái.
- Không nâng một ý tưởng do trợ lý đề xuất thành quyết định đã chốt nếu người dùng chưa đồng ý.
- Nếu quyết định mới mâu thuẫn với quyết định cũ, nêu rõ mâu thuẫn và hỏi xác nhận; sau khi xác nhận, cập nhật tài liệu và ghi quyết định cũ vào lịch sử thay đổi.
- Giữ riêng thông tin **đã xác nhận**, **định hướng**, **chưa chốt** và **trạng thái kỹ thuật**.
- Khi bắt đầu thread mới, đọc file này trước; sau đó kiểm tra trạng thái GitHub hiện tại nếu công việc liên quan đến code/build. Không dựa vào mô tả trạng thái kỹ thuật cũ nếu cần thông tin mới nhất.

## 10. Lịch sử cập nhật

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
