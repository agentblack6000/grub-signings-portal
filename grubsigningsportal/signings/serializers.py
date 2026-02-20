from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Grub

class UserLoginTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        return data


class CreateGrubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grub
        fields = ["name", "description", "price_veg", "price_nonveg"]
