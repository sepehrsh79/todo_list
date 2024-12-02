import json

import pytest
from django.urls import reverse
from todo_list.todo.models import Task


@pytest.mark.django_db
def test_task_post_api(api_client, user1, board1):
    url_ = reverse("api:todo:task", kwargs={'board_id': board1.id})
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
    }

    response = api_client.post(url_, data=json.dumps(task_data), content_type="application/json")
    assert response.data["title"] == "Test Task"
    assert response.status_code == 201

    task = Task.objects.filter(title="Test Task").first()
    assert task is not None
    assert task.board == board1
    assert task.user == user1
