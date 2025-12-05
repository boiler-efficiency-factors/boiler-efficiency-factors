from django.utils import timezone
from .base_trainer import BaseTrainer 
from ..models import SessionStateChoices
# import lightgbm as lgb

class lightgbmTrainer(BaseTrainer):
    """BaseTrainer의 __init__ 메서드(model, session 저장)를 자동으로 상속"""
    
    def run_training(self):
        """
        LightGBM 학습을 수행하고 Session 객체에 결과 및 완료 상태를 저장
        """
        
        try:
            # 1. 🌟 데이터 준비 및 파라미터 로드
            # self.model 객체를 통해 DB에 저장된 정보를 가져옵니다.
            start_date = self.model.start_date
            end_date = self.model.end_date
            params = self.model.parameter or {} # JSONField 파라미터 로드
            
            # 2. 🌟 실제 데이터 로딩 및 전처리 (구현 필요)
            data = self._load_data(start_date, end_date)
            
            # 3. 🌟 모델 학습 실행 (실제 시간이 소요되는 부분)
            # lgb_model = lgb.train(params, data) # <-- 실제 학습 코드
            
            # 4. 결과 계산 및 세션 업데이트
            metrics = self._calculate_metrics() # <-- 임시 함수
            feature_importance = self._generate_feature_importance_base64() # <-- 임시 함수
            
            self.session.metrics = metrics
            self.session.feature = feature_importance
            
            # 5. 🌟 상태 변경 및 DB 저장 (COMPLETED 상태 반영)
            self.session.state = SessionStateChoices.COMPLETED
            self.session.finished_at = timezone.now()
            self.session.save()
            
        except Exception as e:
            # 학습 중 오류 발생 시, Celery tasks.py에서 FAILED 상태로 처리됩니다.
            # 이중 처리가 되지만, 여기서도 필요하다면 FAILED 처리가 가능합니다.
            # 여기서는 예외를 다시 발생시켜 tasks.py의 except 블록에서 FAILED 처리를 유도합니다.
            raise e


    # --- 도우미 메서드 (Helper Methods) ---

    def _load_data(self, start_date, end_date):
        """데이터베이스 또는 파일에서 학습 데이터를 로드하고 전처리하는 로직"""
        # (실제 구현 필요)
        print(f"Loading data from {start_date} to {end_date}...")
        return "Loaded Data Structure"

    def _calculate_metrics(self):
        """학습된 모델의 성능 지표를 계산하는 로직"""
        # (실제 구현 필요)
        return {"accuracy": 0.92, "f1_score": 0.90}

    def _generate_feature_importance_base64(self):
        """특성 중요도 그래프를 생성하고 base64 문자열로 인코딩하는 로직"""
        # (실제 구현 필요)
        return "base64_encoded_graph_string"