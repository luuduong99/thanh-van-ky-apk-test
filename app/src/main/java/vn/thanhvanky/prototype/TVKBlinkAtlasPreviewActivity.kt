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

/** Isolated CP402 artist review screen. Never an approved Lâm Thiển runtime sprite. */
class TVKBlinkAtlasPreviewActivity : Activity() {
    private val requestAtlas = 402
    private val pinnedAtlasSha = "645738fa932a354e3142e2474eb35011491b091d06451a08c4443e6650529c97"
    private lateinit var label: TextView
    private lateinit var art: AtlasView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // IMPORTANT: non-exported and debug-only. User-loaded draft must not enter production.
        if ((applicationInfo.flags and ApplicationInfo.FLAG_DEBUGGABLE) == 0) { finish(); return }
        val layout = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER_HORIZONTAL
            setBackgroundColor(Color.rgb(21, 36, 52))
            setPadding(20, 20, 20, 20)
        }
        val heading = TextView(this).apply {
            text = "Lâm Thiển — CP402 / DRAFT / KHÔNG PHẢI ẢNH GAME ĐÃ DUYỆT"
            textSize = 17f
            setTextColor(Color.WHITE)
        }
        label = TextView(this).apply {
            text = "Chọn chính xác CP402_ATLAS_ROOT_DRAFT_15.png từ bộ ZIP CP402.\nChỉ xem trước trên bản debug; chưa có sprite đã nghiệm thu."
            textSize = 13f
            setTextColor(Color.rgb(250, 207, 158))
        }
        art = AtlasView(this)
        layout.addView(heading)
        layout.addView(label)
        layout.addView(Button(this).apply {
            text = "Chọn atlas CP402 (kiểm tra SHA-256)"
            setOnClickListener {
                val i = Intent(Intent.ACTION_OPEN_DOCUMENT).apply {
                    type = "image/png"
                    addCategory(Intent.CATEGORY_OPENABLE)
                }
                startActivityForResult(i, requestAtlas)
            }
        })
        layout.addView(art, LinearLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT, 0, 1f))
        setContentView(layout)
    }

    @Deprecated("For this private debug file-picker-only activity")
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
                    require(bytes.size() + n <= 8 * 1024 * 1024) { "Atlas vượt giới hạn dung lượng" }
                    bytes.write(buffer, 0, n)
                }
            }
            val blob = bytes.toByteArray()
            val digest = MessageDigest.getInstance("SHA-256").digest(blob)
                .joinToString("") { "%02x".format(it.toInt() and 255) }
            require(digest == pinnedAtlasSha) { "Sai atlas, hash không trùng CP402" }
            val img = BitmapFactory.decodeByteArray(blob, 0, blob.size)
            require(img != null && img.width == 2520 && img.height == 197) {
                "Kích thước atlas không hợp lệ (15×168×197)"
            }
            art.setAtlas(img)
            label.text = "ĐÃ XÁC MINH SHA-256 • chỉ preview trong bản debug • CHƯA DUYỆT MỸ THUẬT"
        } catch (error: Exception) {
            label.text = "Không tải được bản thử: ${error.message}"
        }
    }

    /** Draw 15 authored source-locked pose candidates on a 2.4 s blink loop. */
    private class AtlasView(context: android.content.Context) : View(context) {
        private var atlas: Bitmap? = null
        private val paint = Paint(Paint.ANTI_ALIAS_FLAG or Paint.FILTER_BITMAP_FLAG)
        private val sourceRect = Rect()
        private val targetRect = RectF()
        private var startTime = 0L
        fun setAtlas(image: Bitmap) {
            atlas = image
            startTime = SystemClock.uptimeMillis()
            invalidate()
        }
        override fun onDraw(canvas: Canvas) {
            super.onDraw(canvas)
            val bitmap = atlas ?: return
            if (width <= 0 || height <= 0) return
            val t = ((SystemClock.uptimeMillis() - startTime) % 2400L) / 2400f
            val pose = poseForTime(t)
            sourceRect.set(pose * 168, 0, (pose + 1) * 168, 197)
            val scale = min(width / 168f, height / 197f)
            val w = 168f * scale
            val h = 197f * scale
            targetRect.set((width - w) / 2f, (height - h) / 2f,
                (width + w) / 2f, (height + h) / 2f)
            canvas.drawBitmap(bitmap, sourceRect, targetRect, paint)
            if (isAttachedToWindow && isShown) postInvalidateOnAnimation()
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