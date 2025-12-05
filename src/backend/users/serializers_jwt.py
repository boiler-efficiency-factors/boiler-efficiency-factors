from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    user_name = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # username 필드 제거
        if 'username' in self.fields:
            del self.fields['username']
    
    def validate(self, attrs):
        user_name = attrs.get('user_name')
        password = attrs.get('password')
        
        if not user_name or not password:
            raise serializers.ValidationError(
                '아이디와 비밀번호를 모두 입력해주세요.'
            )
        
        user = authenticate(
            request=self.context.get('request'),
            username=user_name,
            password=password
        )
        
        if not user:
            raise serializers.ValidationError(
                '아이디 또는 비밀번호가 올바르지 않습니다.'
            )
        
        refresh = self.get_token(user)
        
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        
        return data
