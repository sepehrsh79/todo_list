from django.db.models import QuerySet
from todo_list.example.models import Example


def create_example(*, title: str) -> QuerySet[Example]:
    return Example.objects.create(title=title)
