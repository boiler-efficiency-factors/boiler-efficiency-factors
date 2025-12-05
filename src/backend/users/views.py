from django.shortcuts import render
from django.contrib.auth.models import User
from .models import User

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view[('')]
# Auth Endpoints
class LoginView(APIView):
    """
    POST /api/auth/login
    사용자 로그인 처리
    """
    def post(self, request):
        # TODO: 1. 시리얼라이저를 사용하여 사용자 입력(user_name, password) 검증
        # TODO: 2. Django의 authenticate를 사용하여 사용자 인증
        # TODO: 3. 인증 성공 시, 세션이나 토큰(JWT 등) 생성 및 반환
        return Response({"message": "로그인 성공"}, status=status.HTTP_200_OK)


# User Endpoints
class UserRegisterView(APIView):
    """
    POST /api/user/register
    신규 사용자 회원가입 처리
    """
    def post(self, request):
        # TODO: 1. User 시리얼라이저를 사용하여 사용자 입력 검증 및 유효성 확인
        # TODO: 2. 비밀번호 해싱 및 User 모델 객체 생성 후 저장
        # TODO: 3. 성공 응답 반환
        return Response({"message": "회원가입 성공"}, status=status.HTTP_201_CREATED)