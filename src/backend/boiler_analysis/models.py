from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Max
import uuid

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


class UserSequence(models.Model):
    """유저 모델 시퀀스"""
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, db_column='user_id')
    model_id = models.ForeignKey('Model', on_delete=models.CASCADE, db_column='model_id')
    user_sequence_id = models.IntegerField(db_column='user_sequence_id', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_seq'
        unique_together = (('user_id', 'user_sequence_id'),)

    def save(self, *args, **kwargs):
        if not self.pk:
            max_seq_result = UserSequence.objects.filter(user_id=self.user_id).aggregate(
                Max('user_sequence_id')
            )
            max_seq = max_seq_result['user_sequence_id__max']

            self.user_sequence_id = (max_seq or 0) + 1
        
        super().save(*args, **kwargs)
    
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
    workspace = models.CharField(max_length=255)
    model_name = models.CharField(max_length=100, choices=MODEL_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    parameter = models.JSONField(null=True, blank=True)
    tuning = models.CharField(max_length=50)  # 'random', 'grid', 'bayesian' 등
    independent_var = models.CharField(max_length=500)  # 독립변수 목록
    dependent_var = models.TextField()  # 종속변수 목록
    excluded_var = models.TextField(null=True, blank=True)  # 제외할 변수
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'model'
    
    def __str__(self):
        return f"{self.model_name} ({self.start_date} ~ {self.end_date})"


class Session(models.Model):
    """세션 정보"""
    session_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    model_id = models.ForeignKey(Model, on_delete=models.CASCADE, db_column='model_id')
    metrics = models.JSONField(null=True, blank=True)  # train/test 성능 지표
    feature = models.TextField(null=True, blank=True)  # base64 인코딩된 특성 중요도 그래프
    state = models.CharField(max_length=50)  # 'training', 'completed', 'failed' 등
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'session'
    
    def __str__(self):
        return f"Session {self.session_id} - {self.state}"