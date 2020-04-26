from rest_framework import serializers

from api.models import UserData, Disease


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = "__all__"




class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = "__all__"
