from django.db import models
from django.contrib.auth.models import User
import uuid


class AnalysisProject(models.Model):
    """분석 프로젝트 모델"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class DataFile(models.Model):
    """업로드된 CSV 파일 모델"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(AnalysisProject, on_delete=models.CASCADE, related_name='data_files')
    file = models.FileField(upload_to='uploads/csv/')
    original_filename = models.CharField(max_length=255)
    file_size = models.BigIntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.original_filename


class ModelConfiguration(models.Model):
    """AI 모델 설정"""
    MODEL_CHOICES = [
        ('lightgbm', 'LightGBM'),
        ('xgboost', 'XGBoost'),
        ('random_forest', 'Random Forest'),
        ('gradient_boosting', 'Gradient Boosting Machine'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(AnalysisProject, on_delete=models.CASCADE, related_name='model_configs')
    model_type = models.CharField(max_length=50, choices=MODEL_CHOICES)
    parameters = models.JSONField(default=dict)
    is_trained = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.project.name} - {self.get_model_type_display()}"


class AnalysisResult(models.Model):
    """분석 결과 저장"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    model_config = models.ForeignKey(ModelConfiguration, on_delete=models.CASCADE, related_name='results')
    feature_importance = models.JSONField()
    performance_metrics = models.JSONField()
    predictions = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Result for {self.model_config}"