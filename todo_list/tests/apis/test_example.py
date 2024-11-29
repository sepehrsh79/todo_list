import pytest
from django.urls import reverse
from todo_list.users.models import BaseUser
from todo_list.example.models import Example
import json


@pytest.mark.django_db
def test_empty_example_api(api_client, user1, example1):
    url_ = reverse("api:example:example")

    response = api_client.get(url_, content_type="application/json")
    data = json.loads(response.content)

    assert response.status_code == 200
    assert data.get('results') == []
    assert data.get('limit') == 10 


