from django.db import models
from datetime import timedelta
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


class ProjectType(models.Model):
    title = models.CharField(max_length=200)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']


class ProjectStatus(models.Model):
    title = models.CharField(max_length=200)
    rank = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.title


class WorkProject(models.Model):
    title = models.CharField(max_length=200)
    start_date = models.DateField('Start Date', null=True)
    due_date = models.DateField('Due Date', null=True)
    description = models.TextField(null=True, blank=True)
    completion = models.IntegerField(null=True, blank=True)
    priority = models.IntegerField(null=True, blank=True)
    status = models.ForeignKey(ProjectStatus, null=True, blank=True)
    project_type = models.ForeignKey(ProjectType, null=True)
    copy_link = models.CharField(max_length=300, null=True, blank=True)
    final_link = models.CharField(max_length=300, null=True, blank=True)
    note = models.CharField(max_length=300, null=True, blank=True)

    def users_working(self):
        users = ProjectUser.objects.all()
        wu = []
        for user in users:
            last_check_in = CheckIn.objects.filter(user=user.user).filter(work_project=self).order_by('-pk')
            if last_check_in and not last_check_in[0].check_type:
                wu.append(last_check_in[0].user)
            users_working = wu
        return users_working

    def project_time(self):
        checkins = CheckIn.objects.filter(work_project=self).filter(check_type=True)
        i = 0
        time = "0:0:0"
        for checkin in checkins:
            if i == 0:
                time = checkin.time_logged()
                i = i + 1
            else:
                time = time + checkin.time_logged()
        return time

    def __unicode__(self):
        return self.title


class ProjectUser(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    on_projects = models.ManyToManyField(WorkProject, null=True, blank=True, related_name='project_user')

    def __unicode__(self):
        return self.user.get_full_name()


class Ticket(models.Model):
    title = models.CharField(max_length=200)
    assigned_to = models.ForeignKey(ProjectUser, null=True, blank=True)
    belongs_to = models.ForeignKey(User, null=True, blank=True)
    start_time = models.DateTimeField('Start Date', null=True, auto_now_add=True)
    complete_time = models.DateTimeField('Completion Date', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.ForeignKey(ProjectStatus, null=True, blank=True)
    project_type = models.ForeignKey(ProjectType, null=True)
    note = models.CharField(max_length=300, null=True, blank=True)

    def __unicode__(self):
        return self.title


class CheckIn(models.Model):
    work_project = models.ForeignKey(WorkProject,  related_name='checkin', verbose_name="Project")
    user = models.ForeignKey(ProjectUser)
    time = models.DateTimeField('Check In Time',  auto_now_add=True)
    check_type = models.BooleanField()
    completion = models.IntegerField(null=True, blank=True)
    note = models.CharField(max_length=300, null=True, blank=True)

    def time_logged(self):
        current = self.id
        user = self.user
        last_check_in = CheckIn.objects.filter(user=user).filter(pk__lt=current).filter(check_type=False).order_by('-pk')[0:1]
        if last_check_in:
            elapsed = self.time - last_check_in[0].time
        else:
            elapsed = "Check In"
        return elapsed

    def __unicode__(self):
        return self.user.user.get_full_name()
