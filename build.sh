#!/usr/bin/env bash
# Local build (requires Node 18+, JDK 17 and Android SDK). Output: Beberibes-Fighters.apk
set -e
npm install
[ -d android ] || npx cap add android
python3 scripts/patch_android.py
npx cap sync android
cd android && ./gradlew assembleDebug && cd ..
cp android/app/build/outputs/apk/debug/app-debug.apk Beberibes-Fighters.apk
echo "APK pronto: Beberibes-Fighters.apk"
