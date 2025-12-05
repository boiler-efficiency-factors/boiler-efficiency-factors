from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth import get_user_model

from .models import UserSequence, Session, SessionStateChoices
from .tasks import start_model_training
from .serializers import WorkspaceCreateSerializer

class WorkspaceCreateView(APIView):
    @extend_schema(
            request=WorkspaceCreateSerializer,
            responses={
                status.HTTP_201_CREATED: {
                    "type": "object",
                    "properties": {
                        "model_id": {"type": "string", "format": "uuid"},
                        "session_id": {"type": "string", "format": "uuid"},
                        "message": {"type": "string"}
                    }
                },
                status.HTTP_400_BAD_REQUEST: WorkspaceCreateSerializer,
            }
    )
    def post(self, request):
        user = request.user
        
        #TODO: Serializer 유효성 검사
        serializer = WorkspaceCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        #TODO: DB 작업 시작
        with transaction.atomic():
            model_instance = serializer.save() 
            
            UserSequence.objects.create(
                user_id=user,
                model_id=model_instance
            )
            
            session_instance = Session.objects.create(
                model_id=model_instance,
                state=SessionStateChoices.TRAINING
            )
            
            start_model_training.delay(str(session_instance.session_id))
        
        return Response({
            "model_id": model_instance.model_id,
            "session_id": session_instance.session_id,
            "message": "모델 학습이 백그라운드에서 시작되었습니다."
        }, status=status.HTTP_201_CREATED)
