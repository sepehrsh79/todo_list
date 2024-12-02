from django.contrib import admin

from todo_list.todo.models import Group, Board, Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "user", "board", "deadline", "completed")
    list_filter = ("created_at",)
    search_fields = ("id", "title", "description")
    list_editable = ("completed",)
    list_per_page = 25


class BoardAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "user", "group")
    list_filter = ("created_at",)
    search_fields = ("id", "name", "description")
    list_per_page = 25


class GroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user")
    list_filter = ("created_at",)
    search_fields = ("id", "name")
    list_per_page = 25


admin.site.register(Group, GroupAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(Task, TaskAdmin)
