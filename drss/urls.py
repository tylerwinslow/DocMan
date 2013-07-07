from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns
from drss import views

urlpatterns = patterns('drss.views',
                       url(r'^$', 'api_root'),
                       url(r'^projects/$', views.project_list, name='project-list'),
                       url(r'^real-estate/$', views.real_estate_list, name='real-estate-list'),
                       url(r'^real-estate/approval-queue$', views.site_approval_list, name='site-approval-list'),
                       url(r'^projects/create$', views.project_create, name='project_create'),
                       url(r'^comments/$', views.CommentList.as_view(), name='comment-list'),
                       url(r'^documents/$', views.DocumentList.as_view(), name='document-list'),
                       url(r'^payments/$', views.PaymentList.as_view(), name='payment-list'),
                       url(r'^funding-advisors/$', views.fundingadvisor_list, name='funding-advisor-list'),
                       url(r'^funding-advisors/(?P<user_id>\d+)/$', views.fundingadvisor_detail, name='fundingadvisor_detail'),
                       url(r'^salespeople/$', views.salesperson_list, name='salesperson_list'),
                       url(r'^salespeople/(?P<user_id>\d+)/$', views.salesperson_detail, name='salesperson_detail'),
                       url(r'^status/$', views.StatusList.as_view(), name='status-list'),
                       url(r'^projects/(?P<pk>\d+)/$', views.project_detail, name='project_detail'),
                       url(r'^api/projects/(?P<pk>\d+)/$', views.ProjectApi.as_view(), name='project_api'),
                       url(r'^documents/(?P<pk>\d+)/$', views.document_detail, name='document-detail'),
                       url(r'^loi/(?P<pk>\d+)/$', views.loi_detail, name='loi_detail'),
                       url(r'^projects/(?P<pk>\d+)/deposit/$', views.deposit_detail, name='deposit_detail'),
                       url(r'^projects/(?P<pk>\d+)/refund/$', views.process_refund, name='process_refund'),
                       url(r'^projects/(?P<pk>\d+)/turnover_to_re/$', views.turnover_to_re, name='process_turnover_to_re'),
                       url(r'^projects/(?P<pk>\d+)/sites/(?P<site_id>\d+)$', views.site_detail, name='site_detail'),
                       url(r'^projects/(?P<pk>\d+)/sites/$', views.site_create, name='create_site'),
                       url(r'^application/$', views.application, name='application'),
                       url(r'^sdl/$', views.sales_deposit_log, name='sales_deposit_log'),
                       url(r'^assign/finance/$', views.assign_finance, name='assign_finance'),
                       url(r'^refunds/$', views.refunds, name='refunds'),
                       url(r'^application/(?P<app_id>\d+)/$', views.application_detail, name='application_detail'),
                       url(r'^application/(?P<app_id>\d+)/deposit/$', views.deposit, name='deposit_pay'),
                       url(r'^application/(?P<app_id>\d+)/documents/$', views.submit_docs, name='submit_docs'),
                       url(r'^application/(?P<app_id>\d+)/print/$', views.print_app, name='print_app'),
                       url(r'^thankyou/$', views.thankyou, name='thankyou'),
                       url(r'^support/$', views.support, name='thankyou'),
                       url(r'^payment_hook$', views.payment_hook, name='payment_hook'),
                       url(r'^payment_complete/$', views.payment_complete, name='payment_complete'),
                       )

# Format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])

# Default login/logout views
urlpatterns += patterns('',
                        url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
                        )
