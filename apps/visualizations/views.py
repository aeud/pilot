from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse
from apps.visualizations.models import Query, Visualization, Job, Graph
from apps.dashboards.models import Dashboard
import json

def index(request):
    visualizations = Visualization.objects.filter(account=request.user.account, is_active=True).order_by('-created_at')[:24]
    return render(request, 'visualizations/index.html', dict(visualizations=visualizations))

def new(request):
    return render(request, 'visualizations/new.html')

def create(request):
    visualization = Visualization(name=request.POST.get('name'),
                                  description=request.POST.get('description'),
                                  account=request.user.account)
    if request.POST.get('cache_for'):
        visualization.cache_for = int(request.POST.get('cache_for'))
        visualization.cache_until = None
    elif request.POST.get('cache_until'):
        visualization.cache_for = None
        visualization.cache_until = request.POST.get('cache_until')
    else:
        visualization.cache_for = None
        visualization.cache_until = None
    visualization.save()
    return redirect(query, visualization_id=visualization.id)

def show(request, visualization_id):
    visualization = get_object_or_404(Visualization, pk=visualization_id, account=request.user.account)
    if not visualization.query:
        return redirect(query, visualization_id=visualization.id)
    if not visualization.graph:
        return redirect(graph, visualization_id=visualization.id)
    relative_dashboards = Dashboard.objects.filter(dashboardentity__visualization=visualization)
    return render(request, 'visualizations/show.html', dict(visualization=visualization, relative_dashboards=relative_dashboards))

def edit(request, visualization_id):
    visualization = get_object_or_404(Visualization, pk=visualization_id, account=request.user.account)
    return render(request, 'visualizations/edit.html', dict(visualization=visualization))

def update(request, visualization_id):
    visualization = get_object_or_404(Visualization, pk=visualization_id, account=request.user.account)
    visualization.name = request.POST.get('name')
    visualization.description = request.POST.get('description')
    if request.POST.get('cache_for'):
        visualization.cache_for = int(request.POST.get('cache_for'))
        visualization.cache_until = None
    elif request.POST.get('cache_until'):
        visualization.cache_for = None
        visualization.cache_until = request.POST.get('cache_until')
    else:
        visualization.cache_for = None
        visualization.cache_until = None
    visualization.save()
    return redirect(show, visualization_id=visualization.id)

def query(request, visualization_id):
    visualization = get_object_or_404(Visualization, pk=visualization_id, account=request.user.account)
    if request.GET.get('dashboard'):
        dashboard = get_object_or_404(Dashboard, pk=request.GET.get('dashboard'), account=request.user.account)
        return render(request, 'visualizations/query.html', dict(visualization=visualization, dashboard=dashboard))
    return render(request, 'visualizations/query.html', dict(visualization=visualization))

def query_update(request, visualization_id):
    visualization = get_object_or_404(Visualization, pk=visualization_id, account=request.user.account)
    if visualization.query:
        query = visualization.query
        query.script = request.POST.get('script')
        query.unstack = int(request.POST.get('unstack', '0')) == 1
        query.save()
    else:
        query = Query()
        query.script = request.POST.get('script')
        query.unstack = int(request.POST.get('unstack', '0')) == 1
        query.save()
        visualization.query = query
        visualization.save()
    if request.is_ajax():
        return redirect(execute, visualization_id=visualization.id)
    if request.POST.get('dashboard'):
        dashboard = get_object_or_404(Dashboard, pk=request.POST.get('dashboard'), account=request.user.account)
        return redirect('dashboards_play', dashboard_slug=dashboard.slug)
    return redirect(graph, visualization_id=visualization.id)

def graph(request, visualization_id):
    visualization = get_object_or_404(Visualization, pk=visualization_id, account=request.user.account)
    if request.GET.get('dashboard'):
        dashboard = get_object_or_404(Dashboard, pk=request.GET.get('dashboard'), account=request.user.account)
        return render(request, 'visualizations/graph.html', dict(visualization=visualization, dashboard=dashboard))
    return render(request, 'visualizations/graph.html', dict(visualization=visualization))

def graph_update(request, visualization_id):
    visualization = get_object_or_404(Visualization, pk=visualization_id, account=request.user.account)
    if visualization.graph:
        graph = visualization.graph
        graph.options = request.POST.get('options')
        graph.chart_type = request.POST.get('chart_type')
        graph.map_script = request.POST.get('map_script')
        graph.save()
    else:
        graph = Graph()
        graph.options = request.POST.get('options')
        graph.chart_type = request.POST.get('chart_type')
        graph.map_script = request.POST.get('map_script')
        graph.save()
        visualization.graph = graph
        visualization.save()
    if request.POST.get('dashboard'):
        dashboard = get_object_or_404(Dashboard, pk=request.POST.get('dashboard'), account=request.user.account)
        return redirect('dashboards_play', dashboard_slug=dashboard.slug)
    return redirect(show, visualization_id=visualization.id)

def execute(request, visualization_id):
    visualization = get_object_or_404(Visualization, pk=visualization_id, account=request.user.account)
    err, job = visualization.execute()
    if err:
        return HttpResponse(err, 'application/json', status=404)
    return HttpResponse(json.dumps(dict(url=job.cache_url)), 'application/json')

def remove(request, visualization_id):
    visualization = get_object_or_404(Visualization, pk=visualization_id, account=request.user.account)
    visualization.is_active = False
    visualization.save()
    return redirect(index)

def duplicate(request, visualization_id):
    visualization = get_object_or_404(Visualization, pk=visualization_id, account=request.user.account)
    new_visualization = Visualization(name='Copy of ' + visualization.name,
                                      description=visualization.description,
                                      account=visualization.account,
                                      cache_for=visualization.cache_for,
                                      cache_until=visualization.cache_until)
    if visualization.query:
        new_query = Query(script=visualization.query.script, unstack=visualization.query.unstack)
        new_query.save()
        new_visualization.query = new_query

    if visualization.graph:
        new_graph = Graph(options=visualization.graph.options,
                          chart_type=visualization.graph.chart_type,
                          map_script=visualization.graph.map_script)
        new_graph.save()
        new_visualization.graph = new_graph
    new_visualization.save()
    return redirect(edit, visualization_id=new_visualization.id)

def v_export(request, visualization_id):
    visualization = get_object_or_404(Visualization, pk=visualization_id, account=request.user.account)
    response = HttpResponse(json.dumps([visualization.to_dict()]), 'application/json')
    response['Content-Disposition'] = 'attachment; filename="visualization_' + str(visualization.id) + '.json"'
    return response

def v_export_all(request):
    visualizations = Visualization.objects.filter(account=request.user.account, is_active=True)
    response = HttpResponse(json.dumps([visualization.to_dict() for visualization in visualizations]), 'application/json')
    response['Content-Disposition'] = 'attachment; filename="visualization_all.json"'
    return response

def v_import(request):
    return render(request, 'visualizations/import.html')

def v_import_post(request):
    array = json.loads(request.POST.get('file'))
    for v in array:
        visualization = Visualization(name=v.get('name'),
                                      description=v.get('description'),
                                      account=request.user.account,
                                      cache_for=v.get('cache_for'),
                                      cache_until=v.get('cache_until'),)
        if v.get('query'):
            query = Query(script=v.get('query').get('script'),
                          unstack=v.get('query').get('unstack'),)
            query.save()
            visualization.query = query
        if v.get('graph'):
            graph = Graph(options=v.get('graph').get('options'),
                          chart_type=v.get('graph').get('chart_type'),
                          map_script=v.get('graph').get('map_script'),)
            graph.save()
            visualization.graph = graph

        visualization.save()
    return redirect(index)