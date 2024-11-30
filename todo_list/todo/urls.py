from django.urls import path
from .apis.group import GroupAPIView, GroupDetailAPIView
from .apis.board import BoardAPIView, BoardDetailAPIView
from .apis.task import TaskAPIView, TaskDetailAPIView


urlpatterns = [
    # Group APIs
    path('group/', GroupAPIView.as_view(), name='group'),
    path('group/<int:group_id>/', GroupDetailAPIView.as_view(), name='group_detail'),

    # Board APIs
    path('board/group/<int:group_id>/', BoardAPIView.as_view(), name='board'),
    path('board/<int:board_id>/', BoardDetailAPIView.as_view(), name='board-detail'),

    # Task APIs
    path('task/board/<int:board_id>/', TaskAPIView.as_view(), name='task'),
    path('task/<int:task_id>/', TaskDetailAPIView.as_view(), name='task-detail'),
]
