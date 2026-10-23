package vn.thanhvanky.prototype

import android.app.Activity
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.BitmapRegionDecoder
import android.graphics.Rect
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
import kotlin.math.sin

class MainActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(MapPrototypeView(this))
    }
}

private class MapPrototypeView(activity: Activity) : View(activity) {
    private val p = Paint(Paint.ANTI_ALIAS_FLAG or Paint.FILTER_BITMAP_FLAG)
    // Decode once. Read only the left panel of the supplied triptych, without changing its file.
    private val nguyetLyPortrait: Bitmap = context.assets.open("characters/heroines_reference.png").use { stream ->
        val decoder = requireNotNull(BitmapRegionDecoder.newInstance(stream, false))
        try {
            requireNotNull(decoder.decodeRegion(Rect(0, 0, decoder.width / 3, decoder.height), BitmapFactory.Options()))
        } finally { decoder.recycle() }
    }
    private val mainPortrait: Bitmap = context.assets.open("characters/main_portrait.png").use {
        requireNotNull(BitmapFactory.decodeStream(it, null, BitmapFactory.Options().apply { inSampleSize = 2 }))
    }

    private fun portrait(c: Canvas, bitmap: Bitmap, bounds: RectF, shift: Float = 0f) {
        val scale = kotlin.math.max(bounds.width() / bitmap.width, (bounds.height() + 10f) / bitmap.height)
        val w = bitmap.width * scale
        val h = bitmap.height * scale
        val left = bounds.centerX() - w / 2f
        val top = bounds.centerY() - h / 2f
        c.save()
        c.clipRect(bounds)
        c.translate(0f, shift)
        p.alpha = 255
        p.style = Paint.Style.FILL
        c.drawBitmap(bitmap, null, RectF(left, top, left + w, top + h), p)
        c.restore()
    }
    private val storyPrefs = context.getSharedPreferences("tvk_chapter_1", 0)
    private var storyIndex = 0
    private var storyVisible = 0
    private var storyComplete = storyPrefs.getBoolean("complete", false)
    private val storyLines = arrayOf(
        "Sương sớm phủ trên lối đá. Sau nhiều ngày xa tông môn, bạn trở về.",
        "Tô Nguyệt Ly: Huynh về rồi! Muội đã đợi từ sáng. Chuyến đi có thuận lợi không?",
        "Nam chính: Có chút trắc trở, nhưng thấy muội bình an là tốt rồi.",
        "Tô Nguyệt Ly: Đêm qua linh khí ở Rừng Trúc biến động. Muội lo có chuyện chẳng lành.",
        "Một cơn gió lạnh lướt qua mái hiên, mang theo mùi trúc ẩm.",
        "Tô Nguyệt Ly: Chúng ta nên làm gì trước khi trời tối?"
    )
    private var place = "map"
    private var message = "Chạm vào địa điểm để di chuyển"
    private var affection = 0
    private var demoSpeed = 1
    private var demoStrength = 1
    private var demoPlaying = true
    private var demoFrame = 0f
    private var demoVeil = false
    private var romanceMode = 0
    private var romanceText = "Đêm trăng thanh tĩnh."
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
        if (place == "story") drawStory(canvas) else if (place == "map") drawMap(canvas) else if (place == "nguyetly") drawNguyetLy(canvas) else if (place == "animation_demo") drawAnimationDemo(canvas) else if (place == "romance") drawRomance(canvas) else drawLocation(canvas)
        canvas.restore()
        if (place == "animation_demo" && demoPlaying) postInvalidateDelayed(33L)
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

    private fun drawStory(c: Canvas) {
        text(c, "CHƯƠNG I • SƯƠNG TRÊN NÚI", 195f, 43f, 20f, gold, true)
        rounded(c, 12f, 75f, 378f, 530f, Color.rgb(39, 59, 77), 18f)
        portrait(c, nguyetLyPortrait, RectF(65f, 88f, 325f, 510f))
        rounded(c, 15f, 528f, 375f, 663f, Color.rgb(25, 39, 53), 12f)
        val line = storyLines[storyIndex]
        val words = line.take(storyVisible).split(" ")
        val rows = mutableListOf<String>()
        var row = ""
        for (word in words) {
            if ((row.length + word.length) > 38 && row.isNotEmpty()) {
                rows.add(row); row = word
            } else row = if (row.isEmpty()) word else "$"+"row $"+"word"
        }
        if (row.isNotEmpty()) rows.add(row)
        rows.take(4).forEachIndexed { i, v -> text(c, v, 195f, 557f + i * 25f, 12f) }
        if (storyIndex == storyLines.lastIndex && storyVisible == line.length) {
            rounded(c, 18f, 665f, 372f, 709f, gold, 10f)
            text(c, "Cùng Nguyệt Ly đến Rừng Trúc", 195f, 693f, 13f, ink, true)
            rounded(c, 18f, 715f, 372f, 760f, green, 10f)
            text(c, "Về đại điện chuẩn bị trước", 195f, 743f, 13f)
        } else {
            text(c, "Chạm để hiện hết câu / tiếp tục", 195f, 692f, 12f)
            rounded(c, 18f, 715f, 372f, 760f, green, 10f)
            text(c, "← TRỞ VỀ BẢN ĐỒ", 195f, 743f, 13f)
        }
        if (storyVisible < line.length) {
            storyVisible = (storyVisible + 2).coerceAtMost(line.length)
            postInvalidateDelayed(30L)
        }
    }

    private fun interactStory(y: Float) {
        val line = storyLines[storyIndex]
        if (storyIndex == storyLines.lastIndex && storyVisible == line.length) {
            if (y in 665f..760f) {
                val destination = if (y < 712f) "forest" else "sect"
                storyPrefs.edit().putBoolean("complete", true)
                    .putString("choice", destination).apply()
                storyComplete = true
                place = destination
                message = if (destination == "forest")
                    "Nguyệt Ly cùng bạn tiến vào Rừng Trúc."
                else "Hai người trở về đại điện chuẩn bị."
            }
        } else if (y in 715f..760f) {
            place = "map"
        } else if (storyVisible < line.length) {
            storyVisible = line.length
        } else if (storyIndex < storyLines.lastIndex) {
            storyIndex++
            storyVisible = 0
        }
        invalidate()
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
        text(c, "Chạm biểu tượng để khám phá", 195f, 719f, 11f, Color.LTGRAY)
        rounded(c, 32f, 730f, 358f, 770f, gold, 9f)
        text(c, if (storyComplete) "XEM LẠI CHƯƠNG I" else "BẮT ĐẦU CHƯƠNG I", 195f, 756f, 13f, ink, true)
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


    // Portrait supplied and approved by the user; reactions currently use dialogue.
    private fun drawNguyetLy(c: Canvas) {
        text(c, "TÔ NGUYỆT LY", 195f, 43f, 25f, gold, true)
        text(c, "Độ thân thiết: $affection", 195f, 70f, 14f)
        rounded(c, 12f, 90f, 378f, 522f, Color.rgb(53, 78, 94), 20f)
        portrait(c, nguyetLyPortrait, RectF(80f, 122f, 310f, 461f))
        rounded(c, 76f, 90f, 314f, 120f, Color.rgb(100, 70, 110), 8f)
        text(c, "HẸN HÒ DƯỚI TRĂNG", 195f, 111f, 12f)
        rounded(c, 76f, 463f, 314f, 510f, Color.rgb(88, 73, 116), 10f)
        text(c, "THỬ HOẠT ẢNH", 195f, 491f, 13f, cream, true)
        rounded(c, 15f, 525f, 375f, 585f, Color.rgb(29, 48, 56), 10f)
        text(c, interaction, 195f, 558f, 12f)
        rounded(c, 18f, 600f, 187f, 646f, gold, 10f)
        rounded(c, 203f, 600f, 372f, 646f, gold, 10f)
        text(c, "NẮM TAY", 102f, 629f, 14f, ink, true)
        text(c, "TRANG PHỤC", 287f, 629f, 12f, ink, true)
        rounded(c, 18f, 658f, 187f, 704f, gold, 10f)
        rounded(c, 203f, 658f, 372f, 704f, gold, 10f)
        text(c, "TRÒ CHUYỆN", 102f, 687f, 13f, ink, true)
        text(c, "TẶNG HOA", 287f, 687f, 13f, ink, true)
        rounded(c, 25f, 719f, 365f, 765f, Color.rgb(87, 116, 112), 10f)
        text(c, "← TRỞ VỀ THANH VÂN TÔNG", 195f, 748f, 13f)
    }


    // Reusable, content-neutral animation controller prototype.
    // This version moves the approved static portrait; it is not a layered character rig.
    private fun drawAnimationDemo(c: Canvas) {
        if (demoPlaying) demoFrame += 0.065f * (demoSpeed + 1)
        val wave = sin(demoFrame.toDouble()).toFloat() * (demoStrength + 1) * 3f
        text(c, "TÔ NGUYỆT LY • HOẠT ẢNH", 195f, 42f, 21f, gold, true)
        text(c, "Bản thử điều khiển chuyển động 2D", 195f, 69f, 12f)
        rounded(c, 12f, 88f, 378f, 490f, Color.rgb(47, 70, 93), 18f)
        portrait(c, nguyetLyPortrait, RectF(80f, 98f, 310f, 467f), wave * 0.3f)
        text(c, "Ảnh đã chọn • chuyển động ảnh tĩnh", 195f, 482f, 10f)
        if (demoVeil) {
            rounded(c, 22f, 97f, 368f, 467f, Color.argb(185, 34, 41, 64), 16f)
            text(c, "Hiệu ứng màn mờ", 195f, 286f, 17f)
        }
        text(c, "TỐC ĐỘ", 195f, 514f, 13f, gold, true)
        val speedNames = arrayOf("CHẬM", "VỪA", "NHANH")
        for (i in 0..2) {
            val left = 18f + i * 122f
            rounded(c, left, 525f, left + 110f, 565f, if (i == demoSpeed) gold else green, 8f)
            text(c, speedNames[i], left + 55f, 551f, 12f, if (i == demoSpeed) ink else cream, true)
        }
        text(c, "BIÊN ĐỘ CHUYỂN ĐỘNG", 195f, 590f, 13f, gold, true)
        val strengths = arrayOf("NHẸ", "VỪA", "MẠNH")
        for (i in 0..2) {
            val left = 18f + i * 122f
            rounded(c, left, 601f, left + 110f, 641f, if (i == demoStrength) gold else green, 8f)
            text(c, strengths[i], left + 55f, 627f, 12f, if (i == demoStrength) ink else cream, true)
        }
        rounded(c, 18f, 655f, 187f, 696f, gold, 8f)
        rounded(c, 203f, 655f, 372f, 696f, green, 8f)
        text(c, if (demoPlaying) "TẠM DỪNG" else "TIẾP TỤC", 102f, 682f, 13f, ink, true)
        text(c, if (demoVeil) "TẮT MÀN MỜ" else "BẬT MÀN MỜ", 287f, 682f, 12f, cream, true)
        rounded(c, 25f, 715f, 365f, 763f, Color.rgb(87, 116, 112), 10f)
        text(c, "← TRỞ VỀ TÔ NGUYỆT LY", 195f, 745f, 13f)
    }


    private fun drawRomance(c: Canvas) {
        text(c, "TÔ NGUYỆT LY • HẸN HÒ", 195f, 43f, 21f, gold, true)
        text(c, "Độ thân thiết: $affection", 195f, 70f, 14f)
        rounded(c, 12f, 89f, 378f, 495f, Color.rgb(35, 48, 78), 20f)
        paint(Color.rgb(240, 224, 178)); c.drawCircle(306f, 153f, 36f, p)
        val sway = sin(System.currentTimeMillis() / (1100.0 - demoSpeed * 250.0)).toFloat() * (demoStrength + 1) * 0.7f
        portrait(c, mainPortrait, RectF(22f, 105f, 187f, 458f), -sway)
        portrait(c, nguyetLyPortrait, RectF(203f, 105f, 368f, 458f), sway)
        text(c, "NAM CHÍNH", 104f, 480f, 12f, cream, true)
        text(c, "TÔ NGUYỆT LY", 285f, 480f, 12f, cream, true)
        if (romanceMode > 0) text(c, "♥", 195f, 270f, 24f, Color.rgb(245, 155, 169))
        rounded(c, 15f, 500f, 375f, 539f, Color.rgb(39, 56, 65), 8f)
        text(c, romanceText, 195f, 525f, 11f)
        val names = arrayOf("NẮM TAY", "ÔM", "HÔN NHẸ", "VUỐT TÓC")
        for (i in 0..3) {
            val l = if (i % 2 == 0) 18f else 203f
            val t = if (i < 2) 551f else 606f
            rounded(c, l, t, l+169f, t+43f, gold, 8f)
            text(c, names[i], l+84f, t+28f, 13f, ink, true)
        }
        rounded(c, 18f, 660f, 372f, 702f, green, 9f)
        text(c, "CHUYỂN CẢNH RIÊNG TƯ", 195f, 687f, 13f)
        rounded(c, 18f, 715f, 372f, 763f, green, 9f)
        text(c, "← TRỞ VỀ TÔ NGUYỆT LY", 195f, 745f, 13f)
        if (demoVeil) {
            rounded(c, 30f, 100f, 360f, 484f, Color.argb(232, 29, 32, 52), 18f)
            text(c, "Ánh nến dần tắt...", 195f, 283f, 18f)
            text(c, "Chạm cảnh để trở lại", 195f, 309f, 12f)
        }
        postInvalidateDelayed(50L)
    }

    private fun interactRomance(x: Float, y: Float) {
        when {
            demoVeil && y < 495f -> demoVeil = false
            y in 715f..780f -> { demoVeil = false; place = "nguyetly" }
            y in 660f..702f -> demoVeil = !demoVeil
            y in 551f..594f -> {
                if (x < 195f) { romanceMode = 0; romanceText = "Nàng đan tay vào tay bạn."; affection += 2 }
                else { romanceMode = 1; romanceText = "Hai người trao nhau cái ôm ấm áp."; affection += 3 }
            }
            y in 606f..649f -> {
                if (x < 195f) { romanceMode = 2; romanceText = "Nàng đón một nụ hôn dịu dàng."; affection += 4 }
                else { romanceMode = 3; romanceText = "Nàng khép mắt khi bạn vuốt tóc."; affection += 2 }
            }
            y in 120f..490f -> { romanceMode = 1; romanceText = "Nàng nghiêng đầu, mỉm cười."; affection++ }
        }
        invalidate()
    }

    private fun interactAnimationDemo(x: Float, y: Float) {
        when {
            y in 715f..780f -> place = "nguyetly"
            y in 525f..565f -> demoSpeed = ((x - 18f) / 122f).toInt().coerceIn(0, 2)
            y in 601f..641f -> demoStrength = ((x - 18f) / 122f).toInt().coerceIn(0, 2)
            y in 655f..696f && x < 195f -> demoPlaying = !demoPlaying
            y in 655f..696f -> demoVeil = !demoVeil
        }
        invalidate()
    }

    private fun interactNguyetLy(x: Float, y: Float) {
        if (y in 719f..780f) {
            place = "sect"
            message = "Bạn đã trở về Thanh Vân Tông."
        } else if (y in 600f..646f && x < 195f) {
            affection += 2
            interaction = "Nguyệt Ly mỉm cười và nắm tay bạn."
        } else if (y in 600f..646f) {
            interaction = "Chưa có ảnh trang phục khác cho bản thử này."
        } else if (y in 658f..704f && x < 195f) {
            affection += 1
            interaction = "Nguyệt Ly: Hôm nay huynh muốn đi đâu?"
        } else if (y in 658f..704f) {
            affection += 3
            interaction = "Nguyệt Ly vui vẻ nhận bó hoa của bạn."
        } else if (x in 76f..314f && y in 90f..120f) {
            place = "romance"
        } else if (x in 80f..240f && y in 122f..175f) {
            affection += 1
            interaction = "Nguyệt Ly khẽ chỉnh lại mái tóc bạc."
        } else if (x in 140f..245f && y in 175f..230f) {
            affection += 1
            interaction = "Nguyệt Ly đỏ mặt: Huynh đang nhìn gì vậy?"
        } else if (x in 76f..314f && y in 463f..510f) {
            place = "animation_demo"
        } else if (x in 80f..185f && y in 330f..400f) {
            affection += 2
            interaction = "Nguyệt Ly mỉm cười và nắm tay bạn."
        } else if (x in 80f..310f && y in 230f..462f) {
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
        if (place == "story") {
            interactStory(y)
        } else if (place == "romance") {
            interactRomance(x, y)
        } else if (place == "animation_demo") {
            interactAnimationDemo(x, y)
        } else if (place == "nguyetly") {
            interactNguyetLy(x, y)
        } else if (place == "map") {
            if (y in 730f..780f) {
                storyIndex = 0; storyVisible = 0; place = "story"; invalidate()
            } else if (y in 260f..370f && x in 135f..250f) enter("sect", "Bạn đã đến Thanh Vân Tông.")
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
