from django.conf.urls import include, url
from . import accounts, visualizations, dashboards, jobs

urlpatterns = [
    url(r'^$', 'apps.dashboards.views.stars', name='home'),
    url(r'^account/', include(accounts)),
    url(r'^visualizations/', include(visualizations)),
    url(r'^jobs/', include(jobs)),
    url(r'^dashboards/', include(dashboards)),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^login/google$', 'apps.accounts.views.login_google', name='login_google'),
    url(r'^login/google/callback$', 'apps.accounts.views.login_google_callback', name='login_google_callback'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
]