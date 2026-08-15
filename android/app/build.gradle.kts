import java.util.Properties

plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

// Signing secrets are read from a gitignored keystore.properties (Play best
// practice). Without it, release builds are unsigned — copy the template and fill in.
val keystoreProps = Properties().apply {
    val f = rootProject.file("keystore.properties")
    if (f.exists()) f.inputStream().use { load(it) }
}

android {
    namespace = "com.fxerkan.zikirci"
    compileSdk = 36

    defaultConfig {
        // Store/package identity is dhikrer; code namespace stays zikirci.
        applicationId = "com.fxerkan.dhikrer"
        minSdk = 26
        targetSdk = 36
        // versionName = MAJOR.MINOR.PATCH (see CLAUDE.md "Versioning").
        // versionCode = monotonic build counter, +1 every release (Play Store requirement).
        versionCode = 14
        versionName = "1.3.1"
    }

    signingConfigs {
        create("release") {
            // Secrets live only in the gitignored keystore.properties — no fallbacks in VCS.
            storeFile = rootProject.file(keystoreProps.getProperty("storeFile") ?: "zikirci-release.jks")
            storePassword = keystoreProps.getProperty("storePassword") ?: ""
            keyAlias = keystoreProps.getProperty("keyAlias") ?: ""
            keyPassword = keystoreProps.getProperty("keyPassword") ?: ""
        }
    }
    buildTypes {
        release {
            isMinifyEnabled = false
            signingConfig = signingConfigs.getByName("release")
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }
    // assets under app/ (app.html + vendored libs) are large text — no compression needed to avoid issues
    androidResources {
        noCompress += listOf("woff2")
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.appcompat:appcompat:1.7.0")
    implementation("androidx.webkit:webkit:1.11.0")
}
