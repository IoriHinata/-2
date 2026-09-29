[app]
title = Charlie Sensors
package.name = charliesensors
package.domain = org.charlie
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,atlas,ttf
version = 1.0.0

# Minimal recipes required by this Kivy Android app.
requirements = python3,kivy,pyjnius,android
orientation = portrait
fullscreen = 0

# Install-time permissions. main.py requests both permissions at runtime before
# creating Camera or AudioRecord.
android.permissions = CAMERA,RECORD_AUDIO
android.api = 33
android.minapi = 24
android.archs = arm64-v8a
android.private_storage = True
android.enable_androidx = True
android.accept_sdk_license = True
android.debug_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 1
