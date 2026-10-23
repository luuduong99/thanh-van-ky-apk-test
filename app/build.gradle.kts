plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "vn.thanhvanky.prototype"
    compileSdk = 35

    defaultConfig {
        applicationId = "vn.thanhvanky.prototype"
        minSdk = 23
        targetSdk = 35
        versionCode = 1
        versionName = "0.1.0"
    }
}
