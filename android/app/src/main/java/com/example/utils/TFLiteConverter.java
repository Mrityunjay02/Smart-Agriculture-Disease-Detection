package com.example.utils;

import org.tensorflow.lite.Interpreter;
import java.io.File;
import java.io.FileInputStream;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;

public class TFLiteConverter {
    private static final String TAG = "TFLiteConverter";

    /**
     * Load TFLite model from file
     * @param modelPath Path to the .tflite model file
     * @return Interpreter instance
     */
    public static Interpreter loadTFLiteModel(String modelPath) {
        try {
            return new Interpreter(loadModelFile(modelPath));
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    /**
     * Memory-map the model file
     */
    private static MappedByteBuffer loadModelFile(String modelPath) throws Exception {
        File modelFile = new File(modelPath);
        FileInputStream inputStream = new FileInputStream(modelFile);
        FileChannel fileChannel = inputStream.getChannel();
        long startOffset = 0;
        long declaredLength = modelFile.length();
        return fileChannel.map(FileChannel.MapMode.READ_ONLY, startOffset, declaredLength);
    }

    /**
     * Example usage method
     */
    public static void main(String[] args) {
        // Example path to your .tflite model
        String tflitePath = "path/to/your/model.tflite";
        
        // Load the model
        Interpreter tflite = loadTFLiteModel(tflitePath);
        
        if (tflite != null) {
            System.out.println("Model loaded successfully!");
            // You can now use the interpreter for inference
            tflite.close(); // Don't forget to close when done
        } else {
            System.out.println("Failed to load model");
        }
    }
}
