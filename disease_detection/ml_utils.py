import tensorflow as tf
from keras.preprocessing.image import load_img, img_to_array
import numpy as np
import io
import os  # Import os for path management

# Load the TensorFlow model
MODEL_PATH = os.path.join('disease_detection', 'model', 'trained_model.keras')
model = tf.keras.models.load_model(MODEL_PATH)

class_names = [
    'Anthracnose', 'algal leaf', 'bird eye spot', 
    'brown blight', 'gray light', 'healthy', 
    'red leaf spot', 'white spot'
]

# Preprocess the uploaded image
def preprocess_image(image):
    image_bytes = image.read()
    image_io = io.BytesIO(image_bytes)
    img = load_img(image_io, target_size=(128, 128))  # Resize to model's input size
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array /= 255.0  # Normalize to [0, 1]
    return img_array

# Predict disease from the preprocessed image
def predict_leaf_disease(image):
    preprocessed_image = preprocess_image(image)
    prediction = model.predict(preprocessed_image)
    confidence = np.max(prediction)  # Confidence of the highest prediction
    predicted_class = np.argmax(prediction)
    return class_names[predicted_class], confidence
