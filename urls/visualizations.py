from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', 'apps.visualizations.views.index', name='visualizations_index'),
    url(r'^new$', 'apps.visualizations.views.new', name='visualizations_new'),
    url(r'^create$', 'apps.visualizations.views.create', name='visualizations_create'),
    url(r'^(?P<visualization_id>\d+)/$', 'apps.visualizations.views.show', name='visualizations_show'),
    url(r'^(?P<visualization_id>\d+)/edit$', 'apps.visualizations.views.edit', name='visualizations_edit'),
    url(r'^(?P<visualization_id>\d+)/update$', 'apps.visualizations.views.update', name='visualizations_update'),
    url(r'^(?P<visualization_id>\d+)/query$', 'apps.visualizations.views.query', name='visualizations_query'),
    url(r'^(?P<visualization_id>\d+)/query/update$', 'apps.visualizations.views.query_update', name='visualizations_query_update'),
    url(r'^(?P<visualization_id>\d+)/graph$', 'apps.visualizations.views.graph', name='visualizations_graph'),
    url(r'^(?P<visualization_id>\d+)/graph/update$', 'apps.visualizations.views.graph_update', name='visualizations_graph_update'),
    url(r'^(?P<visualization_id>\d+)/execute$', 'apps.visualizations.views.execute', name='visualizations_execute'),
    url(r'^(?P<visualization_id>\d+)/remove$', 'apps.visualizations.views.remove', name='visualizations_remove'),
    url(r'^(?P<visualization_id>\d+)/duplicate$', 'apps.visualizations.views.duplicate', name='visualizations_duplicate'),
    url(r'^(?P<visualization_id>\d+)/export$', 'apps.visualizations.views.v_export', name='visualizations_export'),
    url(r'^export$', 'apps.visualizations.views.v_export_all', name='visualizations_export_all'),
    url(r'^import$', 'apps.visualizations.views.v_import', name='visualizations_import'),
    url(r'^import/post$', 'apps.visualizations.views.v_import_post', name='visualizations_import_post'),
]