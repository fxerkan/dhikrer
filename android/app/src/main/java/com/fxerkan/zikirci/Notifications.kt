package com.fxerkan.zikirci

import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Context

object Notifications {
    const val CHANNEL_REMINDER = "zikir_reminders"
    const val CHANNEL_SERVICE = "zikir_service"

    fun ensureChannel(c: Context) {
        val nm = c.getSystemService(NotificationManager::class.java)
        nm.createNotificationChannel(
            NotificationChannel(CHANNEL_REMINDER, "Zikir Hatırlatıcıları", NotificationManager.IMPORTANCE_HIGH)
        )
        nm.createNotificationChannel(
            NotificationChannel(CHANNEL_SERVICE, "Sayaç Servisi", NotificationManager.IMPORTANCE_LOW).apply {
                setShowBadge(false)
            }
        )
    }
}
