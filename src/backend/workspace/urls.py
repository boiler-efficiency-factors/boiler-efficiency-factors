from django.urls import path
from .views import WorkspaceCreateView

urlpatterns = [
    # 워크스페이스 생성
    # URL: POST /api/home/workspace/create/
    path('home/workspace/create/', 
         WorkspaceCreateView.as_view(), 
         name='workspace-create'),
]