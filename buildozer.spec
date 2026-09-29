[app]
# Charlie — standalone Android application
# Python 3.12 is pinned because the stable p4a 2026.05.09 toolchain
# is documented as stable through Python 3.12.

title = Charlie
package.name = charlie
package.domain = org.charlie
source.dir = .
source.include_exts = py,json,png,jpg,jpeg,atlas,kv,ttf,txt
version = 1.0.0

# Explicitly keep the Android Python runtime on the stable 3.12 recipe.
requirements = python3==3.12.10,hostpython3==3.12.10,kivy,numpy,pyjnius,android
orientation = portrait
fullscreen = 0

android.permissions = android.permission.CAMERA,android.permission.RECORD_AUDIO
android.minapi = 24
android.api = 35
android.ndk = 28c
android.archs = arm64-v8a
android.accept_sdk_license = True

android.entrypoint = org.kivy.android.PythonActivity
android.private_storage = True
android.enable_androidx = True
android.debug_artifact = apk
android.allow_backup = True
android.logcat_filters = *:S python:D

# Stable p4a release v2026.05.09.
p4a.branch = master
p4a.commit = 58d21141

[buildozer]
log_level = 2
warn_on_root = 1
