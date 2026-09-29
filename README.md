# Charlie Sensors — простой Android APK

Проект переписан на минимальный **нативный Android / Java / Gradle** шаблон.
APK собирается без Python, Kivy, Buildozer, NDK и сторонних Android-библиотек.
Исходный код экспериментальной нейросети сохранён в `main.py` и не включается
в Android Gradle-модуль, поэтому он не может сломать сборку APK.

## Сборка

Нужны JDK 17, Gradle 8.9 и доступ к репозиториям Google Maven и Maven Central.

```bash
gradle assembleDebug
```

Готовый файл:

```text
app/build/outputs/apk/debug/app-debug.apk
```

Для проверки без установки на устройство:

```bash
gradle --no-daemon assembleDebug
unzip -t app/build/outputs/apk/debug/app-debug.apk
```

## CI

Workflow [`.github/workflows/android-apk.yml`](.github/workflows/android-apk.yml)
запускается для pull request, push в `main` и вручную из **Actions**. Он
использует Temurin JDK 17, устанавливает Android API 35, выполняет
`assembleDebug`, проверяет ZIP-структуру APK и публикует артефакт
`Charlie-Sensors-debug-apk`.

## Исходный код нейросети

`main.py` восстановлен из исходного коммита проекта. Это оригинальная Python/Kivy
реализация CHARLIE: память, разреженная SNN на 120 000 нейронов, обработка
микрофона и камеры, обучение аудио-визуальных ассоциаций. Она сохранена как
исходник нейросети и не удаляется Gradle-сборкой. Нативный APK-модуль пока
является надёжным минимальным шаблоном сборки и не запускает этот Python-код.

## Структура

- `main.py` — восстановленный исходный код нейросети CHARLIE;
- `app/src/main/java/org/charlie/sensors/MainActivity.java` — экран приложения;
- `app/src/main/AndroidManifest.xml` — Android manifest;
- `app/build.gradle` — Android application module;
- Gradle 8.9 устанавливается в CI через `gradle/actions/setup-gradle`; бинарный Gradle Wrapper в репозиторий не добавляется.
