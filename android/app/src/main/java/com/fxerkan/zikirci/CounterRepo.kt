package com.fxerkan.zikirci

import android.content.Context
import org.json.JSONArray
import org.json.JSONObject

/**
 * Native mirror of the web app's active-counter + relevant settings.
 * The WebView (source of truth while open) pushes state here via the JS bridge;
 * the widget / volume-keys / reminders read from here so every surface agrees.
 *
 * ponytail: mirror + pendingDelta reconciliation, not a shared DB. If the user
 * counts natively (widget) AND in-app before the app reconciles, counts can
 * drift by the un-applied delta; acceptable for v1. Upgrade path: make native
 * the single source and have the web read counts through the bridge.
 */
object CounterRepo {
    private const val PREFS = "zikir_mirror"

    private fun p(c: Context) = c.getSharedPreferences(PREFS, Context.MODE_PRIVATE)

    fun saveFromWeb(c: Context, json: String) {
        val o = JSONObject(json)
        p(c).edit().apply {
            putLong("activeId", o.optLong("activeId"))
            putString("name", o.optString("name"))
            putInt("count", o.optInt("count"))
            putInt("target", o.optInt("target"))
            putBoolean("volumeKeys", o.optBoolean("volumeKeys", true))
            putBoolean("haptic", o.optBoolean("haptic", true))
            putString("lang", o.optString("lang", "tr"))
            putString("reminders", o.optJSONArray("reminders")?.toString() ?: "[]")
            apply()
        }
    }

    fun name(c: Context): String = p(c).getString("name", "Zikir") ?: "Zikir"
    fun count(c: Context): Int = p(c).getInt("count", 0)
    fun target(c: Context): Int = p(c).getInt("target", 0)
    fun volumeKeysEnabled(c: Context): Boolean = p(c).getBoolean("volumeKeys", true)
    fun hapticEnabled(c: Context): Boolean = p(c).getBoolean("haptic", true)
    fun lang(c: Context): String = p(c).getString("lang", "tr") ?: "tr"

    fun reminders(c: Context): JSONArray =
        try { JSONArray(p(c).getString("reminders", "[]")) } catch (e: Exception) { JSONArray() }

    /** Native increment while app is not in foreground: bump mirror + queue delta. */
    fun incrementNative(c: Context, by: Int = 1) {
        p(c).edit()
            .putInt("count", count(c) + by)
            .putInt("pendingDelta", pendingDelta(c) + by)
            .apply()
    }

    fun pendingDelta(c: Context): Int = p(c).getInt("pendingDelta", 0)
    fun clearPending(c: Context) { p(c).edit().putInt("pendingDelta", 0).apply() }
}
