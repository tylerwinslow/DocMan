from django.shortcuts import render
from datetime import date, datetime
from django.template import Template, Context
from django_easyfilters import FilterSet
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from task_manager import forms, models
from drss.models import Project


class WorkProjectFilterSet(FilterSet):
    fields = [
        'project_type',

    ]


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
    tasks = models.Task.objects.filter(user=request.user).filter(completion=False).filter(scheduled_date__lte=date.today()).order_by('scheduled_date')
    today = date.today()
    context = {'tasks': tasks, 'date': today}
    return render(request, 'day-planner.html', context)


def creative(request):
    work_projects = models.WorkProject.objects.all()
    projectsfilter = WorkProjectFilterSet(work_projects, request.GET)
    tickets = {'name': "sample ticket"}
    context = {'work_projects': projectsfilter.qs, 'projectsfilter': projectsfilter, 'tickets': tickets}
    return render(request, 'creative.html', context)


def work_project_detail(request, pk):
    if request.user.is_authenticated():
        project = models.WorkProject.objects.get(pk=pk)
        checkins = project.checkin.all()
        try:
            working = not checkins.filter(user__user=request.user)[0].check_type
        except IndexError:
            working = False
        context = {'project': project, 'checkins': checkins, 'working': working}
        return render(request, 'work-project.html', context)
    else:
        return render(request, 'not-authenticated.html')


def check_in(request, pk):
    if request.user.is_authenticated():
        project = models.WorkProject.objects.get(pk=pk)
        user = models.ProjectUser.objects.get(user=request.user)
        new_check = models.CheckIn(work_project=project, user=user, check_type=False)
        new_check.save()
        return HttpResponseRedirect(reverse('task_manager.views.work_project_detail', args=(pk,)))
    else:
        return render(request, 'not-authenticated.html')


def check_out(request, pk):
    if request.user.is_authenticated():
        if request.method == 'POST':
            completion = request.POST['completion']
            recap = request.POST['recap']
            project = models.WorkProject.objects.get(pk=pk)
            project.note = recap
            project.save()
            user = models.ProjectUser.objects.get(user=request.user)
            new_check = models.CheckIn(work_project=project, user=user, check_type=True, note=recap, completion=completion)
            new_check.save()
            return HttpResponseRedirect(reverse('task_manager.views.work_project_detail', args=(pk,)))
        project = models.WorkProject.objects.get(pk=pk)
        user = models.ProjectUser.objects.get(user=request.user)
        new_check = models.CheckIn(work_project=project, user=user, check_type=True)
        new_check.save()
        return HttpResponseRedirect(reverse('task_manager.views.work_project_detail', args=(pk,)))
    else:
        return render(request, 'not-authenticated.html')
