# -*- coding: utf-8 -*-
"""Charlie sensor test — Android camera and microphone permissions."""

import math
import threading
import time

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar

SAMPLE_RATE = 16_000
CHUNK_SAMPLES = 1_024


def android_grant_result(value):
    """Return True only for an Android granted result (bool or result code 0)."""
    if isinstance(value, bool):
        return value
    try:
        return int(value) == 0  # PackageManager.PERMISSION_GRANTED
    except (TypeError, ValueError):
        return False


class AndroidMicrophone:
    """Small AudioRecord wrapper; all UI updates are scheduled on Kivy's thread."""

    def __init__(self, on_level, on_error):
        self.on_level = on_level
        self.on_error = on_error
        self.record = None
        self.running = False

    def start(self):
        try:
            from jnius import autoclass, jarray

            audio_record = autoclass("android.media.AudioRecord")
            source = autoclass("android.media.MediaRecorder$AudioSource")
            audio_format = autoclass("android.media.AudioFormat")
            channel = audio_format.CHANNEL_IN_MONO
            encoding = audio_format.ENCODING_PCM_16BIT
            minimum = int(audio_record.getMinBufferSize(SAMPLE_RATE, channel, encoding))
            if minimum <= 0:
                raise RuntimeError("Android returned an invalid microphone buffer size")
            self.record = audio_record(source.MIC, SAMPLE_RATE, channel, encoding,
                                       max(minimum, CHUNK_SAMPLES * 2))
            self.record.startRecording()
            self.running = True
            threading.Thread(target=self._read_loop, args=(jarray,), daemon=True).start()
            return True
        except Exception as error:
            self.record = None
            error_name = type(error).__name__
            Clock.schedule_once(
                lambda _dt, name=error_name: self.on_error("Микрофон недоступен: " + name), 0)
            return False

    def _read_loop(self, jarray):
        buffer = jarray("h")(CHUNK_SAMPLES)
        while self.running:
            try:
                count = int(self.record.read(buffer, 0, CHUNK_SAMPLES))
                if count <= 0:
                    continue
                energy = sum(int(buffer[index]) ** 2 for index in range(count)) / count
                level = min(1.0, math.sqrt(energy) / 8_000.0)
                Clock.schedule_once(lambda _dt, value=level: self.on_level(value), 0)
            except Exception:
                if self.running:
                    Clock.schedule_once(lambda _dt: self.on_error("Ошибка чтения микрофона"), 0)
                break

    def stop(self):
        self.running = False
        if self.record is not None:
            try:
                self.record.stop()
                self.record.release()
            except Exception:
                pass
        self.record = None


class SensorScreen(BoxLayout):
    status = StringProperty("Нажмите «Запросить доступ»")
    microphone_level = NumericProperty(0.0)

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=dp(12), spacing=dp(10), **kwargs)
        self.camera = None
        self.microphone = None
        self.camera_allowed = False
        self.microphone_allowed = False
        self._build_ui()
        Clock.schedule_once(lambda _dt: self.request_permissions(), 0.4)
        Clock.schedule_interval(self._refresh, 0.15)

    def _build_ui(self):
        self.add_widget(Label(text="[b]CHARLIE — сенсоры Android[/b]", markup=True,
                              font_size=sp(20), size_hint_y=None, height=dp(42)))
        self.status_label = Label(text=self.status, halign="center", valign="middle",
                                  size_hint_y=None, height=dp(55), font_size=sp(14))
        self.status_label.bind(size=lambda widget, _size: setattr(widget, "text_size", widget.size))
        self.add_widget(self.status_label)

        self.camera_box = BoxLayout(size_hint_y=1)
        self.placeholder = Label(text="Камера будет запущена после выдачи разрешения",
                                 halign="center", valign="middle")
        self.placeholder.bind(size=lambda widget, _size: setattr(widget, "text_size", widget.size))
        self.camera_box.add_widget(self.placeholder)
        self.add_widget(self.camera_box)

        meter = BoxLayout(size_hint_y=None, height=dp(34), spacing=dp(8))
        meter.add_widget(Label(text="Микрофон", size_hint_x=0.3))
        self.microphone_bar = ProgressBar(max=1, value=0, size_hint_x=0.7)
        meter.add_widget(self.microphone_bar)
        self.add_widget(meter)

        controls = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(8))
        request = Button(text="ЗАПРОСИТЬ ДОСТУП")
        request.bind(on_release=lambda _button: self.request_permissions())
        stop = Button(text="ОСТАНОВИТЬ")
        stop.bind(on_release=lambda _button: self.stop_sensors())
        controls.add_widget(request)
        controls.add_widget(stop)
        self.add_widget(controls)

    def _permission_state(self):
        try:
            from android.permissions import Permission, check_permission
            return (bool(check_permission(Permission.CAMERA)),
                    bool(check_permission(Permission.RECORD_AUDIO)))
        except Exception:
            return (False, False)

    def request_permissions(self):
        try:
            from android.permissions import Permission, request_permissions
            camera, microphone = self._permission_state()
            required = []
            if not camera:
                required.append(Permission.CAMERA)
            if not microphone:
                required.append(Permission.RECORD_AUDIO)
            if not required:
                self._permissions_finished(True, True)
                return

            self.status = "Разрешите доступ к камере и микрофону в Android"

            def callback(permissions, grants):
                granted = {str(permission): android_grant_result(result)
                           for permission, result in zip(permissions, grants)}
                current_camera, current_microphone = self._permission_state()
                camera_ok = current_camera or granted.get(str(Permission.CAMERA), False)
                microphone_ok = current_microphone or granted.get(str(Permission.RECORD_AUDIO), False)
                Clock.schedule_once(
                    lambda _dt: self._permissions_finished(camera_ok, microphone_ok), 0)

            request_permissions(required, callback)
        except Exception as error:
            self.status = "Запрос разрешений доступен только в Android: " + type(error).__name__

    def _permissions_finished(self, camera_ok, microphone_ok):
        self.camera_allowed = camera_ok
        self.microphone_allowed = microphone_ok
        self.stop_sensors(keep_status=True)
        results = []
        if camera_ok:
            self.start_camera()
            results.append("камера: разрешена")
        else:
            results.append("камера: запрещена")
        if microphone_ok:
            self.start_microphone()
            results.append("микрофон: разрешён")
        else:
            results.append("микрофон: запрещён")
        self.status = " • ".join(results)

    def start_camera(self):
        try:
            self.camera = Camera(play=False, resolution=(640, 480), size_hint=(1, 1))
            self.camera_box.clear_widgets()
            self.camera_box.add_widget(self.camera)
            self.camera.play = True
        except Exception as error:
            self.camera = None
            self.camera_box.clear_widgets()
            self.placeholder.text = "Камера недоступна\n" + type(error).__name__
            self.camera_box.add_widget(self.placeholder)

    def start_microphone(self):
        self.microphone = AndroidMicrophone(self._set_microphone_level, self._set_error)
        if not self.microphone.start():
            self.microphone = None

    def _set_microphone_level(self, value):
        self.microphone_level = value

    def _set_error(self, message):
        self.status = message

    def _refresh(self, _dt):
        self.status_label.text = self.status
        self.microphone_bar.value = self.microphone_level

    def stop_sensors(self, keep_status=False):
        if self.camera is not None:
            try:
                self.camera.play = False
            except Exception:
                pass
            self.camera = None
        if self.microphone is not None:
            self.microphone.stop()
            self.microphone = None
        self.microphone_level = 0.0
        if not keep_status:
            self.status = "Сенсоры остановлены"

    def on_parent(self, _widget, parent):
        if parent is None:
            self.stop_sensors()


class CharlieApp(App):
    title = "Charlie Sensors"

    def build(self):
        self.screen = SensorScreen()
        return self.screen

    def on_stop(self):
        self.screen.stop_sensors()


if __name__ == "__main__":
    CharlieApp().run()
