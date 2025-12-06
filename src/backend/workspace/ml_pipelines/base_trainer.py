from abc import ABC, abstractmethod
from django.utils import timezone
from ..models import SessionStateChoices

class BaseTrainer(ABC):
    """AI모듈 기본 인터페이스"""

    def __init__(self, model_instance, session_instance):
        self.model = model_instance
        self.session = session_instance

    @abstractmethod
    def _run_model_logic(self):
        """
        1. Load Data
        2. Reprocessing
        3. Setting model
        4. Learning and Assessment
        5. Metrics
        6. feature importance
        """

    def run_training(self):
        """
        학습 전체 흐름 및 상태 관리 및 오류 처리 메서드
        """
        try:
            metrics, feature = self._run_model_logic()

            self.session.metrics = metrics
            self.session.feature = feature
            self.session.finished_at = timezone.now()
            self.session.state = SessionStateChoices.COMPLETED
            self.session.save(update_fields=['metrics', 'feature', 'finished_at', 'state'])
        
        except Exception as e:
            # run_model_logic에서 발생한 모든 예외 처리
            # tasks.py except 블록에서 FAILED 상태로 처리
            raise e