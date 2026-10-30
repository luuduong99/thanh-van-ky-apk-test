package vn.thanhvanky.prototype

import android.app.Activity
import android.app.Dialog
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.BitmapRegionDecoder
import android.graphics.Color
import android.graphics.Rect
import android.graphics.drawable.GradientDrawable
import android.net.Uri
import android.os.Bundle
import android.view.MotionEvent
import android.view.Gravity
import kotlin.math.abs
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.FrameLayout
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.MediaController
import android.widget.ScrollView
import android.widget.TextView
import android.widget.VideoView
import org.json.JSONObject
import java.io.File

/**
 * Reusable Android-native interaction screen. The protagonist accompanies the selected heroine.
 * Catalogue entries and optional non-explicit video paths are defined in assets/character_interactions.json.
 * No explicit clips or fabricated character portraits are bundled here.
 */
class CharacterInteractionActivity : Activity() {
    private val prefs by lazy { getSharedPreferences("tvk_character_interactions", MODE_PRIVATE) }
    private val catalogue by lazy {
        assets.open("character_interactions.json").bufferedReader().use {
            JSONObject(it.readText()).getJSONArray("characters")
        }
    }
    // Approved 5-expression metadata is separate from the character's body model.
    // Unapproved characters receive no borrowed Lam Thien face states.
    private val expressionProfiles by lazy {
        assets.open("character_expression_profiles.json").bufferedReader().use {
            JSONObject(it.readText())
        }
    }
    private var selectedId = "to_nguyet_ly"
    private var currentPose = "front"
    private var messageView: TextView? = null
    private var affinityView: TextView? = null
    private var touchFeedbackView: TextView? = null
    private var videoDialog: Dialog? = null
    private var animatedPortrait: TVKCharacterMotionView? = null
    private val bgColor = Color.rgb(20, 32, 43)
    private val panel = Color.rgb(38, 57, 70)
    private val gold = Color.rgb(225, 190, 123)
    private val cream = Color.rgb(247, 234, 212)
    private val muted = Color.rgb(172, 190, 197)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        selectedId = savedInstanceState?.getString("selected_character")
            ?: intent.getStringExtra("character_id")
            ?: prefs.getString("selected_character", "to_nguyet_ly")
            ?: "to_nguyet_ly"
        if (findCharacter(selectedId) == null) selectedId = "to_nguyet_ly"
        currentPose = savedInstanceState?.getString("selected_pose")
            ?: CharacterAppearanceState.read(this, selectedId).pose
        currentPose = canonicalPose(selectedId, currentPose)
        render()
    }

    override fun onSaveInstanceState(outState: Bundle) {
        outState.putString("selected_character", selectedId)
        outState.putString("selected_pose", currentPose)
        super.onSaveInstanceState(outState)
    }

    override fun onDestroy() {
        videoDialog?.dismiss()
        videoDialog = null
        super.onDestroy()
    }

    private fun dp(n: Int) = (n * resources.displayMetrics.density + .5f).toInt()
    private fun rounded(color: Int, radius: Int = 12) = GradientDrawable().apply {
        setColor(color)
        cornerRadius = dp(radius).toFloat()
    }
    private fun column(pad: Int = 0) = LinearLayout(this).apply {
        orientation = LinearLayout.VERTICAL
        setPadding(dp(pad), dp(pad), dp(pad), dp(pad))
    }
    private fun txt(value: String, size: Float = 14f, color: Int = cream, bold: Boolean = false) =
        TextView(this).apply {
            text = value
            textSize = size
            setTextColor(color)
            gravity = Gravity.CENTER_VERTICAL
            if (bold) typeface = android.graphics.Typeface.DEFAULT_BOLD
        }
    private fun btn(value: String, click: () -> Unit) = Button(this).apply {
        text = value
        textSize = 13f
        isAllCaps = false
        setTextColor(bgColor)
        setBackgroundDrawable(rounded(gold))
        setOnClickListener { click() }
    }
    private fun margin(top: Int) = LinearLayout.LayoutParams(
        ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT
    ).apply { topMargin = dp(top) }

    private fun findCharacter(id: String): JSONObject? {
        for (index in 0 until catalogue.length()) {
            val item = catalogue.getJSONObject(index)
            if (item.optString("id") == id) return item
        }
        return null
    }

    private fun poseDefinition(character: JSONObject, poseId: String): JSONObject? {
        val poses = character.optJSONArray("poses") ?: return null
        for (index in 0 until poses.length()) {
            val pose = poses.getJSONObject(index)
            if (pose.optString("id") == poseId) return pose
        }
        return null
    }

    private fun canonicalPose(characterId: String, requested: String?): String {
        val character = findCharacter(characterId) ?: return "front"
        return if (poseDefinition(character, requested ?: "") != null) requested!! else "front"
    }

    private fun hasAsset(path: String): Boolean {
        if (path.isBlank()) return false
        return try {
            assets.open(path).close()
            true
        } catch (_: Exception) {
            false
        }
    }

    private fun render() {
        val heroine = findCharacter(selectedId) ?: return
        animatedPortrait = null
        touchFeedbackView = null
        val screen = column().apply { setBackgroundColor(bgColor) }
        val scroll = ScrollView(this).apply { isFillViewport = true }
        val content = column(16)
        scroll.addView(content)
        screen.addView(scroll)
        setContentView(screen)

        val header = LinearLayout(this).apply { gravity = Gravity.CENTER_VERTICAL }
        header.addView(btn("← Bản đồ") { finish() }, LinearLayout.LayoutParams(dp(105), dp(44)))
        val title = txt("THANH VÂN KÝ", 20f, gold, true).apply { gravity = Gravity.CENTER }
        header.addView(title, LinearLayout.LayoutParams(0, dp(48), 1f))
        content.addView(header)
        content.addView(txt("TƯƠNG TÁC NHÂN VẬT", 12f, muted), margin(10))

        val chooser = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL }
        for (index in 0 until catalogue.length()) {
            val item = catalogue.getJSONObject(index)
            val id = item.optString("id")
            val choose = btn(item.optString("name")) {
                selectedId = id
                currentPose = CharacterAppearanceState.read(this, id).pose
                currentPose = canonicalPose(id, currentPose)
                prefs.edit().putString("selected_character", id).apply()
                render()
            }
            choose.setBackgroundDrawable(rounded(if (id == selectedId) gold else panel))
            choose.setTextColor(if (id == selectedId) bgColor else cream)
            chooser.addView(choose, LinearLayout.LayoutParams(0, dp(48), 1f).apply {
                rightMargin = dp(8)
            })
        }
        content.addView(chooser, margin(12))

        val portraits = column(10).apply { setBackgroundDrawable(rounded(panel)) }
        portraits.addView(txt("NAM CHÍNH  &  " + heroine.optString("name").uppercase(), 15f, gold, true))
        val pose = poseDefinition(heroine, currentPose)
            ?: poseDefinition(heroine, "front") ?: return
        // One shared character state for wardrobe, damage and pose. Never fallback to
        // fully clothed, undamaged artwork when the requested combination is missing.
        val appearance = CharacterAppearanceState.read(this, selectedId).copy(pose = currentPose)
        val artwork = CharacterAppearanceState.resolveArt(heroine, appearance, ::hasAsset)
        val approvedExpressions = CharacterExpressionCatalog.approvedOptions(
            expressionProfiles, selectedId
        )
        val selectedApprovedExpression = approvedExpressions.firstOrNull {
            it.id == appearance.expression
        }
        val requiresExpressionArt = selectedApprovedExpression != null &&
            CharacterExpressionCatalog.faceVisible(currentPose)
        val expressionArt = if (requiresExpressionArt) CharacterExpressionCatalog.resolveSprite(
            expressionProfiles, selectedId, appearance, ::hasAsset
        ) else null
        // Never display the old neutral pose image as if it showed an approved
        // expression whose costume/integrity/pose-specific sprite is still missing.
        val heroineImage = if (requiresExpressionArt) expressionArt.orEmpty()
            else artwork.path.orEmpty()
        // A debug prototype may display legacy placeholder art for development.
        // A release build must NEVER show it as Lâm Thiển's approved CANON V2.1.
        val hasApprovedLamThienSprite = CharacterExpressionCatalog.hasRuntimeArtApproval(
            expressionProfiles, selectedId
        )
        val debugArtPreview = (applicationInfo.flags and
            android.content.pm.ApplicationInfo.FLAG_DEBUGGABLE) != 0
        // Production Lâm Thiển must use a *state-specific approved expression*
        // sprite only. A partially approved character is NOT permission to show
        // legacy neutral/pose art for combinations without a reviewed sprite.
        val safeHeroineImage =
            if (selectedId == "lin_qian" && !debugArtPreview) expressionArt.orEmpty()
            else heroineImage
        val heroineCrop = artwork.crop
        val outfitId = appearance.wardrobe
        var outfitLabel = outfitId
        val variants = heroine.optJSONArray("wardrobeStates")
        if (variants != null) for (i in 0 until variants.length()) {
            val outfit = variants.getJSONObject(i)
            if (outfit.optString("id") == outfitId) {
                outfitLabel = outfit.optString("label", outfitId)
                break
            }
        }
        val motionSettings = pose.optJSONObject("motionProfile")
        val cycleSeconds = motionSettings?.optDouble("cycleSeconds", 3.6) ?: 3.6
        if (currentPose.startsWith("bed_")) {
            // Landscape bed artwork uses the available width; the protagonist is an inset.
            // Avoid squeezing wide artwork into a narrow half-width portrait.
            val bedFrame = FrameLayout(this).apply {
                setBackgroundDrawable(rounded(Color.rgb(39, 56, 69)))
            }
            bedFrame.addView(portrait(heroine.optString("name"), safeHeroineImage,
                heroineCrop, interactive = true, motionCycleSeconds = cycleSeconds),
                FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(310)))
            bedFrame.addView(portrait("Nam chính", "characters/main_portrait.png", "full"),
                FrameLayout.LayoutParams(dp(92), dp(142),
                    Gravity.BOTTOM or Gravity.START).apply {
                    leftMargin = dp(5)
                    bottomMargin = dp(8)
                })
            portraits.addView(bedFrame)
        } else {
            val row = LinearLayout(this)
            row.addView(portrait("Nam chính", "characters/main_portrait.png", "full"),
                LinearLayout.LayoutParams(0, dp(345), 1f).apply { rightMargin = dp(8) })
            row.addView(portrait(heroine.optString("name"), safeHeroineImage,
                heroineCrop, interactive = true, motionCycleSeconds = cycleSeconds),
                LinearLayout.LayoutParams(0, dp(345), 1f))
            portraits.addView(row)
        }

        // Preview-only CP402. It does not unlock any production sprite path.
        if (selectedId == "lin_qian" && debugArtPreview) {
            portraits.addView(btn("CP402 | Xem thử chớp mắt (DRAFT)") {
                startActivity(android.content.Intent(this, TVKBlinkAtlasPreviewActivity::class.java))
            })
            portraits.addView(btn("CP409 | Chớp mắt theo mí (DRAFT)") {
                startActivity(android.content.Intent(this, TVKBlinkAtlasPreviewActivity::class.java).apply {
                    putExtra("cp409_review", true)
                })
            })
            // CP408: multiple idle channels together, with exact CANON file picker;
            // eye-blink art remains separately gated, no production art fallbacks.
            portraits.addView(btn("CP410 | Body + chớp mắt đồng bộ (DEBUG)") {
                startActivity(android.content.Intent(this, TVKCombinedIdlePreviewActivity::class.java))
            })
            // CP413 reuses the verified CANON picker; it never loads a fake head sprite.
            portraits.addView(btn("CP413 | Kiểm tra đường ghép đầu (DEBUG)") {
                startActivity(android.content.Intent(this, TVKCombinedIdlePreviewActivity::class.java))
            })
            portraits.addView(btn("CP418 | Soi mắt từng khung (DEBUG)") {
                startActivity(android.content.Intent(this, TVKCP417SamePoseBlinkActivity::class.java))
            })
        }

        if (selectedId == "lin_qian" && !hasApprovedLamThienSprite) {
            val notice = if (debugArtPreview)
                "ẢNH TEST / LEGACY — Lâm Thiển chưa có sprite CANON V2.1 được nghiệm thu. " +
                    "Chuyển động đang thấy chỉ là bitmap-mesh demo, không phải Spine/rig chính thức."
            else
                "Sprite Lâm Thiển CANON V2.1 chưa được nghiệm thu và chưa được hiển thị. " +
                    "Hãy sử dụng bản thử nghiệm để xem asset tạm."
            portraits.addView(txt(notice, 11f, Color.rgb(255, 214, 142), true))
        }

        val poseScroller = android.widget.HorizontalScrollView(this).apply {
            isHorizontalScrollBarEnabled = false
        }
        val poseRow = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL }
        val poses = heroine.optJSONArray("poses")
        if (poses != null) for (index in 0 until poses.length()) {
            val option = poses.getJSONObject(index)
            val poseId = option.optString("id")
            val poseButton = btn(option.optString("label")) {
                currentPose = poseId
                CharacterAppearanceState.setPose(this, selectedId, poseId)
                // Do not reset expression, wardrobe or garment integrity
                // when changing pose; expression has a character-scoped state.
                CharacterAppearanceState.setAction(this, selectedId, "pose_change")
                render()
            }
            poseButton.setBackgroundDrawable(rounded(if (poseId == currentPose) gold else bgColor))
            poseButton.setTextColor(if (poseId == currentPose) bgColor else cream)
            poseRow.addView(poseButton, LinearLayout.LayoutParams(dp(135), dp(44)).apply {
                rightMargin = dp(8)
            })
        }
        poseScroller.addView(poseRow)
        portraits.addView(poseScroller)
        portraits.addView(txt(pose.optString("description"), 12f, cream))
        portraits.addView(txt(
            "Trang phục: " + outfitLabel + " · Độ nguyên vẹn: " + appearance.integrity +
                "% · Tư thế: " + pose.optString("label", currentPose),
            12f, gold
        ))
        portraits.addView(txt(
            "Biểu cảm (state): " + (selectedApprovedExpression?.label ?: appearance.expression) +
                " · Hành động: " + appearance.action,
            11f, muted
        ))
        if (approvedExpressions.isNotEmpty()) {
            portraits.addView(txt("5 BIỂU CẢM ĐÃ DUYỆT · CHỌN TRẠNG THÁI", 12f, gold, true))
            val expressionScroll = android.widget.HorizontalScrollView(this).apply {
                isHorizontalScrollBarEnabled = false
            }
            val expressionRow = LinearLayout(this).apply {
                orientation = LinearLayout.HORIZONTAL
            }
            // The existing neutral state is a reset control, NOT a sixth newly
            // approved emotional artwork. It lets testers return from the five
            // locked expressions without modifying any other appearance state.
            val neutralButton = btn("Bình thường") {
                CharacterAppearanceState.setExpression(this, selectedId, "normal")
                render()
            }
            neutralButton.setBackgroundDrawable(rounded(
                if (appearance.expression == "normal") gold else bgColor
            ))
            neutralButton.setTextColor(if (appearance.expression == "normal") bgColor else cream)
            expressionRow.addView(neutralButton,
                LinearLayout.LayoutParams(dp(138), dp(44)).apply {
                    rightMargin = dp(8)
                })
            for (option in approvedExpressions) {
                val chooseExpression = btn(option.label) {
                    CharacterAppearanceState.setExpression(this, selectedId, option.id)
                    // This changes expression ONLY, not wardrobe/HP/pose/action.
                    render()
                }
                val chosen = option.id == appearance.expression
                chooseExpression.setBackgroundDrawable(rounded(if (chosen) gold else bgColor))
                chooseExpression.setTextColor(if (chosen) bgColor else cream)
                expressionRow.addView(chooseExpression,
                    LinearLayout.LayoutParams(dp(138), dp(44)).apply {
                        rightMargin = dp(8)
                    })
            }
            expressionScroll.addView(expressionRow)
            portraits.addView(expressionScroll)
            if (requiresExpressionArt && expressionArt == null) {
                portraits.addView(txt(
                    "Đã lưu biểu cảm «" + selectedApprovedExpression!!.label +
                        "», nhưng chưa có sprite đúng trang phục / độ nguyên vẹn / " +
                        "tư thế. Không hiển thị nhầm ảnh trung tính.",
                    11f, muted
                ))
            } else {
                portraits.addView(txt(
                    "Chọn một nét mặt để kiểm tra trạng thái; art phân lớp/Spine " +
                        "vẫn chờ triển khai theo CANON V2.1.",
                    11f, muted
                ))
            }
        }
        if (artwork.issue != null) {
            portraits.addView(txt(
                artwork.issue + ". Trạng thái đã lưu được giữ nguyên khi đổi tư thế, " +
                    "không mặc lại đồ mặc định. Cần asset đúng trạng thái để hiển thị/tương tác.",
                11f, muted
            ))
        }
        if (pose.optJSONObject("motionProfile")?.optBoolean("spineOrLive2DRequired") == true) {
            portraits.addView(txt(
                "Đã bật chuyển động ảnh tĩnh theo lưới (thở/tóc) và phản ứng chạm. " +
                    "Chuyển động rig Spine/Live2D phân lớp chưa hoàn thiện.",
                11f, muted
            ))
        }
        portraits.addView(txt(heroine.optString("subtitle"), 12f, muted))
        touchFeedbackView = txt("Chạm ảnh nhân vật để xem phản ứng.", 12f, gold)
            .apply { setPadding(dp(5), dp(5), dp(5), dp(5)) }
        portraits.addView(touchFeedbackView!!)
        content.addView(portraits, margin(14))

        affinityView = txt("Thân thiết (bản thử): " + prefs.getInt("affinity_" + selectedId, 0),
            14f, gold, true)
        content.addView(affinityView!!, margin(16))
        content.addView(txt("CHẠM TRỰC TIẾP VÀO NHÂN VẬT", 16f, gold, true), margin(12))
        content.addView(txt(
            if (currentPose == "front" || currentPose == "back")
                "Chạm trực tiếp lên ảnh. Mỗi góc nhìn dùng vùng tương tác riêng và chỉ nhận chạm khi có ảnh đúng tư thế."
            else
                "Tư thế giường dùng ảnh và vùng chạm riêng. Chạm trực tiếp trên ảnh để xem phản ứng.",
            11f, muted
        ), margin(6))
        val controls = heroine.getJSONArray("controls")
        val controlRow = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL }
        for (index in 0 until controls.length()) {
            val control = controls.getJSONObject(index)
            val action = btn(control.optString("title")) { selectScene(heroine, control) }
            controlRow.addView(action, LinearLayout.LayoutParams(0, dp(54), 1f).apply {
                if (index > 0) leftMargin = dp(8)
            })
        }
        content.addView(controlRow, margin(14))
        val dialogues = heroine.getJSONArray("scenes")
        if (dialogues.length() > 0) {
            content.addView(btn("TRÒ CHUYỆN") {
                selectScene(heroine, dialogues.getJSONObject(0))
            }, LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(45)).apply {
                topMargin = dp(10)
            })
        }

        messageView = txt("Chọn một tương tác với " + heroine.optString("name") + ".", 13f)
            .apply {
                setPadding(dp(12), dp(12), dp(12), dp(12))
                setBackgroundDrawable(rounded(panel))
            }
        content.addView(messageView!!, margin(18))
        content.addView(txt(
            "Model Spine Lâm Thiển chưa được nhập vào APK. Không có video hoặc rig giả.",
            11f, muted
        ), margin(12))
    }

    private fun portrait(name: String, assetPath: String, crop: String,
                         interactive: Boolean = false, motionCycleSeconds: Double = 3.6): View {
        val frame = FrameLayout(this).apply { setBackgroundDrawable(rounded(Color.rgb(56, 80, 93))) }
        val bitmap = bitmap(assetPath, crop)
        if (bitmap != null) {
            val pictureView: View =
                if (interactive) TVKCharacterMotionView(
                    this, bitmap, motionCycleSeconds,
                    movement = 1f
                ).also { animatedPortrait = it } else ImageView(this).apply {
                    setImageBitmap(bitmap)
                    scaleType = ImageView.ScaleType.FIT_CENTER
                }
            frame.addView(pictureView, FrameLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT).apply {
                    bottomMargin = dp(34)
                })
        } else {
            frame.addView(txt("Ảnh " + name + "\nchưa có trong APK", 12f, muted).apply {
                gravity = Gravity.CENTER
                setPadding(dp(10), 0, dp(10), 0)
            }, FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.MATCH_PARENT))
        }
        frame.addView(txt(name, 13f, cream, true).apply {
            gravity = Gravity.CENTER
            setBackgroundColor(Color.argb(215, 23, 37, 48))
        }, FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(34), Gravity.BOTTOM))
        if (interactive) {
            frame.contentDescription = "Chạm để tương tác với " + name
            if (bitmap != null) {
                frame.setOnClickListener { /* Touch listener provides the actual hit test. */ }
                var downX = 0f
                var downY = 0f
                frame.setOnTouchListener { view, event ->
                    when (event.actionMasked) {
                        MotionEvent.ACTION_DOWN -> {
                            downX = event.x
                            downY = event.y
                            true
                        }
                        MotionEvent.ACTION_UP -> {
                            if (abs(event.x - downX) <= dp(20) &&
                                abs(event.y - downY) <= dp(20)) {
                                view.performClick()
                                touchPortrait(
                                    event.x, event.y, view.width.toFloat(), view.height.toFloat(),
                                    bitmap.width.toFloat(), bitmap.height.toFloat()
                                )
                            }
                            true
                        }
                        else -> true
                    }
                }
            } else {
                frame.setOnClickListener {
                    messageView?.text = "Chưa có ảnh " + name + " ở tư thế này; không thể xác định vùng chạm."
                }
            }
        }
        return frame
    }

    private fun touchPortrait(
        x: Float, y: Float, width: Float, height: Float, imageWidth: Float, imageHeight: Float
    ) {
        if (width <= 0f || height <= dp(34) || imageWidth <= 0f || imageHeight <= 0f) return
        if (y < 0f || y >= height - dp(34)) return

        // The ImageView uses FIT_CENTER; map the touch into actual image pixels,
        // excluding margins from letterboxing. Avoid matching blank space as body.
        val contentHeight = height - dp(34)
        val scale = kotlin.math.min(width / imageWidth, contentHeight / imageHeight)
        val drawnWidth = imageWidth * scale
        val drawnHeight = imageHeight * scale
        val left = (width - drawnWidth) / 2f
        val top = (contentHeight - drawnHeight) / 2f
        if (x < left || x >= left + drawnWidth || y < top || y >= top + drawnHeight) {
            messageView?.text = "Bạn chạm ngoài hình nhân vật."
            return
        }
        val nx = ((x - left) / drawnWidth).coerceIn(0f, 1f).toDouble()
        val ny = ((y - top) / drawnHeight).coerceIn(0f, 1f).toDouble()
        val heroine = findCharacter(selectedId) ?: return
        val zones = heroine.optJSONArray("touchZones") ?: return
        val pose = currentPose
        for (index in 0 until zones.length()) {
            val zone = zones.getJSONObject(index)
            if (zone.optString("pose", "front") != pose) continue
            val regions = zone.optJSONArray("regions") ?: continue
            for (regionIndex in 0 until regions.length()) {
                val box = regions.getJSONObject(regionIndex)
                if (nx >= box.optDouble("x1") && nx <= box.optDouble("x2") &&
                    ny >= box.optDouble("y1") && ny <= box.optDouble("y2")) {
                    respondToTouch(zone)
                    return
                }
            }
        }
        messageView?.text = "Bạn chạm vào khoảng trống. Hãy chọn một vùng trên nhân vật."
        touchFeedbackView?.text = "Vị trí chạm chưa có phản ứng riêng."
    }

    private fun respondToTouch(zone: JSONObject) {
        animatedPortrait?.react(zone.optString("id"))
        val sensitive = zone.optBoolean("requiresConsent", false)
        val expression = zone.optString(
            "expression", if (sensitive) "troubled" else "smile"
        )
        CharacterAppearanceState.setExpression(this, selectedId, expression)
        CharacterAppearanceState.setAction(this, selectedId, "touch_reaction")
        val zoneName = zone.optString("title", "Tương tác")
        val reactionText = zoneName + ": " + zone.optString("message")
        messageView?.text = reactionText
        touchFeedbackView?.text = reactionText
        if (sensitive) return // Respect character boundaries; do not reward uninvited touch.
        val key = "affinity_" + selectedId
        val points = prefs.getInt(key, 0) + zone.optInt("affinityGain", 0)
        prefs.edit().putInt(key, points).apply()
        affinityView?.text = "Thân thiết (bản thử): " + points
    }

    // Preserve source details for normal character portraits. The old hardcoded
    // inSampleSize=2 needlessly cut even small artwork to half in each dimension.
    // Large future PNGs are still bounded to avoid allocation spikes on Android.
    private fun portraitSampleSize(width: Int, height: Int): Int {
        if (width <= 0 || height <= 0) return 1
        val maxSide = 4096L
        val maxPixels = 8_000_000L // up to ~32 MiB at ARGB_8888
        var sample = 1
        while (width.toLong() / sample > maxSide ||
               height.toLong() / sample > maxSide ||
               (width.toLong() / sample) * (height.toLong() / sample) > maxPixels) {
            sample *= 2
        }
        return sample
    }

    private fun bitmap(assetPath: String, crop: String): Bitmap? {
        if (assetPath.isBlank()) return null
        return try {
            if (crop == "leftThird") {
                assets.open(assetPath).use { source ->
                    val decoder = BitmapRegionDecoder.newInstance(source, false)
                    if (decoder == null) null else try {
                        val right = (decoder.width / 3).coerceAtLeast(1)
                        decoder.decodeRegion(
                            Rect(0, 0, right, decoder.height),
                            BitmapFactory.Options().apply {
                                inSampleSize = portraitSampleSize(right, decoder.height)
                                inPreferredConfig = Bitmap.Config.ARGB_8888
                                inScaled = false
                            }
                        )
                    } finally {
                        decoder.recycle()
                    }
                }
            } else {
                // Decode only header in the first pass; reopen the asset for pixels.
                val bounds = BitmapFactory.Options().apply { inJustDecodeBounds = true }
                assets.open(assetPath).use { source ->
                    BitmapFactory.decodeStream(source, null, bounds)
                }
                if (bounds.outWidth <= 0 || bounds.outHeight <= 0) null
                else assets.open(assetPath).use { source ->
                    BitmapFactory.decodeStream(source, null,
                        BitmapFactory.Options().apply {
                            inSampleSize = portraitSampleSize(bounds.outWidth, bounds.outHeight)
                            inPreferredConfig = Bitmap.Config.ARGB_8888
                            inScaled = false
                        })
                }
            }
        } catch (_: Exception) {
            null
        }
    }

    private fun selectScene(character: JSONObject, scene: JSONObject) {
        val characterId = character.optString("id")
        val sceneKind = scene.optString("kind", "dialogue")
        val expression = when (sceneKind) {
            "romance" -> "blush"
            "fade" -> "relaxed"
            "dialogue" -> "smile"
            else -> "normal"
        }
        // Opening the wardrobe must not reset a manually selected expression.
        if (sceneKind != "wardrobe")
            CharacterAppearanceState.setExpression(this, characterId, expression)
        CharacterAppearanceState.setAction(this, characterId, "scene_" + sceneKind)
        val points = prefs.getInt("affinity_" + characterId, 0) + scene.optInt("affinityGain", 0)
        prefs.edit().putInt("affinity_" + characterId, points).apply()
        affinityView?.text = "Thân thiết (bản thử): " + points
        val narrative = scene.optString("message", scene.optString("status"))
        val text = scene.optString("title") + ": " + narrative
        messageView?.text = text
        if (scene.optString("kind") == "wardrobe") {
            openWardrobe(character)
            return
        }

        if (scene.optString("kind") == "fade") {
            val dialog = Dialog(this)
            val body = column(25).apply {
                setBackgroundColor(Color.rgb(14, 20, 32))
                addView(txt(narrative, 17f).apply {
                    gravity = Gravity.CENTER
                    minHeight = dp(160)
                })
                addView(btn("Trở lại nhân vật") { dialog.dismiss() })
            }
            dialog.setContentView(body)
            dialog.show()
            dialog.window?.setLayout(ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT)
            return
        }
        val file = scene.optString("optionalVideo")
        if (file.isNotEmpty() && !tryVideo(characterId, scene.optString("title"), file))
            messageView?.text = text + "\n(Video chưa có; hiện dùng lời thoại minh họa.)"
    }

    private fun openWardrobe(character: JSONObject) {
        val characterId = character.optString("id")
        val outfits = character.optJSONArray("wardrobeStates")
        if (outfits == null || outfits.length() == 0) {
            messageView?.text = "Nhân vật hiện có trang phục mặc định. Chưa có asset cởi lớp áo riêng."
            return
        }
        val options = ArrayList<String>()
        val wardrobeIds = ArrayList<String>()
        val pose = currentPose
        val integrity = CharacterAppearanceState.read(this, characterId).integrity
        for (i in 0 until outfits.length()) {
            val state = outfits.getJSONObject(i)
            val id = state.optString("id")
            // Show all wardrobe levels so state can be selected/preserved even while
            // artwork is still being produced. Missing art gets a clear placeholder.
            val preview = CharacterAppearanceState.resolveArt(
                character,
                CharacterAppearanceState.State(wardrobe = id, integrity = integrity, pose = pose),
                ::hasAsset
            )
            val label = state.optString("label") + if (preview.path == null) " · thiếu ảnh" else ""
            options.add(label)
            wardrobeIds.add(id)
        }
        android.app.AlertDialog.Builder(this)
            .setTitle("Trang phục · " + character.optString("name"))
            .setItems(options.toTypedArray()) { _, which ->
                val chosen = wardrobeIds.getOrNull(which).orEmpty()
                if (chosen.isBlank()) return@setItems
                // Persist user's selection even without art, but never fabricate a
                // preview or replace it with another outfit when switching poses.
                CharacterAppearanceState.setWardrobe(this, characterId, chosen)
                render()
            }
            .setNegativeButton("Đóng", null)
            .show()
    }

    private fun tryVideo(characterId: String, title: String, relative: String): Boolean {
        if (!relative.startsWith("scenes/" + characterId + "/") ||
            !relative.endsWith(".mp4") || relative.contains("..")) return false
        val cache = File(cacheDir, relative.replace('/', '_'))
        try {
            assets.open(relative).use { input -> cache.outputStream().use { input.copyTo(it) } }
        } catch (_: Exception) {
            return false
        }

        val dialog = Dialog(this)
        val layout = column(12).apply { setBackgroundColor(bgColor) }
        layout.addView(txt(title, 18f, gold, true))
        val video = VideoView(this)
        layout.addView(video, LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(370)))
        layout.addView(btn("Dừng và trở lại") { dialog.dismiss() })
        dialog.setContentView(layout)
        dialog.setOnDismissListener {
            video.stopPlayback()
            if (videoDialog === dialog) videoDialog = null
        }
        videoDialog?.dismiss()
        videoDialog = dialog
        dialog.show()
        dialog.window?.setLayout(ViewGroup.LayoutParams.MATCH_PARENT,
            ViewGroup.LayoutParams.WRAP_CONTENT)
        val controls = MediaController(this)
        controls.setAnchorView(video)
        video.setMediaController(controls)
        video.setVideoURI(Uri.fromFile(cache))
        video.setOnPreparedListener { it.isLooping = true }
        video.setOnErrorListener { _, _, _ ->
            messageView?.text = "Không phát được video: " + title + ". Kiểm tra codec MP4."
            dialog.dismiss()
            true
        }
        video.start()
        return true
    }
}
