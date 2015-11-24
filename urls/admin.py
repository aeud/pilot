from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', 'apps.admin.views.index', name='admin_index'),
    url(r'^last-jobs$', 'apps.admin.views.last_jobs', name='admin_last_jobs'),
    url(r'^users/$', 'apps.admin.views.users', name='admin_users'),
    url(r'^users/(?P<user_id>\d+)/$', 'apps.admin.views.user_show', name='admin_users_show'),
    url(r'^users/(?P<user_id>\d+)/change-password$', 'apps.admin.views.user_change_password', name='admin_users_change_password'),
    url(r'^users/(?P<user_id>\d+)/change-password/post$', 'apps.admin.views.user_change_password_post', name='admin_users_change_password_post'),
    url(r'^users/(?P<user_id>\d+)/invite/auth$', 'apps.admin.views.auth_invite', name='admin_users_auth_invite'),
    url(r'^users/(?P<user_id>\d+)/invite/unauth$', 'apps.admin.views.unauth_invite', name='admin_users_unauth_invite'),
    url(r'^users/(?P<user_id>\d+)/account/(?P<account_id>\d+)$', 'apps.admin.views.user_quick_update_account', name='admin_user_quick_update_account'),
    url(r'^users/(?P<user_id>\d+)/remove-account$', 'apps.admin.views.user_quick_remove_account', name='admin_user_quick_remove_account'),
    url(r'^users/(?P<user_id>\d+)/remove$', 'apps.admin.views.user_remove', name='admin_user_remove'),
    url(r'^users/(?P<user_id>\d+)/active$', 'apps.admin.views.user_active', name='admin_user_active'),
]