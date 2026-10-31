package vn.thanhvanky.prototype

/** State adapter intentionally preserves existing SharedPreferences names and values. */
object TVKQuestEngine {
    const val PREFS_NAME = "tvk_chapter_1"
    const val KEY_COMPLETE = "complete" // Legacy key: intro choice made, NOT entire chapter finished.
    const val KEY_CHOICE = "choice"
    const val FOREST = "forest"
    const val SECT = "sect"

    data class SavedState(val introChoiceMade: Boolean = false, val choice: String? = null)
    data class Objective(val id: String, val label: String, val destinationId: String)

    fun restore(complete: Boolean, choice: String?): SavedState =
        if (complete && (choice == FOREST || choice == SECT)) SavedState(true, choice)
        else SavedState()

    fun choose(progress: TVKDialogueEngine.Progress, choice: String): SavedState? {
        if (!TVKDialogueEngine.choicesVisible(progress)) return null
        if (choice != FOREST && choice != SECT) return null
        return SavedState(true, choice)
    }

    fun objective(state: SavedState): Objective? = when (state.choice.takeIf { state.introChoiceMade }) {
        FOREST -> Objective("investigate_forest", "Điều tra Rừng Trúc", FOREST)
        SECT -> Objective("ask_steward", "Hỏi chấp sự về dị tượng", SECT)
        else -> null
    }

    fun companionIds(state: SavedState): List<String> =
        if (objective(state) == null) emptyList() else listOf("to_nguyet_ly")

    fun destinationMessage(state: SavedState): String? = when (state.choice.takeIf { state.introChoiceMade }) {
        FOREST -> "Nguyệt Ly cùng bạn tiến vào Rừng Trúc."
        SECT -> "Hai người trở về đại điện chuẩn bị."
        else -> null
    }
}
