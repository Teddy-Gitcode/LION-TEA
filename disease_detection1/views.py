from django.shortcuts import render
import numpy as np
import tensorflow as tf
from keras.preprocessing.image import load_img, img_to_array
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os
from .serializers import DiseasePredictionSerializer
import io

# Get the absolute path of the model file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'disease_detection/model/trained_model.keras')

# Load your model
try:
    model = tf.keras.models.load_model(MODEL_PATH)
except ValueError as e:
    raise ValueError(f"Could not load model. Error: {e}")

class_names = [
    'Anthracnose', 'algal leaf', 'bird eye spot', 
    'brown blight', 'gray light', 'healthy', 
    'red leaf spot', 'white spot'
]

def preprocess_image(image):
    # Convert the InMemoryUploadedFile to a BytesIO object
    image_bytes = image.read()
    image_io = io.BytesIO(image_bytes)
    
    img = load_img(image_io, target_size=(128, 128))  # Resize image to match model's expected input
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Create batch axis
    img_array /= 255.0  # Normalize to [0, 1]
    return img_array

@api_view(['POST'])
def predict_disease(request):
    serializer = DiseasePredictionSerializer(data=request.data)
    if serializer.is_valid():
        image = serializer.validated_data['image']
        preprocessed_image = preprocess_image(image)
        prediction = model.predict(preprocessed_image)
        
        result_index = np.argmax(prediction, axis=1)[0]  # Get the index of the highest probability
        model_prediction = class_names[result_index]
        
        return Response({'prediction': model_prediction})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
