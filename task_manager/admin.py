from django.contrib import admin
from django.conf import settings
from task_manager import models
from django.contrib.auth.models import User


class ProjectUserInline(admin.StackedInline):
    model = models.ProjectUser
    extra = 1


class CheckInInline(admin.StackedInline):
    model = models.CheckIn
    extra = 1


class WorkProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'due_date', 'priority', 'completion', 'note')

admin.site.register(models.TaskType)
admin.site.register(models.Result)
admin.site.register(models.ContactTemplate)
admin.site.register(models.Task)
admin.site.register(models.ProjectUser)
admin.site.register(models.WorkProject, WorkProjectAdmin)
admin.site.register(models.CheckIn)
admin.site.register(models.ProjectType)