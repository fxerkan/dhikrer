package com.fxerkan.zikirci

import android.app.AlarmManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import java.util.Calendar

/**
 * Mirrors the web app's reminder list into exact daily AlarmManager alarms.
 * Called on every state push and on boot. Cancels the previous set, schedules
 * the currently-enabled ones (request codes 1000+index, stable within a sync).
 */
object ReminderScheduler {
    private const val BASE = 1000
    private const val PREFS = "zikir_mirror"

    fun sync(c: Context) {
        val am = c.getSystemService(AlarmManager::class.java)
        val prefs = c.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
        val prevMax = prefs.getInt("remCount", 0)
        // cancel previous
        for (i in 0 until prevMax) am.cancel(pi(c, BASE + i, "", 0))

        val list = CounterRepo.reminders(c)
        for (i in 0 until list.length()) {
            val r = list.optJSONObject(i) ?: continue
            if (!r.optBoolean("on")) continue
            val time = r.optString("time")
            val parts = time.split(":")
            if (parts.size != 2) continue
            val hh = parts[0].toIntOrNull() ?: continue
            val mm = parts[1].toIntOrNull() ?: continue
            val label = r.optString("label")
            val trigger = nextTrigger(hh, mm)
            val p = pi(c, BASE + i, label, trigger)
            // Inexact + allow-while-idle: fires within a few minutes of the target,
            // survives Doze, and needs NO exact-alarm permission (Play-policy safe).
            am.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, trigger, p)
        }
        prefs.edit().putInt("remCount", list.length()).apply()
    }

    fun nextTrigger(hh: Int, mm: Int): Long {
        val now = Calendar.getInstance()
        val cal = Calendar.getInstance().apply {
            set(Calendar.HOUR_OF_DAY, hh); set(Calendar.MINUTE, mm)
            set(Calendar.SECOND, 0); set(Calendar.MILLISECOND, 0)
        }
        if (cal.timeInMillis <= now.timeInMillis) cal.add(Calendar.DAY_OF_YEAR, 1)
        return cal.timeInMillis
    }

    private fun pi(c: Context, code: Int, label: String, trigger: Long): PendingIntent {
        val i = Intent(c, ReminderReceiver::class.java).apply {
            putExtra("label", label)
            putExtra("code", code)
        }
        return PendingIntent.getBroadcast(
            c, code, i, PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
    }
}
