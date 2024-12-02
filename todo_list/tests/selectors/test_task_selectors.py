import pytest
from todo_list.todo.selectors.task import task_detail, task_list, check_board_permission_to_add_task


@pytest.mark.django_db
def test_task_list(board1, task1):
    a = task_list(board_id=board1.id)
    assert a.first() == task1


@pytest.mark.django_db
def test_get_task(task1):
    a = task_detail(id=task1.id)
    assert a.id == task1.id


@pytest.mark.django_db
def test_add_task_to_board_permitted_user(board1, user1):
    status = check_board_permission_to_add_task(board=board1, user=user1)
    assert status is True


@pytest.mark.django_db
def test_add_task_to_board_non_permitted_user(board2, user2):
    status = check_board_permission_to_add_task(board=board2, user=user2)
    assert status is False


@pytest.mark.django_db
def test_add_task_to_board_owner(board3, user2):
    status = check_board_permission_to_add_task(board=board3, user=user2)
    assert status is True


@pytest.mark.django_db
def test_add_task_to_board_non_owner(board3, user1):
    status = check_board_permission_to_add_task(board=board3, user=user1)
    assert status is False
