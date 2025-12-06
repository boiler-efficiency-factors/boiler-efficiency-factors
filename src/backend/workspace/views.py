from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiExample
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import UserSequence, Session, SessionStateChoices, Model
from .tasks import start_model_training
from .serializers import WorkspaceCreateSerializer, WorkspaceDetailSerializer

class WorkspaceCreateView(APIView):
    @extend_schema(
            request=WorkspaceCreateSerializer,
            examples=[
                OpenApiExample(
                    '모델 생성 요청 예시',
                    value={
                        "workspace": "보일러_프로젝트_A",
                        "model_name": "lightgbm",
                        "start_date": "2025-12-05",
                        "end_date": "2025-12-31",
                        "parameter": { 
                            "n_estimators": 0.9,
                            "learning_rate": 0.01,
                            "max_depth": 10
                        },
                        "tuning": "grid",
                        "dependent_var": "열효율",
                        "excluded_var": [
                            "센서1", 
                            "센서2"
                        ]
                    },
                    request_only=True
                ),
            ],
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
        serializer = WorkspaceCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        #TODO: DB 작업 시작
        try:
            with transaction.atomic():
                model_instance = serializer.save() 
                
                UserSequence.objects.create(
                    # user_sequence_id는 Model.save() 내에서 자동생성, created 자동 채움
                    user_id=user,
                    model_id=model_instance
                )
                
                session_instance = Session.objects.create(
                    #TODO: started_at은 DateTime 자동으로 해놨는데 timezone을 써야하나?
                    model_id=model_instance,
                    state=SessionStateChoices.CREATED,
                    started_at=timezone.now()
                )
                
                start_model_training.delay(str(session_instance.session_id))
            
            return Response({
                "model_id": model_instance.model_id,
                "session_id": session_instance.session_id,
                "message": "모델 학습이 백그라운드에서 시작되었습니다."
            }, status=status.HTTP_201_CREATED)
    
        except Exception as e:
            # 트랜잭션 내 오류 발생 시 자동 롤백
            return Response({
                "message": f"오류 발생: {e}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class WorkspaceDetailView(APIView):
    def get(self, request, model_id):
        # model_id 로 Model 인스턴스 조회 (없으면 404)
        model_instance = get_object_or_404(Model, model_id=model_id)

        # 직렬화
        serializer = WorkspaceDetailSerializer(model_instance)

        # 응답 반환
        return Response(serializer.data, status=status.HTTP_200_OK)
