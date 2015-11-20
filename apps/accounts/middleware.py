import time
from importlib import import_module

from django.conf import settings
from django.utils.cache import patch_vary_headers
from django.utils.http import cookie_date
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
import re
from apps.dashboards.models import Dashboard


class CustomAuthMiddleware(object):
    def __init__(self):
        engine = import_module(settings.SESSION_ENGINE)
        self.SessionStore = engine.SessionStore

    def process_request(self, request):
        if re.search('login|logout|robots\.txt|test', request.path_info):
            return None
        if request.user.id:
            if request.user.account:
                request.stars = Dashboard.objects.filter(star_users=request.user).order_by('name')
            else:
                return render(request, 'errors/wait.html', status=403)
        else:
            return HttpResponseRedirect(reverse('login') + '?next=' + request.path)
        return None

    def process_response(self, request, response):
        if re.search('login', request.path_info) and request.META.get('HTTP_COOKIE'):
            for name in re.findall('bounceClientVisit\d+', request.META.get('HTTP_COOKIE')):
                response.delete_cookie(name, domain='.luxola.com')
            response.delete_cookie('_v1EmaticSolutions', domain='.luxola.com')
            response.delete_cookie('_v1EmaticSolutionsEI', domain='.luxola.com')
        return response