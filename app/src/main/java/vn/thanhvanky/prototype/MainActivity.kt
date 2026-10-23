package vn.thanhvanky.prototype

import android.app.Activity
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Path
import android.graphics.RectF
import android.os.Bundle
import android.view.MotionEvent
import android.view.View
import android.widget.Toast
import kotlin.math.min

class MainActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(MapPrototypeView(this))
    }
}

private class MapPrototypeView(activity: Activity) : View(activity) {
    private val p = Paint(Paint.ANTI_ALIAS_FLAG)
    private var place = "map"
    private var message = "Chạm vào địa điểm để di chuyển"
    private var affection = 0
    private var outfit = 0
    private var interaction = "Chạm vào tóc, mặt, tay hoặc chọn hành động."
    private val cream = Color.rgb(246, 230, 188)
    private val ink = Color.rgb(48, 54, 48)
    private val green = Color.rgb(84, 122, 91)
    private val gold = Color.rgb(220, 177, 91)

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        canvas.drawColor(Color.rgb(22, 34, 43))
        val s = min(width / 390f, height / 780f)
        canvas.save()
        canvas.scale(s, s)
        if (place == "map") drawMap(canvas) else if (place == "nguyetly") drawNguyetLy(canvas) else drawLocation(canvas)
        canvas.restore()
    }

    private fun paint(color: Int, style: Paint.Style = Paint.Style.FILL, size: Float = 2f) {
        p.color = color
        p.style = style
        p.strokeWidth = size
    }

    private fun text(c: Canvas, value: String, x: Float, y: Float, size: Float, color: Int = cream, bold: Boolean = false) {
        paint(color)
        p.textSize = size
        p.typeface = if (bold) android.graphics.Typeface.create("serif", android.graphics.Typeface.BOLD)
                     else android.graphics.Typeface.create("serif", android.graphics.Typeface.NORMAL)
        p.textAlign = Paint.Align.CENTER
        c.drawText(value, x, y, p)
    }

    private fun rounded(c: Canvas, l: Float, t: Float, r: Float, b: Float, color: Int, radius: Float = 14f) {
        paint(color)
        c.drawRoundRect(RectF(l, t, r, b), radius, radius, p)
    }

    private fun drawMap(c: Canvas) {
        text(c, "THANH VÂN KÝ", 195f, 46f, 25f, gold, true)
        text(c, "BẢN ĐỒ THANH VÂN SƠN", 195f, 72f, 13f)
        rounded(c, 14f, 92f, 376f, 700f, Color.rgb(41, 68, 61), 22f)
        // parchment-like valley
        paint(Color.rgb(91, 119, 81))
        c.drawOval(RectF(30f, 150f, 360f, 620f), p)
        paint(Color.rgb(119, 143, 93))
        c.drawOval(RectF(65f, 205f, 330f, 575f), p)
        // mountain silhouettes
        val peaks = listOf(
            floatArrayOf(18f, 260f, 90f, 125f, 154f, 265f),
            floatArrayOf(95f, 250f, 184f, 105f, 264f, 250f),
            floatArrayOf(210f, 260f, 294f, 135f, 370f, 265f),
            floatArrayOf(15f, 400f, 80f, 285f, 145f, 400f),
            floatArrayOf(245f, 420f, 315f, 285f, 380f, 420f)
        )
        for (v in peaks) {
            paint(Color.rgb(61, 88, 78))
            val path = Path().apply { moveTo(v[0], v[1]); lineTo(v[2], v[3]); lineTo(v[4], v[5]); close() }
            c.drawPath(path, p)
            paint(Color.rgb(170, 184, 148))
            c.drawCircle(v[2], v[3] + 12f, 4f, p)
        }
        // winding river/path
        paint(Color.rgb(110, 177, 190), Paint.Style.STROKE, 8f)
        val river = Path().apply { moveTo(330f, 180f); cubicTo(240f, 290f, 330f, 370f, 190f, 445f); cubicTo(100f, 500f, 170f, 560f, 55f, 620f) }
        c.drawPath(river, p)
        paint(Color.rgb(226, 207, 155), Paint.Style.STROKE, 3f)
        c.drawPath(river, p)
        // locations
        marker(c, 192f, 310f, "Thanh Vân Tông", "🏯")
        marker(c, 92f, 475f, "Trấn Thanh Hà", "◆")
        marker(c, 285f, 525f, "Rừng Trúc", "♣")
        marker(c, 282f, 215f, "Bí cảnh", "✦", true)
        rounded(c, 28f, 642f, 362f, 687f, Color.rgb(27, 43, 39), 12f)
        text(c, message, 195f, 670f, 13f, cream)
        text(c, "Chạm biểu tượng để khám phá • Khu vực khóa sẽ mở theo cốt truyện", 195f, 724f, 10f, Color.LTGRAY)
    }

    private fun marker(c: Canvas, x: Float, y: Float, label: String, symbol: String, locked: Boolean = false) {
        paint(if (locked) Color.rgb(90, 91, 91) else gold)
        c.drawCircle(x, y, 24f, p)
        paint(if (locked) Color.rgb(58, 65, 66) else Color.rgb(77, 83, 57))
        c.drawCircle(x, y, 19f, p)
        text(c, symbol, x, y + 7f, 22f, if (locked) Color.LTGRAY else cream, true)
        text(c, if (locked) "🔒 $label" else label, x, y + 43f, 12f, cream, true)
    }

    private fun drawLocation(c: Canvas) {
        text(c, placeTitle(), 195f, 46f, 24f, gold, true)
        text(c, "CẢNH 2D • CHẠM ĐỂ TƯƠNG TÁC", 195f, 72f, 12f)
        rounded(c, 12f, 92f, 378f, 690f, Color.rgb(67, 91, 78), 20f)
        // sky and distant mountains
        paint(Color.rgb(160, 183, 166))
        c.drawRect(20f, 100f, 370f, 320f, p)
        paint(Color.rgb(94, 125, 105))
        val m1 = Path().apply { moveTo(20f, 310f); lineTo(95f, 180f); lineTo(170f, 310f); close() }
        val m2 = Path().apply { moveTo(120f, 310f); lineTo(235f, 155f); lineTo(370f, 310f); close() }
        c.drawPath(m1, p); c.drawPath(m2, p)
        // courtyard floor
        paint(Color.rgb(173, 151, 111))
        c.drawRect(20f, 310f, 370f, 680f, p)
        paint(Color.rgb(127, 106, 81))
        c.drawRect(20f, 470f, 370f, 490f, p)
        // temple/building
        paint(Color.rgb(85, 58, 51))
        c.drawRect(105f, 245f, 285f, 390f, p)
        paint(Color.rgb(139, 58, 49))
        val roof = Path().apply { moveTo(75f, 260f); lineTo(195f, 190f); lineTo(315f, 260f); close() }
        c.drawPath(roof, p)
        paint(gold, Paint.Style.STROKE, 3f)
        c.drawLine(75f, 260f, 315f, 260f, p)
        paint(Color.rgb(207, 174, 117))
        c.drawRect(170f, 310f, 220f, 390f, p)
        // NPC touch points
        drawNpc(c, 85f, 445f, "Tiểu sư muội")
        drawNpc(c, 300f, 445f, "Chấp sự")
        rounded(c, 32f, 535f, 358f, 605f, Color.rgb(36, 49, 43), 12f)
        text(c, message, 195f, 563f, 13f, cream)
        text(c, "Chạm nhân vật hoặc đại điện để xem tương tác", 195f, 585f, 10f, Color.LTGRAY)
        rounded(c, 34f, 620f, 356f, 670f, gold, 12f)
        text(c, "← QUAY LẠI BẢN ĐỒ", 195f, 650f, 15f, ink, true)
    }

    private fun drawNpc(c: Canvas, x: Float, y: Float, label: String) {
        paint(Color.rgb(44, 52, 48))
        c.drawOval(RectF(x - 23f, y - 8f, x + 23f, y + 56f), p)
        paint(Color.rgb(231, 194, 155))
        c.drawCircle(x, y - 20f, 18f, p)
        paint(Color.rgb(54, 42, 43))
        c.drawCircle(x, y - 25f, 19f, p)
        paint(Color.rgb(231, 194, 155))
        c.drawCircle(x, y - 18f, 14f, p)
        text(c, label, x, y + 78f, 12f, cream, true)
    }


    // Prototype interaction screen: original Canvas placeholder, no external art asset.
    private fun drawNguyetLy(c: Canvas) {
        text(c, "TÔ NGUYỆT LY", 195f, 43f, 25f, gold, true)
        text(c, "Độ thân thiết: $affection", 195f, 70f, 14f)
        rounded(c, 12f, 90f, 378f, 522f, Color.rgb(53, 78, 94), 20f)
        paint(Color.rgb(109, 151, 162))
        c.drawCircle(195f, 265f, 125f, p)
        // Hair silhouette, head, shoulders and robe are simple touch targets.
        paint(Color.rgb(216, 220, 234))
        c.drawOval(RectF(127f, 120f, 263f, 415f), p)
        paint(Color.rgb(245, 211, 195))
        c.drawOval(RectF(151f, 170f, 239f, 279f), p)
        paint(Color.rgb(234, 238, 249))
        c.drawOval(RectF(102f, 298f, 288f, 495f), p)
        paint(if (outfit == 0) Color.rgb(126, 184, 207) else Color.rgb(183, 145, 200))
        c.drawOval(RectF(135f, 315f, 255f, 490f), p)
        paint(gold, Paint.Style.STROKE, 3f)
        c.drawOval(RectF(135f, 315f, 255f, 490f), p)
        text(c, "Tóc", 195f, 151f, 13f, ink)
        text(c, "Khuôn mặt", 195f, 227f, 12f, ink)
        text(c, "Trang phục", 195f, 399f, 13f, ink)
        rounded(c, 15f, 525f, 375f, 585f, Color.rgb(29, 48, 56), 10f)
        text(c, interaction, 195f, 558f, 12f)
        rounded(c, 18f, 600f, 187f, 646f, gold, 10f)
        rounded(c, 203f, 600f, 372f, 646f, gold, 10f)
        text(c, "NẮM TAY", 102f, 629f, 14f, ink, true)
        text(c, "ĐỔI TRANG PHỤC", 287f, 629f, 12f, ink, true)
        rounded(c, 18f, 658f, 187f, 704f, gold, 10f)
        rounded(c, 203f, 658f, 372f, 704f, gold, 10f)
        text(c, "TRÒ CHUYỆN", 102f, 687f, 13f, ink, true)
        text(c, "TẶNG HOA", 287f, 687f, 13f, ink, true)
        rounded(c, 25f, 719f, 365f, 765f, Color.rgb(87, 116, 112), 10f)
        text(c, "← TRỞ VỀ THANH VÂN TÔNG", 195f, 748f, 13f)
    }

    private fun interactNguyetLy(x: Float, y: Float) {
        if (y in 719f..780f) {
            place = "sect"
            message = "Bạn đã trở về Thanh Vân Tông."
        } else if (y in 600f..646f && x < 195f) {
            affection += 2
            interaction = "Nguyệt Ly mỉm cười và nắm tay bạn."
        } else if (y in 600f..646f) {
            outfit = 1 - outfit
            interaction = "Nguyệt Ly đã đổi sang bộ trang phục khác."
        } else if (y in 658f..704f && x < 195f) {
            affection += 1
            interaction = "Nguyệt Ly: Hôm nay huynh muốn đi đâu?"
        } else if (y in 658f..704f) {
            affection += 3
            interaction = "Nguyệt Ly vui vẻ nhận bó hoa của bạn."
        } else if (x in 120f..270f && y in 120f..180f) {
            affection += 1
            interaction = "Nguyệt Ly khẽ chỉnh lại mái tóc bạc."
        } else if (x in 145f..245f && y in 180f..290f) {
            affection += 1
            interaction = "Nguyệt Ly đỏ mặt: Huynh đang nhìn gì vậy?"
        } else if (x in 90f..300f && y in 295f..510f) {
            interaction = "Trang phục tiên hiệp mềm mại, điểm viền vàng."
        } else {
            interaction = "Hãy chạm vào nhân vật hoặc chọn hành động."
        }
        invalidate()
    }

    private fun placeTitle() = when (place) {
        "sect" -> "Thanh Vân Tông"
        "town" -> "Trấn Thanh Hà"
        "forest" -> "Rừng Trúc"
        else -> "Bí cảnh"
    }

    override fun onTouchEvent(event: MotionEvent): Boolean {
        if (event.action != MotionEvent.ACTION_UP) return true
        val s = min(width / 390f, height / 780f)
        val x = event.x / s
        val y = event.y / s
        if (place == "nguyetly") {
            interactNguyetLy(x, y)
        } else if (place == "map") {
            if (y in 260f..370f && x in 135f..250f) enter("sect", "Bạn đã đến Thanh Vân Tông.")
            else if (y in 420f..510f && x in 40f..145f) enter("town", "Trấn Thanh Hà: có thể tìm thương nhân và tin tức.")
            else if (y in 470f..575f && x in 230f..345f) enter("forest", "Rừng Trúc: nghe thấy tiếng động lạ.")
            else if (y in 170f..250f && x in 235f..330f) {
                message = "Bí cảnh chưa mở. Hãy tiếp tục cốt truyện!"
                invalidate()
            } else {
                message = "Hãy chạm một biểu tượng địa điểm."
                invalidate()
            }
        } else {
            if (y in 610f..685f) {
                place = "map"; message = "Chạm vào địa điểm để di chuyển"; invalidate()
            } else if (y in 390f..535f && x < 145f) {
                if (place == "sect") { place = "nguyetly"; interaction = "Nguyệt Ly: Huynh đã về rồi!"; invalidate(); return true }
                message = "Tiểu sư muội: “Sư huynh, huynh vừa trở về sao?”"
                Toast.makeText(context, message, Toast.LENGTH_LONG).show(); invalidate()
            } else if (y in 390f..535f && x > 245f) {
                message = "Chấp sự: “Có nhiệm vụ mới ở đại điện.”"
                Toast.makeText(context, message, Toast.LENGTH_LONG).show(); invalidate()
            } else if (y in 180f..400f && x in 100f..290f) {
                message = "Đại điện: nơi nhận nhiệm vụ và gặp trưởng lão."
                Toast.makeText(context, message, Toast.LENGTH_LONG).show(); invalidate()
            } else {
                message = "Chạm NPC hoặc công trình để tương tác."
                invalidate()
            }
        }
        return true
    }

    private fun enter(id: String, text: String) {
        place = id
        message = text
        invalidate()
    }
}
