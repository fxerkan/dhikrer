package com.fxerkan.zikirci

import android.app.PendingIntent
import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.widget.RemoteViews

/** Resizable home-screen widget (2x2 .. 4x2): live count + tap-to-count + open app. */
class ZikirWidget : AppWidgetProvider() {

    companion object {
        const val ACTION_TAP = "com.fxerkan.zikirci.WIDGET_TAP"

        fun refresh(c: Context) {
            val mgr = AppWidgetManager.getInstance(c)
            val ids = mgr.getAppWidgetIds(ComponentName(c, ZikirWidget::class.java))
            for (id in ids) render(c, mgr, id)
        }

        private fun render(c: Context, mgr: AppWidgetManager, id: Int) {
            val rv = RemoteViews(c.packageName, R.layout.widget_layout)
            val name = CounterRepo.name(c)
            val count = CounterRepo.count(c)
            val target = CounterRepo.target(c)
            rv.setTextViewText(R.id.w_name, name)
            rv.setTextViewText(R.id.w_count, count.toString())
            rv.setTextViewText(
                R.id.w_target,
                if (target > 0) "%d / %d".format(count, target) else c.getString(R.string.free)
            )

            // "+" -> count
            val tap = Intent(c, ZikirWidget::class.java).apply { action = ACTION_TAP }
            rv.setOnClickPendingIntent(
                R.id.w_plus,
                PendingIntent.getBroadcast(c, 1, tap, PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE)
            )
            // body -> open app
            val open = Intent(c, MainActivity::class.java).apply {
                flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_SINGLE_TOP
            }
            rv.setOnClickPendingIntent(
                R.id.w_body,
                PendingIntent.getActivity(c, 2, open, PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE)
            )
            mgr.updateAppWidget(id, rv)
        }
    }

    override fun onUpdate(c: Context, mgr: AppWidgetManager, ids: IntArray) {
        for (id in ids) render(c, mgr, id)
    }

    override fun onReceive(c: Context, intent: Intent) {
        super.onReceive(c, intent)
        if (intent.action == ACTION_TAP) {
            if (MainActivity.isAlive()) MainActivity.applyTaps(1)
            else NativeFeedback.tap(c, CounterRepo.incrementNative(c, 1))
            refresh(c)
        }
    }
}
