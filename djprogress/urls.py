from django.conf.urls import url

from djprogress.views import api_get_progress, overview, resolve, show_exception

app_name = "djprogress"

urlpatterns = [
    url(r'^$', overview, name='djprogress_overview'),
    url(r'^exception/(?P<progress_id>\d+)/$', show_exception, name='djprogress_show_exception'),
    url(r'^resolve/(?P<progress_id>\d+)/$', resolve, name='djprogress_resolve'),
    url(r'^api/get/$', api_get_progress, name='djprogress_api_get'),
]
