# from rest_framework import serializers
# from .models import User, UserSequence, Model, Session


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['user_id', 'user_name', 'user_password']
#         extra_kwargs = {'user_password': {'write_only': True}}
    
#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data['user_name'],
#             password=validated_data['user_password']
#         )
#         return user


# class ModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Model
#         fields = [
#             'model_id', 'model_name', 'start_date', 'end_date',
#             'parameter', 'tuning', 'independent_var', 
#             'dependent_var', 'excluded_var'
#         ]
#         read_only_fields = ['model_id']
    
#     def validate_parameter(self, value):
#         """하이퍼파라미터 검증"""
#         if not value:
#             return value
        
#         model_name = self.initial_data.get('model_name')
        
#         if model_name == 'lightgbm':
#             return self._validate_lightgbm_params(value)
#         elif model_name == 'xgboost':
#             return self._validate_xgboost_params(value)
#         elif model_name == 'random_forest':
#             return self._validate_rf_params(value)
#         elif model_name == 'gradient_boosting':
#             return self._validate_gbm_params(value)
        
#         return value
    
#     def _validate_lightgbm_params(self, params):
#         """LightGBM 파라미터 검증"""
#         valid_params = {
#             'num_leaves': (int, lambda x: x >= 2),
#             'max_depth': (int, lambda x: x >= -1),
#             'learning_rate': (float, lambda x: 0 < x <= 1),
#             'n_estimators': (int, lambda x: x >= 1),
#             'min_child_samples': (int, lambda x: x >= 1),
#             'subsample': (float, lambda x: 0 < x <= 1),
#             'colsample_bytree': (float, lambda x: 0 < x <= 1),
#             'reg_alpha': (float, lambda x: x >= 0),
#             'reg_lambda': (float, lambda x: x >= 0),
#         }
        
#         for key, value in params.items():
#             if key in valid_params:
#                 expected_type, validator = valid_params[key]
#                 if not isinstance(value, expected_type):
#                     raise serializers.ValidationError(f"{key}는 {expected_type.__name__} 타입이어야 합니다.")
#                 if not validator(value):
#                     raise serializers.ValidationError(f"{key}의 값이 유효 범위를 벗어났습니다.")
        
#         return params
    
#     def _validate_xgboost_params(self, params):
#         """XGBoost 파라미터 검증"""
#         valid_params = {
#             'max_depth': (int, lambda x: x >= 1),
#             'min_child_weight': (float, lambda x: x >= 0),
#             'gamma': (float, lambda x: x >= 0),
#             'learning_rate': (float, lambda x: 0 < x <= 1),
#             'max_delta_step': (float, lambda x: x >= 0),
#             'reg_lambda': (float, lambda x: x >= 0),
#             'reg_alpha': (float, lambda x: x >= 0),
#             'subsample': (float, lambda x: 0 < x <= 1),
#             'colsample_bytree': (float, lambda x: 0 < x <= 1),
#             'n_estimators': (int, lambda x: x >= 1),
#         }
        
#         for key, value in params.items():
#             if key in valid_params:
#                 expected_type, validator = valid_params[key]
#                 if not isinstance(value, expected_type):
#                     raise serializers.ValidationError(f"{key}는 {expected_type.__name__} 타입이어야 합니다.")
#                 if not validator(value):
#                     raise serializers.ValidationError(f"{key}의 값이 유효 범위를 벗어났습니다.")
        
#         return params
    
#     def _validate_rf_params(self, params):
#         """Random Forest 파라미터 검증"""
#         # n_estimators
#         if 'n_estimators' in params:
#             if not isinstance(params['n_estimators'], int) or params['n_estimators'] < 1:
#                 raise serializers.ValidationError("n_estimators는 1 이상의 정수여야 합니다.")
        
#         # max_depth
#         if 'max_depth' in params:
#             md = params['max_depth']
#             if md is not None and (not isinstance(md, int) or md < 1):
#                 raise serializers.ValidationError("max_depth는 None 또는 1 이상의 정수여야 합니다.")
        
#         # min_samples_split
#         if 'min_samples_split' in params:
#             mss = params['min_samples_split']
#             if isinstance(mss, int):
#                 if mss < 2:
#                     raise serializers.ValidationError("min_samples_split(int)는 2 이상이어야 합니다.")
#             elif isinstance(mss, float):
#                 if not (0 < mss <= 1):
#                     raise serializers.ValidationError("min_samples_split(float)는 (0, 1] 범위여야 합니다.")
#             else:
#                 raise serializers.ValidationError("min_samples_split는 int 또는 float여야 합니다.")
        
#         # min_samples_leaf
#         if 'min_samples_leaf' in params:
#             msl = params['min_samples_leaf']
#             if isinstance(msl, int):
#                 if msl < 1:
#                     raise serializers.ValidationError("min_samples_leaf(int)는 1 이상이어야 합니다.")
#             elif isinstance(msl, float):
#                 if not (0 < msl <= 0.5):
#                     raise serializers.ValidationError("min_samples_leaf(float)는 (0, 0.5] 범위여야 합니다.")
#             else:
#                 raise serializers.ValidationError("min_samples_leaf는 int 또는 float여야 합니다.")
        
#         # max_features
#         if 'max_features' in params:
#             mf = params['max_features']
#             if not (isinstance(mf, (int, float)) or mf in ['sqrt', 'log2', None]):
#                 raise serializers.ValidationError("max_features는 int, float, 'sqrt', 'log2', None 중 하나여야 합니다.")
        
#         # min_impurity_decrease
#         if 'min_impurity_decrease' in params:
#             if not isinstance(params['min_impurity_decrease'], (int, float)) or params['min_impurity_decrease'] < 0:
#                 raise serializers.ValidationError("min_impurity_decrease는 0 이상이어야 합니다.")
        
#         return params
    
#     def _validate_gbm_params(self, params):
#         """Gradient Boosting Machine 파라미터 검증"""
#         # n_estimators
#         if 'n_estimators' in params:
#             if not isinstance(params['n_estimators'], int) or params['n_estimators'] < 1:
#                 raise serializers.ValidationError("n_estimators는 1 이상의 정수여야 합니다.")
        
#         # learning_rate
#         if 'learning_rate' in params:
#             lr = params['learning_rate']
#             if not isinstance(lr, (int, float)) or not (0 < lr <= 1):
#                 raise serializers.ValidationError("learning_rate는 (0, 1] 범위여야 합니다.")
        
#         # max_depth
#         if 'max_depth' in params:
#             if not isinstance(params['max_depth'], int) or params['max_depth'] < 1:
#                 raise serializers.ValidationError("max_depth는 1 이상의 정수여야 합니다.")
        
#         # min_samples_split
#         if 'min_samples_split' in params:
#             mss = params['min_samples_split']
#             if isinstance(mss, int):
#                 if mss < 2:
#                     raise serializers.ValidationError("min_samples_split(int)는 2 이상이어야 합니다.")
#             elif isinstance(mss, float):
#                 if not (0 < mss <= 1):
#                     raise serializers.ValidationError("min_samples_split(float)는 (0, 1] 범위여야 합니다.")
        
#         # min_samples_leaf
#         if 'min_samples_leaf' in params:
#             msl = params['min_samples_leaf']
#             if isinstance(msl, int):
#                 if msl < 1:
#                     raise serializers.ValidationError("min_samples_leaf(int)는 1 이상이어야 합니다.")
#             elif isinstance(msl, float):
#                 if not (0 < msl <= 0.5):
#                     raise serializers.ValidationError("min_samples_leaf(float)는 (0, 0.5] 범위여야 합니다.")
        
#         # subsample
#         if 'subsample' in params:
#             ss = params['subsample']
#             if not isinstance(ss, (int, float)) or not (0 < ss <= 1):
#                 raise serializers.ValidationError("subsample는 (0, 1] 범위여야 합니다.")
        
#         # max_features
#         if 'max_features' in params:
#             mf = params['max_features']
#             if not (isinstance(mf, (int, float)) or mf in ['sqrt', 'log2', None]):
#                 raise serializers.ValidationError("max_features는 int, float, 'sqrt', 'log2', None 중 하나여야 합니다.")
        
#         return params


# class SessionSerializer(serializers.ModelSerializer):
#     model = ModelSerializer(source='model_id', read_only=True)
    
#     class Meta:
#         model = Session
#         fields = ['session_id', 'model', 'metrics', 'feature', 'state']
#         read_only_fields = ['session_id']


# class UserSequenceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserSequence
#         fields = ['user_sequence_id', 'user_id', 'model_id', 'created_at']
#         read_only_fields = ['user_sequence_id', 'created_at']