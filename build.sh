#!/usr/bin/env bash
set -e
mkdir -p www
cp index.html www/index.html
npm install
[ -d android ] || npx cap add android
python3 patch_android.py
npx cap sync android
cd android && chmod +x gradlew && ./gradlew assembleDebug && cd ..
cp android/app/build/outputs/apk/debug/app-debug.apk Beberibes-Fighters.apk
