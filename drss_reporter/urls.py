from django.conf.urls import patterns, url
from drss_reporter import views

urlpatterns = patterns('drss_reporter.views',
                      url(r'^$', views.reports_list, name='reports_list'),
                       )
