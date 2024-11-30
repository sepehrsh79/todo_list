from rest_framework import serializers

from todo_list.users.models import BaseUser


class PermittedUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ("id", "email",)
