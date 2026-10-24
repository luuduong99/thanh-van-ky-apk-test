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
    private var selectedId = "to_nguyet_ly"
    private var currentPose = "front"
    private var messageView: TextView? = null
    private var affinityView: TextView? = null
    private var videoDialog: Dialog? = null
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
            ?: prefs.getString("pose_" + selectedId, "front") ?: "front"
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
                currentPose = prefs.getString("pose_" + id, "front") ?: "front"
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
        val row = LinearLayout(this)
        row.addView(portrait("Nam chính", "characters/main_portrait.png", "full"),
            LinearLayout.LayoutParams(0, dp(345), 1f).apply { rightMargin = dp(8) })
        val pose = poseDefinition(heroine, currentPose)
            ?: poseDefinition(heroine, "front") ?: return
        val heroineImage = pose.optString("image")
        val heroineCrop = pose.optString("crop", "full")
        row.addView(portrait(heroine.optString("name"), heroineImage,
            heroineCrop, interactive = true), LinearLayout.LayoutParams(0, dp(345), 1f))
        portraits.addView(row)

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
                prefs.edit().putString("pose_" + selectedId, poseId).apply()
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
        if (!hasAsset(heroineImage)) {
            portraits.addView(txt(
                "Chưa có ảnh riêng cho tư thế này của " + heroine.optString("name") +
                    ". Các vùng chạm chưa hoạt động ở tư thế này.",
                11f, muted
            ))
        }
        if (pose.optJSONObject("motionProfile")?.optBoolean("spineOrLive2DRequired") == true) {
            portraits.addView(txt(
                "Đã ghi cấu hình chuyển động thở và dao động phụ theo nhịp; " +
                    "cần model phân lớp để hiển thị chuyển động thật.",
                11f, muted
            ))
        }
        portraits.addView(txt(heroine.optString("subtitle"), 12f, muted))
        content.addView(portraits, margin(14))

        affinityView = txt("Thân thiết (bản thử): " + prefs.getInt("affinity_" + selectedId, 0),
            14f, gold, true)
        content.addView(affinityView!!, margin(16))
        content.addView(txt("CHẠM TRỰC TIẾP VÀO NHÂN VẬT", 16f, gold, true), margin(12))
        content.addView(txt(
            if (currentPose == "front" || currentPose == "back")
                "Chạm trực tiếp lên ảnh. Mỗi góc nhìn dùng vùng tương tác riêng và chỉ nhận chạm khi có ảnh đúng tư thế."
            else
                "Tư thế giường đã được đăng ký. Cần ảnh và vùng chạm riêng trước khi tương tác; không áp tọa độ tư thế đứng.",
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
                         interactive: Boolean = false): View {
        val frame = FrameLayout(this).apply { setBackgroundDrawable(rounded(Color.rgb(56, 80, 93))) }
        val bitmap = bitmap(assetPath, crop)
        if (bitmap != null) {
            frame.addView(ImageView(this).apply {
                setImageBitmap(bitmap)
                scaleType = ImageView.ScaleType.FIT_CENTER
            }, FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.MATCH_PARENT))
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
        val scale = kotlin.math.min(width / imageWidth, height / imageHeight)
        val drawnWidth = imageWidth * scale
        val drawnHeight = imageHeight * scale
        val left = (width - drawnWidth) / 2f
        val top = (height - drawnHeight) / 2f
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
    }

    private fun respondToTouch(zone: JSONObject) {
        val sensitive = zone.optBoolean("requiresConsent", false)
        val zoneName = zone.optString("title", "Tương tác")
        messageView?.text = zoneName + ": " + zone.optString("message")
        if (sensitive) return // Respect character boundaries; do not reward uninvited touch.
        val key = "affinity_" + selectedId
        val points = prefs.getInt(key, 0) + zone.optInt("affinityGain", 0)
        prefs.edit().putInt(key, points).apply()
        affinityView?.text = "Thân thiết (bản thử): " + points
    }

    private fun bitmap(assetPath: String, crop: String): Bitmap? {
        return try {
            assets.open(assetPath).use { source ->
                if (crop == "leftThird") {
                    val decoder = BitmapRegionDecoder.newInstance(source, false)
                    if (decoder == null) null else try {
                        decoder.decodeRegion(
                            Rect(0, 0, decoder.width / 3, decoder.height),
                            BitmapFactory.Options().apply { inSampleSize = 2 }
                        )
                    } finally {
                        decoder.recycle()
                    }
                } else {
                    BitmapFactory.decodeStream(source, null,
                        BitmapFactory.Options().apply { inSampleSize = 2 })
                }
            }
        } catch (_: Exception) {
            null
        }
    }

    private fun selectScene(character: JSONObject, scene: JSONObject) {
        val characterId = character.optString("id")
        val points = prefs.getInt("affinity_" + characterId, 0) + scene.optInt("affinityGain", 0)
        prefs.edit().putInt("affinity_" + characterId, points).apply()
        affinityView?.text = "Thân thiết (bản thử): " + points
        val narrative = scene.optString("message", scene.optString("status"))
        val text = scene.optString("title") + ": " + narrative
        messageView?.text = text
        if (scene.optString("kind") == "wardrobe") return

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
