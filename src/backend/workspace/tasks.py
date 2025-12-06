from celery import shared_task
from django.utils import timezone
from .models import Session, SessionStateChoices
from .ml_pipelines import trainer_factory
import logging

logger = logging.getLogger(__name__)

@shared_task
def start_model_training(session_id: str):
    session = None
    try:
        session = Session.objects.get(session_id=session_id)
        model_instance = session.model_id

        session.state = SessionStateChoices.TRAINING
        session.save(update_fields=['state'])

        TrainerClass = trainer_factory.get_trainer(model_instance.model_name)
        trainer = TrainerClass(model_instance, session)

        #TODO: run_training()에서 각 모듈 내부에서 FAILED/COMPLETED 상태 저장.
        trainer.run_training()
    
    except Session.DoesNotExist:
        #TODO: DB에서 해당 세션 정보를 찾지 못한 경우 log
        logger.error(f"Session ID {session_id} not found. Task aborted.")
    
    except Exception as e:
        if session:
            session.state = SessionStateChoices.FAILED
            session.finished_at = timezone.now()
            session.save(update_fields=['state', 'finished_at'])
            logger.error(f"Training failed for session {session_id}: {e}", exc_info=True)

        raise e

