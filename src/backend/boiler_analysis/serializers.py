from rest_framework import serializers
from .models import AnalysisProject, DataFile, ModelConfiguration, AnalysisResult


class DataFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataFile
        fields = ['id', 'original_filename', 'file_size', 'uploaded_at', 'is_processed']
        read_only_fields = ['id', 'uploaded_at', 'is_processed']


class ModelConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelConfiguration
        fields = ['id', 'model_type', 'parameters', 'is_trained', 'created_at']
        read_only_fields = ['id', 'is_trained', 'created_at']


class AnalysisResultSerializer(serializers.ModelSerializer):
    model_config = ModelConfigurationSerializer(read_only=True)
    
    class Meta:
        model = AnalysisResult
        fields = ['id', 'model_config', 'feature_importance', 'performance_metrics', 'predictions', 'created_at']
        read_only_fields = ['id', 'created_at']


class AnalysisProjectSerializer(serializers.ModelSerializer):
    data_files = DataFileSerializer(many=True, read_only=True)
    model_configs = ModelConfigurationSerializer(many=True, read_only=True)
    
    class Meta:
        model = AnalysisProject
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'data_files', 'model_configs']
        read_only_fields = ['id', 'created_at', 'updated_at']


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    
    def validate_file(self, value):
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("CSV 파일만 업로드 가능합니다.")
        return value