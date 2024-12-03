# Django To-Do App

A modular To-Do application built with Django, featuring user authentication, task management, and collaborative boards. The app utilizes Celery and Celery Beat for scheduling background tasks and sending emails for overdue tasks.


## Features
- User Registration & Authentication: Secure user management.
  
- Task Management: Add, edit, delete, and organize tasks with deadlines.
  
- Collaborative Boards: Share boards with other users and manage task permissions.
  
- Deadline Reminders: Automatic Email notifications for overdue tasks.
  
- Asynchronous Processing: Background task handling with Celery and Redis.
  
- Responsive API: Designed with Django REST Framework (DRF), supporting pagination and robust validation.
  

## project setup

1- complete cookiecutter workflow (recommendation: leave project_slug empty) and go inside the project
```
cd todo_list
```

2- SetUp venv
```
virtualenv -p python3.12 venv
source venv/bin/activate
```

3- install Dependencies
```
pip install -r requirements_dev.txt
pip install -r requirements.txt
```

4- create your env
```
cp .env.example .env
```

5- Create tables
```
python manage.py migrate
```

6- spin off docker compose
```
docker compose -f docker-compose.dev.yml up -d
```

7- run the project
```
python manage.py runserver
```
##

While this project could be implemented using WebSockets and Django Channels for real-time updates, I chose to use RESTful APIs for simplicity, scalability, and broader compatibility with front-end frameworks and third-party integrations. Real-time updates can also be achieved using techniques such as polling, long polling, or Server-Sent Events (SSE), providing flexibility while maintaining a RESTful architecture.

