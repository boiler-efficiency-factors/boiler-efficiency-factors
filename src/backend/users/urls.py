from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from .views import UserRegisterView, CustomTokenObtainPairView, UserProfileView

urlpatterns = [
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', UserRegisterView.as_view(), name='user_register'),
    path('auth/profile/', UserProfileView.as_view(), name='user_profile'),
]
