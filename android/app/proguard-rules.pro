# Keep JS bridge interface methods (called from WebView)
-keepclassmembers class com.fxerkan.zikirci.** {
    @android.webkit.JavascriptInterface <methods>;
}
