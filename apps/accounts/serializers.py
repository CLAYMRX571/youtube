from rest_framework.serializers import ModelSerializer
from .models import Chanel

class ChanelSerializer(ModelSerializer):
    class Meta:
        model = Chanel
        fields = ['name', 'id', 'user', 'icon', 'desc', 'banner']

