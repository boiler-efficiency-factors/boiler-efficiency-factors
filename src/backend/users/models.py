from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """사용자 모델"""
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=150, unique=True)
    
    # AbstractUser의 username 필드를 user_name으로 매핑
    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = []

    # 1. groups 필드의 related_name 수정
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        related_name='custom_user_groups', 
        related_query_name='custom_user',
    )

    # 2. user_permissions 필드의 related_name 수정
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_permissions',
        related_query_name='custom_permission',
    )

    class Meta:
        db_table = 'user'
    
    def __str__(self):
        return self.user_name