# workspace/ml_pipelines/base_trainer.py

class BaseTrainer:
    """모든 AI 모델 트레이너의 기본 인터페이스"""
    
    def __init__(self, model_instance, session_instance):
        self.model = model_instance
        self.session = session_instance
        # 모델 정보와 세션 정보를 저장하여 모든 트레이너가 접근할 수 있게 함
        
    def run_training(self):
        """
        실제 학습을 수행하는 추상 메서드.
        하위 클래스에서 반드시 구현
        """
        raise NotImplementedError("Subclasses must implement run_training()")