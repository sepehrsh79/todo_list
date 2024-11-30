from todo_list.core.exceptions import ApplicationError
from todo_list.todo.models import Task, Board
from todo_list.users.models import BaseUser
from todo_list.common.services import model_update


def create_task(*, title: str, description: str, board: Board,  user: BaseUser) -> Task:
    try:
        return Task.objects.create(title=title, description=description, board=board, user=user)
    except Exception as ex:
        raise ApplicationError(message="Database Error - " + str(ex))


def update_task(*, task: Task, data) -> Task:
    fields = ["title", "description", "board"]
    try:
        task, has_updated = model_update(instance=task, fields=fields, data=data)
    except Exception as ex:
        raise ApplicationError(message="Database Error - " + str(ex))
    return task


def delete_task(*, task: Task) -> any:
    try:
        task.delete()
    except Exception as ex:
        raise ApplicationError(message="Database Error - " + str(ex))
