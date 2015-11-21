from django.conf.urls import include, url

urlpatterns = [
    url(r'^(?P<job_id>\d+)/export$', 'apps.jobs.views.export', name='jobs_export'),
#    url(r'^(?P<job_id>\d+)/plot$', 'apps.jobs.views.plot', name='jobs_plot'),
]