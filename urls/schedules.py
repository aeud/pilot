from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', 'apps.schedules.views.index', name='schedules_index'),
    url(r'^(?P<schedule_id>\d+)/$', 'apps.schedules.views.remove', name='schedules_remove'),
]