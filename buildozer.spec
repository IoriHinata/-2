[app]

title = Charlie
package.name = charlie
package.domain = org.charlie

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,json,txt,atlas,ttf

version = 1.0.0

requirements = python3,kivy,numpy,pyjnius,android

orientation = portrait
fullscreen = 0

android.permissions = android.permission.CAMERA,android.permission.RECORD_AUDIO

android.minapi = 24
android.api = 35
android.ndk = 28c
android.archs = arm64-v8a

android.private_storage = True
android.enable_androidx = True
android.debug_artifact = apk

[buildozer]

log_level = 2
warn_on_root = 1
