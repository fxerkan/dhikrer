package com.fxerkan.zikirci

import android.annotation.SuppressLint
import android.content.Intent
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.os.VibrationEffect
import android.os.Vibrator
import android.view.KeyEvent
import android.webkit.JavascriptInterface
import android.webkit.WebResourceRequest
import android.webkit.WebResourceResponse
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.WindowInsetsControllerCompat
import androidx.webkit.WebSettingsCompat
import androidx.webkit.WebViewAssetLoader
import androidx.webkit.WebViewFeature
import org.json.JSONArray
import java.lang.ref.WeakReference

class MainActivity : AppCompatActivity() {

    private lateinit var web: WebView
    private var loaded = false

    companion object {
        private var ref: WeakReference<MainActivity>? = null
        /** True when a live Activity can apply taps directly into the web app. */
        fun isAlive(): Boolean = ref?.get()?.loaded == true
        /** Apply n real taps in the running web app (fires haptics/milestones/persist). */
        fun applyTaps(n: Int) {
            val a = ref?.get() ?: return
            a.runOnUiThread { if (a.loaded) a.web.evaluateJavascript("window.__zikirTap($n)", null) }
        }
    }

    @SuppressLint("SetJavaScriptEnabled")
    private var insets = intArrayOf(0, 0, 0, 0) // top, bottom, left, right (px)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        ref = WeakReference(this)
        Notifications.ensureChannel(this)
        // targetSdk 35 draws edge-to-edge; we forward the system-bar insets to the
        // web layout (as CSS vars) so the header/nav stay inside the safe area.
        WindowCompat.setDecorFitsSystemWindows(window, false)

        val loader = WebViewAssetLoader.Builder()
            .addPathHandler("/assets/", WebViewAssetLoader.AssetsPathHandler(this))
            .build()

        web = WebView(this)
        web.setBackgroundColor(0xFF161826.toInt())
        web.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true
            mediaPlaybackRequiresUserGesture = false
            allowFileAccess = false
            allowContentAccess = false
            useWideViewPort = true
            loadWithOverviewMode = true
        }
        // The app controls its own light/dark palette (10 themes). Stop WebView
        // from auto-inverting colors by system dark mode (that broke dark themes).
        if (WebViewFeature.isFeatureSupported(WebViewFeature.ALGORITHMIC_DARKENING)) {
            WebSettingsCompat.setAlgorithmicDarkeningAllowed(web.settings, false)
        }
        web.webViewClient = object : WebViewClient() {
            override fun shouldInterceptRequest(
                view: WebView, request: WebResourceRequest
            ): WebResourceResponse? = loader.shouldInterceptRequest(request.url)

            // Open external links (e.g. @FXerkan) in the system browser, not in-app.
            override fun shouldOverrideUrlLoading(
                view: WebView, request: WebResourceRequest
            ): Boolean {
                val url = request.url
                if (url.host == "appassets.androidplatform.net") return false
                return try {
                    startActivity(Intent(Intent.ACTION_VIEW, url).apply {
                        addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                    })
                    true
                } catch (e: Exception) { true }
            }

            override fun onPageFinished(view: WebView, url: String) {
                loaded = true
                pushInsets()
                reconcilePending()
            }
        }
        web.addJavascriptInterface(Bridge(), "ZikirNative")
        setContentView(web)

        ViewCompat.setOnApplyWindowInsetsListener(web) { _, wi ->
            val b = wi.getInsets(WindowInsetsCompat.Type.systemBars() or WindowInsetsCompat.Type.displayCutout())
            insets = intArrayOf(b.top, b.bottom, b.left, b.right)
            pushInsets()
            wi
        }
        // Force a fresh insets dispatch: the listener above is attached after the
        // window's first dispatch on some devices (e.g. API 35+ emulators), so it
        // never fires and --zk-sat stays 0 → header overlaps the status bar.
        ViewCompat.requestApplyInsets(web)

        // immersive-ish: draw behind system bars handled by theme; keep simple
        web.loadUrl("https://appassets.androidplatform.net/assets/app/app.html")

        // ask for notification permission (reminders) on Android 13+
        if (Build.VERSION.SDK_INT >= 33 &&
            checkSelfPermission(android.Manifest.permission.POST_NOTIFICATIONS) !=
            android.content.pm.PackageManager.PERMISSION_GRANTED
        ) {
            requestPermissions(arrayOf(android.Manifest.permission.POST_NOTIFICATIONS), 1)
        }
    }

    private fun pushInsets() {
        if (!loaded) return
        val d = resources.displayMetrics.density
        fun px(v: Int) = (v / d)
        web.evaluateJavascript(
            "var s=document.documentElement.style;" +
                "s.setProperty('--zk-sat','${px(insets[0])}px');" +
                "s.setProperty('--zk-sab','${px(insets[1])}px');" +
                "s.setProperty('--zk-sal','${px(insets[2])}px');" +
                "s.setProperty('--zk-sar','${px(insets[3])}px');", null
        )
    }

    private fun reconcilePending() {
        val d = CounterRepo.pendingDelta(this)
        if (d > 0 && loaded) {
            web.evaluateJavascript("window.__zikirApplyPending($d)", null)
            CounterRepo.clearPending(this)
        }
    }

    override fun onResume() {
        super.onResume()
        reconcilePending()
        // keep the screen-off volume-key service running if enabled
        if (CounterRepo.volumeKeysEnabled(this)) VolumeKeyService.start(this)
    }

    // Volume keys while app is focused (screen on) -> count.
    override fun onKeyDown(keyCode: Int, event: KeyEvent): Boolean {
        if ((keyCode == KeyEvent.KEYCODE_VOLUME_UP || keyCode == KeyEvent.KEYCODE_VOLUME_DOWN) &&
            CounterRepo.volumeKeysEnabled(this) && loaded
        ) {
            applyTaps(1)
            return true
        }
        return super.onKeyDown(keyCode, event)
    }

    /** Called by the web app on every state change. */
    inner class Bridge {
        @JavascriptInterface
        fun onState(json: String) {
            CounterRepo.saveFromWeb(this@MainActivity, json)
            ZikirWidget.refresh(this@MainActivity)
            ReminderScheduler.sync(this@MainActivity)
            if (CounterRepo.volumeKeysEnabled(this@MainActivity)) VolumeKeyService.start(this@MainActivity)
            else VolumeKeyService.stop(this@MainActivity)
            // match system-bar icon color to the active theme (light icons on dark)
            val dark = try { org.json.JSONObject(json).optBoolean("dark", true) } catch (e: Exception) { true }
            runOnUiThread {
                val c = WindowInsetsControllerCompat(window, web)
                c.isAppearanceLightStatusBars = !dark
                c.isAppearanceLightNavigationBars = !dark
            }
        }

        /** Reliable haptics — navigator.vibrate is unreliable in WebView, so the
         *  web app's vibrate() is shimmed to call this. pattern = JSON number or
         *  array of ms (Web Vibration API semantics: [on,off,on,...]). */
        @JavascriptInterface
        fun vibrate(pattern: String) {
            val vib = getSystemService(Vibrator::class.java) ?: return
            if (!vib.hasVibrator()) return
            try {
                val trimmed = pattern.trim()
                val timings: LongArray = if (trimmed.startsWith("[")) {
                    val arr = JSONArray(trimmed)
                    LongArray(arr.length()) { arr.optLong(it) }
                } else {
                    longArrayOf(trimmed.toDoubleOrNull()?.toLong() ?: return)
                }
                if (timings.isEmpty() || timings.all { it <= 0 }) return
                if (timings.size == 1) {
                    vib.vibrate(VibrationEffect.createOneShot(timings[0].coerceAtLeast(1), VibrationEffect.DEFAULT_AMPLITUDE))
                } else {
                    vib.vibrate(VibrationEffect.createWaveform(timings, -1))
                }
            } catch (e: Exception) { /* ignore malformed pattern */ }
        }
    }
}
