from django.db.models import QuerySet
from rest_framework.generics import get_object_or_404

from todo_list.todo.models import Task


def task_list(board_id: int) -> QuerySet[Task]:
    return Task.objects.filter(board_id=board_id)


def task_detail(*, id: int) -> Task:
    return get_object_or_404(Task, id=id)
