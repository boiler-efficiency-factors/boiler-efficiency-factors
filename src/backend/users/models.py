from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """사용자 모델"""
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=150, unique=True)
    
    # AbstractUser의 username 필드를 user_name으로 매핑
    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'auth'
    
    def __str__(self):
        return self.user_name