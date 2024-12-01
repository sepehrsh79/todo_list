from drf_spectacular.types import OpenApiTypes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from todo_list.api.pagination import LimitOffsetPagination, get_paginated_response_context

from todo_list.todo.models import Task, Board
from todo_list.todo.selectors.task import task_list, task_detail, check_board_permission_to_add_task
from todo_list.todo.services.task import create_task, update_task, delete_task
from todo_list.api.mixins import ApiAuthMixin


class TaskAPIView(ApiAuthMixin, APIView):
    permission_classes = [IsAuthenticated]

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class TaskInputSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=100)
        description = serializers.CharField(allow_blank=True)
        deadline = serializers.DateField(required=False)

    class TaskOutPutSerializer(serializers.ModelSerializer):
        user = serializers.SerializerMethodField("get_user")
        board = serializers.SerializerMethodField("get_board")

        class Meta:
            model = Task
            fields = ["id", "title", "description", "board", "user", "deadline", "created_at", "updated_at"]

        def get_user(self, task):
            return task.user.email

        def get_board(self, task):
            return task.board.name

    @extend_schema(
        tags=["Tasks"],
        description="More descriptive text",
        responses=TaskOutPutSerializer,
        request=TaskInputSerializer,
    )
    def post(self, request, board_id):
        serializer = self.TaskInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        board = get_object_or_404(Board, id=board_id)
        if not check_board_permission_to_add_task(board=board, user=request.user):
            return Response({"error": "You are not authorized to add tasks to this board."},
                            status=status.HTTP_403_FORBIDDEN)
        task = create_task(
            title=serializer.validated_data.get("title"),
            description=serializer.validated_data.get("description"),
            deadline=serializer.validated_data.get("deadline"),
            board=board,
            user=request.user,
        )
        return Response(self.TaskOutPutSerializer(task, context={"request": request}).data)

    @extend_schema(
        tags=["Tasks"],
        responses=TaskOutPutSerializer,
    )
    def get(self, request, board_id):
        query = task_list(board_id=board_id)

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=self.TaskOutPutSerializer,
            queryset=query,
            request=request,
            view=self,
        )


class TaskDetailAPIView(ApiAuthMixin, APIView):
    permission_classes = [IsAuthenticated]

    class TaskDetailInputSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=100)
        description = serializers.CharField(allow_blank=True)
        board_id = serializers.IntegerField()
        deadline = serializers.DateField(required=False)

        def validate_board(self, board_id):
            if Board.objects.filter(id=board_id).exists():
                return board_id
            raise serializers.ValidationError("Board not found!")

    class TaskDetailOutPutSerializer(serializers.ModelSerializer):
        user = serializers.SerializerMethodField("get_user")
        board = serializers.SerializerMethodField("get_board")

        class Meta:
            model = Task
            fields = ["id", "title", "description", "board", "user", "deadline", "created_at", "updated_at"]

        def get_user(self, task):
            return task.user.email

        def get_board(self, task):
            return task.board.name

    @extend_schema(
        tags=["Tasks"],
        responses=TaskDetailOutPutSerializer,
    )
    def get(self, request, task_id):
        task = task_detail(id=task_id)
        serializer = self.TaskDetailOutPutSerializer(task)
        return Response(serializer.data)

    @extend_schema(
        tags=["Tasks"],
        request=TaskDetailInputSerializer,
        responses=TaskDetailOutPutSerializer,
    )
    def put(self, request, task_id):
        task = task_detail(id=task_id)
        serializer = self.TaskDetailInputSerializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        board = Board.objects.filter(id=serializer.validated_data.get("board_id"))
        if board.exists():
            if not check_board_permission_to_add_task(board=board.first(), user=request.user):
                return Response({"error": "You are not authorized to add tasks to this board."},
                                status=status.HTTP_403_FORBIDDEN)
        task = update_task(task=task, **serializer.validated_data)
        serializer = self.TaskDetailOutPutSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Tasks"],
        responses=None,
    )
    def delete(self, request, task_id):
        task = task_detail(id=task_id)
        delete_task(task=task)
        return Response(
            {"message": "Task deleted successfully."},
            status=status.HTTP_200_OK,
        )
