from django.db.models import QuerySet
from rest_framework.generics import get_object_or_404

from todo_list.todo.models import Task, Board
from todo_list.users.models import BaseUser


def task_list(board_id: int) -> QuerySet[Task]:
    return Task.objects.filter(board_id=board_id)


def task_detail(*, id: int) -> Task:
    return get_object_or_404(Task, id=id)


def check_board_permission_to_add_task(board: Board, user: BaseUser):
    if board and hasattr(board, "permitted_users"):
        permitted_users = board.permitted_users.all()
        if user != board.user and (permitted_users and user not in permitted_users):
            return False
    return True
