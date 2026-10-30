package vn.thanhvanky.prototype

import android.content.Context
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Paint
import android.graphics.RectF
import android.view.View
import kotlin.math.PI
import kotlin.math.exp
import kotlin.math.min
import kotlin.math.sin

/** Debug-only single-bitmap deformation, not a jointed body rig or approved animation.
 * CP410: shares clock with a separately labeled face-crop blink review pane.
 */
class TVKCombinedIdleMotionView(
    context: Context,
    private val canonCrop: Bitmap,
    private val timeline: TVKPreviewClock = TVKPreviewClock()
) : View(context) {
    private val columns = 20
    private val rows = 36
    private val mesh = FloatArray((columns + 1) * (rows + 1) * 2)
    private val paint = Paint(Paint.ANTI_ALIAS_FLAG or Paint.FILTER_BITMAP_FLAG)
    private val box = RectF()
    private val enabled = BooleanArray(5) { true } // breath, head, arm, hair, silk
    private var auditNeutralSource = false
    fun setAuditNeutralSource(on: Boolean) { auditNeutralSource = on; invalidate() }
    val playing: Boolean get() = timeline.playing

    fun setPlaying(active: Boolean) { timeline.setPlaying(active); invalidate() }
    fun flipChannel(index: Int): Boolean {
        require(index in 0..4)
        enabled[index] = !enabled[index]
        invalidate()
        return enabled[index]
    }
    fun activeChannelCount() = enabled.count { it }
    private fun gaussian(z: Double, center: Double, spread: Double): Double {
        val d = (z - center) / spread
        return exp(-.5 * d * d)
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        if (width < 2 || height < 2) return
        val scale = min(width.toFloat() / canonCrop.width, height.toFloat() / canonCrop.height)
        val w = canonCrop.width * scale
        val h = canonCrop.height * scale
        box.set((width - w) * .5f, (height - h) * .5f, (width + w) * .5f, (height + h) * .5f)
        if (auditNeutralSource) {
            // Draw exact original front pose, not a t=0 mesh with nonzero phase offsets.
            canvas.drawBitmap(canonCrop, null, box, paint)
            return
        }
        // Unlike CP408, PAUSE freezes exact current time rather than snapping to t=0.
        val t = timeline.elapsedSeconds()
        val breathing = if (enabled[0]) sin(2 * PI * t / 3.8) else 0.0
        val head = if (enabled[1]) sin(2 * PI * t / 6.2 + .42) else 0.0
        val arms = if (enabled[2]) sin(2 * PI * t / 5.3 + .9) else 0.0
        val hair = if (enabled[3]) sin(2 * PI * t / 5.7 + .15) else 0.0
        val silk = if (enabled[4]) sin(2 * PI * t / 4.5 + .3) else 0.0
        for (row in 0..rows) {
            val v = row.toDouble() / rows
            for (col in 0..columns) {
                val u = col.toDouble() / columns
                var dx = 0.0
                var dy = 0.0
                val torso = gaussian(v, .29, .13) * gaussian(u, .49, .22)
                dx += (u - .49) * .010 * breathing * torso
                dy -= .0031 * breathing * torso
                val headMask = gaussian(v, .13, .09) * gaussian(u, .50, .30)
                dx += .0055 * head * headMask
                dy += .0013 * head * headMask
                val armMask = gaussian(v, .45, .19) * (gaussian(u, .19, .10) + gaussian(u, .81, .10))
                dx += .0045 * arms * armMask
                dy += .0011 * arms * armMask
                val hairMask = gaussian(v, .32, .29) * (gaussian(u, .14, .13) + gaussian(u, .89, .13))
                dx += .0065 * hair * hairMask
                dy += .0009 * hair * hairMask
                val hem = gaussian(v, .80, .23) * (gaussian(u, .15, .23) + gaussian(u, .84, .23))
                dx += .0085 * silk * hem
                dy += .0014 * silk * hem
                val i = (row * (columns + 1) + col) * 2
                mesh[i] = ((u + dx) * w).toFloat()
                mesh[i + 1] = ((v + dy) * h).toFloat()
            }
        }
        canvas.save()
        canvas.clipRect(box)
        canvas.translate(box.left, box.top)
        canvas.drawBitmapMesh(canonCrop, columns, rows, mesh, 0, null, 0, paint)
        canvas.restore()
        if (playing && isAttachedToWindow && activeChannelCount() > 0) postInvalidateOnAnimation()
    }
}