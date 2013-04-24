from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('djprogress.views',
    url(r'^$', 'overview', name='djprogress_overview'),
    url(r'^api/get/$', 'api_get_progress', name='djprogress_api_get'),
)
