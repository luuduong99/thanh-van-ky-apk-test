package vn.thanhvanky.prototype

import android.content.Context
import org.json.JSONObject

/**
 * Shared appearance state for EVERY character. Wardrobe, garment condition, pose,
 * expression and action are independent. None is implicitly reset by changing another.
 *
 * The saved state is authoritative even when the required art has not yet been drawn.
 * Missing artwork is reported, never replaced silently with another costume/condition.
 */
internal object CharacterAppearanceState {
    private const val PREFS = "tvk_character_appearance_v1"
    private const val OLD_INTERACTIONS = "tvk_character_interactions"
    private const val OLD_CHAPTER = "tvk_chapter_1"
    val INTEGRITY_STEPS = intArrayOf(100, 70, 50, 30)

    data class State(
        val wardrobe: String = "default",
        val integrity: Int = 100,
        val pose: String = "front",
        val expression: String = "normal",
        val action: String = "idle"
    )

    data class Art(
        val path: String?,
        val issue: String? = null,
        val crop: String = "full"
    )

    private fun prefKey(id: String, name: String): String = "${id}__${name}"
    private fun validId(id: String): Boolean = id.matches(Regex("[a-z0-9_]{1,64}"))
    private fun preferences(context: Context) = context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)

    fun read(context: Context, id: String): State {
        if (!validId(id)) return State()
        val prefs = preferences(context)
        val old = context.getSharedPreferences(OLD_INTERACTIONS, Context.MODE_PRIVATE)
        val oldChapter = context.getSharedPreferences(OLD_CHAPTER, Context.MODE_PRIVATE)
        val wardrobe = if (prefs.contains(prefKey(id, "wardrobe")))
            prefs.getString(prefKey(id, "wardrobe"), "default") ?: "default"
        else old.getString("outfit_" + id, "default") ?: "default"
        val pose = if (prefs.contains(prefKey(id, "pose")))
            prefs.getString(prefKey(id, "pose"), "front") ?: "front"
        else old.getString("pose_" + id, "front") ?: "front"
        val legacyIntegrity = if (id == "to_nguyet_ly" && oldChapter.contains("garment_step"))
            INTEGRITY_STEPS[oldChapter.getInt("garment_step", 0).coerceIn(0, 3)]
        else 100
        val integrity = prefs.getInt(prefKey(id, "integrity"), legacyIntegrity)
            .let { if (it in INTEGRITY_STEPS) it else 100 }
        return State(
            wardrobe = wardrobe,
            integrity = integrity,
            pose = pose,
            expression = prefs.getString(prefKey(id, "expression"), "normal") ?: "normal",
            action = prefs.getString(prefKey(id, "action"), "idle") ?: "idle"
        )
    }

    fun setWardrobe(context: Context, id: String, wardrobe: String) {
        if (validId(id) && wardrobe.matches(Regex("[a-z0-9_]{1,64}")))
            preferences(context).edit().putString(prefKey(id, "wardrobe"), wardrobe).apply()
    }

    fun setIntegrity(context: Context, id: String, integrity: Int) {
        if (validId(id) && integrity in INTEGRITY_STEPS)
            preferences(context).edit().putInt(prefKey(id, "integrity"), integrity).apply()
    }

    fun setPose(context: Context, id: String, pose: String) {
        if (validId(id) && pose.matches(Regex("[a-z0-9_]{1,64}")))
            preferences(context).edit().putString(prefKey(id, "pose"), pose).apply()
    }

    fun setExpression(context: Context, id: String, expression: String) {
        if (validId(id) && expression.matches(Regex("[a-z0-9_]{1,64}")))
            preferences(context).edit().putString(prefKey(id, "expression"), expression).apply()
    }

    fun setAction(context: Context, id: String, action: String) {
        if (validId(id) && action.matches(Regex("[a-z0-9_]{1,64}")))
            preferences(context).edit().putString(prefKey(id, "action"), action).apply()
    }

    /**
     * A missing combination returns a blank art path; it NEVER renders fully
     * clothed 100% default art for an undressed / damaged saved state.
     *
     * Optional schema: wardrobeStates[].integrityImages["70"][poseId] = assetPath
     * for 70/50/30. Without a matching real file the state remains saved but art
     * is withheld. A 100% default outfit uses pose.image as before.
     */
    fun resolveArt(character: JSONObject, state: State, exists: (String) -> Boolean): Art {
        val poses = character.optJSONArray("poses")
        var matchedPose: JSONObject? = null
        if (poses != null) for (i in 0 until poses.length()) {
            val candidate = poses.optJSONObject(i) ?: continue
            if (candidate.optString("id") == state.pose) {
                matchedPose = candidate
                break
            }
        }
        if (matchedPose == null) return Art(null, "Tư thế chưa được đăng ký")
        val crop = matchedPose.optString("crop", "full")
        val states = character.optJSONArray("wardrobeStates")
        var wardrobe: JSONObject? = null
        if (states != null) for (i in 0 until states.length()) {
            val candidate = states.optJSONObject(i) ?: continue
            if (candidate.optString("id") == state.wardrobe) {
                wardrobe = candidate
                break
            }
        }
        if (wardrobe == null) return Art(null, "Chưa đăng ký mức trang phục: " + state.wardrobe, crop)
        val path = if (state.integrity == 100) {
            if (state.wardrobe == "default") matchedPose.optString("image")
            else wardrobe.optJSONObject("images")?.optString(state.pose).orEmpty()
        } else {
            wardrobe.optJSONObject("integrityImages")
                ?.optJSONObject(state.integrity.toString())
                ?.optString(state.pose).orEmpty()
        }
        if (path.isBlank() || !exists(path)) {
            return Art(null, "Thiếu ảnh: " + state.wardrobe +
                " / " + state.integrity + "% / " + state.pose, crop)
        }
        return Art(path, crop = crop)
    }
}
