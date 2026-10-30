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
import android.net.Uri
import android.os.Bundle
import android.os.SystemClock
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView
import java.io.ByteArrayOutputStream
import java.security.MessageDigest
import kotlin.math.min
import kotlin.math.roundToInt

/**
 * CP417 DEBUG / NOT APPROVED ART. Single CANON front pose with moving eyelid
 * geometry inside two tiny ROIs, using a user-selected private verified atlas.
 * This is not a layered head rig, not Spine and not a production animation.
 */
class TVKCP417SamePoseBlinkActivity : Activity() {
    companion object {
        private const val PICK_CANON = 4171
        private const val PICK_ATLAS = 4172
        private const val CANON_SHA = "f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a"
        private const val ATLAS_SHA = "cb6cbe03cb1b9ccd3201e4a6bb6ba0e9cc3225111c4f78d441d7d9d7296d05cb"
        private const val FRAMES = 5
        private const val W = 208
        private const val H = 443
        private val FRONT = intArrayOf(16, 180, 224, 623)
    }
    private var front: Bitmap? = null
    private var atlas: Bitmap? = null
    private lateinit var status: TextView
    private lateinit var chooseAtlas: Button
    private lateinit var playPause: Button
    private lateinit var viewer: BlinkView
    private var playing = true

    private fun dp(n: Int) = (n * resources.displayMetrics.density + .5f).toInt()
    private fun button(label: String, action: () -> Unit) = Button(this).apply {
        text = label; isAllCaps = false; setOnClickListener { action() }
    }
    private fun info(label: String, size: Float) = TextView(this).apply {
        text = label; textSize = size; setTextColor(Color.rgb(239, 246, 255))
    }
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Do not expose this private source review in release builds.
        if ((applicationInfo.flags and ApplicationInfo.FLAG_DEBUGGABLE) == 0) { finish(); return }
        val col = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(10), dp(10), dp(10), dp(10))
            setBackgroundColor(Color.rgb(21, 35, 52))
        }
        col.addView(info("CP417 • LÂM THIỂN — CÙNG POSE (DEBUG)", 17f))
        col.addView(info("Mắt trên ảnh đứng 208×443. Chỉ bản nháp, chưa nghiệm thu mỹ thuật.", 12f))
        val pick = LinearLayout(this)
        pick.addView(button("1. Chọn CANON V2.1") { pick(PICK_CANON) },
            LinearLayout.LayoutParams(0, dp(48), 1f))
        chooseAtlas = button("2. Chọn atlas CP417") { pick(PICK_ATLAS) }
        chooseAtlas.isEnabled = false
        pick.addView(chooseAtlas, LinearLayout.LayoutParams(0, dp(48), 1f))
        col.addView(pick)
        status = info("Chọn đúng file CANON gốc trước (khóa SHA-256).", 12f)
        col.addView(status)
        viewer = BlinkView()
        col.addView(viewer, LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, 0, 1f))
        playPause = button("Tạm dừng") {
            playing = !playing
            viewer.setPlaying(playing)
            playPause.text = if (playing) "Tạm dừng" else "Tiếp tục"
        }
        col.addView(playPause, LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(42)))
        col.addView(info("Ảnh CANON không nằm trong APK. 5 khung mắt DRAFT, không phải rig/Spine.", 12f))
        setContentView(col)
    }
    private fun pick(code: Int) {
        val intent = Intent(Intent.ACTION_OPEN_DOCUMENT).apply {
            addCategory(Intent.CATEGORY_OPENABLE)
            type = "image/png"
        }
        startActivityForResult(intent, code)
    }
    private fun decodeVerified(uri: Uri, expected: String, maxSize: Int, w: Int, h: Int): Bitmap {
        val bytes = contentResolver.openInputStream(uri)?.use { stream ->
            val buffer = ByteArrayOutputStream()
            val block = ByteArray(8192)
            while (true) {
                val n = stream.read(block)
                if (n < 0) break
                require(buffer.size() + n <= maxSize) { "File vượt giới hạn" }
                buffer.write(block, 0, n)
            }
            buffer.toByteArray()
        } ?: throw IllegalArgumentException("Không thể đọc ảnh")
        val got = MessageDigest.getInstance("SHA-256").digest(bytes)
            .joinToString("") { "%02x".format(it.toInt() and 0xff) }
        require(got == expected) { "Sai SHA nguồn; từ chối file" }
        val options = BitmapFactory.Options().apply { inJustDecodeBounds = true }
        BitmapFactory.decodeByteArray(bytes, 0, bytes.size, options)
        require(options.outWidth == w && options.outHeight == h) { "Kích thước sai" }
        return BitmapFactory.decodeByteArray(bytes, 0, bytes.size)
            ?: throw IllegalArgumentException("Không thể giải mã PNG")
    }
    private fun validAtlas(source: Bitmap, sheet: Bitmap): Boolean {
        val first = Bitmap.createBitmap(sheet, 0, 0, W, H)
        if (!first.sameAs(source)) return false
        // Reject a sheet which secretly changes body/hair/costume outside two ROIs.
        for (i in 1 until FRAMES) for (y in 0 until H) for (x in 0 until W) {
            val inLeft = x in 88 until 104 && y in 50 until 56
            val inRight = x in 107 until 124 && y in 50 until 57
            if (!inLeft && !inRight && sheet.getPixel(i * W + x, y) != source.getPixel(x, y))
                return false
        }
        return true
    }
    @Deprecated("Compatible document picker on minSdk 23")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (resultCode != RESULT_OK || requestCode !in listOf(PICK_CANON, PICK_ATLAS)) return
        val uri = data?.data ?: return
        try {
            if (requestCode == PICK_CANON) {
                val png = decodeVerified(uri, CANON_SHA, 5_000_000, 941, 1672)
                val crop = Bitmap.createBitmap(png, FRONT[0], FRONT[1], W, H)
                front = crop
                atlas = null
                chooseAtlas.isEnabled = true
                viewer.setAssets(crop, null)
                status.text = "CANON ✓ | Mở đúng ảnh gốc 208×443. Chọn atlas CP417 để xem nháy mắt."
            } else {
                val source = front ?: throw IllegalArgumentException("Chọn CANON trước")
                val candidate = decodeVerified(uri, ATLAS_SHA, 3_000_000, FRAMES * W, H)
                require(validAtlas(source, candidate)) { "Atlas sửa sai pixel ngoài mắt / frame 0" }
                atlas = candidate
                viewer.setAssets(source, candidate)
                status.text = "CANON ✓ | CP417 atlas ✓ | 5 khung cùng pose. DEMO, không phải production."
            }
        } catch (e: Exception) {
            if (requestCode == PICK_CANON) {
                front = null; atlas = null; chooseAtlas.isEnabled = false
                viewer.setAssets(null, null)
            } else {
                atlas = null
                viewer.setAssets(front, null)
            }
            status.text = "Từ chối tệp: ${e.message}"
        }
    }
    override fun onStop() { viewer.setPlaying(false); super.onStop() }
    override fun onResume() { super.onResume(); if (::viewer.isInitialized) viewer.setPlaying(playing) }

    private inner class BlinkView : View(this@TVKCP417SamePoseBlinkActivity) {
        private var source: Bitmap? = null
        private var sheet: Bitmap? = null
        private var anchor = SystemClock.uptimeMillis()
        private var freeze = 0L
        private var active = true
        private val paint = Paint(Paint.ANTI_ALIAS_FLAG or Paint.FILTER_BITMAP_FLAG)
        fun setAssets(front: Bitmap?, atlas: Bitmap?) {
            source = front; sheet = atlas; anchor = SystemClock.uptimeMillis(); freeze = 0L
            invalidate()
        }
        fun setPlaying(on: Boolean) {
            if (active == on) return
            if (on) anchor = SystemClock.uptimeMillis() - freeze
            else freeze = (SystemClock.uptimeMillis() - anchor).coerceAtLeast(0L)
            active = on
            invalidate()
        }
        private fun eased(t: Double): Double {
            val x = t.coerceIn(0.0, 1.0); return x*x*(3-2*x)
        }
        private fun currentFrame(): Int {
            val t = ((if (active) SystemClock.uptimeMillis()-anchor else freeze).toDouble()/1000.0) % 2.4
            return when {
                t < 1.80 -> 0
                t < 1.95 -> (4*eased((t-1.80)/0.15)).roundToInt().coerceIn(0,4)
                t < 2.03 -> 4
                t < 2.22 -> (4*(1-eased((t-2.03)/0.19))).roundToInt().coerceIn(0,4)
                else -> 0
            }
        }
        override fun onDraw(canvas: Canvas) {
            super.onDraw(canvas)
            val src = source ?: return
            val scale = min(width.toFloat()/W, height.toFloat()/H)
            val w = W*scale; val h = H*scale
            val destination = RectF((width-w)/2f,(height-h)/2f,(width+w)/2f,(height+h)/2f)
            canvas.drawColor(Color.rgb(227, 237, 246))
            val data = sheet
            if (data == null) canvas.drawBitmap(src, null, destination, paint)
            else {
                val i = currentFrame()
                canvas.drawBitmap(data, Rect(i*W, 0, (i+1)*W, H), destination, paint)
                if (active && isAttachedToWindow) postInvalidateOnAnimation()
            }
        }
    }
}