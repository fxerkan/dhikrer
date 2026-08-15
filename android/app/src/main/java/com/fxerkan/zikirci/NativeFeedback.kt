package com.fxerkan.zikirci

import android.content.Context
import android.media.AudioManager
import android.media.ToneGenerator
import android.os.Build
import android.os.Handler
import android.os.Looper
import android.os.VibrationEffect
import android.os.Vibrator

/**
 * Haptic + audio feedback for taps that happen while the app is NOT in the
 * foreground (widget, screen-off volume keys). Mirrors what the running web app
 * does on a tap, and makes the "target completed" tick deliberately louder and
 * longer than a normal tick so it grabs the user's attention.
 */
object NativeFeedback {

    fun tap(c: Context, tick: CounterRepo.Tick) {
        val haptic = CounterRepo.hapticEnabled(c)
        when (tick) {
            CounterRepo.Tick.COUNTED ->
                if (haptic) buzz(c, longArrayOf(0, 20))            // brief single pulse
            CounterRepo.Tick.COMPLETED -> {
                if (haptic) buzz(c, longArrayOf(0, 160, 80, 160, 80, 240)) // triple, escalating
                completionTone()                                   // distinct double beep
            }
            CounterRepo.Tick.AT_TARGET -> {}                       // already done → stay silent
        }
    }

    private fun buzz(c: Context, timings: LongArray) {
        val v = c.getSystemService(Vibrator::class.java) ?: return
        if (!v.hasVibrator()) return
        if (Build.VERSION.SDK_INT >= 26) v.vibrate(VibrationEffect.createWaveform(timings, -1))
        else @Suppress("DEPRECATION") v.vibrate(timings, -1)
    }

    /** Notification-stream tone → respects silent/DND, no bundled audio asset needed. */
    private fun completionTone() {
        try {
            val tg = ToneGenerator(AudioManager.STREAM_NOTIFICATION, 100)
            tg.startTone(ToneGenerator.TONE_PROP_BEEP2, 500)  // two-tone chirp, unmistakable
            Handler(Looper.getMainLooper()).postDelayed({ tg.release() }, 700)
        } catch (e: Exception) { /* ToneGenerator busy/unavailable — skip */ }
    }
}
