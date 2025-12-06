from django.urls import path
from .views import WorkspaceCreateView, WorkspaceDetailView

urlpatterns = [
    # 워크스페이스 생성
    # URL: POST /api/home/workspace/create/
    path('home/workspace/create/', 
         WorkspaceCreateView.as_view(), 
         name='workspace-create'),
    
    # 워크스페이스 상세 조회
    # URL: GET /api/home/workspace/get/<model_id>/
    path('home/workspace/get/<uuid:model_id>/',
         WorkspaceDetailView.as_view(),
         name='workspace-detail'),
]