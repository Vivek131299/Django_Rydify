from rest_framework import serializers
from .models import Location, TravelDetails


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class TravelDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelDetails
        fields = '__all__'
