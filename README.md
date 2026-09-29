# Charlie Sensors — Android APK

Проект полностью пересоздан как небольшое Kivy Android-приложение для проверки
доступа к **камере** и **микрофону**. После запуска оно запрашивает Android
runtime permissions, показывает изображение камеры и уровень входного звука.

## Сборка APK в GitHub Actions

Новый workflow находится в
[`.github/workflows/android-apk.yml`](.github/workflows/android-apk.yml).

1. Поместите изменения в ветку `main`.
2. Откройте **Actions → Charlie Android APK (container)**.
3. Нажмите **Run workflow** и выберите `main`.
4. После успеха скачайте **Artifacts → Charlie-Sensors-APK**.

Не используйте **Re-run jobs** у старого workflow: GitHub повторяет тот же
старый commit. Запускайте новый workflow с именем **Charlie Android APK
(container)**.

## Android-права

APK объявляет `CAMERA` и `RECORD_AUDIO` в `buildozer.spec`. При запуске
`main.py` запрашивает оба разрешения, а `Camera` и `AudioRecord` создаются
только после ответа Android.

## Конфигурация

- API target: 33;
- minimum API: 24;
- архитектура APK: `arm64-v8a`;
- опубликованный готовый образ: `kivy/buildozer:latest`;
- Python recipes: `python3,kivy,pyjnius,android`.
