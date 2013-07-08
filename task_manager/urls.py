from django.conf.urls import patterns, url
from task_manager import views

urlpatterns = patterns('task_manager.views',
                       url(r'^day-planner/$', views.day_planner, name='day-planner'),
                       url(r'^projects/(?P<pk>\d+)/tasks/$', views.create_task, name='task-list'),
                       url(r'^projects/(?P<pk>\d+)/emails/$', views.send_email, name='email-list'),
                       url(r'^projects/(?P<pk>\d+)/phonecalls/$', views.log_phone_call, name='email-list'),
                       url(r'^projects/(?P<pk>\d+)/tasks/(?P<taskid>\d+)/$', views.task_detail, name='task-detail'),
                       url(r'^creative/$', views.creative, name='creative'),
                       url(r'^creative/workproject/$', views.create_work_project, name='workproject-create'),
                       url(r'^creative/workproject/(?P<pk>\d+)/$', views.work_project_detail, name='workproject-detail'),
                       url(r'^creative/ticket/(?P<pk>\d+)/complete$', views.complete_ticket, name='ticket-complete'),
                       url(r'^creative/ticket/$', views.create_ticket, name='ticket-create'),
                       url(r'^creative/ticket/(?P<pk>\d+)/$', views.ticket_detail, name='ticket-detail'),
                       url(r'^creative/workproject/(?P<pk>\d+)/check-in/$', views.check_in, name='workproject-checkin'),
                       url(r'^creative/workproject/(?P<pk>\d+)/check-out/$', views.check_out, name='workproject-checkout'),
                       )
