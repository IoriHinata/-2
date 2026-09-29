# Чарли — сборка Android APK

Этот вариант специально настроен для GitHub Actions и очищает старую Android-сборку перед каждым запуском.

Главное изменение: Android Python runtime принудительно использует Python 3.12.10:
`python3==3.12.10,hostpython3==3.12.10`.

На стороне GitHub Actions используется Python 3.12, Buildozer 1.6.0 и Cython 0.29.34.

Это сделано потому, что python-for-android v2026.05.09 по документации стабилен для Python до 3.12, тогда как Python 3.14 использует более новый develop toolchain.

## Сборка

1. Загрузите файлы в корень репозитория.
2. Проверьте, что workflow находится именно здесь:
   `.github/workflows/build-apk.yml`
3. Откройте **Actions**.
4. Выберите **Build Charlie Android APK**.
5. Нажмите **Run workflow**.
6. После успешной сборки откройте **Artifacts → Charlie-APK**.

APK получает разрешения `CAMERA` и `RECORD_AUDIO`, поэтому камера и микрофон работают как часть отдельного Android-приложения, а не через Pydroid.

## Что проверяется перед сборкой

- синтаксис `main.py`;
- версия host Python 3.12;
- Cython 0.29.34;
- наличие workflow и `buildozer.spec`;
- явная фиксация Android Python 3.12.10;
- разрешения камеры и микрофона;
- целостность полученного APK.
