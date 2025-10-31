import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
# ML 라이브러리들을 조건부로 import
try:
    import lightgbm as lgb
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False

try:
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    import joblib
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
import os
import sys
from django.conf import settings

# 백엔드 내부 전처리 모듈 사용
try:
    from .preprocessor import preprocessor
    PREPROCESSOR_AVAILABLE = True
except ImportError:
    PREPROCESSOR_AVAILABLE = False


class DataProcessingService:
    """데이터 전처리 서비스"""
    
    def process_csv(self, data_file):
        """CSV 파일 전처리 - 기존 AI utils 전처리 코드 사용"""
        try:
            # CSV 파일 읽기
            df = pd.read_csv(data_file.file.path, encoding='utf-8')
        except UnicodeDecodeError:
            # EUC-KR 인코딩으로 재시도
            df = pd.read_csv(data_file.file.path, encoding='euc-kr')
        
        # 백엔드 전처리 함수 사용
        try:
            if PREPROCESSOR_AVAILABLE:
                df_processed = preprocessor(df)
            else:
                # fallback: 기본 전처리
                df_processed = self._clean_data(df)
        except Exception as e:
            print(f"전처리 실패, 기본 전처리 사용: {e}")
            df_processed = self._clean_data(df)
        
        # 전처리된 파일 저장
        processed_path = self._get_processed_file_path(data_file)
        df_processed.to_csv(processed_path, index=False)
        
        return processed_path
    
    def _clean_data(self, df):
        """기본 데이터 정리 (fallback 함수)"""
        print("기본 전처리 함수 사용")
        
        # 불필요한 컬럼 제거 (기존 AI utils와 동일)
        columns_to_drop = [
            '생성일', '소비전류', '진동센서1', '진동센서2', '운전시간', '정상 운전 확률', '송풍기 고장 확률',
            'AIR 댐퍼 고장 확률', 'GAS 앰퍼 고장 확률', '확률 업데이트 시간', '순간 스팀량', '입출력법 효율',
            '열 손실법 효율', '효율(입출력법-스팀)'
        ]
        
        # 존재하는 컬럼만 제거
        existing_columns_to_drop = [col for col in columns_to_drop if col in df.columns]
        if existing_columns_to_drop:
            df = df.drop(columns=existing_columns_to_drop)
            print(f"불필요한 컬럼 {len(existing_columns_to_drop)}개 제거")
        
        # 결측값 처리
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())
        
        # 범주형 데이터 처리
        categorical_columns = df.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else 'Unknown')
            # 레이블 인코딩
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
        
        # 이상치 제거 (IQR 방법) - 수치형 컬럼에만 적용
        for col in numeric_columns:
            if df[col].nunique() > 10:  # 연속형 변수에만 적용
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                if IQR > 0:  # IQR이 0이 아닌 경우만
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
        
        return df
    
    def _get_processed_file_path(self, data_file):
        """전처리된 파일 경로 생성"""
        base_path = os.path.dirname(data_file.file.path)
        filename = f"processed_{data_file.id}.csv"
        return os.path.join(base_path, filename)


class ModelTrainingService:
    """모델 훈련 서비스"""
    
    def __init__(self):
        self.models = {
            'lightgbm': self._train_lightgbm,
            'xgboost': self._train_xgboost,
            'random_forest': self._train_random_forest,
            'gradient_boosting': self._train_gradient_boosting
        }
    
    def train_model(self, model_config):
        """모델 훈련 실행"""
        # 데이터 로드
        data_file = model_config.project.data_files.filter(is_processed=True).first()
        if not data_file:
            raise ValueError("처리된 데이터 파일이 없습니다.")
        
        df = pd.read_csv(data_file.file.path)
        
        # 특성과 타겟 분리 (효율을 타겟으로 가정)
        target_column = self._identify_target_column(df)
        X = df.drop(columns=[target_column])
        y = df[target_column]
        
        # 범주형 변수 인코딩
        X = self._encode_categorical_features(X)
        
        # 데이터 분할
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # 모델 훈련
        model_trainer = self.models[model_config.model_type]
        model, feature_importance = model_trainer(X_train, y_train, model_config.parameters)
        
        # 예측 및 평가
        y_pred = model.predict(X_test)
        metrics = self._calculate_metrics(y_test, y_pred)
        
        # 모델 저장
        model_path = self._save_model(model, model_config)
        
        return {
            'feature_importance': dict(zip(X.columns, feature_importance)),
            'performance_metrics': metrics,
            'model_path': model_path,
            'predictions': {
                'actual': y_test.tolist(),
                'predicted': y_pred.tolist()
            }
        }
    
    def _identify_target_column(self, df):
        """타겟 컬럼 식별 (효율 관련 컬럼 찾기)"""
        # 기존 AI 데이터에서 사용하는 효율 컬럼명들
        efficiency_keywords = ['효율(순간)', '효율', 'efficiency', '열효율', 'thermal_efficiency']
        
        for col in df.columns:
            for keyword in efficiency_keywords:
                if keyword.lower() in col.lower():
                    print(f"타겟 컬럼으로 '{col}' 선택")
                    return col
        
        # 키워드가 없으면 마지막 컬럼을 타겟으로 가정
        print(f"효율 관련 컬럼을 찾지 못해 '{df.columns[-1]}'을 타겟으로 사용")
        return df.columns[-1]
    
    def _encode_categorical_features(self, X):
        """범주형 특성 인코딩"""
        categorical_columns = X.select_dtypes(include=['object']).columns
        
        for col in categorical_columns:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
        
        return X
    
    def _train_lightgbm(self, X_train, y_train, parameters):
        """LightGBM 모델 훈련"""
        if not LIGHTGBM_AVAILABLE:
            raise ValueError("LightGBM이 설치되지 않았습니다.")
            
        default_params = {
            'objective': 'regression',
            'metric': 'rmse',
            'boosting_type': 'gbdt',
            'num_leaves': 31,
            'learning_rate': 0.05,
            'feature_fraction': 0.9
        }
        default_params.update(parameters)
        
        train_data = lgb.Dataset(X_train, label=y_train)
        model = lgb.train(default_params, train_data, num_boost_round=100)
        
        feature_importance = model.feature_importance(importance_type='gain')
        return model, feature_importance
    
    def _train_xgboost(self, X_train, y_train, parameters):
        """XGBoost 모델 훈련"""
        if not XGBOOST_AVAILABLE:
            raise ValueError("XGBoost가 설치되지 않았습니다.")
            
        default_params = {
            'objective': 'reg:squarederror',
            'max_depth': 6,
            'learning_rate': 0.1,
            'n_estimators': 100
        }
        default_params.update(parameters)
        
        model = xgb.XGBRegressor(**default_params)
        model.fit(X_train, y_train)
        
        feature_importance = model.feature_importances_
        return model, feature_importance
    
    def _train_random_forest(self, X_train, y_train, parameters):
        """Random Forest 모델 훈련"""
        if not SKLEARN_AVAILABLE:
            raise ValueError("scikit-learn이 설치되지 않았습니다.")
            
        default_params = {
            'n_estimators': 100,
            'max_depth': None,
            'random_state': 42
        }
        default_params.update(parameters)
        
        model = RandomForestRegressor(**default_params)
        model.fit(X_train, y_train)
        
        feature_importance = model.feature_importances_
        return model, feature_importance
    
    def _train_gradient_boosting(self, X_train, y_train, parameters):
        """Gradient Boosting Machine 모델 훈련"""
        if not SKLEARN_AVAILABLE:
            raise ValueError("scikit-learn이 설치되지 않았습니다.")
            
        default_params = {
            'n_estimators': 100,
            'learning_rate': 0.1,
            'max_depth': 3,
            'random_state': 42,
            'subsample': 0.8,
            'max_features': 'sqrt'
        }
        default_params.update(parameters)
        
        model = GradientBoostingRegressor(**default_params)
        model.fit(X_train, y_train)
        
        feature_importance = model.feature_importances_
        return model, feature_importance
    
    def _calculate_metrics(self, y_true, y_pred):
        """성능 지표 계산"""
        return {
            'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
            'mae': mean_absolute_error(y_true, y_pred),
            'r2_score': r2_score(y_true, y_pred),
            'mape': np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        }
    
    def _save_model(self, model, model_config):
        """모델 저장"""
        if not SKLEARN_AVAILABLE:
            raise ValueError("joblib이 설치되지 않았습니다.")
            
        models_dir = os.path.join(settings.MEDIA_ROOT, 'models')
        os.makedirs(models_dir, exist_ok=True)
        
        model_filename = f"model_{model_config.id}.pkl"
        model_path = os.path.join(models_dir, model_filename)
        
        joblib.dump(model, model_path)
        return model_path


class PredictionService:
    """예측 서비스"""
    
    def predict(self, model_config, input_data):
        """새로운 데이터에 대한 예측"""
        model_path = os.path.join(settings.MEDIA_ROOT, 'models', f"model_{model_config.id}.pkl")
        
        if not os.path.exists(model_path):
            raise ValueError("훈련된 모델이 없습니다.")
        
        if not SKLEARN_AVAILABLE:
            raise ValueError("joblib이 설치되지 않았습니다.")
            
        model = joblib.load(model_path)
        predictions = model.predict(input_data)
        
        return predictions.tolist()