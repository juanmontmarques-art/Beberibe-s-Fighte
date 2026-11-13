import re, pathlib
a = pathlib.Path("android/app/src/main")
# 1) Manifest: horizontal + fullscreen
m = a/"AndroidManifest.xml"
t = m.read_text()
t = re.sub(r'(<activity\b)', r'\1 android:screenOrientation="sensorLandscape"', t, count=1)
t = t.replace('android:configChanges="', 'android:configChanges="orientation|screenSize|', 1) if 'configChanges' in t else t
m.write_text(t)
# 2) Tema fullscreen + notch
s = a/"res/values/styles.xml"
t = s.read_text()
extra = '''
        <item name="android:windowFullscreen">true</item>
        <item name="android:windowLayoutInDisplayCutoutMode">shortEdges</item>
        <item name="android:windowBackground">@android:color/black</item>'''
t = re.sub(r'(<style name="AppTheme.NoActionBarLaunch".*?>)', r'\1', t)
t = t.replace('<style name="AppTheme.NoActionBar" parent="Theme.AppCompat.DayNight.NoActionBar">',
              '<style name="AppTheme.NoActionBar" parent="Theme.AppCompat.DayNight.NoActionBar">'+extra, 1)
s.write_text(t)
# 3) MainActivity: modo imersivo (esconde barras)
j = next(a.glob("java/**/MainActivity.java"))
j.write_text('''package com.beberibe.fighters;

import android.os.Bundle;
import android.view.View;
import android.view.WindowManager;
import androidx.core.view.WindowCompat;
import androidx.core.view.WindowInsetsControllerCompat;
import androidx.core.view.WindowInsetsCompat;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        hide();
    }
    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        if (hasFocus) hide();
    }
    private void hide() {
        WindowCompat.setDecorFitsSystemWindows(getWindow(), false);
        WindowInsetsControllerCompat c = new WindowInsetsControllerCompat(getWindow(), getWindow().getDecorView());
        c.hide(WindowInsetsCompat.Type.systemBars());
        c.setSystemBarsBehavior(WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE);
    }
}
''')
print("patched", j)
