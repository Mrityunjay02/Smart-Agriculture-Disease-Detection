package com.example;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import com.example.utils.TFLiteConverter;
import org.tensorflow.lite.Interpreter;

public class MainActivity extends AppCompatActivity {
    private static final String TAG = "MainActivity";
    private Interpreter tflite;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Load model from assets folder
        try {
            String modelPath = getAssets().open("model.tflite").toString();
            tflite = TFLiteConverter.loadTFLiteModel(modelPath);
            if (tflite != null) {
                Log.d(TAG, "Model loaded successfully");
            }
        } catch (Exception e) {
            Log.e(TAG, "Error loading model: " + e.getMessage());
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (tflite != null) {
            tflite.close();
        }
    }
}
