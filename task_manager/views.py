from django.shortcuts import render
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
            form = forms.NewTask()  # An unbound form
        project = Project.objects.get(pk=pk)
        return render(request, 'task-create.html', {
            'form': form, 'project': project
        })
    else:
        return render(request, 'not-authenticated.html')


def send_email(request, pk):
    if request.user.is_authenticated():
        if request.method == 'POST':  # If the form has been submitted...
            form = forms.NewEmail(request.POST)  # A form bound to the POST data
            if form.is_valid():  # All validation rules pass
                form.save()
                return HttpResponseRedirect(reverse('drss.views.project_detail', args=(pk,)))  # Redirect after POST
        else:
            form = forms.NewEmail()  # An unbound form
        project = Project.objects.get(pk=pk)
        return render(request, 'email-create.html', {
            'form': form, 'project': project
        })
    else:
        return render(request, 'not-authenticated.html')


def task_detail(request, pk, taskid):
    if request.user.is_authenticated():
        project = Project.objects.get(pk=pk)
        task = models.Task.objects.get(pk=taskid)
        context = {'task': task, 'project': project}
        return render(request, 'task-detail.html', context)
    else:
        return render(request, 'not-authenticated.html')
