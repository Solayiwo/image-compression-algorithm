from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import CustomUser, GuestUser, CompressionTask


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = CustomUser.objects.create_user(**validated_data)
        return user
        
        
class GuestUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = GuestUser
        fields = '__all__'
    
    def create(self, validated_data):
            guest_user = GuestUser.objects.create_user(**validated_data)
            return guest_user


class ImageCompressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompressionTask
        fields = '__all__'