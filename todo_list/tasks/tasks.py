from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now

from todo_list.todo.models import Task


@shared_task
def send_deadline_reminder():
    expired_tasks = Task.objects.filter(deadline__lt=now().date(), is_notified=False)
    for task in expired_tasks:
        send_mail(
            'Task Reminder',
            f'Remember to complete your task {task.id}!',
            'from@example.com',
            [task.created_by.email],
            fail_silently=False,
        )
        task.is_notified = True
        task.save()
