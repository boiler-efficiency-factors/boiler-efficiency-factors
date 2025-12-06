from django.utils import timezone
from .base_trainer import BaseTrainer
from ..models import SessionStateChoices
from .utils.data_loader import data_loader
from .utils.preprocessor import preprocessor

import pandas as pd
import numpy as np
import base64
import io
import matplotlib.pyplot as plt

# 💡 실제 XGBoost 라이브러리 import (import xgboost as xgb)
from xgboost import XGBRegressor

from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split

class xgboostTrainer(BaseTrainer):
    """
    XGBoost 모델 학습을 담당합니다.
    """
    
    def run_training(self):
        """XGBoost 학습을 수행하고 Session 객체에 결과 및 완료 상태를 저장합니다."""
        
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
            
            # 🌟 실제 XGBoost 모델 학습 실행 코드
            xgb_model = XGBRegressor(
                **params,
                random_state=42
            )
            xgb_model.fit(X_train, y_train)
            
            # 결과 계산
            metrics = self._calculate_metrics(xgb_model, X_test, y_test)
            feature_importance = self._generate_feature_importance(xgb_model, X_train)
            
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

    def _calculate_metrics(self, model, X_test, y_test):

        y_pred = model.predict(X_test)

        y_test_arr = np.array(y_test)
        y_pred_arr = np.array(y_pred)

        # MSE
        mse = mean_squared_error(y_test_arr, y_pred_arr)
        
        # RMSE
        rmse = np.sqrt(mse)

        # MAE
        mae = mean_absolute_error(y_test_arr, y_pred_arr)

        # MAPE
        non_zero_mask = y_test_arr != 0
        if np.any(non_zero_mask):
            mape = float(
                np.mean(
                    np.abs(
                        (y_test_arr[non_zero_mask] - y_pred_arr[non_zero_mask])
                        / y_test_arr[non_zero_mask]
                    )
                ) * 100.0
            )
        else:
            mape = None
    
        return {
            "mse": float(mse),
            "rmse": float(rmse),
            "mae": float(mae),
            "mape": float(mape) if mape is not None else None,
        }

    def _generate_feature_importance(self, model, X_train):

        importance = model.feature_importances_

        if hasattr(X_train, "columns"):
            feature_names = list(X_train.columns)
        else:
            feature_names = [f"f{i}" for i in range(len(importance))]
        
        importance_df = pd.DataFrame({
            "feature": feature_names,
            "importance": importance
        })
        importance_df = importance_df.sort_values(by="importance", ascending=False)
        
        # 중요도 상위 10개 feature
        top_n = 10
        top_features = importance_df.head(top_n).iloc[::-1]

        # 시각화
        plt.figure(figsize=(12, 6))
        plt.barh(top_features["feature"], top_features["importance"])
        plt.xlabel("Importance", fontsize=12)
        plt.ylabel("Feature", fontsize=12)
        plt.title(f"Top {top_n} Important Features", fontsize=14)
        plt.tight_layout()

        # 이미지 버퍼에 저장 → base64 문자열로 변환
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        plt.close()
        buffer.seek(0)

        img_base64 = base64.b64encode(buffer.read()).decode("utf-8")
        return img_base64 # base64_xgboost_string 