from django.db import models

from todo_list.common.models import BaseModel
from todo_list.users.models import BaseUser


class Board(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="boards")

    def __str__(self):
        return self.name


class Task(BaseModel):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="user_tasks")
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="board_tasks")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
