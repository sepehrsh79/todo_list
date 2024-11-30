from django.db.models import QuerySet
from rest_framework.generics import get_object_or_404

from todo_list.todo.models import Board


def board_list(group_id: int) -> QuerySet[Board]:
    return Board.objects.filter(group_id=group_id)


def board_detail(*, id: int) -> Board:
    return get_object_or_404(Board, id=id)
