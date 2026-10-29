package vn.thanhvanky.prototype

import android.content.Context
import android.content.pm.ApplicationInfo
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Paint
import android.graphics.RectF
import android.os.SystemClock
import android.util.Log
import android.view.View
import kotlin.math.PI
import kotlin.math.exp
import kotlin.math.min
import kotlin.math.sin

/**
 * Renders subtle, continuous local movement on an existing portrait:
 * breathing in the upper torso and a slight delay in loose hair.
 * This is a bitmap-mesh preview, NOT a skeletal Spine/Live2D rig.
 * It cannot articulate limbs, change pose, or remove clothing.
 */
class TVKCharacterMotionView(
    context: Context,
    private val sprite: Bitmap,
    private val cycleSeconds: Double = 3.6,
    private val movement: Float = 1f
) : View(context) {
    private val cols = 16
    private val rows = 28
    private val mesh = FloatArray((cols + 1) * (rows + 1) * 2)
    private val paint = Paint(Paint.ANTI_ALIAS_FLAG or Paint.FILTER_BITMAP_FLAG)
    private val bounds = RectF()
    private val startMs = SystemClock.uptimeMillis()
    // Debug-only Canvas callback pacing; this is not GPU presentation time.
    private val collectFrameStats =
        (context.applicationInfo.flags and ApplicationInfo.FLAG_DEBUGGABLE) != 0
    private var windowStartMs = 0L
    private var previousDrawMs = 0L
    private var windowDraws = 0
    private var lateDraws = 0

    private fun sampleDrawCadence(nowMs: Long) {
        if (!collectFrameStats || !animate || !isShown) return
        if (previousDrawMs == 0L || nowMs - previousDrawMs > 1000L) {
            windowStartMs = nowMs
            windowDraws = 0
            lateDraws = 0
        } else {
            if (nowMs - previousDrawMs > 33L) lateDraws++
            windowDraws++
        }
        previousDrawMs = nowMs
        val ms = nowMs - windowStartMs
        if (ms >= 2000L) {
            val fps = if (ms > 0L) windowDraws * 1000f / ms else 0f
            Log.d("TVKMotion", "canvas_draw_fps=" +
                String.format(java.util.Locale.US, "%.1f", fps) +
                " slow_intervals_over_33ms=$lateDraws/$windowDraws" +
                " debug_only_not_display_fps")
            windowStartMs = nowMs
            windowDraws = 0
            lateDraws = 0
        }
    }

    private var animate = true
    private var reactionRegion = ""
    private var reactionStartMs = 0L

    /** Brief, local movement on touch; visual only, with no explicit imagery. */
    fun react(regionId: String) {
        reactionRegion = regionId
        reactionStartMs = SystemClock.uptimeMillis()
        invalidate()
    }

    fun setMotionEnabled(enabled: Boolean) {
        animate = enabled
        invalidate()
    }

    override fun onAttachedToWindow() {
        super.onAttachedToWindow()
        invalidate()
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        if (sprite.width <= 0 || sprite.height <= 0 || width <= 0 || height <= 0) return
        val scale = min(width.toFloat() / sprite.width, height.toFloat() / sprite.height)
        val w = sprite.width * scale
        val h = sprite.height * scale
        bounds.set((width - w) * .5f, (height - h) * .5f,
            (width + w) * .5f, (height + h) * .5f)
        val nowMs = SystemClock.uptimeMillis()
        sampleDrawCadence(nowMs)
        val elapsed = (nowMs - startMs).toDouble() / 1000.0
        val phase = if (animate) elapsed * 2.0 * PI / cycleSeconds.coerceAtLeast(1.8) else 0.0
        val breath = if (animate) sin(phase).toFloat() * movement else 0f
        val hair = if (animate) sin(phase * .63 + .65).toFloat() * movement else 0f
        val reactionElapsed = SystemClock.uptimeMillis() - reactionStartMs
        val reactProgress = (reactionElapsed / 600f).coerceIn(0f, 1f)
        val reactAmplitude = if (reactionRegion.isNotEmpty() && reactProgress < 1f)
            (sin(reactProgress * PI).toFloat() * (1f - reactProgress)) else 0f
        val reactCenterY = when (reactionRegion) {
            "head", "face" -> .17f
            "hand" -> .42f
            "chest", "belly" -> .43f
            "thigh", "buttocks" -> .72f
            "leg" -> .85f
            else -> .48f
        }

        for (row in 0..rows) {
            val v = row.toFloat() / rows
            val torsoY = exp(-((v - .365f) * (v - .365f) / (.135f * .135f)))
            val headY = exp(-((v - .155f) * (v - .155f) / (.25f * .25f)))
            for (col in 0..cols) {
                val u = col.toFloat() / cols
                val torsoX = exp(-((u - .5f) * (u - .5f) / (.35f * .35f)))
                val looseHair = exp(-((u - .20f) * (u - .20f) / .05f)) +
                    exp(-((u - .80f) * (u - .80f) / .05f))
                val dx = (u - .5f) * .012f * breath * torsoY * torsoX +
                    .0022f * hair * headY * looseHair
                val reactWeight = exp(-((v - reactCenterY) * (v - reactCenterY) / .035f)) * torsoX
                val dy = -.0052f * breath * torsoY * torsoX +
                    .0015f * hair * headY * looseHair +
                    .004f * reactAmplitude * reactWeight
                val index = (row * (cols + 1) + col) * 2
                mesh[index] = (u + dx) * w
                mesh[index + 1] = (v + dy) * h
            }
        }
        canvas.save()
        canvas.clipRect(bounds)
        canvas.translate(bounds.left, bounds.top)
        canvas.drawBitmapMesh(sprite, cols, rows, mesh, 0, null, 0, paint)
        canvas.restore()
        // Queue the next drawing at the display's VSYNC, instead of a fixed
        // 40 ms delay (~25 FPS). This improves frame pacing on 60/90/120 Hz
        // devices but does not guarantee a measured frame rate on any phone.
        if ((animate || reactAmplitude > 0f) && isAttachedToWindow)
            postInvalidateOnAnimation()
    }
}
