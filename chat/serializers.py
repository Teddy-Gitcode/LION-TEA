from rest_framework.serializers import ModelSerializer

from .  models import Farmer

class FarmerSerializers(ModelSerializer):
    class Meta:
        model = Farmer
        fields = '__all__'