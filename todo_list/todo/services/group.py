from todo_list.core.exceptions import ApplicationError
from todo_list.todo.models import Group
from todo_list.users.models import BaseUser
from todo_list.common.services import model_update


def create_group(*, name: str, user: BaseUser) -> Group:
    try:
        return Group.objects.create(name=name, user=user)
    except Exception as ex:
        raise ApplicationError(message="Database Error - " + str(ex))


def update_group(*, group: Group, **data) -> Group:
    fields = ['name']
    try:
        group, has_updated = model_update(instance=group, fields=fields, data=data)
    except Exception as ex:
        raise ApplicationError(message="Database Error - " + str(ex))
    return group


def delete_group(*, group: Group) -> any:
    try:
        group.delete()
    except Exception as ex:
        raise ApplicationError(message="Database Error - " + str(ex))
