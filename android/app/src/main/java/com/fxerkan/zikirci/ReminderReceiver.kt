package com.fxerkan.zikirci

import android.app.NotificationManager
import android.app.PendingIntent
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import androidx.core.app.NotificationCompat

class ReminderReceiver : BroadcastReceiver() {
    override fun onReceive(c: Context, intent: Intent) {
        Notifications.ensureChannel(c)
        val label = intent.getStringExtra("label") ?: ""
        val code = intent.getIntExtra("code", 1000)

        val open = PendingIntent.getActivity(
            c, 0, Intent(c, MainActivity::class.java).apply {
                flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_SINGLE_TOP
            }, PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val title = c.getString(R.string.reminder_title)
        val text = if (label.isNotBlank()) label else c.getString(R.string.reminder_text)
        val n = NotificationCompat.Builder(c, Notifications.CHANNEL_REMINDER)
            .setSmallIcon(R.drawable.ic_bead)
            .setContentTitle(title)
            .setContentText(text)
            .setAutoCancel(true)
            .setContentIntent(open)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .build()
        c.getSystemService(NotificationManager::class.java).notify(code, n)

        // re-arm the same reminder for tomorrow (exact repeating isn't allowed)
        ReminderScheduler.sync(c)
    }
}
