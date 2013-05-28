from django.shortcuts import render
from datetime import date, datetime
from django.template import Template, Context
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from task_manager import forms, models
from drss.models import Project


def create_task(request, pk):
    if request.user.is_authenticated():
        if request.method == 'POST':  # If the form has been submitted...
            form = forms.NewTask(request.POST)  # A form bound to the POST data
            if form.is_valid():  # All validation rules pass
                form.save()
                return HttpResponseRedirect(reverse('drss.views.project_detail', args=(pk,)))  # Redirect after POST
        else:
            project = Project.objects.get(pk=pk)
            form = forms.NewTask(initial={'project': project, 'user': request.user})  # An unbound form
        project = Project.objects.get(pk=pk)
        return render(request, 'task-create.html', {
            'form': form, 'project': project
        })
    else:
        return render(request, 'not-authenticated.html')


def send_email(request, pk):
    if request.user.is_authenticated():
        if request.method == 'POST':  # If the form has been submitted...
            data = request.POST
            result = models.Result.objects.get(pk=3)
            project = Project.objects.get(pk=pk)
            task_type = models.TaskType.objects.get(title="email")
            task = models.Task(title=data['subject'],
                               subject=data['subject'],
                               body=data['body'],
                               completion_date=date.today(),
                               completion=True,
                               end_time=datetime.now(),
                               result=result,
                               task_type=task_type,
                               project=project,
                               user=request.user)
            task.save()
            task.send_email()
            return HttpResponseRedirect(reverse('drss.views.project_detail', args=(pk,)))  # Redirect after POST
        else:
            project = Project.objects.get(pk=pk)
            templates = models.ContactTemplate.objects.all()
            context = Context({'employee': request.user.get_full_name(), 'client': project.last_name})
            for template in templates:
                t = Template(template.body)
                template.body = t.render(context)
            return render(request, 'email-create.html', {'project': project, 'templates': templates})
    else:
        return render(request, 'not-authenticated.html')


def log_phone_call(request, pk):
    if request.user.is_authenticated():
        if request.method == 'POST':  # If the form has been submitted...
            data = request.POST
            result = models.Result.objects.get(pk=data['result'])
            project = Project.objects.get(pk=pk)
            task_type = models.TaskType.objects.get(title="phone")
            task = models.Task(title=data['subject'],
                               subject=data['subject'],
                               body=data['body'],
                               completion_date=date.today(),
                               completion=True,
                               end_time=datetime.now(),
                               result=result,
                               task_type=task_type,
                               project=project,
                               user=request.user)
            task.save()
            return HttpResponseRedirect(reverse('drss.views.project_detail', args=(pk,)))  # Redirect after POST
        else:
            project = Project.objects.get(pk=pk)
            return render(request, 'phonecall-create.html', {'project': project})
    else:
        return render(request, 'not-authenticated.html')


def task_detail(request, pk, taskid):
    if request.user.is_authenticated():
        if request.method == 'POST':
            data = request.POST
            task = models.Task.objects.get(pk=taskid)
            result = models.Result.objects.get(id=data['result'])
            task.body = data['body']
            task.completion = True
            task.completion_date = date.today()
            task.end_time = datetime.now()
            task.result = result
            task.save()
            return HttpResponseRedirect(reverse('drss.views.project_detail', args=(pk,)))
        task = models.Task.objects.get(pk=taskid)
        project = Project.objects.get(pk=pk)
        context = {'task': task, 'project': project}
        return render(request, 'task-detail.html', context)
    else:
        return render(request, 'not-authenticated.html')


def day_planner(request):
    tasks = models.Task.objects.filter(user=request.user).filter(completion=False)
    today = date.today()
    context = {'tasks': tasks, 'date': today}
    return render(request, 'day-planner.html', context)
