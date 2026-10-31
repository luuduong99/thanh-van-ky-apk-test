package vn.thanhvanky.prototype

import android.os.SystemClock

/** One monotonic timeline for CP410's debug-only body and eye *comparison* views.
 * The eye artwork is a different source pose: never composited onto the body.
 */
class TVKPreviewClock {
    private var epochMs = SystemClock.uptimeMillis()
    private var frozenMs = 0L
    var playing: Boolean = true
        private set

    fun elapsedSeconds(): Double = (
        if (playing) SystemClock.uptimeMillis() - epochMs else frozenMs
    ).coerceAtLeast(0L) / 1000.0

    fun setPlaying(active: Boolean) {
        if (active == playing) return
        if (active) epochMs = SystemClock.uptimeMillis() - frozenMs
        else frozenMs = (SystemClock.uptimeMillis() - epochMs).coerceAtLeast(0L)
        playing = active
    }

    fun reset() {
        epochMs = SystemClock.uptimeMillis()
        frozenMs = 0L
    }
}

/** Mirrors CP409's timeline curve, but sampled from exactly the same clock as body idle. */
object TVKDebugBlinkTiming {
    fun poseAt(seconds: Double): Int {
        val phase = ((seconds % 2.4) + 2.4) % 2.4 / 2.4
        fun ease(value: Double): Double {
            val x = value.coerceIn(0.0, 1.0)
            return x * x * (3.0 - 2.0 * x)
        }
        return when {
            phase < .30 -> 0
            phase < .355 -> kotlin.math.round(7.0 * ease((phase - .30) / .055)).toInt().coerceIn(0,7)
            phase < .395 -> 7
            phase < .455 -> kotlin.math.round(7.0 + 7.0 * ease((phase - .395) / .060)).toInt().coerceIn(7,14)
            else -> 0
        }
    }
}