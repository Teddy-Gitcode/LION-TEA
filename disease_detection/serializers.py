# disease_detection/serializers.py

from rest_framework import serializers

class DiseasePredictionSerializer(serializers.Serializer):
    image = serializers.ImageField()
