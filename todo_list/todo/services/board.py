from todo_list.core.exceptions import ApplicationError
from todo_list.todo.models import Board, Group
from todo_list.users.models import BaseUser
from todo_list.common.services import model_update


def create_board(*, name: str, description: str, group: Group,  user: BaseUser) -> Board:
    try:
        return Board.objects.create(name=name, description=description, group=group, user=user)
    except Exception as ex:
        raise ApplicationError(message="Database Error - " + str(ex))


def update_board(*, board: Board, data) -> Board:
    fields = ["name", "description", "board"]
    try:
        board, has_updated = model_update(instance=board, fields=fields, data=data)
    except Exception as ex:
        raise ApplicationError(message="Database Error - " + str(ex))
    return board


def delete_board(*, board: Board) -> any:
    try:
        board.delete()
    except Exception as ex:
        raise ApplicationError(message="Database Error - " + str(ex))
