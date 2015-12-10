from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', 'apps.schedules.views.index', name='schedules_index'),
    url(r'^(?P<schedule_id>\d+)/remove$', 'apps.schedules.views.remove', name='schedules_remove'),
    url(r'^(?P<schedule_id>\d+)/send-all$', 'apps.schedules.views.send_all', name='schedules_send_all'),
    url(r'^(?P<schedule_id>\d+)/send-one$', 'apps.schedules.views.send_one', name='schedules_send_one'),
    url(r'^(?P<schedule_id>\d+)/show$', 'apps.schedules.views.show', name='schedules_show'),
]