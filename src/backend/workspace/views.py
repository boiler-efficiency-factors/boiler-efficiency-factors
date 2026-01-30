from django.db import transaction
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse, OpenApiParameter
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
import logging
from .models import UserSequence, Session, SessionStateChoices, Model
from .tasks import start_model_training
from .serializers import WorkspaceCreateSerializer, WorkspaceDetailSerializer, SessionDetailSerializer, WorkspacePaginationSerializer

logger = logging.getLogger(__name__)

class WorkspacePagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    max_page_size = 100

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

        try:
            with transaction.atomic():
                model_instance = serializer.save() 
                
                UserSequence.objects.create(
                    # user_sequence_id는 Model.save() 내에서 자동생성, created 자동 채움
                    user_id=user,
                    model_id=model_instance
                )
                
                session_instance = Session.objects.create(
                    model_id=model_instance,
                    state=SessionStateChoices.CREATED,
                    started_at=timezone.now()
                )

                transaction.on_commit(
                    lambda: start_model_training.delay(str(session_instance.session_id))
                )
            
            return Response({
                "model_id": model_instance.model_id,
                "session_id": session_instance.session_id,
                "message": "모델 학습이 백그라운드에서 시작되었습니다."
            }, status=status.HTTP_201_CREATED)
    
        except Exception as e:
            # 트랜잭션 내 오류 발생 시 자동 롤백
            logger.error(f"Workspace creation failed: {e}", exc_info=True)
            return Response({
                "message": f"오류 발생: {e}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class WorkspaceDetailView(APIView):
    @extend_schema(
        summary="워크스페이스 상세 조회",
        parameters=[
            OpenApiParameter(
                name="model_id",
                type=str,
                location=OpenApiParameter.PATH,
                required=True,
                description="조회할 모델의 UUID"
            ),
        ],
        responses={
            200: WorkspaceDetailSerializer,
            404: OpenApiResponse(description="해당 model_id에 해당하는 Workspace를 찾을 수 없습니다.")
        }
    )
    def get(self, request, model_id):
        model_instance = get_object_or_404(Model, model_id=model_id)
        serializer = WorkspaceDetailSerializer(model_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

class WorkspaceSessionView(APIView):
    @extend_schema(
        summary="모델 세션 정보 조회",  
        description="모델 세션 정보 조회 데이터를 반환합니다.",
        responses={200: SessionDetailSerializer}
    )
    def get(self, request, model_id):
        session = Session.objects.filter(model_id=model_id).last()
        if not session:
            return Response({"message": "결과가 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SessionDetailSerializer(session)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class WorkspaceListView(generics.ListAPIView):
    serializer_class = WorkspacePaginationSerializer
    pagination_class = WorkspacePagination

    @extend_schema(
        summary="워크스페이스 목록 조회",
        responses=WorkspaceCreateSerializer,
        examples=[
            OpenApiExample(
                name='목록 조회 응답 예시',
                summary='페이지네이션 및 필드 타입 반영 예시',
                description='실제 Model 구조에 맞춘 응답 데이터입니다.',
                value={
                    "count": 15,
                    "next": "http://127.0.0.1:8000/api/workspace/list/?page=2",
                    "previous": None,
                    "results": [
                        {
                            "model_id": "550e8400-e29b-41d4-a716-446655440000",
                            "workspace": "2024_하반기_보일러_효율분석",
                            "model_name": "lightgbm",
                            "start_date": "2024-01-01",
                            "end_date": "2024-06-30",
                            "parameter": {
                                "n_estimators": 500,
                                "learning_rate": 0.01,
                                "max_depth": -1
                            },
                            "tuning": "grid",
                            "dependent_var": "heat_efficiency",
                            "excluded_var": ["sensor_error_flag", "maintenance_mode"],
                            "created_at": "2025-12-08T10:00:00Z",
                            "updated_at": "2025-12-08T10:30:00Z"
                        },
                        {
                            "model_id": "a1b2c3d4-e5f6-7890-1234-56789abcdef0",
                            "workspace": "테스트_모델_RandomForest",
                            "model_name": "randomforest",
                            "start_date": "2024-07-01",
                            "end_date": "2024-07-07",
                            "parameter": {
                                "n_estimators": 100,
                                "max_depth": 5
                            },
                            "tuning": "random",
                            "dependent_var": "output_temperature",
                            "excluded_var": [],
                            "created_at": "2025-12-07T15:20:00Z",
                            "updated_at": "2025-12-07T15:20:00Z"
                        }
                    ]
                },
                response_only=True
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Model.objects.all().order_by('-created_at')

class WorkspaceDeleteView(generics.DestroyAPIView):
    queryset = Model.objects.all()
    lookup_field = 'model_id'

    @extend_schema(
        summary="워크스페이스(모델) 삭제",
        responses={
            204: None,
            404: {"description": "해당 model_id를 찾을 수 없음"}
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    

class DashboardSummaryView(APIView):
    """전일 현황 및 그래프용 데이터 반환"""
    def get(self, request):
        # 실제 데이터 집계 로직 (예시)
        last_log = BoilerOperationLog.objects.order_by('-log_date').first()
        # 주간 데이터 (최근 7일)
        weekly_data = BoilerOperationLog.objects.order_by('-log_date')[:7]
        
        return Response({
            "daily_summary": {
                "pressure": last_log.avg_pressure,
                "efficiency": last_log.efficiency,
                "gas": last_log.gas_usage
            },
            "weekly_chart": [
                {"date": log.log_date, "efficiency": log.efficiency} for log in weekly_data
            ]
        })

class SessionComparisonView(APIView):
    """여러 세션 성능 지표 비교 (ids=uuid1,uuid2...)"""
    @extend_schema(
        parameters=[OpenApiParameter(name="ids", description="비교할 세션 UUID 리스트 (쉼표구분)", type=str)]
    )
    def get(self, request):
        ids_str = request.query_params.get('ids', '')
        if not ids_str:
            return Response({"message": "ID가 제공되지 않았습니다."}, status=400)
            
        session_ids = ids_str.split(',')
        # 선택된 세션들의 성능 지표(metrics)만 가져오기
        sessions = Session.objects.filter(session_id__in=session_ids)
        
        comparison_result = []
        for s in sessions:
            comparison_result.append({
                "session_id": s.session_id,
                "model_name": s.model_id.model_name,
                "metrics": s.metrics  # R2, RMSE 등 포함된 JSON
            })
            
        return Response(comparison_result, status=200)