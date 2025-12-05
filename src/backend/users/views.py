from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView # JWT 로그인
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer # 토큰 생성
from .serializers import UserRegisterSerializer

class LoginTokenView(TokenObtainPairView):
    """
    POST /api/auth/login
    사용자 로그인 처리 Simple JWT의 표준 뷰 상속
    """
    permission_classes = [AllowAny]
    serializer_class = TokenObtainPairSerializer

class UserRegisterView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        request=UserRegisterSerializer,
        responses={
            status.HTTP_201_CREATED: {
                "type": "object",
                "properties": {
                    "user_name": {"type": "string"},
                    "message": {"type": "string"}
                }
            },
            status.HTTP_400_BAD_REQUEST: UserRegisterSerializer,
        }
    )
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            
            # 🌟 응답에서 user_id 제거
            return Response({
                "user_name": user.user_name,
                "message": "회원가입 성공. 로그인 페이지로 이동하세요."
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)