from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only = True,
        required=True
    )

    class Meta:
        model=User
        fields=['user_id', 'user_name', 'password']
        read_only_fields = ['user_id']
    
    @transaction.atomic
    def create(self, validated_data):
        """회원가입 시 비밀번호를 해싱하여 저장"""
        password = validated_data.pop('password')
        user_name = validated_data.pop('user_name')

        user = User.objects.create_user(
            username=user_name,
            password=password,
            **validated_data
        )

        return user