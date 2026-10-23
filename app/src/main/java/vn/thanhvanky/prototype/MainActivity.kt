package vn.thanhvanky.prototype

import android.app.Activity
import android.graphics.Color
import android.graphics.Typeface
import android.os.Bundle
import android.view.Gravity
import android.view.ViewGroup
import android.widget.Button
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView

class MainActivity : Activity() {
    private lateinit var root: LinearLayout
    private lateinit var story: TextView
    private lateinit var status: TextView
    private var spirit = 0
    private var courage = 0
    private var chapter = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        showGame()
    }

    private fun showGame() {
        val scroll = ScrollView(this)
        root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER_HORIZONTAL
            setPadding(24, 28, 24, 28)
            setBackgroundColor(Color.rgb(16, 24, 42))
        }
        scroll.addView(root)
        setContentView(scroll)

        addText("THANH VÂN KÝ", 30, Color.rgb(235, 207, 143), true, 18)
        addText("BẢN THỬ NGHIỆM ANDROID", 13, Color.LTGRAY, false, 28)
        status = addText("", 16, Color.rgb(155, 218, 205), true, 24)
        story = addText("", 19, Color.WHITE, false, 26)
        renderChapter()
    }

    private fun addText(text: String, size: Int, color: Int, bold: Boolean, bottom: Int): TextView {
        val view = TextView(this).apply {
            this.text = text
            textSize = size.toFloat()
            setTextColor(color)
            gravity = Gravity.CENTER
            if (bold) setTypeface(null, Typeface.BOLD)
            setPadding(8, 8, 8, 8)
        }
        root.addView(view, LinearLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT
        ).apply { bottomMargin = bottom })
        return view
    }

    private fun addChoice(label: String, onClick: () -> Unit) {
        val button = Button(this).apply {
            text = label
            textSize = 16f
            isAllCaps = false
            setOnClickListener { onClick() }
        }
        root.addView(button, LinearLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT
        ).apply { bottomMargin = 12 })
    }

    private fun renderChapter() {
        root.removeViews(root.indexOfChild(story) + 1, root.childCount - root.indexOfChild(story) - 1)
        status.text = "Linh lực: $spirit     Dũng khí: $courage"
        when (chapter) {
            0 -> {
                story.text = "Bạn tỉnh dậy dưới chân núi Thanh Vân. Sương mù phủ kín con đường cổ, còn phía xa có ánh đèn le lói từ một ngôi miếu."
                addChoice("Đi vào ngôi miếu") { spirit += 1; chapter = 1; renderChapter() }
                addChoice("Men theo con đường lên núi") { courage += 1; chapter = 2; renderChapter() }
            }
            1 -> {
                story.text = "Trong miếu, một đạo sĩ già đặt trước mặt bạn viên linh thạch phát sáng. “Người hữu duyên, hãy giữ lấy nó.”"
                addChoice("Nhận linh thạch") { spirit += 2; chapter = 3; renderChapter() }
                addChoice("Từ chối và hỏi đường") { courage += 1; chapter = 3; renderChapter() }
            }
            2 -> {
                story.text = "Tiếng động vang lên giữa rừng trúc. Một con linh thú nhỏ bị mắc bẫy, đôi mắt nhìn bạn cầu cứu."
                addChoice("Cứu linh thú") { spirit += 1; courage += 1; chapter = 3; renderChapter() }
                addChoice("Cẩn thận rời đi") { courage += 1; chapter = 3; renderChapter() }
            }
            else -> {
                story.text = "Bình minh lên trên đỉnh Thanh Vân. Hành trình tu tiên của bạn chính thức bắt đầu!\n\nĐây mới là chương mở đầu của bản thử nghiệm."
                addChoice("Chơi lại từ đầu") { spirit = 0; courage = 0; chapter = 0; renderChapter() }
            }
        }
    }
}
