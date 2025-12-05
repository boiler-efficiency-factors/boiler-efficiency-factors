from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}) 
    
    verify_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['user_name', 'password', 'verify_password']
        extra_kwargs = {
            'user_name': {'required': True}
        }

    def validate(self, data):
        if not data.get('password') or not data.get('verify_password'):
            raise serializers.ValidationError({"detail": "Password and confirmation are required."})

        if data['password'] != data['verify_password']:
            raise serializers.ValidationError({"verify_password": "Passwords do not match."})

        data.pop('verify_password')
        
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            user_name=validated_data['user_name'],
            password=validated_data['password']
        )
        return user