from rest_framework import serializers
from .models import Model, MLModelChoices, Session

class XGBoostParamSerializer(serializers.Serializer):
    max_depth = serializers.IntegerField(
        required=False, 
        min_value=1, 
        default=6, 
        help_text="트리의 최대 깊이"
    )
    
    n_estimators = serializers.IntegerField(
        required=False, 
        min_value=1, 
        default=100,
        help_text="생성할 트리의 개수"
    )

    min_child_weight = serializers.FloatField(
        required=False, 
        min_value=0, 
        default=1, 
        help_text="관측치에 대한 가중치 합의 최솟값"
    )
    
    gamma = serializers.FloatField(
        required=False, 
        min_value=0, 
        default=0, 
        help_text="리프 노드를 추가적으로 나눌 때 필요한 최소 손실 감소값"
    )
    
    learning_rate = serializers.FloatField(
        required=False, 
        min_value=0.000001, 
        max_value=1.0, 
        default=0.3, 
        help_text="학습률"
    )
    
    max_delta_step = serializers.FloatField(
        required=False, 
        min_value=0, 
        default=0, 
        help_text="각 트리의 가중치 추정을 위한 제약"
    )
    
    reg_lambda = serializers.FloatField(
        required=False, 
        min_value=0, 
        default=1, 
        help_text="L2 정규화 가중치"
    )
    
    reg_alpha = serializers.FloatField(
        required=False, 
        min_value=0, 
        default=0, 
        help_text="L1 정규화 가중치"
    )
    
    subsample = serializers.FloatField(
        required=False, 
        min_value=0.000001, 
        max_value=1.0, 
        default=1, 
        help_text="데이터 샘플링 비율"
    )
    
    colsample_bytree = serializers.FloatField(
        required=False, 
        min_value=0.000001, 
        max_value=1.0, 
        default=1, 
        help_text="각 트리 구성 시 컬럼 샘플링 비율"
    )


class LightGBMParamSerializer(serializers.Serializer):
    num_leaves = serializers.IntegerField(
        required=False, 
        min_value=2, 
        default=31, 
        help_text="전체 트리의 최대 리프 노드 수"
    )

    max_depth = serializers.IntegerField(
        required=False, 
        min_value=-1, 
        default=-1, 
        help_text="트리의 최대 깊이, -1은 제한 없음을 의미"
    )

    n_estimators = serializers.IntegerField(
        required=False, 
        min_value=1, 
        default=100, 
        help_text="반복 수행하려는 트리의 개수"
    )

    min_child_samples = serializers.IntegerField(
        required=False, 
        min_value=0, 
        default=20, 
        help_text="리프 노드가 되기 위한 최소 데이터 수, 과적합 방지"
    )

    learning_rate = serializers.FloatField(
        required=False, 
        min_value=0.000001, 
        default=0.1, 
        help_text="학습률"
    )

    min_split_gain = serializers.FloatField(
        required=False, 
        min_value=0, 
        default=0, 
        help_text="트리 분기를 위해 필요한 최소 손실 감소값"
    )

    reg_lambda = serializers.FloatField(
        required=False, 
        min_value=0, 
        default=0, 
        help_text="L2 정규화 가중치"
    )

    reg_alpha = serializers.FloatField(
        required=False, 
        min_value=0, 
        default=0, 
        help_text="L1 정규화 가중치"
    )

    subsample = serializers.FloatField(
        required=False, 
        min_value=0.000001,
        max_value=1.0, 
        default=1.0, 
        help_text="데이터 샘플링 비율"
    )

    colsample_bytree = serializers.FloatField(
        required=False, 
        min_value=0.000001, 
        max_value=1.0, 
        default=1.0, 
        help_text="각 트리 구성 시 컬럼(피처) 샘플링 비율"
    )

class RandomForestParamSerializer(serializers.Serializer):
    n_estimators = serializers.IntegerField(
        required=False,
        min_value=1,
        default=100,
        help_text="생성할 트리의 개수"
    )

    max_depth = serializers.IntegerField(
        required=False,
        min_value=1,
        allow_null=True,
        default=None,
        help_text="트리의 최대 깊이"
    )

    min_samples_split = serializers.IntegerField(
        required=False,
        min_value=2,
        default=2,
        help_text="노드를 분할하기 위해 필요한 최소 샘플 수"
    )

    min_samples_leaf = serializers.IntegerField(
        required=False,
        min_value=1,
        default=1,
        help_text="리프 노드에 있어야 하는 최소 샘플 수"
    )

    criterion = serializers.ChoiceField(
        choices=[
            ('squared_error', 'Squared Error (MSE)'),
            ('absolute_error', 'Absolute Error (MAE)'),
            ('friedman_mse', 'Friedman MSE'),
            ('poisson', 'Poisson')
        ],
        required=False,
        default='squared_error',
        help_text="분할 품질을 측정하는 기능"
    )

    max_features = serializers.ChoiceField(
        choices=[
            ('sqrt', 'Square Root'),
            ('log2', 'Log2'),
            (1.0, 'All Features (None)')
        ],
        required=False,
        default=1.0,
        help_text="각 분할에서 고려할 최대 피처 수"
    )

    bootstrap = serializers.BooleanField(
        required=False,
        default=True,
        help_text="트리 생성 시 부트스트랩 샘플링 사용 여부"
    )

class GBMParamSerializer(serializers.ModelSerializer):
    n_estimators = serializers.IntegerField(
        required=False,
        min_value=1,
        default=100,
        help_text="부스팅 단계를 수행할 횟수 (기본값: 100)"
    )

    max_depth = serializers.IntegerField(
        required=False,
        min_value=1,
        default=3,
        help_text="개별 회귀 트리의 최대 깊이 (기본값: 3)"
    )

    min_samples_split = serializers.IntegerField(
        required=False,
        min_value=2,
        default=2,
        help_text="노드를 분할하기 위해 필요한 최소 샘플 수 (기본값: 2)"
    )

    min_samples_leaf = serializers.IntegerField(
        required=False,
        min_value=1,
        default=1,
        help_text="리프 노드에 있어야 하는 최소 샘플 수 (기본값: 1)"
    )

    learning_rate = serializers.FloatField(
        required=False,
        min_value=0.000001,
        default=0.1,
        help_text="각 트리의 기여도를 줄이는 학습률 (기본값: 0.1)"
    )

    subsample = serializers.FloatField(
        required=False,
        min_value=0.000001,
        max_value=1.0,
        default=1.0,
        help_text="트리 학습에 사용할 데이터 샘플링 비율 (기본값: 1.0)"
    )

    alpha = serializers.FloatField(
        required=False,
        min_value=0.000001,
        max_value=0.999999,
        default=0.9,
        help_text="Huber/Quantile 손실 함수 사용 시 필요한 알파 값 (기본값: 0.9)"
    )

    loss = serializers.ChoiceField(
        choices=[
            ('squared_error', 'Squared Error (LS)'),
            ('absolute_error', 'Absolute Error (LAD)'),
            ('huber', 'Huber Loss'),
            ('quantile', 'Quantile Loss'),
        ],
        required=False,
        default='squared_error',
        help_text="최적화할 손실 함수 (기본값: squared_error)"
    )

class WorkspaceCreateSerializer(serializers.ModelSerializer):
    excluded_var = serializers.ListField(
        child=serializers.CharField(max_length=200),
        required=False,
        allow_empty=True
    )
    parameter = serializers.JSONField(
        required=False,
        help_text='AI 모델의 학습 파라미터 (예: {"n_estimators": 500, "learning_rate": 0.05})'
    )
    PARAM_SERIALIZERS = {
        'lightgbm': LightGBMParamSerializer,
        'xgboost': XGBoostParamSerializer,
        'random_forest': RandomForestParamSerializer,
        'gradient_boosting': GBMParamSerializer,
    }
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
    
    def validate(self, data):
        """전체 데이터 유효성 검사"""
        model_name = data.get('model_name')
        raw_params = data.get('parameter') or {}

        param_serializer_cls = self.PARAM_SERIALIZERS.get(model_name)

        if param_serializer_cls:
            serializer = param_serializer_cls(data=raw_params)

            if not serializer.is_valid():
                raise serializers.ValidationError({
                    "parameter": serializer.errors
                })
            
            data['parameter'] = serializer.validated_data
        else:
            raise serializers.ValidationError({
                "model_name": f"지원하지 않는 모델입니다. ({model_name})"
            })
        
        return data


class WorkspaceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = [
            'model_id',
            'workspace', 
            'model_name', 
            'start_date', 
            'end_date',
            'parameter', 
            'tuning',
            'dependent_var', 
            'excluded_var',
            'created_at'
        ]

class SessionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        # 피쳐 중요도(feature)와 성능지표, 상태를 프론트엔드로 보냅니다.
        fields = ['session_id', 'model_id', 'feature', 'metrics', "top_features", 'state']

class WorkspacePaginationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = '__all__'