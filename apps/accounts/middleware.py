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
        if request.user.id:
            request.stars = Dashboard.objects.filter(star_users=request.user).order_by('name')
        return None

    def process_response(self, request, response):
        return response