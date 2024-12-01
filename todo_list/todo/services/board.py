from todo_list.core.exceptions import ApplicationError
from todo_list.todo.models import Board, Group
from todo_list.users.models import BaseUser
from todo_list.common.services import model_update


def set_permitted_users(permitted_users: list, board: Board) -> None:
    checked_permitted_users = []
    for user_id in permitted_users:
        if BaseUser.objects.filter(id=user_id).exists():
            checked_permitted_users.append(user_id)
    board.permitted_users.set(checked_permitted_users)


def create_board(*, name: str, description: str, group: Group, permitted_users: list,  user: BaseUser) -> Board:
    try:
        board = Board.objects.create(name=name, description=description, group=group, user=user)
        set_permitted_users(permitted_users, board)
        return board
    except Exception as ex:
        raise ApplicationError(message="Database Error - " + str(ex))


def update_board(*, board: Board, **data) -> Board:
    fields = ["name", "description", "group_id"]
    permitted_users = data.pop('permitted_users')
    try:
        board, has_updated = model_update(instance=board, fields=fields, data=data)
        set_permitted_users(permitted_users, board)
    except Exception as ex:
        raise ApplicationError(message="Database Error - " + str(ex))
    return board


def delete_board(*, board: Board) -> any:
    try:
        board.delete()
    except Exception as ex:
        raise ApplicationError(message="Database Error - " + str(ex))
