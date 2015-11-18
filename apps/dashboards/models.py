from django.db import models
from apps.visualizations.models import Visualization
from apps.accounts.models import Account, User

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

class DashboardRedirection(models.Model):
    account        = models.ForeignKey(Account)
    dashboard      = models.ForeignKey(Dashboard)
    slug           = models.CharField(max_length=32, unique=True)
    created_at     = models.DateTimeField(auto_now_add=True)