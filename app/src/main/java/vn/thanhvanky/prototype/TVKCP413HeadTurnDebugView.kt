package vn.thanhvanky.prototype

import android.content.Context
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Path
import android.graphics.RectF
import android.view.View
import kotlin.math.min

/** CP413: diagnostic of the exact front-standing CANON, NOT character art or a head rig.
 *
 * At 0 degrees this renders the unmodified bitmap. At the four sample angles the
 * conservative CP411 head polygon is moved above an intentionally BLANK underpaint.
 * White seams are failures to fix by hand painting, NEVER final art. No other pose,
 * expression crop, blur/upscale or character bitmap may be substituted.
 *
 * This view is only instantiated from a SHA-verified CANON crop in a debug Activity.
 */
internal class TVKCP413HeadTurnDebugView(context: Context, private val canon: Bitmap) : View(context) {
    init { require(canon.width == 208 && canon.height == 443) { "Wrong CANON front crop size" } }
    companion object {
        private const val W = 208f
        private const val H = 443f
        private const val PIVOT_X = 104f
        private const val PIVOT_Y = 77f
        private val HEAD = floatArrayOf(
            100f,1f, 91f,2f, 81f,8f, 72f,18f, 66f,31f, 64f,46f,
            69f,58f, 75f,68f, 85f,77f, 94f,82f, 106f,85f,
            118f,80f, 129f,73f, 138f,60f, 143f,47f,
            138f,33f, 131f,22f, 128f,13f, 115f,3f
        )
        val angles = intArrayOf(-4, -2, 0, 2, 4)
        val exposedAreaPixels = intArrayOf(271, 174, 0, 174, 276)
    }
    private val imagePaint = Paint(Paint.ANTI_ALIAS_FLAG or Paint.FILTER_BITMAP_FLAG)
    private val holePaint = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = Color.WHITE; style = Paint.Style.FILL }
    private val outlinePaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        color = Color.rgb(218, 42, 59); style = Paint.Style.STROKE; strokeWidth = 0.7f
    }
    private val path = Path().apply {
        moveTo(HEAD[0], HEAD[1]); for (i in 2 until HEAD.size step 2) lineTo(HEAD[i], HEAD[i + 1]); close()
    }
    private val bodyWithMissingPaint = Bitmap.createBitmap(208, 443, Bitmap.Config.ARGB_8888).also {
        Canvas(it).apply { drawBitmap(canon, 0f, 0f, imagePaint); drawPath(path, holePaint) }
    }
    private val headExperimental = Bitmap.createBitmap(208, 443, Bitmap.Config.ARGB_8888).also {
        Canvas(it).apply {
            save(); clipPath(path); drawBitmap(canon, 0f, 0f, imagePaint); restore()
        }
    }
    private var sampleAngle = 0
    fun setAngle(degrees: Int) {
        require(degrees in angles) { "Only the 5 CP412-reviewed sample angles are allowed" }
        sampleAngle = degrees; invalidate()
    }
    fun currentAngle() = sampleAngle

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        if (width < 2 || height < 2) return
        val scale = min(width.toFloat() / W, height.toFloat() / H)
        val rect = RectF((width - W * scale) / 2f, (height - H * scale) / 2f,
            (width + W * scale) / 2f, (height + H * scale) / 2f)
        canvas.save(); canvas.clipRect(rect)
        canvas.translate(rect.left, rect.top); canvas.scale(scale, scale)
        if (sampleAngle == 0) {
            // Exact source at the neutral keyframe; no mesh deformation or overlays.
            canvas.drawBitmap(canon, 0f, 0f, imagePaint)
        } else {
            // Intentionally unpainted hole: show the blocker rather than hiding it.
            canvas.drawBitmap(bodyWithMissingPaint, 0f, 0f, imagePaint)
            canvas.save(); canvas.rotate(sampleAngle.toFloat(), PIVOT_X, PIVOT_Y)
            canvas.drawBitmap(headExperimental, 0f, 0f, imagePaint)
            canvas.restore()
            canvas.drawPath(path, outlinePaint)
        }
        canvas.restore()
    }
}