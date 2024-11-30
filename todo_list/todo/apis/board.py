from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from drf_spectacular.utils import extend_schema

from todo_list.api.pagination import LimitOffsetPagination, get_paginated_response_context

from todo_list.todo.models import Board, Group
from todo_list.todo.selectors.board import board_list, board_detail
from todo_list.todo.services.board import create_board, update_board, delete_board
from todo_list.api.mixins import ApiAuthMixin


class BoardAPIView(ApiAuthMixin, APIView):
    permission_classes = [IsAuthenticated]

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=100)
        description = serializers.CharField(allow_blank=True)

    class OutPutSerializer(serializers.ModelSerializer):
        user = serializers.SerializerMethodField("get_user")
        group = serializers.SerializerMethodField("get_group")

        class Meta:
            model = Board
            fields = ["id", "name", "description", "group", "user", "created_at", "updated_at"]

        def get_user(self, board):
            return board.user.email

        def get_group(self, board):
            return board.group.name

    @extend_schema(
        tags=['Boards'],
        responses=OutPutSerializer,
        request=InputSerializer,
    )
    def post(self, request, group_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group = get_object_or_404(Group, id=group_id)
        board = create_board(
            name=serializer.validated_data.get("name"),
            description=serializer.validated_data.get("description"),
            group=group,
            user=request.user,
        )
        return Response(self.OutPutSerializer(board, context={"request": request}).data)

    @extend_schema(
        tags=['Boards'],
        responses=OutPutSerializer,
    )
    def get(self, request, group_id):
        query = board_list(group_id=group_id)

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=self.OutPutSerializer,
            queryset=query,
            request=request,
            view=self,
        )


class BoardDetailAPIView(ApiAuthMixin, APIView):
    permission_classes = [IsAuthenticated]

    class InputDetailSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=100)
        description = serializers.CharField(allow_blank=True)
        group = serializers.IntegerField()

        def validate_group(self, group_id):
            if Group.objects.filter(id=group_id).exists():
                return group_id
            raise serializers.ValidationError("Group not found!")

    class OutPutDetailSerializer(serializers.ModelSerializer):
        user = serializers.SerializerMethodField("get_user")
        group = serializers.SerializerMethodField("get_group")

        class Meta:
            model = Board
            fields = ["id", "name", "description", "group", "user", "created_at", "updated_at"]

        def get_user(self, board):
            return board.user.email

        def get_group(self, board):
            return board.group.name

    @extend_schema(
        tags=['Boards'],
        responses=OutPutDetailSerializer,
    )
    def get(self, request, id):
        board = board_detail(id=id)
        serializer = self.OutPutSerializer(board)
        return Response(serializer.data)

    @extend_schema(
        tags=['Boards'],
        request=InputDetailSerializer,
        responses=OutPutDetailSerializer,
    )
    def put(self, request, id):
        board = board_detail(id=id)
        serializer = self.InputSerializer(board, data=request.data)
        serializer.is_valid(raise_exception=True)
        update_board(board=board, **serializer.validated_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=['Boards'],
        responses=None,
    )
    def delete(self, request, id):
        board = board_detail(id=id)
        delete_board(board=board)
        return Response(
            {"message": "Group deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
