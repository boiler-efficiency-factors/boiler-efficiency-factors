from django.utils import timezone
from ..models import SessionStateChoices
from .base_trainer import BaseTrainer
from lightgbm import LGBMRegressor
import lightgbm as lgb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from .utils.load import load
from .utils.preprocessor import preprocessor
from .utils.metrics import metrics
from .utils.feature import feature

class lightgbmTrainer(BaseTrainer):

    def run(self):
        """LightGBM 학습 & Session 객체에 결과 및 완료 상태를 저장"""
        try:
            start_date = self.model.start_date
            end_date = self.model.end_date
            params = self.model.parameter or {}

            # 데이터 로딩 및 전처리
            X_train, X_test, y_train, y_test = self._set(start_date, end_date)
            
            #TODO: 모델 학습 실행
            lgbm_model = LGBMRegressor(
                **params,
                random_state=42,
                n_jobs=-1,
                objective='regression',
                force_col_wise=True
            )
            lgbm_model.fit(
                X_train, y_train,
                eval_set=[(X_test, y_test)],
                eval_metric='rmse',
                callbacks=[
                    lgb.early_stopping(stopping_rounds=50), 
                    lgb.log_evaluation(period=100)
                ]
            )
            # 결과 계산
            test_metrics = metrics(lgbm_model, X_test, y_test)
            train_metrics = metrics(lgbm_model, X_train, y_train)

            metrics_result = {
                "test": test_metrics,
                "train": train_metrics
            }
            img_base64, top_features_df = feature(lgbm_model, X_train)
            
            self.session.metrics = metrics_result
            self.session.feature = img_base64
            self.session.top_features = top_features_df.to_dict(orient="records")
            
            self.session.state = SessionStateChoices.COMPLETED
            self.session.finished_at = timezone.now()
            self.session.save()
            
        except Exception as e:
            # 학습 중 오류 발생 시, Celery tasks.py에서 FAILED 상태로 처리
            raise e

    def _set(self, start_date, end_date):
        """데이터 로드 및 전처리 후 학습/테스트 데이터셋 분리"""
        
        print(f"Loading data from {start_date} to {end_date}...")

        df = load(start_date, end_date) # 데이터 로드
        df = preprocessor(df)           # 데이터 전처리

        # 타겟 변수 선택
        y_col = self.model.dependent_var
        X = df.drop(columns=[y_col])
        y = df[y_col]

        # split data into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True)

        return X_train, X_test, y_train, y_test #Loaded Data Structure