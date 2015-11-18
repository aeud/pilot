from django.db import models
from apps.visualizations.models import Visualization
from apps.accounts.models import Account, User
import uuid

class Dashboard(models.Model):
    account    = models.ForeignKey(Account)
    name       = models.CharField(max_length=32)
    slug       = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active  = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    star_users = models.ManyToManyField(User)

    class Meta:
        unique_together = ('account', 'slug',)

    def to_dict(self):
        dashboard_entities = DashboardEntity.objects.filter(dashboard=self, visualization__is_active=True).order_by('position')
        return dict(name=self.name,
                    slug=self.slug,
                    entities=[entity.to_dict() for entity in dashboard_entities],)

    def new_from_dict(request, d):
        try:
            Dashboard(name=d.get('name'), slug=d.get('slug'), account=request.user.account)
            slug = d.get('slug') + '-' + str(uuid.uuid1())
        except Dashboard.DoesNotExist:
            slug = d.get('slug')
        dashboard = Dashboard(name=d.get('name'),
                              slug=slug,
                              account=request.user.account,)
        dashboard.save()
        for e in d.get('entities'):
            DashboardEntity.new_from_dict(request, dashboard, e)
        return dashboard

class DashboardEntity(models.Model):
    dashboard      = models.ForeignKey(Dashboard)
    position       = models.IntegerField()
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)
    size           = models.CharField(max_length=32)
    visualization  = models.ForeignKey(Visualization)

    def to_dict(self):
        return dict(position=self.position,
                    size=self.size,
                    visualization=self.visualization.to_dict(),)

    def new_from_dict(request, dashboard, e):
        entity = DashboardEntity(size=e.get('size'),
                                 position=e.get('position'),
                                 dashboard=dashboard,
                                 visualization=Visualization.new_from_dict(request, e.get('visualization')))
        entity.save()
        return entity

class DashboardRedirection(models.Model):
    account        = models.ForeignKey(Account)
    dashboard      = models.ForeignKey(Dashboard)
    slug           = models.CharField(max_length=255, unique=True)
    created_at     = models.DateTimeField(auto_now_add=True)