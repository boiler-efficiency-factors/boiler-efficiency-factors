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
    def post(self, request, user_id):
        User = get_user_model()

        #TODO: User 유효성 검사
        try:
            user = get_object_or_404(User, pk=user_id)
        except Exception:
            return Response({"error": "User not found"},
                            status=status.HTTP_404_NOT_FOUND)
        
        #TODO: Serializer 유효성 검사
        serializer = WorkspaceCreateSerializer(data=request.data)
        serializer.is_valid(reise_exception=True)

        #TODO: DB 작업 시작
        with transaction.atomic():
            model_instance = WorkspaceCreateSerializer.save() 
            
            # 2. UserSequence 객체 생성 및 저장 (history 기록)
            UserSequence.objects.create(
                user_id=user,
                model_id=model_instance
            )
            
            # 3. Session 객체 생성 및 TRAINING 상태로 초기화
            session_instance = Session.objects.create(
                model_id=model_instance,
                state=SessionStateChoices.TRAINING # 🌟 즉시 TRAINING 상태 반영
            )
            
            # 4. Celery에 session_id를 인자로 넘겨 작업 위임
            start_model_training.delay(str(session_instance.session_id))
        
        return Response({
            "model_id": model_instance.model_id,
            "session_id": session_instance.session_id,
            "message": "모델 학습이 백그라운드에서 시작되었습니다."
        }, status=status.HTTP_201_CREATED)
