package vn.thanhvanky.prototype

import org.json.JSONObject

/**
 * Two independent approvals:
 * 1. Character/expression *reference* approval controls which emotion options
 *    appear in the UI; 2. production *sprite* approval controls what may render.
 * A successful visual preview, alpha-patch test, or green CI is NOT approval of
 * actual game sprites. Missing/unsafe art must never fall back to another
 * wardrobe, condition or expression.
 */
internal object CharacterExpressionCatalog {
    data class Option(val id: String, val label: String)

    private val SAFE_ID = Regex("[a-z0-9_]{1,64}")
    private val SHA256 = Regex("[0-9a-f]{64}")

    private fun approvedCharacter(catalogue: JSONObject, characterId: String): JSONObject? {
        if (catalogue.optInt("schema_version") != 1 || !SAFE_ID.matches(characterId)) return null
        val characters = catalogue.optJSONArray("characters") ?: return null
        for (i in 0 until characters.length()) {
            val item = characters.optJSONObject(i) ?: continue
            if (item.optString("id") == characterId &&
                item.optString("approval_status") == "explicit_user_approved_expression_preview") {
                return item
            }
        }
        return null
    }

    /** Approved emotion *direction*; independent of sprite readiness. */
    fun approvedOptions(catalogue: JSONObject, characterId: String): List<Option> {
        val item = approvedCharacter(catalogue, characterId) ?: return emptyList()
        val items = item.optJSONArray("approved_expressions") ?: return emptyList()
        val result = mutableListOf<Option>()
        val seen = mutableSetOf<String>()
        for (i in 0 until items.length()) {
            val obj = items.optJSONObject(i) ?: return emptyList()
            val id = obj.optString("id")
            val label = obj.optString("label")
            if (!SAFE_ID.matches(id) || label.isBlank() || !seen.add(id)) return emptyList()
            result.add(Option(id, label))
        }
        return result
    }

    /** Used by debug UI to distinguish old placeholder art from released CANON sprites. */
    fun hasRuntimeArtApproval(catalogue: JSONObject, characterId: String): Boolean {
        val approved = approvedCharacter(catalogue, characterId) ?: return false
        return approvedSpriteRelease(approved) != null &&
            (approved.optJSONObject("sprite_paths")?.length() ?: 0) > 0
    }

    fun isApproved(catalogue: JSONObject, characterId: String, expression: String): Boolean =
        approvedOptions(catalogue, characterId).any { it.id == expression }

    fun faceVisible(pose: String): Boolean = pose != "back" && pose != "back_turn"

    /** The user-approved reference is never enough to ship a sprite. */
    private fun approvedSpriteRelease(character: JSONObject): JSONObject? {
        val release = character.optJSONObject("production_release") ?: return null
        if (release.optString("status") != "approved_for_runtime" ||
            !release.optBoolean("artist_qa_passed") ||
            !release.optBoolean("runtime_qa_passed") ||
            release.optString("user_asset_approval_id").isBlank()) return null

        if (release.optString("canonical_body_visual_id") != character.optString("canonical_body_visual_id") ||
            release.optString("canonical_body_sha256") != character.optString("canonical_body_sha256") ||
            release.optString("approved_expression_profile_id") != character.optString("approved_profile_id") ||
            release.optString("approved_expression_sha256") != character.optString("expression_preview_sha256") ||
            !SHA256.matches(release.optString("sprite_manifest_sha256"))) return null

        return if (release.optJSONObject("approved_sprite_hashes") != null) release else null
    }

    /**
     * Require a reviewed production release and exact artwork combination:
     * expression × wardrobe × integrity × pose. Path hashes in the approval
     * manifest are verified against actual APK assets by CI before shipping.
     * Android performs only path/metadata lookups on the UI thread.
     */
    fun resolveSprite(
        catalogue: JSONObject,
        characterId: String,
        state: CharacterAppearanceState.State,
        exists: (String) -> Boolean
    ): String? {
        if (!isApproved(catalogue, characterId, state.expression)) return null
        val character = approvedCharacter(catalogue, characterId) ?: return null
        val release = approvedSpriteRelease(character) ?: return null
        val path = character.optJSONObject("sprite_paths")
            ?.optJSONObject(state.expression)
            ?.optJSONObject(state.wardrobe)
            ?.optJSONObject(state.integrity.toString())
            ?.optString(state.pose).orEmpty()
        if (path.isBlank() ||
            !path.startsWith("characters/" + characterId + "/") ||
            !path.endsWith(".png") || path.contains("..") || path.contains('\\') ||
            !path.matches(Regex("[A-Za-z0-9_./-]+"))) return null
        val hash = release.optJSONObject("approved_sprite_hashes")?.optString(path).orEmpty()
        if (!SHA256.matches(hash)) return null
        return if (exists(path)) path else null
    }
}