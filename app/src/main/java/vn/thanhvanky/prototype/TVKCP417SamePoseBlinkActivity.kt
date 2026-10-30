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
import kotlin.math.PI
import kotlin.math.exp
import kotlin.math.sin
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
    private lateinit var compareMode: Button
    private lateinit var combinedMode: Button
    private var requestedCombined = false
    private val frameButtons = ArrayList<Button>()
    private var changedPixels = IntArray(FRAMES)
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
        requestedCombined = intent.getBooleanExtra("cp419_combined", false)
        if ((applicationInfo.flags and ApplicationInfo.FLAG_DEBUGGABLE) == 0) { finish(); return }
        val col = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(10), dp(10), dp(10), dp(10))
            setBackgroundColor(Color.rgb(21, 35, 52))
        }
        col.addView(info("CP419 • LÂM THIỂN — CÙNG POSE: IDLE + BLINK (DEBUG)", 17f))
        col.addView(info("CANON đứng 208×443 + 5 khung mắt cùng pose. Kết hợp 5 kênh idle trên ảnh phẳng, KHÔNG phải rig.", 12f))
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
            if (viewer.hasAtlas()) {
                playing = !playing
                viewer.setFrameOverride(null)
                viewer.setPlaying(playing)
                playPause.text = if (playing) "Tạm dừng" else "Tiếp tục"
                status.text = if (playing) "Đang xem blink DRAFT (2,4 giây/chu kỳ)." else "Đã tạm dừng: chọn một trong 5 khung để soi."
            }
        }
        playPause.isEnabled = false
        col.addView(playPause, LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(42)))
        compareMode = button("Soi cận 2 mặt: CANON / khung đang chọn") {
            val next = !viewer.comparing
            viewer.setCompareMode(next)
            if (next && viewer.combined) {
                viewer.setCombinedMode(false)
                combinedMode.text = "CP419 | Bật thở + đầu + tay + tóc + lụa cùng mắt"
            }
            compareMode.text = if (next) "Về toàn thân" else "Soi cận 2 mặt: CANON / khung đang chọn"
        }
        compareMode.isEnabled = false
        col.addView(compareMode, LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(38)))
        combinedMode = button("CP419 | Bật thở + đầu + tay + tóc + lụa cùng mắt") {
            viewer.setCombinedMode(!viewer.combined)
            if (viewer.combined && viewer.comparing) {
                viewer.setCompareMode(false)
                compareMode.text = "Soi cận 2 mặt: CANON / khung đang chọn"
            }
            combinedMode.text = if (viewer.combined) "CP419 | Tắt chuyển động cơ thể" else "CP419 | Bật thở + đầu + tay + tóc + lụa cùng mắt"
            status.text = if (viewer.combined) "CP419 | CÙNG POSE: mesh 5 kênh + blink; DEBUG, KHÔNG phải rig/Spine." else "CP418 | Soi 5 khung, không có chuyển động cơ thể."
        }
        combinedMode.isEnabled = false
        col.addView(combinedMode, LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(42)))
        val stepRow = LinearLayout(this)
        for (step in 0 until FRAMES) {
            val b = button("$step/4") {
                playing = false
                viewer.setPlaying(false)
                viewer.setFrameOverride(step)
                playPause.text = "Chạy lại"
                status.text = "CP418 | Khung $step/4: ${changedPixels[step]} pixel khác CANON, chỉ trong vùng mắt."
            }
            b.isEnabled = false
            frameButtons.add(b)
            stepRow.addView(b, LinearLayout.LayoutParams(0, dp(40), 1f))
        }
        col.addView(stepRow)
        col.addView(info("Ảnh CANON không nằm trong APK. Phóng to chỉ để kiểm pixel, không tạo HD/rig/Spine.", 11f))
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
    private fun validAtlas(source: Bitmap, sheet: Bitmap): IntArray? {
        val first = Bitmap.createBitmap(sheet, 0, 0, W, H)
        if (!first.sameAs(source)) return null
        // One bulk read per bitmap, no hundreds of thousands of getPixel JNI calls.
        val original = IntArray(W * H)
        source.getPixels(original, 0, W, 0, 0, W, H)
        val atlasPixels = IntArray(FRAMES * W * H)
        sheet.getPixels(atlasPixels, 0, FRAMES * W, 0, 0, FRAMES * W, H)
        val differences = IntArray(FRAMES)
        // Fail closed if any frame changes skin/body/costume/hair outside two eye ROIs.
        for (i in 1 until FRAMES) for (y in 0 until H) for (x in 0 until W) {
            val inLeft = x in 88 until 104 && y in 50 until 56
            val inRight = x in 107 until 124 && y in 50 until 57
            val sourcePixel = original[y * W + x]
            val atlasPixel = atlasPixels[y * FRAMES * W + i * W + x]
            if (sourcePixel != atlasPixel) {
                if (!inLeft && !inRight) return null
                differences[i]++
            }
        }
        return differences
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
                playPause.isEnabled = false
                compareMode.isEnabled = false
                combinedMode.isEnabled = false
                viewer.setCombinedMode(false)
                for (button in frameButtons) button.isEnabled = false
                viewer.setCompareMode(false)
                compareMode.text = "Soi cận 2 mặt: CANON / khung đang chọn"
                viewer.setAssets(crop, null)
                status.text = "CANON ✓ | Mở đúng ảnh gốc 208×443. Chọn atlas CP417 để xem nháy mắt."
            } else {
                val source = front ?: throw IllegalArgumentException("Chọn CANON trước")
                val candidate = decodeVerified(uri, ATLAS_SHA, 3_000_000, FRAMES * W, H)
                val counts = validAtlas(source, candidate)
                    ?: throw IllegalArgumentException("Atlas sửa sai pixel ngoài mắt / frame 0")
                changedPixels = counts
                atlas = candidate
                viewer.setAssets(source, candidate)
                playing = true
                viewer.setPlaying(true)
                playPause.text = "Tạm dừng"
                playPause.isEnabled = true
                compareMode.isEnabled = true
                combinedMode.isEnabled = true
                viewer.setCombinedMode(requestedCombined)
                combinedMode.text = if (requestedCombined) "CP419 | Tắt chuyển động cơ thể" else "CP419 | Bật thở + đầu + tay + tóc + lụa cùng mắt"
                for (button in frameButtons) button.isEnabled = true
                status.text = "CANON ✓ | Atlas CP417 ✓ | So cận và chọn 0/4…4/4; chưa duyệt art."
            }
        } catch (e: Exception) {
            if (requestCode == PICK_CANON) {
                front = null; atlas = null; chooseAtlas.isEnabled = false
                playPause.isEnabled = false
                compareMode.isEnabled = false
                combinedMode.isEnabled = false
                viewer.setCombinedMode(false)
                for (button in frameButtons) button.isEnabled = false
                viewer.setAssets(null, null)
            } else {
                atlas = null
                playPause.isEnabled = false
                compareMode.isEnabled = false
                combinedMode.isEnabled = false
                viewer.setCombinedMode(false)
                for (button in frameButtons) button.isEnabled = false
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
        private var frameOverride: Int? = null
        private var slices: List<Bitmap> = emptyList()
        private val motionColumns = 20
        private val motionRows = 36
        private val motionMesh = FloatArray((motionColumns+1)*(motionRows+1)*2)
        var combined = false
            private set
        var comparing = false
            private set
        private val paint = Paint(Paint.ANTI_ALIAS_FLAG or Paint.FILTER_BITMAP_FLAG)
        private val pixelPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply { isFilterBitmap = false }
        private val outline = Paint(Paint.ANTI_ALIAS_FLAG).apply {
            color = Color.rgb(255, 193, 37); style = Paint.Style.STROKE; strokeWidth = 1.5f
        }
        private val caption = Paint(Paint.ANTI_ALIAS_FLAG).apply {
            color = Color.rgb(25, 45, 70); textSize = dp(12).toFloat()
        }
        fun hasAtlas(): Boolean = sheet != null
        fun setFrameOverride(index: Int?) {
            require(index == null || index in 0 until FRAMES)
            frameOverride = index
            invalidate()
        }
        fun setCompareMode(on: Boolean) { comparing = on; invalidate() }
        fun setCombinedMode(on: Boolean) {
            combined = on && sheet != null
            invalidate()
        }
        fun setAssets(front: Bitmap?, atlas: Bitmap?) {
            source = front; sheet = atlas; frameOverride = null
            // All five slices contain the exact SAME front body pose. No extra face image.
            slices = if (atlas == null) emptyList() else (0 until FRAMES).map {
                Bitmap.createBitmap(atlas, it*W, 0, W, H)
            }
            combined = false
            anchor = SystemClock.uptimeMillis(); freeze = 0L
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
        private fun elapsedSeconds(): Double = (if (active) SystemClock.uptimeMillis()-anchor else freeze)
            .coerceAtLeast(0L).toDouble() / 1000.0
        private fun currentFrame(tSeconds: Double): Int {
            val t = tSeconds % 2.4
            return when {
                t < 1.80 -> 0
                t < 1.95 -> (4*eased((t-1.80)/0.15)).roundToInt().coerceIn(0,4)
                t < 2.03 -> 4
                t < 2.22 -> (4*(1-eased((t-2.03)/0.19))).roundToInt().coerceIn(0,4)
                else -> 0
            }
        }
        private fun gaussian(x: Double, center: Double, spread: Double): Double {
            val d=(x-center)/spread
            return exp(-0.5*d*d)
        }
        // CP419 technical mesh uses THE SAME timestamp and SAME source frame as blink.
        // Not head/neck separation, painting, physics, or a production rig.
        private fun drawSamePoseMotion(canvas: Canvas, frame: Bitmap, destination: RectF, seconds: Double) {
            val breath=sin(2*PI*seconds/3.8)
            val head=sin(2*PI*seconds/6.2+0.42)
            val arm=sin(2*PI*seconds/5.3+0.9)
            val hair=sin(2*PI*seconds/5.7+0.15)
            val silk=sin(2*PI*seconds/4.5+0.3)
            for (row in 0..motionRows) {
                val v=row.toDouble()/motionRows
                for (col in 0..motionColumns) {
                    val u=col.toDouble()/motionColumns
                    var dx=0.0
                    var dy=0.0
                    val torso=gaussian(v,0.29,0.13)*gaussian(u,0.49,0.22)
                    dx+=(u-0.49)*0.010*breath*torso
                    dy-=0.0031*breath*torso
                    val headRegion=gaussian(v,0.13,0.09)*gaussian(u,0.50,0.30)
                    dx+=0.0055*head*headRegion
                    dy+=0.0013*head*headRegion
                    val armRegion=gaussian(v,0.45,0.19)*(gaussian(u,0.19,0.10)+gaussian(u,0.81,0.10))
                    dx+=0.0045*arm*armRegion
                    dy+=0.0011*arm*armRegion
                    val hairRegion=gaussian(v,0.32,0.29)*(gaussian(u,0.14,0.13)+gaussian(u,0.89,0.13))
                    dx+=0.0065*hair*hairRegion
                    dy+=0.0009*hair*hairRegion
                    val hem=gaussian(v,0.80,0.23)*(gaussian(u,0.15,0.23)+gaussian(u,0.84,0.23))
                    dx+=0.0085*silk*hem
                    dy+=0.0014*silk*hem
                    val index=(row*(motionColumns+1)+col)*2
                    motionMesh[index]=((u+dx)*destination.width()).toFloat()
                    motionMesh[index+1]=((v+dy)*destination.height()).toFloat()
                }
            }
            canvas.save()
            canvas.clipRect(destination)
            canvas.translate(destination.left,destination.top)
            canvas.drawBitmapMesh(frame,motionColumns,motionRows,motionMesh,0,null,0,paint)
            canvas.restore()
        }
        override fun onDraw(canvas: Canvas) {
            super.onDraw(canvas)
            val src = source ?: return
            val scale = min(width.toFloat()/W, height.toFloat()/H)
            val w = W*scale; val h = H*scale
            val destination = RectF((width-w)/2f,(height-h)/2f,(width+w)/2f,(height+h)/2f)
            canvas.drawColor(Color.rgb(227, 237, 246))
            val data = sheet
            // One monotonic clock chooses both the eyelid state and body deformation.
            val seconds = elapsedSeconds()
            val i = frameOverride ?: currentFrame(seconds)
            if (comparing && data != null) {
                // Two true source-pixel crops side-by-side. Large display != new HD artwork.
                val face = Rect(80, 34, 135, 91)
                val space = dp(8).toFloat()
                val paneWidth = ((width.toFloat() - 3f * space) / 2f).coerceAtLeast(1f)
                val paneScale = min(paneWidth / face.width(), (height.toFloat() - dp(48)) / face.height())
                val pw = face.width() * paneScale; val ph = face.height() * paneScale
                val top = ((height.toFloat() - ph) / 2f).coerceAtLeast(dp(30).toFloat())
                val left = RectF(space, top, space + pw, top + ph)
                val rightX = 2f * space + paneWidth
                val right = RectF(rightX, top, rightX + pw, top + ph)
                canvas.drawText("CANON · GỐC", left.left, (top - dp(9)).coerceAtLeast(dp(14).toFloat()), caption)
                canvas.drawText("KHUNG $i/4", right.left, (top - dp(9)).coerceAtLeast(dp(14).toFloat()), caption)
                canvas.drawBitmap(src, face, left, pixelPaint)
                val frameFace = Rect(i*W + face.left, face.top, i*W + face.right, face.bottom)
                canvas.drawBitmap(data, frameFace, right, pixelPaint)
                fun markEyes(pane: RectF) {
                    val sx = pane.width() / face.width(); val sy = pane.height() / face.height()
                    for (rect in listOf(Rect(88,50,104,56), Rect(107,50,124,57))) {
                        val rx = pane.left + (rect.left-face.left)*sx
                        val ry = pane.top + (rect.top-face.top)*sy
                        canvas.drawRect(rx, ry, pane.left+(rect.right-face.left)*sx,
                            pane.top+(rect.bottom-face.top)*sy, outline)
                    }
                }
                markEyes(left); markEyes(right)
            } else if (data == null) canvas.drawBitmap(src, null, destination, paint)
            else if (combined && slices.size == FRAMES) {
                drawSamePoseMotion(canvas, slices[i], destination, seconds)
            } else canvas.drawBitmap(data, Rect(i*W, 0, (i+1)*W, H), destination, paint)
            if (active && data != null && frameOverride == null && isAttachedToWindow) postInvalidateOnAnimation()
        }
    }
}