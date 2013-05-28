from django.shortcuts import render
from datetime import date, datetime
from django.template import Template, Context
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from drss.models import Project


def reports_list(request):
    return render(request, 'reports_list.html')
