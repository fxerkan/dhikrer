package com.fxerkan.zikirci

import android.app.PendingIntent
import android.app.Service
import android.content.Context
import android.content.Intent
import android.content.pm.ServiceInfo
import android.media.VolumeProvider
import android.media.session.MediaSession
import android.media.session.PlaybackState
import android.os.Build
import android.os.IBinder
import android.os.VibrationEffect
import android.os.Vibrator
import androidx.core.app.NotificationCompat

/**
 * Keeps a MediaSession active so hardware volume keys are routed to us as a
 * *remote* volume adjustment even while the screen is off — each press counts.
 * The session's remote VolumeProvider swallows the adjustment (stream volume is
 * untouched) and increments the active dhikr instead.
 *
 * ponytail: the standard tasbih-app trick. Ceiling: some OEM battery managers
 * kill background FGS; user may need to exempt the app. Upgrade path: none
 * needed for a personal build.
 */
class VolumeKeyService : Service() {

    private var session: MediaSession? = null

    companion object {
        private const val NOTIF_ID = 42
        fun start(c: Context) {
            val i = Intent(c, VolumeKeyService::class.java)
            if (Build.VERSION.SDK_INT >= 26) c.startForegroundService(i) else c.startService(i)
        }
        fun stop(c: Context) { c.stopService(Intent(c, VolumeKeyService::class.java)) }
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onCreate() {
        super.onCreate()
        Notifications.ensureChannel(this)

        val vp = object : VolumeProvider(VOLUME_CONTROL_RELATIVE, 100, 50) {
            override fun onAdjustVolume(direction: Int) {
                if (direction == 0) return
                if (!CounterRepo.volumeKeysEnabled(this@VolumeKeyService)) return
                count()
                currentVolume = 50 // keep centered so more presses are always possible
            }
        }

        session = MediaSession(this, "ZikirVolume").apply {
            setPlaybackState(
                PlaybackState.Builder()
                    .setActions(PlaybackState.ACTION_PLAY_PAUSE)
                    .setState(PlaybackState.STATE_PLAYING, 0, 1f)
                    .build()
            )
            setPlaybackToRemote(vp)
            isActive = true
        }

        val open = PendingIntent.getActivity(
            this, 0, Intent(this, MainActivity::class.java),
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
        val notif = NotificationCompat.Builder(this, Notifications.CHANNEL_SERVICE)
            .setSmallIcon(R.drawable.ic_bead)
            .setContentTitle(getString(R.string.svc_title))
            .setContentText(getString(R.string.svc_text))
            .setOngoing(true)
            .setContentIntent(open)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .build()

        if (Build.VERSION.SDK_INT >= 34) {
            startForeground(NOTIF_ID, notif, ServiceInfo.FOREGROUND_SERVICE_TYPE_SPECIAL_USE)
        } else {
            startForeground(NOTIF_ID, notif)
        }
    }

    private fun count() {
        if (MainActivity.isAlive()) MainActivity.applyTaps(1)
        else CounterRepo.incrementNative(this, 1)
        ZikirWidget.refresh(this)
        if (CounterRepo.hapticEnabled(this)) {
            val v = getSystemService(Vibrator::class.java)
            if (Build.VERSION.SDK_INT >= 26) v.vibrate(VibrationEffect.createOneShot(20, VibrationEffect.DEFAULT_AMPLITUDE))
            else @Suppress("DEPRECATION") v.vibrate(20)
        }
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int = START_STICKY

    override fun onDestroy() {
        session?.isActive = false
        session?.release()
        session = null
        super.onDestroy()
    }
}
