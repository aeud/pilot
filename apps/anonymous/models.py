from django.db import models
from django.core.urlresolvers import reverse
from apps.visualizations.models import Visualization
from apps.dashboards.models import Dashboard
from apps.accounts.models import User
import uuid

class SharedVisualization(models.Model):
    created_at     = models.DateTimeField(auto_now_add=True)
    is_active      = models.BooleanField(default=True)
    visualization  = models.ForeignKey(Visualization)
    created_by     = models.ForeignKey(User, null=True)
    token          = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    valid_until    = models.DateTimeField(null=True)
    label          = models.CharField(max_length=255, null=True)

    def generate_url(self, request):
        return request.build_absolute_uri(reverse('visualizations_show_anonymous', kwargs=dict(visualization_id=self.visualization.id, token=str(self.token))))

class SharedDashboard(models.Model):
    created_at     = models.DateTimeField(auto_now_add=True)
    is_active      = models.BooleanField(default=True)
    dashboard      = models.ForeignKey(Dashboard)
    created_by     = models.ForeignKey(User, null=True)
    token          = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    valid_until    = models.DateTimeField(null=True)
    label          = models.CharField(max_length=255, null=True)

    def generate_url(self, request):
        return request.build_absolute_uri(reverse('dashboards_play_anonymous', kwargs=dict(dashboard_id=self.dashboard.id, token=str(self.token))))
    
