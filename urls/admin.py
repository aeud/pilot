from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', 'apps.admin.views.index', name='admin_index'),
    url(r'^last-jobs$', 'apps.admin.views.last_jobs', name='admin_last_jobs'),
    url(r'^users/$', 'apps.admin.views.users', name='admin_users'),
    url(r'^users/(?P<user_id>\d+)/$', 'apps.admin.views.user_show', name='admin_users_show'),
    url(r'^users/(?P<user_id>\d+)/change-password$', 'apps.admin.views.user_change_password', name='admin_users_change_password'),
    url(r'^users/(?P<user_id>\d+)/change-password/post$', 'apps.admin.views.user_change_password_post', name='admin_users_change_password_post'),
]