from django.db import models
from apps.visualizations.models import Visualization
from apps.accounts.models import Account, User

class Dashboard(models.Model):
    account    = models.ForeignKey(Account)
    name       = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active  = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

class DashboardEntity(models.Model):
    dashboard      = models.ForeignKey(Dashboard)
    position       = models.IntegerField()
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)
    size           = models.IntegerField()
    visualization  = models.ForeignKey(Visualization)