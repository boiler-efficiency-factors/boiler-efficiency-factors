from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenBlacklistView
from .views import LoginTokenView, UserRegisterView

urlpatterns = [
    # 로그인 (토큰 발급)
    # URL: POST /api/auth/login/
    path('auth/login/', LoginTokenView.as_view(), name='auth-login'),

    # 토큰 갱신
    # URL: POST /api/auth/refresh/
    path('auth/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # 로그아웃
    # URL: POST /api/auth/logout
    path('auth/logout/', TokenBlacklistView.as_view(), name='auth-logout'),
    
    # 회원가입
    # URL: POST /api/user/register/
    path('user/register/', UserRegisterView.as_view(), name='user-register'),
]