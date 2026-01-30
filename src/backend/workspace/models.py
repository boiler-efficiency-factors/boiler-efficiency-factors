from django.db import models
from django.db.models import Max, TextChoices
import uuid
from django.conf import settings

class MLModelChoices(TextChoices):
    LIGHTGBM = 'lightgbm'
    XGBOOST = 'xgboost'
    RANDOM_FOREST = 'random_forest'
    GRADIENT_BOOSTING = 'gradient_boosting'


class SessionStateChoices(TextChoices):
    CREATED = 'created'
    TRAINING = 'training'
    COMPLETED = 'completed'
    FAILED = 'failed'


class Model(models.Model):
    model_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    workspace = models.CharField(max_length=255)
    model_name = models.CharField(max_length=50,choices=MLModelChoices.choices)
    start_date = models.DateField()
    end_date = models.DateField()
    parameter = models.JSONField(null=True, blank=True)
    tuning = models.CharField(max_length=50)  # 'random', 'grid', 'bayesian' 등
    dependent_var = models.TextField()  # 종속변수 목록
    excluded_var = models.JSONField(default=list, null=True, blank=True)  # 제외할 변수
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'model'
    
    def __str__(self):
        return f"{self.model_name} ({self.start_date} ~ {self.end_date})"
    

class UserSequence(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='user_id')
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
    

class Session(models.Model):
    session_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    model_id = models.ForeignKey(Model, on_delete=models.CASCADE, db_column='model_id')
    metrics = models.JSONField(null=True, blank=True)
    feature = models.TextField(null=True, blank=True)
    state = models.CharField(max_length=50, choices=SessionStateChoices.choices)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'session'
    
    def __str__(self):
        return f"Session {self.session_id} - {self.state}"
    

class BoilerOperationLog(models.Model):
    """보일러 실시간/일별 운전 데이터 저장"""
    log_date = models.DateField(unique=True) # 요약 데이터라면 날짜별 유니크
    avg_pressure = models.FloatField(verbose_name="평균 압력")
    avg_temp = models.FloatField(verbose_name="배기가스 온도")
    water_usage = models.FloatField(verbose_name="급수 사용량")
    gas_usage = models.FloatField(verbose_name="가스 사용량")
    efficiency = models.FloatField(verbose_name="평균 효율")
    
    class Meta:
        db_table = 'boiler_operation_log'

class MaintenanceHistory(models.Model):
    """최근 A/S 및 세관 정비 이력 관리"""
    maintenance_date = models.DateField()
    content = models.TextField(verbose_name="정비 내용")
    m_type = models.CharField(max_length=50, choices=[('AS', 'A/S'), ('CLEAN', '세관정비')])
    
    class Meta:
        db_table = 'maintenance_history'