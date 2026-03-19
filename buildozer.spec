[app]
title = SerialTool
package.name = serialtool
package.domain = org.serial
source.dir = .
source.include_exts = py,png,jpg,kv,at
version = 1.0

# Android
android.api = 33
android.apptheme = @android:style/Theme.Holo.Light
android.sdk = 24
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.permissions = SERIAL_PORT, OTG, INTERNET
android.use_aapt2 = True

# 依赖
requirements = python3,kivy,pyserial

# 不开启调试
android.debug = False