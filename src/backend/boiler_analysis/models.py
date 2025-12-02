from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    """사용자 모델"""
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=150, unique=True)
    user_password = models.CharField(max_length=128)
    
    # AbstractUser의 username 필드를 user_name으로 매핑
    USERNAME_FIELD = 'user_name'
    
    class Meta:
        db_table = 'auth'
    
    def __str__(self):
        return self.user_name


class UserSequence(models.Model):
    """유저 모델 시퀀스"""
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    model_id = models.UUIDField(default=uuid.uuid4)
    user_sequence_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_seq'
    
    def __str__(self):
        return f"{self.user_id} - Sequence {self.user_sequence_id}"


class Model(models.Model):
    """모델 정보"""
    MODEL_CHOICES = [
        ('lightgbm', 'LightGBM'),
        ('xgboost', 'XGBoost'),
        ('random_forest', 'Random Forest'),
        ('gradient_boosting', 'Gradient Boosting Machine'),
    ]
    
    model_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    model_name = models.CharField(max_length=100, choices=MODEL_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    parameter = models.JSONField(null=True, blank=True)
    tuning = models.CharField(max_length=50)  # 'random', 'grid', 'bayesian' 등
    independent_var = models.CharField(max_length=500)  # 독립변수 목록
    dependent_var = models.TextField(null=True, blank=True)  # 종속변수 목록
    excluded_var = models.TextField(null=True, blank=True)  # 제외할 변수
    
    class Meta:
        db_table = 'model'
    
    def __str__(self):
        return f"{self.model_name} ({self.start_date} ~ {self.end_date})"


class Session(models.Model):
    """세션 정보"""
    session_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    model_id = models.ForeignKey(Model, on_delete=models.CASCADE, db_column='model_id2')
    metrics = models.JSONField(null=True, blank=True)  # train/test 성능 지표
    feature = models.TextField(null=True, blank=True)  # base64 인코딩된 특성 중요도 그래프
    state = models.CharField(max_length=50)  # 'training', 'completed', 'failed' 등
    
    class Meta:
        db_table = 'session'
    
    def __str__(self):
        return f"Session {self.session_id} - {self.state}"