from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
import pandas as pd
import json
import os
from .serializers import (
    AnalysisProjectSerializer, DataFileSerializer, ModelConfigurationSerializer,
    AnalysisResultSerializer, FileUploadSerializer
)
from .services import ModelTrainingService, DataProcessingService
from rest_framework.views import APIView
from .models import User, Model, Session

# Auth Endpoints
class LoginView(APIView):
    """
    POST /api/auth/login
    사용자 로그인 처리
    """
    def post(self, request):
        # TODO: 1. 시리얼라이저를 사용하여 사용자 입력(user_name, password) 검증
        # TODO: 2. Django의 authenticate를 사용하여 사용자 인증
        # TODO: 3. 인증 성공 시, 세션이나 토큰(JWT 등) 생성 및 반환
        return Response({"message": "로그인 성공"}, status=status.HTTP_200_OK)


# User Endpoints
class UserRegisterView(APIView):
    """
    POST /api/user/register
    신규 사용자 회원가입 처리
    """
    def post(self, request):
        # TODO: 1. User 시리얼라이저를 사용하여 사용자 입력 검증 및 유효성 확인
        # TODO: 2. 비밀번호 해싱 및 User 모델 객체 생성 후 저장
        # TODO: 3. 성공 응답 반환
        return Response({"message": "회원가입 성공"}, status=status.HTTP_201_CREATED)


# Home/Workspace Endpoints
# 모든 Workspace 관련 뷰는 권한 확인(JWT)이 필요함
class WorkspaceListView(APIView):
    """
    GET /api/home/workspace/get/paging/{user_id}?page=10&size=10
    특정 유저의 모든 모델 목록을 페이지네이션하여 조회
    """
    def get(self, request, user_id):
        # TODO: 1. 요청 사용자(request.user)가 user_id와 일치하는지 권한 확인
        # TODO: 2. 쿼리 파라미터에서 page와 size를 추출 (request.query_params)
        # TODO: 3. UserSequence 모델을 필터링하여 해당 user_id의 모델 목록 조회
        # TODO: 4. Pagination 처리 후 시리얼라이즈하여 반환
        return Response({"message": f"User {user_id}의 모델 목록 조회"}, status=status.HTTP_200_OK)


class WorkspaceDeleteView(APIView):
    """
    DELETE /api/home/workspace/delete/{model_id}
    특정 모델 삭제
    """
    def delete(self, request, model_id):
        # TODO: 1. model_id에 해당하는 Model 객체 조회 (get_object_or_404 사용)
        # TODO: 2. 요청 사용자(request.user)가 해당 모델의 소유자인지 확인 (권한 확인)
        # TODO: 3. Model.delete() 호출
        return Response({"message": f"Model {model_id} 삭제 완료"}, status=status.HTTP_204_NO_CONTENT)


class WorkspaceCreateView(APIView):
    """
    POST /api/home/workspace/register/{user_id}
    새로운 모델 생성 (workspace 등록)
    """
    def post(self, request, user_id):
        # TODO: 1. 요청 사용자(request.user)가 user_id와 일치하는지 권한 확인
        # TODO: 2. Model 시리얼라이저와 UserSequence 시리얼라이저를 사용하여 데이터 검증
        # TODO: 3. 검증 통과 후, Model 객체와 UserSequence 객체를 순차적으로 생성 및 저장
        #       (이때 UserSequence의 save()에서 시퀀스 ID가 자동 계산됨)
        return Response({"message": "새 모델 및 워크스페이스 등록 완료"}, status=status.HTTP_201_CREATED)


class WorkspaceDetailView(APIView):
    """
    GET /api/home/workspace/get/{model_id}
    특정 모델의 상세 정보 조회
    """
    def get(self, request, model_id):
        # TODO: 1. model_id에 해당하는 Model 객체 조회
        # TODO: 2. 요청 사용자에게 조회 권한이 있는지 확인
        # TODO: 3. Model 상세 정보를 시리얼라이즈하여 반환 (파라미터, 변수 등 포함)
        return Response({"message": f"Model {model_id} 상세 정보 조회"}, status=status.HTTP_200_OK)


class FeatureImportanceView(APIView):
    """
    GET /api/home/workspace/get/feature/{model_id}
    특정 모델의 피처 중요도(Feature Importance) 데이터 조회
    """
    def get(self, request, model_id):
        # TODO: 1. model_id에 연결된 최신 Session 객체 조회
        # TODO: 2. Session 객체의 'feature' 필드(base64 인코딩 데이터)를 반환
        return Response({"message": f"Model {model_id} 피처 중요도 조회"}, status=status.HTTP_200_OK)


class MetricsView(APIView):
    """
    GET /api/home/workspace/get/matrix/{model_id}
    특정 모델의 지표(Metrics) 데이터 조회 (train/test 성능 지표)
    """
    def get(self, request, model_id):
        # TODO: 1. model_id에 연결된 최신 Session 객체 조회
        # TODO: 2. Session 객체의 'metrics' 필드(JSON 데이터)를 반환
        return Response({"message": f"Model {model_id} 지표 조회"}, status=status.HTTP_200_OK)

# @extend_schema_view(
#     list=extend_schema(
#         summary="프로젝트 목록 조회",
#         description="사용자의 모든 분석 프로젝트 목록을 조회합니다.",
#         tags=["프로젝트 관리"]
#     ),
#     create=extend_schema(
#         summary="프로젝트 생성",
#         description="새로운 분석 프로젝트를 생성합니다.",
#         tags=["프로젝트 관리"]
#     ),
#     retrieve=extend_schema(
#         summary="프로젝트 상세 조회",
#         description="특정 프로젝트의 상세 정보를 조회합니다.",
#         tags=["프로젝트 관리"]
#     ),
#     update=extend_schema(
#         summary="프로젝트 수정",
#         description="프로젝트 정보를 수정합니다.",
#         tags=["프로젝트 관리"]
#     ),
#     destroy=extend_schema(
#         summary="프로젝트 삭제",
#         description="프로젝트를 삭제합니다.",
#         tags=["프로젝트 관리"]
#     ),
# )
# class AnalysisProjectViewSet(viewsets.ModelViewSet):
#     serializer_class = AnalysisProjectSerializer
    
#     def get_queryset(self):
#         return AnalysisProject.objects.filter(user=self.request.user)
    
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
    
#     @extend_schema(
#         summary="CSV 파일 업로드",
#         description="보일러 데이터 CSV 파일을 업로드하고 자동으로 전처리를 수행합니다.",
#         tags=["데이터 관리"],
#         request=FileUploadSerializer,
#     )
#     @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser])
#     def upload_csv(self, request, pk=None):
#         """CSV 파일 업로드"""
#         project = self.get_object()
#         serializer = FileUploadSerializer(data=request.data)
        
#         if serializer.is_valid():
#             uploaded_file = serializer.validated_data['file']
            
#             # 파일 저장
#             data_file = DataFile.objects.create(
#                 project=project,
#                 file=uploaded_file,
#                 original_filename=uploaded_file.name,
#                 file_size=uploaded_file.size
#             )
            
#             # 데이터 전처리 시작
#             try:
#                 processing_service = DataProcessingService()
#                 processing_service.process_csv(data_file)
#                 data_file.is_processed = True
#                 data_file.save()
                
#                 return Response({
#                     'message': 'CSV 파일이 성공적으로 업로드되고 처리되었습니다.',
#                     'file_id': data_file.id
#                 }, status=status.HTTP_201_CREATED)
#             except Exception as e:
#                 return Response({
#                     'error': f'파일 처리 중 오류가 발생했습니다: {str(e)}'
#                 }, status=status.HTTP_400_BAD_REQUEST)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     @extend_schema(
#         summary="데이터 미리보기",
#         description="업로드된 CSV 데이터의 처음 10개 행을 미리 봅니다.",
#         tags=["데이터 관리"],
#     )
#     @action(detail=True, methods=['get'])
#     def data_preview(self, request, pk=None):
#         """데이터 미리보기"""
#         project = self.get_object()
#         data_file = project.data_files.filter(is_processed=True).first()
        
#         if not data_file:
#             return Response({'error': '처리된 데이터 파일이 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
#         try:
#             df = pd.read_csv(data_file.file.path)
#             preview_data = {
#                 'columns': df.columns.tolist(),
#                 'data': df.head(10).to_dict('records'),
#                 'shape': df.shape,
#                 'dtypes': df.dtypes.to_dict()
#             }
#             return Response(preview_data)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
#     @extend_schema(
#         summary="AI 모델 훈련",
#         description="선택한 AI 모델(LightGBM, XGBoost, Random Forest, GBM)로 훈련을 수행합니다.",
#         tags=["모델 훈련"],
#         examples=[
#             OpenApiExample(
#                 'LightGBM 예시',
#                 value={
#                     'model_type': 'lightgbm',
#                     'parameters': {
#                         'num_leaves': 31,
#                         'learning_rate': 0.05
#                     }
#                 }
#             ),
#         ]
#     )
#     @action(detail=True, methods=['post'])
#     def train_model(self, request, pk=None):
#         """모델 훈련"""
#         project = self.get_object()
#         model_type = request.data.get('model_type')
#         parameters = request.data.get('parameters', {})
        
#         if not model_type:
#             return Response({'error': '모델 타입을 선택해주세요.'}, status=status.HTTP_400_BAD_REQUEST)
        
#         # 모델 설정 생성
#         model_config = ModelConfiguration.objects.create(
#             project=project,
#             model_type=model_type,
#             parameters=parameters
#         )
        
#         try:
#             # 모델 훈련 서비스 실행
#             training_service = ModelTrainingService()
#             result = training_service.train_model(model_config)
            
#             # 결과 저장
#             analysis_result = AnalysisResult.objects.create(
#                 model_config=model_config,
#                 feature_importance=result['feature_importance'],
#                 performance_metrics=result['performance_metrics'],
#                 predictions=result.get('predictions', {})
#             )
            
#             model_config.is_trained = True
#             model_config.save()
            
#             return Response({
#                 'message': '모델 훈련이 완료되었습니다.',
#                 'result_id': analysis_result.id,
#                 'performance_metrics': result['performance_metrics']
#             }, status=status.HTTP_201_CREATED)
            
#         except Exception as e:
#             return Response({
#                 'error': f'모델 훈련 중 오류가 발생했습니다: {str(e)}'
#             }, status=status.HTTP_400_BAD_REQUEST)
    
#     @extend_schema(
#         summary="분석 결과 조회",
#         description="프로젝트의 모든 분석 결과를 조회합니다.",
#         tags=["분석 결과"],
#     )
#     @action(detail=True, methods=['get'])
#     def analysis_results(self, request, pk=None):
#         """분석 결과 조회"""
#         project = self.get_object()
#         results = AnalysisResult.objects.filter(model_config__project=project)
#         serializer = AnalysisResultSerializer(results, many=True)
#         return Response(serializer.data)


# class ModelConfigurationViewSet(viewsets.ModelViewSet):
#     serializer_class = ModelConfigurationSerializer
    
#     def get_queryset(self):
#         return ModelConfiguration.objects.filter(project__user=self.request.user)
    
#     @action(detail=True, methods=['post'])
#     def update_parameters(self, request, pk=None):
#         """모델 파라미터 업데이트"""
#         model_config = self.get_object()
#         new_parameters = request.data.get('parameters', {})
        
#         model_config.parameters.update(new_parameters)
#         model_config.save()
        
#         return Response({
#             'message': '파라미터가 업데이트되었습니다.',
#             'parameters': model_config.parameters
#         })


# class AnalysisResultViewSet(viewsets.ReadOnlyModelViewSet):
#     serializer_class = AnalysisResultSerializer
    
#     def get_queryset(self):
#         return AnalysisResult.objects.filter(model_config__project__user=self.request.user)
    
#     @action(detail=True, methods=['get'])
#     def feature_importance_chart(self, request, pk=None):
#         """특성 중요도 차트 데이터"""
#         result = self.get_object()
#         return Response({
#             'chart_data': result.feature_importance,
#             'model_type': result.model_config.model_type
#         })
    
#     @action(detail=True, methods=['get'])
#     def prediction_chart(self, request, pk=None):
#         """예측 결과 차트 데이터"""
#         result = self.get_object()
#         return Response({
#             'predictions': result.predictions,
#             'metrics': result.performance_metrics
#         })