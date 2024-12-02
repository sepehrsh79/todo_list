import datetime
import pytest

from django.utils import timezone

from todo_list.todo.models import Task
from todo_list.todo.services.task import create_task, update_task, delete_task


@pytest.mark.django_db
def test_create_post(user1, board1):
    deadline = timezone.now() + datetime.timedelta(days=10)
    a = create_task(user=user1, title="foo", description="Content", board=board1, deadline=deadline)

    assert a.user == user1
    assert a.board == board1
    assert a.title == "foo"
    assert a.description == "Content"
    assert a.deadline == deadline


@pytest.mark.django_db
def test_update_task(task1, board2):
    new_title = "Updated Task Title"
    new_description = "Updated Task Description"
    new_deadline = timezone.now().date() + datetime.timedelta(days=20)
    new_board_id = board2.id

    updated_task = update_task(
        task=task1,
        title=new_title,
        description=new_description,
        board_id=new_board_id,
        deadline=new_deadline
    )

    assert updated_task.title == new_title
    assert updated_task.description == new_description
    assert updated_task.deadline == new_deadline
    assert updated_task.board_id == new_board_id


@pytest.mark.django_db
def test_delete_task(task1):
    delete_task(task=task1)

    with pytest.raises(Task.DoesNotExist):
        Task.objects.get(id=task1.id)
