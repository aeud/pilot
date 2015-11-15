from django.conf.urls import include, url

urlpatterns = [
    url(r'^(?P<job_id>\d+)/export$', 'apps.jobs.views.export', name='jobs_export'),
]