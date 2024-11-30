from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from drf_spectacular.utils import extend_schema

from todo_list.api.pagination import LimitOffsetPagination, get_paginated_response_context

from todo_list.todo.models import Group
from todo_list.todo.selectors.group import group_list, group_detail
from todo_list.todo.services.group import create_group, update_group, delete_group
from todo_list.api.mixins import ApiAuthMixin


class GroupAPIView(ApiAuthMixin, APIView):
    permission_classes = [IsAuthenticated]

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class GroupInputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=100)

    class GroupOutPutSerializer(serializers.ModelSerializer):
        user = serializers.SerializerMethodField("get_user")

        class Meta:
            model = Group
            fields = ["id", "name", "user", "created_at", "updated_at"]

        def get_user(self, group):
            return group.user.email

    @extend_schema(
        tags=['Groups'],
        responses=GroupOutPutSerializer,
        request=GroupInputSerializer,
    )
    def post(self, request):
        serializer = self.GroupInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group = create_group(
            name=serializer.validated_data.get("name"),
            user=request.user,
        )
        return Response(self.GroupOutPutSerializer(group, context={"request": request}).data)

    @extend_schema(
        tags=['Groups'],
        responses=GroupOutPutSerializer,
    )
    def get(self, request):
        query = group_list()

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=self.GroupOutPutSerializer,
            queryset=query,
            request=request,
            view=self,
        )


class GroupDetailAPIView(ApiAuthMixin, APIView):
    permission_classes = [IsAuthenticated]

    class GroupDetailInputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=100)

    class GroupDetailOutPutSerializer(serializers.ModelSerializer):
        user = serializers.SerializerMethodField("get_user")

        class Meta:
            model = Group
            fields = ["id", "name", "user", "created_at", "updated_at"]

        def get_user(self, group):
            return group.user.email

    @extend_schema(
        tags=['Groups'],
        responses=GroupDetailOutPutSerializer,
    )
    def get(self, request, group_id):
        group = group_detail(id=group_id)
        serializer = self.GroupDetailOutPutSerializer(group)
        return Response(serializer.data) 

    @extend_schema(
        tags=['Groups'],
        request=GroupDetailInputSerializer,
        responses=GroupDetailOutPutSerializer,
    )
    def put(self, request, group_id):
        group = group_detail(id=group_id)
        serializer = self.GroupDetailInputSerializer(group, data=request.data)
        serializer.is_valid(raise_exception=True)
        update_group(group=group, **serializer.validated_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=['Groups'],
        responses=None,
    )
    def delete(self, request, group_id):
        group = group_detail(id=group_id)
        delete_group(group=group)
        return Response(
            {"message": "Group deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
