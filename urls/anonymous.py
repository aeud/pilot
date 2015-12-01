from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', 'apps.anonymous.views.index', name='anonymous_index'),
    url(r'^/dashboard/update$', 'apps.anonymous.views.update_shared_dashboard', name='anonymous_update_shared_dashboard'),
    url(r'^/dashboard/(?P<shared_dashboard_id>\d+)/remove$', 'apps.anonymous.views.remove_dashboard', name='anonymous_remove_dashboard'),
]