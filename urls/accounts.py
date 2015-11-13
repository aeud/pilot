from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', 'apps.accounts.views.index', name="accounts_index"),
    url(r'^bigquery/connect$', 'apps.accounts.views.bq_connect', name="accounts_bigquery_connect"),
    url(r'^bigquery/connect/callback$', 'apps.accounts.views.oauth_callback', name="accounts_bigquery_connect_callback"),
    url(r'^bigquery/choose-project$', 'apps.accounts.views.bq_choose_project', name="accounts_bigquery_choose_project"),
    url(r'^bigquery/choose-project/post$', 'apps.accounts.views.bq_choose_project_post', name="accounts_bigquery_choose_project_post"),
    url(r'^bigquery/remove-project$', 'apps.accounts.views.bq_remove_project', name="accounts_bigquery_remove_project"),
    url(r'^aws/connect$', 'apps.accounts.views.aws_connect', name="accounts_aws_connect"),
    url(r'^aws/connect/post$', 'apps.accounts.views.aws_connect_post', name="accounts_aws_connect_post"),
    url(r'^aws/remove$', 'apps.accounts.views.aws_remove', name="accounts_aws_remove"),
    url(r'^invite$', 'apps.accounts.views.invite', name="accounts_invite"),
    url(r'^invite/post$', 'apps.accounts.views.invite_post', name="accounts_invite_post"),
]