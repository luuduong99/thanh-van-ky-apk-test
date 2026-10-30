package vn.thanhvanky.prototype

import android.app.Activity
import android.content.Intent
import android.content.pm.ApplicationInfo
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Color
import android.net.Uri
import android.os.Bundle
import android.view.Gravity
import android.view.ViewGroup
import android.widget.Button
import android.widget.FrameLayout
import android.widget.LinearLayout
import android.widget.TextView
import java.security.MessageDigest

/** Debug-only CP408: source-locked, combined idle preview. NOT a real art/rig release. */
class TVKCombinedIdlePreviewActivity:Activity(){
    companion object {
        private const val PICK_CANON=408
        private const val EXPECTED_HASH="f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a"
        private val FRONT=intArrayOf(16,180,224,623)
        private const val MAX_BYTES=5_000_000 // reject huge/hostile image uploads
    }
    private var preview:TVKCombinedIdleMotionView?=null
    private lateinit var frame:FrameLayout
    private lateinit var status:TextView
    private lateinit var play:Button
    private val names=arrayOf("Thở", "Đầu", "Tay", "Tóc", "Lụa")
    private var running=true
    private fun density(n:Int)=(n*resources.displayMetrics.density+.5f).toInt()
    private fun text(s:String,size:Float=13f)=TextView(this).apply {
        text=s
        textSize=size
        setTextColor(Color.rgb(234,240,255))
    }
    private fun button(s:String,f:()->Unit)=Button(this).apply {text=s;isAllCaps=false;setOnClickListener{f()}}

    override fun onCreate(savedInstanceState:Bundle?){
        super.onCreate(savedInstanceState)
        // No back door to production images: even explicit launching is refused in release builds.
        if((applicationInfo.flags and ApplicationInfo.FLAG_DEBUGGABLE)==0){finish();return}
        val root=LinearLayout(this).apply {
            orientation=LinearLayout.VERTICAL
            setPadding(density(9),density(9),density(9),density(9))
            setBackgroundColor(Color.rgb(26,37,50))
        }
        root.addView(text("CP408 — Lâm Thiển | IDLE nhiều lớp (DEBUG)",19f))
        root.addView(text("Nguồn CANON V2.1 giữ nguyên. Chưa có rig xương, chớp mắt được duyệt hay tích hợp chính thức."))
        val select=button("Chọn đúng ảnh CANON V2.1 (PNG)"){
            val intent=Intent(Intent.ACTION_OPEN_DOCUMENT).apply {
                addCategory(Intent.CATEGORY_OPENABLE)
                type="image/png"
            }
            startActivityForResult(intent,PICK_CANON)
        }
        root.addView(select)
        status=text("Chưa chọn nguồn CANON. Chỉ chấp nhận SHA-256 chính xác.")
        root.addView(status)
        frame=FrameLayout(this).apply {setBackgroundColor(Color.rgb(236,242,250))}
        root.addView(frame,LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,0,1f))
        val controls=LinearLayout(this).apply {orientation=LinearLayout.HORIZONTAL;gravity=Gravity.CENTER}
        play=button("Tạm dừng") {
            running=!running
            preview?.setPlaying(running)
            play.text=if(running)"Tạm dừng" else "Tiếp tục"
        }
        controls.addView(play,LinearLayout.LayoutParams(0,density(49),1f))
        for(i in 0..4){
            val b=button(names[i]){}
            b.setOnClickListener{
                val active=preview?.flipChannel(i) ?: false
                b.text=names[i]+if(active)" ✓" else " ×"
            }
            b.text=names[i]+" ✓"
            controls.addView(b,LinearLayout.LayoutParams(0,density(49),1f))
        }
        root.addView(controls)
        root.addView(text("Chuyển động đa kênh chạy đồng thời. Không vẽ giả mí/lông mi; kênh chớp mắt chờ master được duyệt."))
        setContentView(root)
    }

    @Deprecated("Compatible with Android API 23 in this debug-only prototype")
    override fun onActivityResult(requestCode:Int,resultCode:Int,data:Intent?){
        super.onActivityResult(requestCode,resultCode,data)
        if(requestCode!=PICK_CANON || resultCode!=RESULT_OK)return
        val uri:Uri=data?.data ?:return
        try{
            // File picker data is untrusted: verify raw file bytes BEFORE bitmap decode.
            val all=contentResolver.openInputStream(uri)?.use { input->
                val out=java.io.ByteArrayOutputStream()
                val buffer=ByteArray(8192)
                while(true){
                    val n=input.read(buffer)
                    if(n<0)break
                    if(out.size()+n>MAX_BYTES)throw IllegalArgumentException("PNG quá lớn")
                    out.write(buffer,0,n)
                }
                out.toByteArray()
            } ?: throw IllegalArgumentException("Không đọc được file")
            val hash=MessageDigest.getInstance("SHA-256").digest(all)
                .joinToString(""){"%02x".format(it.toInt() and 0xff)}
            if(hash!=EXPECTED_HASH)throw IllegalArgumentException("File không đúng CANON V2.1 — SHA khác")
            val options=BitmapFactory.Options().apply {inJustDecodeBounds=true}
            BitmapFactory.decodeByteArray(all,0,all.size,options)
            if(options.outWidth!=941||options.outHeight!=1672)throw IllegalArgumentException("Kích thước không khớp CANON")
            val source=BitmapFactory.decodeByteArray(all,0,all.size) ?: throw IllegalArgumentException("PNG không hợp lệ")
            val crop=Bitmap.createBitmap(source,FRONT[0],FRONT[1],FRONT[2]-FRONT[0],FRONT[3]-FRONT[1])
            frame.removeAllViews()
            preview=TVKCombinedIdleMotionView(this,crop).also {
                it.setPlaying(running)
                frame.addView(it,FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,ViewGroup.LayoutParams.MATCH_PARENT))
            }
            status.text="CANON SHA ✓ — 5 chuyển động kỹ thuật đang ghép. Mắt: CHƯA DUYỆT."
        }catch(e:Exception){
            frame.removeAllViews();preview=null
            status.text="Từ chối ảnh: ${e.message}"
        }
    }
    override fun onStop(){super.onStop();preview?.setPlaying(false)}
    override fun onResume(){super.onResume();preview?.setPlaying(running)}
}