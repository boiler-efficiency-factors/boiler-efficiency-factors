from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    class Meta:
        model=User
        fields=['user_id', 'user_name', 'password']
        read_only_fields = ['user_id']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user_name = validated_data.pop('user_name')

        user = User.objects.create_user(
            user_name=user_name,
            password=password
        )

        return user