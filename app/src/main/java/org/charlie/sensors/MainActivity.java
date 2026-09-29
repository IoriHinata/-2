package org.charlie.sensors;

import android.app.Activity;
import android.graphics.Color;
import android.os.Bundle;
import android.view.Gravity;
import android.widget.LinearLayout;
import android.widget.TextView;

/** Entry point for a deliberately dependency-free Android APK template. */
public final class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        int padding = (int) (24 * getResources().getDisplayMetrics().density);
        LinearLayout content = new LinearLayout(this);
        content.setOrientation(LinearLayout.VERTICAL);
        content.setGravity(Gravity.CENTER);
        content.setPadding(padding, padding, padding, padding);
        content.setBackgroundColor(Color.rgb(18, 18, 18));

        TextView title = new TextView(this);
        title.setText("Charlie Sensors");
        title.setTextColor(Color.WHITE);
        title.setTextSize(28);
        title.setGravity(Gravity.CENTER);

        TextView message = new TextView(this);
        message.setText("APK успешно собран\nНативный Android-шаблон готов к расширению.");
        message.setTextColor(Color.LTGRAY);
        message.setTextSize(17);
        message.setGravity(Gravity.CENTER);
        message.setPadding(0, padding, 0, 0);

        content.addView(title);
        content.addView(message);
        setContentView(content);
    }
}
