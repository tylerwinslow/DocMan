from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns
from drss.views import ProjectList, CommentList, DocumentList, PaymentList, ProjectDetail, CommentDetail, DocumentDetail, PaymentDetail, application, application_detail, thankyou, deposit

urlpatterns = patterns('drss.views',
                       url(r'^$', 'api_root'),
                       url(r'^projects/$', ProjectList.as_view(), name='project-list'),
                       url(r'^projects/$', ProjectDetail.as_view(), name='project-detail'),
                       url(r'^comments/$', CommentList.as_view(), name='comment-list'),
                       url(r'^documents/$', DocumentList.as_view(), name='document-list'),
                       url(r'^payments/$', PaymentList.as_view(), name='payment-list'),
                       url(r'^projects/(?P<pk>\d+)/$', ProjectDetail.as_view(), name='project-detail'),
                       url(r'^comments/(?P<pk>\d+)/$', CommentDetail.as_view(), name='comment-detail'),
                       url(r'^documents/(?P<pk>\d+)/$', DocumentDetail.as_view(), name='document-detail'),
                       url(r'^payments/(?P<pk>\d+)/$', PaymentDetail.as_view(), name='payment-detail'),
                       url(r'^application/$', application, name='application'),
                       url(r'^application/(?P<app_id>\d+)/$', application_detail, name='application_detail'),
                       url(r'^application/(?P<app_id>\d+)/deposit/$', deposit, name='deposit_pay'),
                       url(r'^thankyou/$', thankyou, name='thankyou'),
                       )

# Format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])

# Default login/logout views
urlpatterns += patterns('',
                        url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
                        )
