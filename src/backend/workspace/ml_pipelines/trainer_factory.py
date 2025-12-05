from .lightgbm import lightgbmTrainer
from .xgboost import xgboostTriner
from .randomforest import randomforestTrainer
from .gbm import gbmTrainer
from django.core.exceptions import ImproperlyConfigured

TRAINER_MAP = {
    'lightgbm': lightgbmTrainer,
    'xgboost': xgboostTriner,
    'random_forest': randomforestTrainer,
    'gradient_boosting': gbmTrainer,
}