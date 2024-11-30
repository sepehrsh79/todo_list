from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from todo_list.todo.models import Group


def group_list() -> QuerySet[Group]:
    return Group.objects.all()


def group_detail(*, id: int) -> Group:
    return get_object_or_404(Group, pk=id)


