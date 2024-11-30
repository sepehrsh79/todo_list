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
from todo_list.users.nested_serializers import PermittedUsersSerializer


class BoardAPIView(ApiAuthMixin, APIView):
    permission_classes = [IsAuthenticated]

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class BoardInputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=100)
        description = serializers.CharField(allow_blank=True)
        permitted_users = serializers.ListField(
            default=[],
            child=serializers.IntegerField(),
            allow_empty=True
        )

    class BoardOutPutSerializer(serializers.ModelSerializer):
        user = serializers.SerializerMethodField("get_user")
        group = serializers.SerializerMethodField("get_group")
        permitted_users = PermittedUsersSerializer(many=True)

        class Meta:
            model = Board
            fields = ["id", "name", "description", "group", "user", "permitted_users", "created_at", "updated_at"]

        def get_user(self, board):
            return board.user.email

        def get_group(self, board):
            return board.group.name

    @extend_schema(
        tags=['Boards'],
        responses=BoardOutPutSerializer,
        request=BoardInputSerializer,
    )
    def post(self, request, group_id):
        serializer = self.BoardInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group = get_object_or_404(Group, id=group_id)
        board = create_board(
            name=serializer.validated_data.get("name"),
            description=serializer.validated_data.get("description"),
            permitted_users=serializer.validated_data.get("permitted_users", []),
            group=group,
            user=request.user,
        )
        return Response(self.BoardOutPutSerializer(board, context={"request": request}).data)

    @extend_schema(
        tags=['Boards'],
        responses=BoardOutPutSerializer,
    )
    def get(self, request, group_id):
        query = board_list(group_id=group_id)

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=self.BoardOutPutSerializer,
            queryset=query,
            request=request,
            view=self,
        )


class BoardDetailAPIView(ApiAuthMixin, APIView):
    permission_classes = [IsAuthenticated]

    class BoardDetailInputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=100)
        description = serializers.CharField(allow_blank=True)
        group = serializers.IntegerField()
        permitted_users = serializers.ListField(
            child=serializers.IntegerField(),
            allow_empty=True
        )

        def validate_group(self, group_id):
            if Group.objects.filter(id=group_id).exists():
                return group_id
            raise serializers.ValidationError("Group not found!")

    class BoardDetailOutPutSerializer(serializers.ModelSerializer):
        user = serializers.SerializerMethodField("get_user")
        group = serializers.SerializerMethodField("get_group")

        class Meta:
            model = Board
            fields = ["id", "name", "description", "group", "user", "permitted_users", "created_at", "updated_at"]

        def get_user(self, board):
            return board.user.email

        def get_group(self, board):
            return board.group.name

    @extend_schema(
        tags=['Boards'],
        responses=BoardDetailOutPutSerializer,
    )
    def get(self, request, board_id):
        board = board_detail(id=board_id)
        serializer = self.BoardDetailOutPutSerializer(board)
        return Response(serializer.data)

    @extend_schema(
        tags=['Boards'],
        request=BoardDetailInputSerializer,
        responses=BoardDetailOutPutSerializer,
    )
    def put(self, request, board_id):
        board = board_detail(id=board_id)
        serializer = self.BoardDetailInputSerializer(board, data=request.data)
        serializer.is_valid(raise_exception=True)
        board = update_board(board=board, **serializer.validated_data)
        serializer = self.BoardDetailOutPutSerializer(board)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Boards'],
        responses=None,
    )
    def delete(self, request, board_id):
        board = board_detail(id=board_id)
        delete_board(board=board)
        return Response(
            {"message": "Board deleted successfully."},
            status=status.HTTP_200_OK,
        )
