from django.contrib import admin
from django.conf import settings
from task_manager import models
from django.contrib.auth.models import User


admin.site.register(models.TaskType)
admin.site.register(models.Result)
admin.site.register(models.ContactTemplate)
admin.site.register(models.Task)
