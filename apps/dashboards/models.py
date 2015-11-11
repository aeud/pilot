from django.db import models
from apps.visualizations.models import Visualization
from apps.accounts.models import Account, User

class Dashboard(models.Model):
    account    = models.ForeignKey(Account)
    name       = models.CharField(max_length=32)
    slug       = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active  = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    star_users = models.ManyToManyField(User)

    class Meta:
        unique_together = ('account', 'slug',)

class DashboardEntity(models.Model):
    dashboard      = models.ForeignKey(Dashboard)
    position       = models.IntegerField()
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)
    size           = models.CharField(max_length=32)
    visualization  = models.ForeignKey(Visualization)

class DashboardRedirection(models.Model):
    account        = models.ForeignKey(Account)
    dashboard      = models.ForeignKey(Dashboard)
    slug           = models.CharField(max_length=32, unique=True)
    created_at     = models.DateTimeField(auto_now_add=True)