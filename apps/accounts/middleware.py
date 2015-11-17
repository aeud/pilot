import time
from importlib import import_module

from django.conf import settings
from django.utils.cache import patch_vary_headers
from django.utils.http import cookie_date
from django.shortcuts import render, redirect
import re
from apps.dashboards.models import Dashboard


class CustomAuthMiddleware(object):
    def __init__(self):
        engine = import_module(settings.SESSION_ENGINE)
        self.SessionStore = engine.SessionStore

    def process_request(self, request):
        if re.search('login|logout|robots\.txt', request.path_info):
            return None
        print(request.path_info)
        print(request.user)
        if request.user.id:
            if request.user.account:
                request.stars = Dashboard.objects.filter(star_users=request.user).order_by('name')
            else:
                return render(request, 'errors/wait.html', status=403)
        else:
            return render(request, 'errors/403.html', status=403)
        return None

    def process_response(self, request, response):
        return response