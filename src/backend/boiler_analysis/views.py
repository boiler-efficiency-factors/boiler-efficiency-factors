from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
import pandas as pd
import json
import os
from .models import AnalysisProject, DataFile, ModelConfiguration, AnalysisResult
from .serializers import (
    AnalysisProjectSerializer, DataFileSerializer, ModelConfigurationSerializer,
    AnalysisResultSerializer, FileUploadSerializer
)
from .services import ModelTrainingService, DataProcessingService


class AnalysisProjectViewSet(viewsets.ModelViewSet):
    serializer_class = AnalysisProjectSerializer
    
    def get_queryset(self):
        return AnalysisProject.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def upload_csv(self, request, pk=None):
        """CSV 파일 업로드"""
        project = self.get_object()
        serializer = FileUploadSerializer(data=request.data)
        
        if serializer.is_valid():
            uploaded_file = serializer.validated_data['file']
            
            # 파일 저장
            data_file = DataFile.objects.create(
                project=project,
                file=uploaded_file,
                original_filename=uploaded_file.name,
                file_size=uploaded_file.size
            )
            
            # 데이터 전처리 시작
            try:
                processing_service = DataProcessingService()
                processing_service.process_csv(data_file)
                data_file.is_processed = True
                data_file.save()
                
                return Response({
                    'message': 'CSV 파일이 성공적으로 업로드되고 처리되었습니다.',
                    'file_id': data_file.id
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    'error': f'파일 처리 중 오류가 발생했습니다: {str(e)}'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def data_preview(self, request, pk=None):
        """데이터 미리보기"""
        project = self.get_object()
        data_file = project.data_files.filter(is_processed=True).first()
        
        if not data_file:
            return Response({'error': '처리된 데이터 파일이 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            df = pd.read_csv(data_file.file.path)
            preview_data = {
                'columns': df.columns.tolist(),
                'data': df.head(10).to_dict('records'),
                'shape': df.shape,
                'dtypes': df.dtypes.to_dict()
            }
            return Response(preview_data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def train_model(self, request, pk=None):
        """모델 훈련"""
        project = self.get_object()
        model_type = request.data.get('model_type')
        parameters = request.data.get('parameters', {})
        
        if not model_type:
            return Response({'error': '모델 타입을 선택해주세요.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 모델 설정 생성
        model_config = ModelConfiguration.objects.create(
            project=project,
            model_type=model_type,
            parameters=parameters
        )
        
        try:
            # 모델 훈련 서비스 실행
            training_service = ModelTrainingService()
            result = training_service.train_model(model_config)
            
            # 결과 저장
            analysis_result = AnalysisResult.objects.create(
                model_config=model_config,
                feature_importance=result['feature_importance'],
                performance_metrics=result['performance_metrics'],
                predictions=result.get('predictions', {})
            )
            
            model_config.is_trained = True
            model_config.save()
            
            return Response({
                'message': '모델 훈련이 완료되었습니다.',
                'result_id': analysis_result.id,
                'performance_metrics': result['performance_metrics']
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'error': f'모델 훈련 중 오류가 발생했습니다: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def analysis_results(self, request, pk=None):
        """분석 결과 조회"""
        project = self.get_object()
        results = AnalysisResult.objects.filter(model_config__project=project)
        serializer = AnalysisResultSerializer(results, many=True)
        return Response(serializer.data)


class ModelConfigurationViewSet(viewsets.ModelViewSet):
    serializer_class = ModelConfigurationSerializer
    
    def get_queryset(self):
        return ModelConfiguration.objects.filter(project__user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def update_parameters(self, request, pk=None):
        """모델 파라미터 업데이트"""
        model_config = self.get_object()
        new_parameters = request.data.get('parameters', {})
        
        model_config.parameters.update(new_parameters)
        model_config.save()
        
        return Response({
            'message': '파라미터가 업데이트되었습니다.',
            'parameters': model_config.parameters
        })


class AnalysisResultViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AnalysisResultSerializer
    
    def get_queryset(self):
        return AnalysisResult.objects.filter(model_config__project__user=self.request.user)
    
    @action(detail=True, methods=['get'])
    def feature_importance_chart(self, request, pk=None):
        """특성 중요도 차트 데이터"""
        result = self.get_object()
        return Response({
            'chart_data': result.feature_importance,
            'model_type': result.model_config.model_type
        })
    
    @action(detail=True, methods=['get'])
    def prediction_chart(self, request, pk=None):
        """예측 결과 차트 데이터"""
        result = self.get_object()
        return Response({
            'predictions': result.predictions,
            'metrics': result.performance_metrics
        })