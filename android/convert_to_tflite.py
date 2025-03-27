import tensorflow as tf

def convert_h5_to_tflite(h5_model_path, tflite_model_path):
    # Load the H5 model
    model = tf.keras.models.load_model(h5_model_path)
    
    # Convert the model to TFLite format
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    
    # Save the TFLite model
    with open(tflite_model_path, 'wb') as f:
        f.write(tflite_model)
    
    print(f"Model successfully converted and saved to: {tflite_model_path}")

if __name__ == "__main__":
    # Replace these paths with your actual paths
    h5_model_path = "path/to/your/model.h5"  # Input your .h5 model path here
    tflite_model_path = "path/to/save/model.tflite"  # Where you want to save the .tflite file
    
    convert_h5_to_tflite(h5_model_path, tflite_model_path)
