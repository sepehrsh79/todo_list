from django.urls import path, include

urlpatterns = [
    path('todo/', include(('todo_list.todo.urls', 'todo'))),
    path('auth/', include(('todo_list.authentication.urls', 'auth')))
]
