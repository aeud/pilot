from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', 'apps.admin.views.index', name='admin_index'),
]