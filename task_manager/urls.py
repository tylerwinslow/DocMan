from django.conf.urls import patterns, url
from task_manager import views

urlpatterns = patterns('task_manager.views',
                       url(r'^day-planner/$', views.day_planner, name='day-planner'),
                       url(r'^projects/(?P<pk>\d+)/tasks/$', views.create_task, name='task-list'),
                       url(r'^projects/(?P<pk>\d+)/emails/$', views.send_email, name='email-list'),
                       url(r'^projects/(?P<pk>\d+)/phonecalls/$', views.log_phone_call, name='email-list'),
                       url(r'^projects/(?P<pk>\d+)/tasks/(?P<taskid>\d+)/$', views.task_detail, name='task-detail'),

                       )
