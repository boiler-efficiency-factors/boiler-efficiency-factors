from .lightgbm import lightgbmTrainer
from .xgboost import xgboostTrainer
from .randomforest import randomforestTrainer
from .gbm import gbmTrainer
from django.core.exceptions import ImproperlyConfigured

TRAINER_MAP = {
    'lightgbm': lightgbmTrainer,
    'xgboost': xgboostTrainer,
    'random_forest': randomforestTrainer,
    'gradient_boosting': gbmTrainer,
}

def get_trainer(model_name: str):
    """모델 이름 문자열에 해당하는 트레이너 클래스를 반환"""

    if model_name not in TRAINER_MAP:
        raise ImproperlyConfigured(f"Unsupported model name: {model_name}")
    
    return TRAINER_MAP[model_name]