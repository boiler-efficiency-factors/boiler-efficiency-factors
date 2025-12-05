from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    """Custom User Manager"""
    
    def create_user(self, user_name, password=None, **extra_fields):
        if not user_name:
            raise ValueError('User name is required')
        
        user = self.model(user_name=user_name, username=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, user_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(user_name, password, **extra_fields)


class User(AbstractUser):
    """사용자 모델"""
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=150, unique=True)
    
    # AbstractUser의 username 필드를 user_name으로 매핑
    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    # related_name 충돌 해결
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user',
    )

    class Meta:
        db_table = 'auth'
    
    def __str__(self):
        return self.user_name