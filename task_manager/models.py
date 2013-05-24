from django.db import models
from django.contrib.auth.models import User
from drss.models import Project, Department


class TaskType(models.Model):
    title = models.CharField(max_length=64)

    def __unicode__(self):
        return self.title


class Result(models.Model):
    title = models.CharField(max_length=64)
    quality = models.CharField(max_length=64)

    def __unicode__(self):
        return self.title


class ContactTemplate(models.Model):
    template_type = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    body = models.TextField(max_length=5000)

    def __unicode__(self):
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User,  related_name='contact_employee', verbose_name="Employee")
    project = models.ForeignKey(Project,  related_name='contact_project', verbose_name="Project", null=True, blank=True)
    template = models.ForeignKey(ContactTemplate,  related_name='email_template', verbose_name="Email Template", null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField(max_length=5000, null=True, blank=True)
    department = models.ForeignKey(Department,  related_name='department', verbose_name="Department", null=True, blank=True)
    task_type = models.ForeignKey(TaskType,  related_name='Task Type', verbose_name="Task Type", null=True, blank=True)
    scheduled_date = models.DateField('Scheduled Date', null=True, blank=True)
    completion_date = models.DateField('Completion Date', null=True, blank=True)
    start_time = models.DateField('Completion Date', null=True, blank=True)
    end_time = models.DateField('Completion Date', null=True, blank=True)
    completion_time = models.FloatField(null=True, blank=True)
    completion = models.BooleanField()
    result = models.ForeignKey(Result,  related_name='Result', verbose_name="Result", null=True, blank=True)
    recording = models.FileField(upload_to="documents", null=True, blank=True)

    def __unicode__(self):
        return self.title