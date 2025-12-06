from rest_framework import serializers
from .models import Model, MLModelChoices

class WorkspaceCreateSerializer(serializers.ModelSerializer):
    excluded_var = serializers.ListField(
        child=serializers.CharField(max_length=200),
        required=False,
        allow_empty=True
    )
    parameter = serializers.JSONField(
        required=False,
        # help_text를 추가하여 문서화에 도움을 줍니다.
        help_text='AI 모델의 학습 파라미터 (예: {"n_estimators": 500, "learning_rate": 0.05})'
    )
    class Meta:
        model = Model
        fields = ['workspace', 'model_name', 'start_date', 'end_date',
                  'parameter', 'tuning', 'dependent_var', 'excluded_var']
        
        extra_kwargs = {
            'workspace': {'required': True, 'allow_blank': False},
            'model_name': {'required': True},
            'start_date': {'required': True},
            'end_date': {'required': True},
            'tuning': {'required': False},
            'dependent_var': {'required': True},
            'parameter': {'required': False},
            'excluded_var': {'required': False}
        }