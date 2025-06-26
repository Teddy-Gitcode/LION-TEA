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

# Information for the diseases, including specific medicines from companies
disease_info = {
    'Anthracnose': {
        'cause': 'Fungal infection caused by Colletotrichum species.',
        'treatment': 'Remove infected leaves and apply fungicides.',
        'medicine': [
            {'name': 'Copper Oxychloride', 'company': 'BASF', 'application_rate': '1 bottle per hectare'},
            {'name': 'Propiconazole', 'company': 'Syngenta', 'application_rate': '1 bottle per hectare'}
        ]
    },
    'algal leaf': {
        'cause': 'Caused by algae growing on leaf surfaces.',
        'treatment': 'Improve airflow around plants and use fungicides.',
        'medicine': [
            {'name': 'Copper Sulfate', 'company': 'Bayer', 'application_rate': '1 bottle per hectare'},
            {'name': 'Chlorothalonil', 'company': 'Dow Agrosciences', 'application_rate': '1 bottle per hectare'}
        ]
    },
    'bird eye spot': {
        'cause': 'Fungal infection caused by Helminthosporium species.',
        'treatment': 'Remove infected leaves and apply fungicides.',
        'medicine': [
            {'name': 'Tebuconazole', 'company': 'FMC Corporation', 'application_rate': '1 bottle per hectare'},
            {'name': 'Carbendazim', 'company': 'Syngenta', 'application_rate': '1 bottle per hectare'}
        ]
    },
    'brown blight': {
        'cause': 'Fungal infection caused by various species.',
        'treatment': 'Prune infected areas and apply fungicides.',
        'medicine': [
            {'name': 'Mancozeb', 'company': 'BASF', 'application_rate': '1 bottle per hectare'},
            {'name': 'Azoxystrobin', 'company': 'Dow Agrosciences', 'application_rate': '1 bottle per hectare'}
        ]
    },
    'gray light': {
        'cause': 'Caused by a fungal pathogen, typically Botrytis species.',
        'treatment': 'Improve plant spacing and apply fungicides.',
        'medicine': [
            {'name': 'Fludioxonil', 'company': 'Syngenta', 'application_rate': '1 bottle per hectare'},
            {'name': 'Boscalid', 'company': 'Bayer', 'application_rate': '1 bottle per hectare'}
        ]
    },
    'healthy': {
        'cause': 'No disease, healthy plant.',
        'treatment': 'Continue standard plant care.',
        'medicine': 'N/A'
    },
    'red leaf spot': {
        'cause': 'Fungal infection, often by species like Phaeosphaeria.',
        'treatment': 'Remove infected leaves and use fungicides.',
        'medicine': [
            {'name': 'Azoxystrobin', 'company': 'Bayer', 'application_rate': '1 bottle per hectare'},
            {'name': 'Fluopyram', 'company': 'BASF', 'application_rate': '1 bottle per hectare'}
        ]
    },
    'white spot': {
        'cause': 'Fungal or bacterial infection.',
        'treatment': 'Remove affected parts and use fungicides.',
        'medicine': [
            {'name': 'Thiophanate-Methyl', 'company': 'Syngenta', 'application_rate': '1 bottle per hectare'},
            {'name': 'Chlorothalonil', 'company': 'Dow Agrosciences', 'application_rate': '1 bottle per hectare'}
        ]
    }
}

# Predict disease from the preprocessed image
def predict_leaf_disease(image):
    preprocessed_image = preprocess_image(image)
    prediction = model.predict(preprocessed_image)
    confidence = np.max(prediction)  # Confidence of the highest prediction
    predicted_class = np.argmax(prediction)
    disease = class_names[predicted_class]
    
    # Return disease, cause, treatment, and medicine for 'Anthracnose'
    if disease == 'Anthracnose':
        info = disease_info[disease]
        return {
            'disease': disease,
            'cause': info['cause'],
            'treatment': info['treatment'],
            'medicine': info['medicine'],
            'confidence': confidence
        }
    
    return {
        'disease': disease,
        'confidence': confidence
    }
