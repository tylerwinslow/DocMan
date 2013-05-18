from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	                   url(r'^search/', include('haystack.urls')),
                       url(r'', include('drss.urls')),
                       url(r'', include('drss_reporter.urls')),
                       url(r'', include('social_auth.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                       url(r'^logout/$', 'django.contrib.auth.views.logout', name="auth_logout"),
                       )
