from django.db import models
from django.utils import timezone
from apps.visualizations.models import Visualization
from apps.dashboards.models import Dashboard
from apps.accounts.models import User, Account
import uuid

class Schedule(models.Model):
    visualization  = models.ForeignKey(Visualization)
    created_at     = models.DateTimeField(auto_now_add=True)
    created_by     = models.ForeignKey(User)
    email          = models.CharField(max_length=255)
    time           = models.CharField(max_length=255)
    frequency      = models.CharField(max_length=255)
    is_active      = models.BooleanField(default=True)
    show_sum       = models.BooleanField(default=False)

    def generate_subject(self):
        return 'Colors: Your report ' + self.visualization.name + ' is ready. [' + timezone.now().strftime('%d/%m/%Y') + ', ' + self.time + ']'


class ScheduleOption(models.Model):
    schedule  = models.ForeignKey(Schedule)
    option    = models.IntegerField()

class GlobaleSchedule(models.Model):
    created_at       = models.DateTimeField(auto_now_add=True)
    created_by       = models.ForeignKey(User)
    email            = models.CharField(max_length=255)
    time             = models.CharField(max_length=255)
    frequency        = models.CharField(max_length=255)
    subject          = models.CharField(max_length=255, null=False)
    is_active        = models.BooleanField(default=True)
    anonymous_link   = models.BooleanField(default=False)
    message          = models.TextField(null=True)
    account          = models.ForeignKey(Account, null=True)
    linked_dashboard = models.ForeignKey(Dashboard, null=True)

class GlobaleScheduleOption(models.Model):
    schedule  = models.ForeignKey(GlobaleSchedule)
    option    = models.IntegerField()

class GlobaleScheduleVisualization(models.Model):
    schedule       = models.ForeignKey(GlobaleSchedule)
    visualization  = models.ForeignKey(Visualization)
    position       = models.IntegerField()
    is_image       = models.BooleanField(default=False)
    show_sum       = models.BooleanField(default=False)
