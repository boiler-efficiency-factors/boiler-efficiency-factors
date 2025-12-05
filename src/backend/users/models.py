from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError

# === 커스텀 유저 매니저 정의 ===
class CustomUserManager(BaseUserManager):
    def create_user(self, user_name, password=None, **extra_fields):
        if not user_name:
            raise ValueError('The User Name must be set')

        user = self.model(user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        # 커스텀 create_user 메서드를 사용하여 슈퍼유저 생성
        return self.create_user(user_name, password, **extra_fields)

# === 사용자 모델 수정 ===
class User(AbstractUser):
    """사용자 모델"""
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=150, unique=True)
    
    # 기본 AbstractUser 필드들을 비활성화 (선택 사항)
    username = None 
    first_name = None
    last_name = None

    # 커스텀 필드를 USERNAME_FIELD로 지정
    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['email'] # 'email'을 REQUIRED_FIELDS에 추가하는 것이 일반적입니다.

    objects = CustomUserManager() 
    
    class Meta:
        db_table = 'user'
        
    def __str__(self):
        return self.user_name