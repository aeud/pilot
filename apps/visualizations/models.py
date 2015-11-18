from django.db import models
from apps.accounts.models import Account
import hashlib

class Query(models.Model):
    script        = models.TextField()
    checksum      = models.CharField(max_length=32)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)
    unstack       = models.BooleanField(default=False)

    def to_dict(self):
        return dict(script=self.script,
                    unstack=self.unstack,)

    def save(self, *args, **kwargs):
        m = hashlib.md5()
        m.update(self.script.encode('utf-8'))
        if self.unstack:
            m.update('unstack'.encode('utf-8'))
        self.checksum = m.hexdigest()
        return super(Query, self).save(*args, **kwargs)

class Graph(models.Model):
    options            = models.TextField()
    chart_type         = models.CharField(max_length=255)
    map_script         = models.TextField(null=True)
    options_is_stacked = models.CharField(max_length=255)

    def to_dict(self):
        return dict(options=self.options,
                    chart_type=self.chart_type,
                    map_script=self.map_script,)

class Visualization(models.Model):
    is_active    = models.BooleanField(default=True)
    query        = models.OneToOneField(Query, null=True)
    graph        = models.OneToOneField(Graph, null=True)
    name         = models.CharField(max_length=255)
    description  = models.TextField(null=True)
    account      = models.ForeignKey(Account)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    cache_for    = models.IntegerField(null=True)
    cache_until  = models.TimeField(null=True)

    def to_dict(self):
        return dict(name=self.name,
                    description=self.description,
                    cache_for=self.cache_for,
                    cache_until=self.cache_until.isoformat() if self.cache_until else None,
                    query=self.query.to_dict(),
                    graph=self.graph.to_dict(),)
