package vn.thanhvanky.prototype

/** Pure location hit-testing in the original 390 x 780 logical map coordinates. */
object TVKWorldMap {
    data class Location(
        val id: String,
        val label: String,
        val left: Float,
        val top: Float,
        val right: Float,
        val bottom: Float,
        val unlocked: Boolean
    ) {
        fun contains(x: Float, y: Float) = x in left..right && y in top..bottom
    }

    data class Selection(val destination: String?, val message: String, val locked: Boolean = false)

    val locations = listOf(
        Location("sect", "Thanh Vân Tông", 135f, 260f, 250f, 370f, true),
        Location("town", "Trấn Thanh Hà", 40f, 420f, 145f, 510f, true),
        Location("forest", "Rừng Trúc", 230f, 470f, 345f, 575f, true),
        Location("secret", "Bí cảnh", 235f, 170f, 330f, 250f, false)
    )

    fun select(x: Float, y: Float): Selection {
        val hit = locations.firstOrNull { it.contains(x, y) }
            ?: return Selection(null, "Hãy chạm một biểu tượng địa điểm.")
        if (!hit.unlocked) return Selection(null, "Bí cảnh chưa mở. Hãy tiếp tục cốt truyện!", true)
        val message = when (hit.id) {
            "sect" -> "Bạn đã đến Thanh Vân Tông."
            "town" -> "Trấn Thanh Hà: có thể tìm thương nhân và tin tức."
            "forest" -> "Rừng Trúc: nghe thấy tiếng động lạ."
            else -> return Selection(null, "Địa điểm chưa hỗ trợ.", true)
        }
        return Selection(hit.id, message)
    }
}
