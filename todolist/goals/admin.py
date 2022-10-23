from django.contrib import admin

from goals.models import GoalCategory, Goal


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'created', 'updated', 'is_deleted']
    search_fields = ['title', 'user']
    readonly_fields = ['created', 'updated']
    list_display_links = ['id', 'title']
    list_filter = ['is_deleted']


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'category', 'due_date', 'status', 'priority']
    search_fields = ['title', 'user']
    readonly_fields = ['created', 'updated']
    list_display_links = ['id', 'title']
    list_filter = ['created', 'updated', 'due_date']
