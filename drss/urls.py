from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns
from drss import views

urlpatterns = patterns('drss.views',
                       url(r'^$', 'api_root'),
                       url(r'^projects/$', views.project_list, name='project-list'),
                       url(r'^projects/create$', views.project_create, name='project_create'),
                       url(r'^comments/$', views.CommentList.as_view(), name='comment-list'),
                       url(r'^documents/$', views.DocumentList.as_view(), name='document-list'),
                       url(r'^payments/$', views.PaymentList.as_view(), name='payment-list'),
                       url(r'^projects/(?P<pk>\d+)/$', views.project_detail, name='project_detail'),
                       url(r'^documents/(?P<pk>\d+)/$', views.document_detail, name='document-detail'),
                       url(r'^projects/(?P<pk>\d+)/deposit/$', views.deposit_detail, name='deposit_detail'),
                       url(r'^application/$', views.application, name='application'),
                       url(r'^application/(?P<app_id>\d+)/$', views.application_detail, name='application_detail'),
                       url(r'^application/(?P<app_id>\d+)/deposit/$', views.deposit, name='deposit_pay'),
                       url(r'^application/(?P<app_id>\d+)/documents/$', views.submit_docs, name='submit_docs'),
                       url(r'^thankyou/$', views.thankyou, name='thankyou'),
                       url(r'^support/$', views.support, name='thankyou'),
                       url(r'^payment_complete/$', views.payment_complete, name='payment_complete'),
                       )

# Format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])

# Default login/logout views
urlpatterns += patterns('',
                        url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
                        )
