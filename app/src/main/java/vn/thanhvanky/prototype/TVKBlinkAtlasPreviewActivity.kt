package vn.thanhvanky.prototype

import android.app.Activity
import android.content.Intent
import android.content.pm.ApplicationInfo
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Rect
import android.graphics.RectF
import android.os.Bundle
import android.os.SystemClock
import android.view.Gravity
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView
import java.io.ByteArrayOutputStream
import java.security.MessageDigest
import kotlin.math.min
import kotlin.math.roundToInt

/** CP403 artist inspection screen. NOT a production CANON sprite or approved eye art. */
class TVKBlinkAtlasPreviewActivity : Activity() {
    private val requestAtlas = 403
    // This SHA is pinned to the EXACT private-source CP402 preview PNG, not any older concept.
    private val modeCp409 by lazy { intent.getBooleanExtra("cp409_review", false) }
    private val pinnedAtlasSha: String get() = if (modeCp409)
        "d9234630eab9e13ec07527e2c7b6fbbacd849117bf2e4983bf35ac4bcf73a07e"
        else "645738fa932a354e3142e2474eb35011491b091d06451a08c4443e6650529c97"
    private lateinit var label: TextView
    private lateinit var controlsLabel: TextView
    private lateinit var playPause: Button
    private lateinit var art: AtlasCompareView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Explicit development gate. The manifest also declares exported=false.
        if ((applicationInfo.flags and ApplicationInfo.FLAG_DEBUGGABLE) == 0) { finish(); return }
        val layout = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER_HORIZONTAL
            setBackgroundColor(Color.rgb(21, 36, 52))
            setPadding(12, 12, 12, 12)
        }
        fun heading(text: String, size: Float) = TextView(this).apply {
            this.text = text
            textSize = size
            setTextColor(Color.WHITE)
        }
        layout.addView(heading("Lâm Thiển — " + (if (modeCp409) "CP409 | MÍ CHUYỂN ĐỘNG (DRAFT)" else "CP403 | KIỂM TRA MẮT NHẮM (DRAFT)"), 16f))
        label = heading((if (modeCp409) "Chọn CP409_15_POSE_NATIVE_SHA_LOCKED_DRAFT.png" else "Chọn CP402_ATLAS_ROOT_DRAFT_15.png") + "; so sánh CANON mở và mắt thử. " +
            "KHÔNG PHẢI ẢNH GAME ĐÃ DUYỆT", 12f)
        label.setTextColor(Color.rgb(250, 207, 158))
        layout.addView(label)
        controlsLabel = heading("Chưa có atlas | 0/14 | Chưa nghiệm thu mỹ thuật", 12f)
        layout.addView(controlsLabel)
        val chooser = Button(this).apply {
            text = "Chọn atlas — SHA-256 bắt buộc"
            setOnClickListener {
                val i = Intent(Intent.ACTION_OPEN_DOCUMENT).apply {
                    type = "image/png"
                    addCategory(Intent.CATEGORY_OPENABLE)
                }
                startActivityForResult(i, requestAtlas)
            }
        }
        layout.addView(chooser)
        val actions = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL }
        playPause = Button(this).apply {
            text = "Tạm dừng"
            setOnClickListener {
                val playing = art.togglePlaying()
                this.text = if (playing) "Tạm dừng" else "Tiếp tục"
                updateFrameLabel()
            }
        }
        actions.addView(playPause, LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f))
        actions.addView(Button(this).apply {
            text = "Từng khung"
            setOnClickListener {
                art.step()
                playPause.text = "Tiếp tục"
                updateFrameLabel()
            }
        }, LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f))
        actions.addView(Button(this).apply {
            text = "Pixel / Mịn"
            setOnClickListener {
                art.toggleFiltering()
                updateFrameLabel()
            }
        }, LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f))
        layout.addView(actions)
        art = AtlasCompareView(this, if (modeCp409) "CP409" else "CP402") { updateFrameLabel() }
        layout.addView(art, LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, 0, 1f))
        setContentView(layout)
    }

    private fun updateFrameLabel() {
        if (!::art.isInitialized) return
        controlsLabel.text = "Khung ${art.currentPoseIndex()}/14 | " +
            (if (art.isPlaying) "đang chạy" else "đã dừng") + " | " +
            (if (art.isSharp) "pixel gốc" else "lọc mịn") + " | Chưa duyệt"
    }

    override fun onPause() {
        super.onPause()
        if (::art.isInitialized) {
            art.pause()
            if (::playPause.isInitialized) playPause.text = "Tiếp tục"
        }
    }

    @Deprecated("File-picker callback for isolated debug review activity")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode != requestAtlas || resultCode != RESULT_OK) return
        val uri = data?.data ?: return
        try {
            val bytes = ByteArrayOutputStream()
            val buffer = ByteArray(8192)
            contentResolver.openInputStream(uri).use { input ->
                require(input != null) { "Không đọc được atlas" }
                while (true) {
                    val n = input.read(buffer)
                    if (n < 0) break
                    require(bytes.size() + n <= 8 * 1024 * 1024) { "Atlas vượt 8 MB" }
                    bytes.write(buffer, 0, n)
                }
            }
            val blob = bytes.toByteArray()
            val digest = MessageDigest.getInstance("SHA-256").digest(blob)
                .joinToString("") { "%02x".format(it.toInt() and 255) }
            require(digest == pinnedAtlasSha) { "Sai ảnh: SHA-256 không khớp atlas đã khóa cho chế độ xem này" }
            val image = BitmapFactory.decodeByteArray(blob, 0, blob.size)
            require(image != null && image.width == 2520 && image.height == 197) {
                "Sai kích thước 15 × 168 × 197"
            }
            art.setAtlas(image)
            playPause.text = "Tạm dừng"
            label.text = (if (modeCp409) "ĐÚNG ATLAS CP409" else "ĐÚNG ATLAS CP402") + " — xem CANON mở bên cạnh mắt thử. " +
                "KHÔNG PHẢI ẢNH GAME ĐÃ DUYỆT"
            updateFrameLabel()
        } catch (e: Exception) {
            label.text = "Không tải được atlas: ${e.message}"
        }
    }

    /** Exact source crop is frame zero. Preview is a separate frame from the SAME verified atlas. */
    private class AtlasCompareView(
        context: android.content.Context,
        private val draftName: String,
        private val onFrame: () -> Unit
    ) : View(context) {
        private var atlas: Bitmap? = null
        private val picture = Paint(Paint.ANTI_ALIAS_FLAG)
        private val legend = Paint(Paint.ANTI_ALIAS_FLAG).apply {
            textSize = 31f
            color = Color.WHITE
        }
        private val source = Rect()
        private val dest = RectF()
        private var startMs = SystemClock.uptimeMillis()
        private var elapsedOnPauseMs = 0L
        private var frozenPose: Int? = null
        private var lastDisplayedPose: Int = -1
        var isPlaying = true
            private set
        var isSharp = true
            private set

        fun setAtlas(image: Bitmap) {
            atlas?.takeUnless { it === image }?.recycle()
            atlas = image
            elapsedOnPauseMs = 0
            frozenPose = null
            startMs = SystemClock.uptimeMillis()
            isPlaying = true
            lastDisplayedPose = -1
            invalidate()
        }

        fun togglePlaying(): Boolean {
            if (atlas == null) return false
            if (isPlaying) pause() else {
                isPlaying = true
                if (frozenPose != null) {
                    // Resume at the same visual pose, then continue the natural loop.
                    val p = frozenPose!!
                    val t = when {
                        p <= 0 -> 0.30f
                        p <= 7 -> .31f + (p / 7f) * .045f
                        else -> .395f + ((p - 7f) / 7f) * .065f
                    }
                    elapsedOnPauseMs = (t * 2400).toLong()
                    frozenPose = null
                }
                startMs = SystemClock.uptimeMillis() - elapsedOnPauseMs
                invalidate()
            }
            return isPlaying
        }

        fun pause() {
            if (isPlaying) {
                elapsedOnPauseMs = (SystemClock.uptimeMillis() - startMs) % 2400L
                isPlaying = false
                invalidate()
            }
        }

        fun step() {
            if (atlas == null) return
            pause()
            frozenPose = ((frozenPose ?: poseForTime(elapsedOnPauseMs / 2400f)) + 1) % 15
            invalidate()
        }

        fun toggleFiltering() {
            isSharp = !isSharp
            invalidate()
        }

        fun currentPoseIndex(): Int = frozenPose ?: poseForTime(
            (if (isPlaying) ((SystemClock.uptimeMillis() - startMs) % 2400L) else elapsedOnPauseMs) / 2400f
        )

        override fun onDraw(canvas: Canvas) {
            super.onDraw(canvas)
            val image = atlas ?: return
            if (width <= 0 || height <= 0) return
            val index = currentPoseIndex()
            picture.isFilterBitmap = !isSharp
            if (index != lastDisplayedPose) { lastDisplayedPose = index; post { onFrame() } }
            val horizontal = width > height
            if (horizontal) {
                drawPanel(canvas, image, 0, RectF(0f, 0f, width * .5f, height.toFloat()), "MỞ / CANON")
                drawPanel(canvas, image, index, RectF(width * .5f, 0f, width.toFloat(), height.toFloat()), "$draftName / DRAFT")
            } else {
                drawPanel(canvas, image, 0, RectF(0f, 0f, width.toFloat(), height * .5f), "MỞ / CANON")
                drawPanel(canvas, image, index, RectF(0f, height * .5f, width.toFloat(), height.toFloat()), "$draftName / DRAFT")
            }
            if (isPlaying && isAttachedToWindow && isShown) {
                postInvalidateOnAnimation()
            }
            // Only update labels on user interaction, not every display refresh.
        }

        private fun drawPanel(canvas: Canvas, image: Bitmap, frame: Int, area: RectF, name: String) {
            val panelH = area.height() - 42f
            if (panelH <= 0) return
            val scale = min(area.width() / 168f, panelH / 197f)
            val w = 168f * scale
            val h = 197f * scale
            val cx = area.centerX(); val cy = area.top + 21f + panelH * .5f
            dest.set(cx - w * .5f, cy - h * .5f, cx + w * .5f, cy + h * .5f)
            source.set(frame * 168, 0, (frame + 1) * 168, 197)
            canvas.drawBitmap(image, source, dest, picture)
            canvas.drawText(name, area.left + 8f, area.top + 35f, legend)
        }

        companion object {
            private fun smooth(v: Float): Float {
                val z = v.coerceIn(0f, 1f)
                return z * z * (3f - 2f * z)
            }
            fun poseForTime(t: Float): Int = when {
                t < .31f -> 0
                t < .355f -> (7 * smooth((t - .31f) / .045f)).roundToInt().coerceIn(0, 7)
                t < .395f -> 7
                t < .46f -> (14 - 7 * smooth((.46f - t) / .065f)).roundToInt().coerceIn(7, 14)
                else -> 0
            }
        }
    }
}