from django.urls import path, include

urlpatterns = [
    path('example/', include(('todo_list.example.urls', 'example')))
]
