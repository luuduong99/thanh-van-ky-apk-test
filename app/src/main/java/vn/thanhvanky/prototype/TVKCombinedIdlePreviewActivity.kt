package vn.thanhvanky.prototype

import android.app.Activity
import android.content.Intent
import android.content.pm.ApplicationInfo
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Color
import android.net.Uri
import android.os.Bundle
import android.view.Gravity
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.FrameLayout
import android.widget.LinearLayout
import android.widget.TextView
import java.io.ByteArrayOutputStream
import java.security.MessageDigest

/** Debug-only CP410: body mesh and separately labelled CANON face blink on ONE clock.
 * The two images are distinct poses on the same CANON sheet. Never paste face onto body.
 */
class TVKCombinedIdlePreviewActivity : Activity() {
    companion object {
        private const val PICK_CANON = 408
        private const val PICK_BLINK = 410
        private const val CANON_HASH = "f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a"
        private const val BLINK_HASH = "d9234630eab9e13ec07527e2c7b6fbbacd849117bf2e4983bf35ac4bcf73a07e"
        private const val MAX_CANON = 5_000_000
        private const val MAX_BLINK = 8_000_000
        private val FRONT = intArrayOf(16, 180, 224, 623)
        private val FACE = intArrayOf(25, 684, 193, 881)
    }
    private val clock = TVKPreviewClock()
    private var canonSheet: Bitmap? = null
    private var preview: TVKCombinedIdleMotionView? = null
    private var blinkPreview: TVKCombinedBlinkInsetView? = null
    private lateinit var frame: FrameLayout
    private lateinit var blinkPanel: LinearLayout
    private lateinit var blinkContainer: FrameLayout
    private lateinit var status: TextView
    private lateinit var play: Button
    private lateinit var blinkChoose: Button
    private lateinit var auditButton: Button
    private var auditOverlay: TVKFrontPoseRigAuditOverlay? = null
    private var auditVisible = false
    private val names = arrayOf("Thở", "Đầu", "Tay", "Tóc", "Lụa")
    private var running = true
    private fun dp(n: Int) = (n * resources.displayMetrics.density + .5f).toInt()
    private fun text(s: String, size: Float = 13f) = TextView(this).apply {
        text = s
        textSize = size
        setTextColor(Color.rgb(234, 240, 255))
    }
    private fun button(s: String, f: () -> Unit) = Button(this).apply {
        text = s; isAllCaps = false; setOnClickListener { f() }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        if ((applicationInfo.flags and ApplicationInfo.FLAG_DEBUGGABLE) == 0) { finish(); return }
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(8), dp(6), dp(8), dp(6))
            setBackgroundColor(Color.rgb(26, 37, 50))
        }
        root.addView(text("CP410 — Lâm Thiển | ĐỒNG HỒ CHUNG (DEBUG)", 17f))
        root.addView(text("Thân đứng + khuôn mặt phóng lớn là HAI TƯ THẾ KHÁC NHAU. Chưa có rig hoặc mắt production."))
        val picks = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL }
        picks.addView(button("1. CANON V2.1") { pickFile(PICK_CANON) },
            LinearLayout.LayoutParams(0, dp(46), 1f))
        blinkChoose = button("2. Atlas mắt CP409") { pickFile(PICK_BLINK) }
        blinkChoose.isEnabled = false
        picks.addView(blinkChoose, LinearLayout.LayoutParams(0, dp(46), 1f))
        root.addView(picks)
        status = text("Chọn file CANON trước; sẽ xác minh SHA-256 và kích thước.")
        root.addView(status)
        frame = FrameLayout(this).apply { setBackgroundColor(Color.rgb(236, 242, 250)) }
        root.addView(frame, LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, 0, 1f))
        blinkPanel = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            visibility = View.GONE
        }
        blinkPanel.addView(text("MẮT — ảnh mặt CANON khác góc đứng, chỉ kiểm đồng bộ", 12f))
        blinkContainer = FrameLayout(this)
        blinkPanel.addView(blinkContainer, LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, 0, 1f))
        root.addView(blinkPanel, LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(155)))
        val controls = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER }
        play = button("Tạm dừng") {
            running = !running
            clock.setPlaying(running && !auditVisible)
            preview?.invalidate()
            blinkPreview?.invalidate()
            play.text = if (running) "Tạm dừng" else "Tiếp tục"
        }
        controls.addView(play, LinearLayout.LayoutParams(0, dp(46), 1f))
        for (i in 0..4) {
            val b = button(names[i] + " ✓") { }
            b.setOnClickListener {
                val active = preview?.flipChannel(i) ?: false
                b.text = names[i] + (if (active) " ✓" else " ×")
            }
            controls.addView(b, LinearLayout.LayoutParams(0, dp(46), 1f))
        }
        root.addView(controls)
        auditButton = button("CP411 | Soi mốc đầu / mắt / cổ (DEBUG)") {
            if (preview == null) return@button
            auditVisible = !auditVisible
            if (auditVisible) {
                // Overlay only on the UNWARPED CANON source: freeze and reset the shared clock.
                running = false
                clock.reset()
                clock.setPlaying(false)
                play.text = "Tiếp tục"
                play.isEnabled = false
                preview?.invalidate()
                blinkPreview?.invalidate()
                auditOverlay?.visibility = View.VISIBLE
                status.text = "CP411 | Đầu vàng, mắt xanh, cổ hồng. Mặt nạ thô, không phải rig đã duyệt."
                auditButton.text = "CP411 | Đóng chỉ dẫn"
            } else {
                auditOverlay?.visibility = View.GONE
                play.isEnabled = true
                auditButton.text = "CP411 | Soi mốc đầu / mắt / cổ (DEBUG)"
                status.text = "Đã đóng overlay CP411. Đây là mô phỏng CP410, chưa có rig thật."
            }
        }
        auditButton.isEnabled = false
        root.addView(auditButton, LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(42)))
        root.addView(text("Hai nguồn cùng thời gian; KHÔNG ghép mắt vào body; KHÔNG là asset game đã duyệt."))
        setContentView(root)
    }

    private fun pickFile(code: Int) {
        val request = Intent(Intent.ACTION_OPEN_DOCUMENT).apply {
            addCategory(Intent.CATEGORY_OPENABLE)
            type = "image/png"
        }
        startActivityForResult(request, code)
    }

    private fun decodeVerified(uri: Uri, hash: String, limit: Int, width: Int, height: Int): Bitmap {
        // Decode only AFTER checking raw bytes against source-of-truth.
        val blob = contentResolver.openInputStream(uri)?.use { input ->
            val bytes = ByteArrayOutputStream()
            val buffer = ByteArray(8192)
            while (true) {
                val n = input.read(buffer)
                if (n < 0) break
                require(bytes.size() + n <= limit) { "PNG vượt giới hạn" }
                bytes.write(buffer, 0, n)
            }
            bytes.toByteArray()
        } ?: throw IllegalArgumentException("Không đọc được file")
        val actual = MessageDigest.getInstance("SHA-256").digest(blob)
            .joinToString("") { "%02x".format(it.toInt() and 255) }
        require(actual == hash) { "Sai file CANON/atlas (SHA-256 không khớp)" }
        val opts = BitmapFactory.Options().apply { inJustDecodeBounds = true }
        BitmapFactory.decodeByteArray(blob, 0, blob.size, opts)
        require(opts.outWidth == width && opts.outHeight == height) { "Kích thước ảnh không đúng" }
        return BitmapFactory.decodeByteArray(blob, 0, blob.size)
            ?: throw IllegalArgumentException("PNG không hợp lệ")
    }

    @Deprecated("Android API 23 compatible document picker")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (resultCode != RESULT_OK || (requestCode != PICK_CANON && requestCode != PICK_BLINK)) return
        val uri = data?.data ?: return
        try {
            if (requestCode == PICK_CANON) {
                val source = decodeVerified(uri, CANON_HASH, MAX_CANON, 941, 1672)
                canonSheet = source
                // These coordinates are on the CANON concept sheet, not production rig layers.
                val crop = Bitmap.createBitmap(source, FRONT[0], FRONT[1], FRONT[2] - FRONT[0], FRONT[3] - FRONT[1])
                frame.removeAllViews()
                auditVisible = false
                auditOverlay = null
                if (::auditButton.isInitialized) { auditButton.isEnabled = false; auditButton.text = "CP411 | Soi mốc đầu / mắt / cổ (DEBUG)" }
                if (::play.isInitialized) play.isEnabled = true
                blinkContainer.removeAllViews()
                blinkPreview = null
                blinkPanel.visibility = View.GONE
                clock.reset()
                clock.setPlaying(running)
                preview = TVKCombinedIdleMotionView(this, crop, clock).also {
                    frame.addView(it, FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,
                        ViewGroup.LayoutParams.MATCH_PARENT))
                }
                auditOverlay = TVKFrontPoseRigAuditOverlay(this).also {
                    it.visibility = View.GONE
                    frame.addView(it, FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,
                        ViewGroup.LayoutParams.MATCH_PARENT))
                }
                auditButton.isEnabled = true
                blinkChoose.isEnabled = true
                status.text = "CANON ✓ | 5 kênh cơ thể chạy. Có thể chọn atlas CP409 để xem mắt ở panel riêng."
            } else {
                val sheet = canonSheet ?: throw IllegalArgumentException("Hãy chọn CANON trước")
                val atlas = decodeVerified(uri, BLINK_HASH, MAX_BLINK, 2520, 197)
                // Strict identity check: frame 0 MUST be identical to face region on the same CANON.
                val face = Bitmap.createBitmap(sheet, FACE[0], FACE[1], FACE[2] - FACE[0], FACE[3] - FACE[1])
                val first = Bitmap.createBitmap(atlas, 0, 0, 168, 197)
                require(first.sameAs(face)) { "Frame đầu không đúng mặt CANON" }
                blinkContainer.removeAllViews()
                blinkPreview = TVKCombinedBlinkInsetView(this, atlas, clock).also {
                    blinkContainer.addView(it, FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,
                        ViewGroup.LayoutParams.MATCH_PARENT))
                }
                blinkPanel.visibility = View.VISIBLE
                status.text = "CANON ✓ Atlas CP409 ✓ | Đồng hồ chung; hai pose KHÔNG chồng lên nhau."
            }
        } catch (e: Exception) {
            // Fail closed: never show mismatched source, stale overlays, or a fallback character.
            if (requestCode == PICK_CANON) {
                canonSheet = null
                preview = null
                blinkPreview = null
                blinkChoose.isEnabled = false
                auditVisible = false
                auditOverlay = null
                auditButton.isEnabled = false
                play.isEnabled = true
                frame.removeAllViews()
                blinkContainer.removeAllViews()
                blinkPanel.visibility = View.GONE
            } else {
                blinkPreview = null
                blinkContainer.removeAllViews()
                blinkPanel.visibility = View.GONE
            }
            status.text = "Từ chối ảnh: ${e.message}"
        }
    }

    override fun onStop() { super.onStop(); clock.setPlaying(false); preview?.invalidate(); blinkPreview?.invalidate() }
    override fun onResume() {
        super.onResume()
        if (::frame.isInitialized) {
            clock.setPlaying(running)
            preview?.invalidate()
            blinkPreview?.invalidate()
        }
    }
}