from django.utils import timezone
from .base_trainer import BaseTrainer
from ..models import SessionStateChoices
from .utils.data_loader import data_loader
from .utils.preprocessor import preprocessor
from .utils.metrics import calculate_metrics
from .utils.feature_importance import generate_feature_importance


import pandas as pd
import numpy as np
import base64
import io
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split

class randomforestTrainer(BaseTrainer):
    """
    Random Forest 모델 학습을 담당합니다.
    """
    
    def run_training(self):
        """Random Forest 학습을 수행하고 Session 객체에 결과 및 완료 상태를 저장합니다."""
        
        try:
            # state: traning으로 변경
            self.session.state = SessionStateChoices.TRAINING
            self.session.save(update_fields=["state"])

            # 모델 정보
            start_date = self.model.start_date
            end_date = self.model.end_date
            params = self.model.parameter or {}

            # 데이터 로딩 및 전처리
            X_train, X_test, y_train, y_test = self._load_data(start_date, end_date)
            
            # 🌟 실제 Random Forest 모델 학습 실행 코드
            rf_model = RandomForestRegressor(
                **params,
                random_state=42,
                n_jobs=-1 # Use all CPU cores
            )
            rf_model.fit(X_train, y_train)
            
            # 결과 계산
            metrics = calculate_metrics(rf_model, X_test, y_test)
            feature_importance = generate_feature_importance(rf_model, X_train)
            
            self.session.metrics = metrics
            self.session.feature = feature_importance
            
            # 상태 변경 및 DB 저장
            self.session.state = SessionStateChoices.COMPLETED
            self.session.finished_at = timezone.now()
            self.session.save(
                update_fields=["metrics", "feature", "state", "finished_at"]
            )
            
        except Exception as e:
            # 예외 발생 시 Celery tasks.py에서 FAILED 상태로 처리됩니다.
            raise e

    # --- 도우미 메서드 (Helper Methods) ---
    def _load_data(self, start_date, end_date):
        """데이터 로드 및 전처리 후 학습/테스트 데이터셋 분리"""
        
        print(f"Loading data from {start_date} to {end_date}...")

        # 사용자가 입력한 기간의 데이터 로드
        df = data_loader.load_data(start_date, end_date)

        # object 타입 컬럼 문자열 변환
        object_cols = df.select_dtypes(include=['object']).columns
        
        for col in object_cols:
            df[col] = df[col].astype(str)
        
        # 전처리
        df = preprocessor.preprocessor(df)

        # 타겟 변수 선택
        y_col = self.model.dependent_var
        X = df.drop(columns=[y_col])
        y = df[y_col]

        # split data into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True)

        return X_train, X_test, y_train, y_test #Loaded Data Structure