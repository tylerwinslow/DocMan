from django.db import models
from django.contrib.auth.models import User
from templated_email import send_templated_mail
from drss.models import Project, Department, Comment
from datetime import date


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
    task_type = models.ForeignKey(TaskType,  related_name='Task Type', verbose_name="Task Type", null=True)
    scheduled_date = models.DateField('Scheduled Date', null=True, blank=True)
    completion_date = models.DateField('Completion Date', null=True, blank=True)
    start_time = models.DateTimeField('Start Time', null=True, blank=True)
    end_time = models.DateTimeField('End Time', null=True, blank=True)
    completion_time = models.FloatField(null=True, blank=True, default=0)
    completion = models.BooleanField()
    result = models.ForeignKey(Result,  related_name='Result', verbose_name="Result", null=True, blank=True)
    recording = models.FileField(upload_to="documents", null=True, blank=True)

    def past_due(self):
        if date.today() > self.scheduled_date and not self.completion:
            return True
        else:
            return False

    def send_email(self):
        send_templated_mail(template_name='drss_sales',
                            from_email=self.user.email,
                            recipient_list=[self.project.email, 'steve.castle@drssmail.com'],
                            context={'subject': self.subject, 'body': self.body}
                            )

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        super(Task, self).save(*args, **kwargs)
        if self.body:
            body = self.body
            user = self.user
            project = self.project
            comment = Comment(body=body, author=user, internal=False, project=project)
            comment.save()

    def __unicode__(self):
        return self.title
