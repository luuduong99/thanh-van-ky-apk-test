package vn.thanhvanky.prototype

import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Path
import android.graphics.RectF
import android.view.View
import kotlin.math.min

/**
 * CP411 DEBUG-only technical annotations. NO sprite or rig is produced.
 * These coordinates are local to the exact CANON 208x443 standing-front crop.
 * Must ONLY be displayed when the body preview clock is reset and paused.
 */
class TVKFrontPoseRigAuditOverlay(context: Context) : View(context) {
    companion object {
        private const val ART_W = 208f
        private const val ART_H = 443f
        // Research polygon copied from cp411_front_head_preflight.py (not a final matte).
        private val HEAD_POLY = floatArrayOf(
            100f,1f, 91f,2f, 81f,8f, 72f,18f, 66f,31f, 64f,46f,
            69f,58f, 75f,68f, 85f,77f, 94f,82f, 106f,85f,
            118f,80f, 129f,73f, 138f,60f, 143f,47f,
            138f,33f, 131f,22f, 128f,13f, 115f,3f
        )
    }
    private val shape = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        style = Paint.Style.STROKE
        strokeWidth = 1.6f
        color = Color.rgb(250, 170, 25)
    }
    private val eye = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        style = Paint.Style.STROKE; strokeWidth = 1.2f
        color = Color.rgb(37, 160, 139)
    }
    private val neck = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        style = Paint.Style.STROKE; strokeWidth = 1.3f
        color = Color.rgb(211, 72, 137)
    }
    private val marker = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        style = Paint.Style.FILL
        color = Color.rgb(220, 45, 45)
    }
    private val title = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        textSize = 9f; color = Color.rgb(23, 80, 139)
    }
    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        if (width < 1 || height < 1) return
        val s = min(width / ART_W, height / ART_H)
        val x = (width - ART_W * s) / 2f
        val y = (height - ART_H * s) / 2f
        canvas.save()
        canvas.translate(x, y)
        canvas.scale(s, s)
        val p = Path().apply {
            moveTo(HEAD_POLY[0], HEAD_POLY[1])
            for (i in 2 until HEAD_POLY.size step 2) lineTo(HEAD_POLY[i], HEAD_POLY[i+1])
            close()
        }
        canvas.drawPath(p, shape)
        // Boxes are measured on the same standing-front pose, not the expression portrait.
        canvas.drawRect(RectF(83f, 40f, 128f, 74f), shape)
        canvas.drawRect(RectF(89f, 48f, 102f, 58f), eye)
        canvas.drawRect(RectF(107f, 48f, 122f, 58f), eye)
        canvas.drawRect(RectF(92f, 70f, 117f, 91f), neck)
        canvas.drawCircle(104f, 77f, 2.1f, marker)
        canvas.drawText("CANON 208x443 / ROUGH HEAD", 7f, 13f, title)
        canvas.restore()
    }
}