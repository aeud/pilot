from django.conf.urls import include, url
from . import accounts, visualizations, dashboards, jobs, admin
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete

urlpatterns = [
    url(r'^$', 'apps.dashboards.views.stars', name='home'),
    url(r'^account/', include(accounts)),
    url(r'^visualizations/', include(visualizations)),
    url(r'^jobs/', include(jobs)),
    url(r'^dashboards/', include(dashboards)),
    url(r'^admin/', include(admin)),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^login/password-reset$', password_reset, name='password_reset'),
    url(r'^login/password-reset/done$', password_reset_done, name='password_reset_done'),
    url(r'^login/password-reset/(?P<uidb64>.+)/(?P<token>.+)$', password_reset_confirm, name='password_reset_confirm'),
    url(r'^login/password-reset/complete', password_reset_complete, name='password_reset_complete'),
    url(r'^login/google$', 'apps.accounts.views.login_google', name='login_google'),
    url(r'^login/google/callback$', 'apps.accounts.views.login_google_callback', name='login_google_callback'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^test$', 'apps.accounts.views.test', name='test'),
]