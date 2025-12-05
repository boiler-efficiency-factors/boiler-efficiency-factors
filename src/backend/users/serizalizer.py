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
    
    def create(self, validated_date):
        password = validated_date.pop('password')

        user = User.objects.create_user(
            username=validated_date.get('user_name'),
            password=password,
            **validated_date
        )

        return user