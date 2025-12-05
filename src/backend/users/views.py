from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny # 회원가입은 인증 불필요
from rest_framework_simplejwt.views import TokenObtainPairView # JWT 로그인
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer # 토큰 생성
from .serializers import UserRegisterSerializer

class LoginTokenView(TokenObtainPairView):
    """
    POST /api/auth/login
    사용자 로그인 처리 Simple JWT의 표준 뷰 상속
    """
    permission_classes = [AllowAny]

class UserRegisterView(APIView):

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            
            # 2. 토큰 생성 및 쿠키 설정 로직을 모두 제거!

            return Response({
                "user_id": user.user_id,
                "user_name": user.user_name,
                "message": "회원가입 성공. 로그인 페이지로 이동하세요."
            }, status=status.HTTP_201_CREATED) # 201 Created 반환
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)