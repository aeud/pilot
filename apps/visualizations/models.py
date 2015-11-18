from django.db import models
from apps.accounts.models import Account
import hashlib

class Query(models.Model):
    script        = models.TextField()
    checksum      = models.CharField(max_length=32)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)
    unstack       = models.BooleanField(default=False)

    def duplicate(query):
        duplicate = Query(script=query.script,
                          unstack=query.unstack,)
        duplicate.save()
        return duplicate

    def new_from_dict(q):
        query = Query(script=q.get('script'),
                      unstack=q.get('unstack'),)
        query.save()
        return query

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

    def duplicate(graph):
        duplicate = Graph(options=graph.options,
                          chart_type=graph.chart_type,
                          map_script=graph.map_script,
                          options_is_stacked=graph.options_is_stacked,)
        duplicate.save()
        return duplicate

    def new_from_dict(g):
        graph = Graph(options=g.get('options'),
                      chart_type=g.get('chart_type'),
                      map_script=g.get('map_script'),
                      options_is_stacked=g.get('options_is_stacked'))
        graph.save()
        return graph

    def to_dict(self):
        return dict(options=self.options,
                    chart_type=self.chart_type,
                    map_script=self.map_script,
                    options_is_stacked=self.options_is_stacked)

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

    def duplicate(visualization):
        duplicate = Visualization(name='Copy of ' + visualization.name,
                                  description=visualization.description,
                                  account=visualization.account,
                                  cache_for=visualization.cache_for,
                                  cache_until=visualization.cache_until)
        if visualization.query:
            duplicate.query = Query.duplicate(visualization.query)
        if visualization.graph:
            duplicate.graph = Graph.duplicate(visualization.graph)
        duplicate.save()
        return duplicate

    def new_from_dict(request, v):
        visualization = Visualization(name=v.get('name'),
                                      description=v.get('description'),
                                      account=request.user.account,
                                      cache_for=v.get('cache_for'),
                                      cache_until=v.get('cache_until'),)
        if v.get('query'):
            visualization.query = Query.new_from_dict(v.get('query'))
        if v.get('graph'):
            visualization.graph = Graph.new_from_dict(v.get('graph'))

        visualization.save()
        return visualization

    def to_dict(self):
        return dict(name=self.name,
                    description=self.description,
                    cache_for=self.cache_for,
                    cache_until=self.cache_until.isoformat() if self.cache_until else None,
                    query=self.query.to_dict(),
                    graph=self.graph.to_dict(),)
