from rest_framework import serializers
from .models import Model, MLModelChoices

class WorkspaceCreateSerializer(serializers.ModelSerializer):

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