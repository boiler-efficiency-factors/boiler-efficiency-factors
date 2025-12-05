from celery import shared_task
from django.utils import timezone
from .models import Session, SessionStateChoices
from .ml_pipelines import trainer_factory
import logging

logger = logging.getLogger(__name__)

@shared_task
def start_model_training(session_id):
    """모델 학습을 백그라운드에서 실행하는 Celery Task"""
    session = None

    try:
        # get session_id for model_id
        session = Session.objects.get(session_id=session_id)
        model_instance = session_id.model_id

        # model select with model_name
        TrainerClass = trainer_factory.get_trainer(model_instance.model_name)
        trainer = TrainerClass(model_instance, session)

        #TODO: run_training() 내부에서 COMPLETED 상태를 저장해야 함.
        trainer.run_training()
    
    except Session.DoesNotExist:
        #TODO: DB에서 해당 세션 정보를 찾지 못한 경우 log
        logger.error(f"Session ID {session_id} not found. Task aborted.")
    
    except Exception as e:
        if session:
            session.state = SessionStateChoices.FAILED
            session.finished_at = timezone.now()
            session.save()
            logger.error(f"Training failed for session {session_id}: {e}", exc_info=True)

        raise e

