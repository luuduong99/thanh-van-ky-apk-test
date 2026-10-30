package vn.thanhvanky.prototype

import android.content.Context
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Rect
import android.graphics.RectF
import android.view.View
import kotlin.math.min

/** CP410 debug face-expression inset, deliberately SEPARATE from the standing-body pose.
 * This is not fullbody blink integration. It uses the exact CANON/CP409 atlas only.
 */
class TVKCombinedBlinkInsetView(
    context: Context,
    private val atlas: Bitmap,
    private val clock: TVKPreviewClock
) : View(context) {
    private val artPaint = Paint(Paint.ANTI_ALIAS_FLAG or Paint.FILTER_BITMAP_FLAG)
    private val textPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        color = Color.rgb(42, 58, 82)
        textSize = 25f
    }
    private val src = Rect()
    private val dst = RectF()

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        if (width <= 0 || height <= 0) return
        val frame = TVKDebugBlinkTiming.poseAt(clock.elapsedSeconds())
        // Frame 0 is pixel-identical to CANON face. Other frames are CP409 drafts.
        src.set(frame * 168, 0, (frame + 1) * 168, 197)
        val scale = min(width / 168f, (height - 30f).coerceAtLeast(1f) / 197f)
        val w = 168f * scale
        val h = 197f * scale
        dst.set((width - w) / 2, 30f + (height - 30f - h) / 2,
            (width + w) / 2, 30f + (height - 30f + h) / 2)
        canvas.drawColor(Color.rgb(239, 243, 248))
        canvas.drawBitmap(atlas, src, dst, artPaint)
        canvas.drawText("Mắt CP409, pose khác — ${frame + 1}/15", 5f, 26f, textPaint)
        if (clock.playing && isAttachedToWindow && isShown) postInvalidateOnAnimation()
    }
}