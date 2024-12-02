import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from todo_list.users.models import BaseUser
from todo_list.tests.factories import (
    BaseUserFactory,
    GroupFactory,
    BoardFactory,
    TaskFactory,
)


@pytest.fixture
def user1():
    return BaseUserFactory()


@pytest.fixture
def user2():
    return BaseUserFactory()


@pytest.fixture
def api_client(user1):
    client = APIClient()
    refresh = RefreshToken.for_user(user1)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    return client


@pytest.fixture
def group(user1):
    return GroupFactory(user=user1)


@pytest.fixture
def board1(user1, user2, group):
    return BoardFactory.create(user=user1, group=group, permitted_users=(user1, user2))


@pytest.fixture
def board2(user1, group):
    return BoardFactory(user=user1, group=group, permitted_users=(user1,))


@pytest.fixture
def board3(user2, group):
    return BoardFactory(user=user2, group=group)


@pytest.fixture
def task1(user1, board1):
    return TaskFactory(user=user1, board=board1)


@pytest.fixture
def task2(user2, board2):
    return TaskFactory(user=user2, board=board2)


@pytest.fixture
def task3(user2, board3):
    return TaskFactory(user=user2, board=board3)


@pytest.fixture
def task4(user1, board3):
    return TaskFactory(user=user1, board=board3)
