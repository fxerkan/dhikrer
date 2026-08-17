package com.fxerkan.zikirci

import android.app.PendingIntent
import android.app.Service
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.pm.ServiceInfo
import android.media.MediaMetadata
import android.media.VolumeProvider
import android.media.session.MediaSession
import android.media.session.PlaybackState
import android.os.Build
import android.os.IBinder
import androidx.core.app.NotificationCompat

/**
 * Runs ONLY while the screen is off (started by MainActivity on ACTION_SCREEN_OFF
 * when the app was in the foreground) so volume keys keep counting after the phone
 * is locked. Keeps a MediaSession active so the hardware volume keys are routed to
 * us as a *remote* volume adjustment; the remote VolumeProvider swallows the
 * adjustment (stream volume untouched) and increments the active dhikr instead.
 * Self-stops the instant the screen comes back on, so there is no lingering media
 * control or notification during normal (screen-on) use.
 *
 * ponytail: the standard tasbih-app trick, scoped to screen-off. Ceiling: volume-key
 * routing to a remote session while the screen is off is device-dependent — a few
 * OEMs only honor it for the session that most recently played audio. Upgrade path
 * if a device ignores us: hold transient audio focus (costs interrupting the user's
 * Quran/music playback), so we don't do it by default.
 */
class VolumeKeyService : Service() {

    private var session: MediaSession? = null
    private var screenOn: BroadcastReceiver? = null

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

        val open = PendingIntent.getActivity(
            this, 0, Intent(this, MainActivity::class.java),
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        session = MediaSession(this, "ZikirVolume").apply {
            // Clean, explicit metadata so the lock-screen control reads "Zikirci"
            // (an empty session used to surface a stale/foreign media title).
            setMetadata(
                MediaMetadata.Builder()
                    .putString(MediaMetadata.METADATA_KEY_TITLE, getString(R.string.svc_title))
                    .putString(MediaMetadata.METADATA_KEY_ARTIST, getString(R.string.svc_text))
                    .build()
            )
            setPlaybackState(
                PlaybackState.Builder()
                    .setActions(PlaybackState.ACTION_PLAY_PAUSE)
                    .setState(PlaybackState.STATE_PLAYING, 0, 1f)
                    .build()
            )
            setSessionActivity(open)
            setPlaybackToRemote(vp)
            isActive = true
        }

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

        // Self-stop the moment the screen turns on — MainActivity may already be
        // destroyed by then, so the service owns its own teardown.
        screenOn = object : BroadcastReceiver() {
            override fun onReceive(c: Context?, i: Intent?) { stopSelf() }
        }
        registerReceiver(screenOn, IntentFilter(Intent.ACTION_SCREEN_ON))
    }

    private fun count() {
        // This service only runs while the screen is off, so the WebView is not
        // visible and its JS is throttled — never route through applyTaps() here
        // (it could silently drop counts). Persist natively; MainActivity.onResume
        // reconciles the pending delta back into the web app when it returns.
        val tick = CounterRepo.incrementNative(this, 1)
        ZikirWidget.refresh(this)
        NativeFeedback.tap(this, tick)  // clamps at target + distinct completion feedback
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int = START_STICKY

    override fun onDestroy() {
        screenOn?.let { try { unregisterReceiver(it) } catch (e: Exception) {} }
        screenOn = null
        session?.isActive = false
        session?.release()
        session = null
        super.onDestroy()
    }
}
