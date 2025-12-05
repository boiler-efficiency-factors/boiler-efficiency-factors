from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .serizalizer import UserSerializer
from .serializers_jwt import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    POST /api/auth/login
    user_name과 password로 로그인
    """
    serializer_class = CustomTokenObtainPairSerializer


class UserRegisterView(APIView):
    """
    POST /api/auth/register
    신규 사용자 회원가입 처리
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            # 중복 체크
            user_name = serializer.validated_data.get('user_name')
            if User.objects.filter(user_name=user_name).exists():
                return Response(
                    {"error": "이미 존재하는 사용자 이름입니다."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 사용자 생성
            serializer.save()
            return Response(
                {"message": "회원가입이 완료되었습니다."},
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """
    GET /api/auth/profile
    현재 로그인한 사용자 정보 조회 (테스트용)
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        return Response({
            "user_id": user.user_id,
            "user_name": user.user_name,
            "message": f"안녕하세요, {user.user_name}님!"
        })