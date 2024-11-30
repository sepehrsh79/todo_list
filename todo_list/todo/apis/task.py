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
from todo_list.todo.selectors.task import task_list, task_detail
from todo_list.todo.services.task import create_task, update_task, delete_task
from todo_list.api.mixins import ApiAuthMixin


class TaskAPIView(ApiAuthMixin, APIView):
    permission_classes = [IsAuthenticated]

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=100)
        description = serializers.CharField(allow_blank=True)

    class OutPutSerializer(serializers.ModelSerializer):
        user = serializers.SerializerMethodField("get_user")
        board = serializers.SerializerMethodField("get_group")

        class Meta:
            model = Task
            fields = ["id", "title", "description", "board", "user", "created_at", "updated_at"]

        def get_user(self, task):
            return task.user.email

        def get_board(self, task):
            return task.board.name

    @extend_schema(
        tags=['Tasks'],
        description='More descriptive text',
        responses=OutPutSerializer,
        request=InputSerializer,
    )
    def post(self, request, board_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        board = get_object_or_404(Board, id=board_id)
        task = create_task(
            title=serializer.validated_data.get("name"),
            description=serializer.validated_data.get("description"),
            board=board,
            user=request.user,
        )
        return Response(self.OutPutSerializer(task, context={"request": request}).data)

    @extend_schema(
        tags=['Tasks'],
        responses=OutPutSerializer,
    )
    def get(self, request, board_id):
        query = task_list(board_id=board_id)

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=self.OutPutSerializer,
            queryset=query,
            request=request,
            view=self,
        )


class TaskDetailAPIView(ApiAuthMixin, APIView):
    permission_classes = [IsAuthenticated]

    class InputDetailSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=100)
        description = serializers.CharField(allow_blank=True)
        board = serializers.IntegerField()

        def validate_board(self, board_id):
            if Board.objects.filter(id=board_id).exists():
                return board_id
            raise serializers.ValidationError("Board not found!")

    class OutPutDetailSerializer(serializers.ModelSerializer):
        user = serializers.SerializerMethodField("get_user")
        board = serializers.SerializerMethodField("get_group")

        class Meta:
            model = Task
            fields = ["id", "title", "description", "board", "user", "created_at", "updated_at"]

        def get_user(self, task):
            return task.user.email

        def get_board(self, task):
            return task.board.name

    @extend_schema(
        tags=['Tasks'],
        responses=OutPutDetailSerializer,
    )
    def get(self, request, id):
        task = task_detail(id=id)
        serializer = self.OutPutSerializer(task)
        return Response(serializer.data)

    @extend_schema(
        tags=['Tasks'],
        request=InputDetailSerializer,
        responses=OutPutDetailSerializer,
    )
    def put(self, request, id):
        task = task_detail(id=id)
        serializer = self.InputSerializer(task, data=request.data)
        serializer.is_valid(raise_exception=True)
        update_task(task=task, **serializer.validated_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=['Tasks'],
        responses=None,
    )
    def delete(self, request, id):
        task = task_detail(id=id)
        delete_task(task=task)
        return Response(
            {"message": "Group deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
