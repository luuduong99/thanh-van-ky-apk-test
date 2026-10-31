package vn.thanhvanky.prototype

/** Dialogue content mirrors the six already-shipped Chapter I lines; no new CANON dialogue. */
object TVKDialogueEngine {
    data class Line(val id: String, val speakerId: String, val textVi: String)
    data class Progress(val lineIndex: Int = 0, val visibleChars: Int = 0)

    val lines = listOf(
        Line("ch01_001", "narrator", "Sương sớm phủ trên lối đá. Sau nhiều ngày xa tông môn, bạn trở về."),
        Line("ch01_002", "to_nguyet_ly", "Tô Nguyệt Ly: Huynh về rồi! Muội đã đợi từ sáng. Chuyến đi có thuận lợi không?"),
        Line("ch01_003", "protagonist", "Nam chính: Có chút trắc trở, nhưng thấy muội bình an là tốt rồi."),
        Line("ch01_004", "to_nguyet_ly", "Tô Nguyệt Ly: Đêm qua linh khí ở Rừng Trúc biến động. Muội lo có chuyện chẳng lành."),
        Line("ch01_005", "narrator", "Một cơn gió lạnh lướt qua mái hiên, mang theo mùi trúc ẩm."),
        Line("ch01_006", "to_nguyet_ly", "Tô Nguyệt Ly: Chúng ta nên làm gì trước khi trời tối?")
    )

    fun current(state: Progress): Line = lines[state.lineIndex.coerceIn(0, lines.lastIndex)]

    fun typeNext(state: Progress, chars: Int = 2): Progress {
        require(chars >= 0) { "chars must be nonnegative" }
        val index = state.lineIndex.coerceIn(0, lines.lastIndex)
        return Progress(index, (state.visibleChars + chars).coerceIn(0, lines[index].textVi.length))
    }

    /** First tap reveals the whole line, second tap advances; final line waits for a choice. */
    fun tap(state: Progress): Progress {
        val index = state.lineIndex.coerceIn(0, lines.lastIndex)
        val length = lines[index].textVi.length
        if (state.visibleChars < length) return Progress(index, length)
        return if (index < lines.lastIndex) Progress(index + 1, 0) else Progress(index, length)
    }

    fun choicesVisible(state: Progress): Boolean =
        state.lineIndex == lines.lastIndex && state.visibleChars >= lines.last().textVi.length
}
