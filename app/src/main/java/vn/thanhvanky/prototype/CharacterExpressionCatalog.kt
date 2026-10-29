package vn.thanhvanky.prototype

import org.json.JSONObject

/**
 * Approved expression metadata for individual characters.
 *
 * A reference image is not a sprite. Missing facial art must never silently
 * fall back to a different expression, costume or garment integrity.
 * The five Lam Thien previews were approved independently of CANON BODY V2.
 */
internal object CharacterExpressionCatalog {
    data class Option(val id: String, val label: String)

    private fun approvedCharacter(catalogue: JSONObject, characterId: String): JSONObject? {
        if (catalogue.optInt("schema_version") != 1) return null
        val characters = catalogue.optJSONArray("characters") ?: return null
        for (i in 0 until characters.length()) {
            val item = characters.optJSONObject(i) ?: continue
            if (item.optString("id") == characterId &&
                item.optString("approval_status") == "approved_reference_sprite_pending") {
                return item
            }
        }
        return null
    }

    /** Only explicitly approved expressions are user-selectable. */
    fun approvedOptions(catalogue: JSONObject, characterId: String): List<Option> {
        val item = approvedCharacter(catalogue, characterId) ?: return emptyList()
        val items = item.optJSONArray("approved_expressions") ?: return emptyList()
        val result = mutableListOf<Option>()
        val seen = mutableSetOf<String>()
        for (i in 0 until items.length()) {
            val obj = items.optJSONObject(i) ?: return emptyList()
            val id = obj.optString("id")
            val label = obj.optString("label")
            if (!id.matches(Regex("[a-z0-9_]{1,64}")) ||
                label.isBlank() || !seen.add(id)) return emptyList()
            result.add(Option(id, label))
        }
        return result
    }

    fun isApproved(catalogue: JSONObject, characterId: String, expression: String): Boolean =
        approvedOptions(catalogue, characterId).any { it.id == expression }

    /** Back-facing poses may preserve expression state without drawing a visible face. */
    fun faceVisible(pose: String): Boolean = pose != "back" && pose != "back_turn"

    /**
     * An optional future image must match ALL appearance dimensions:
     * expression -> wardrobe -> integrity -> pose. Never use a generic 100%
     * reference for damaged, changed-clothes or differently posed states.
     *
     * The approved Lam Thien profile has no sprite_paths yet, so this
     * intentionally returns null until real QA-approved art is supplied.
     */
    fun resolveSprite(
        catalogue: JSONObject,
        characterId: String,
        state: CharacterAppearanceState.State,
        exists: (String) -> Boolean
    ): String? {
        if (!isApproved(catalogue, characterId, state.expression)) return null
        val character = approvedCharacter(catalogue, characterId) ?: return null
        val path = character.optJSONObject("sprite_paths")
            ?.optJSONObject(state.expression)
            ?.optJSONObject(state.wardrobe)
            ?.optJSONObject(state.integrity.toString())
            ?.optString(state.pose).orEmpty()
        if (path.isBlank() ||
            !path.startsWith("characters/" + characterId + "/") ||
            !path.endsWith(".png") || path.contains("..") ||
            path.contains('\\')) return null
        return if (exists(path)) path else null
    }
}
