from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse
from apps.visualizations.models import Query, Visualization, Job, Graph
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
    visualization.save()
    return redirect(query, visualization_id=visualization.id)

def show(request, visualization_id):
    visualization = get_object_or_404(Visualization, pk=visualization_id, account=request.user.account)
    if not visualization.query:
        return redirect(query, visualization_id=visualization.id)
    if not visualization.graph:
        return redirect(graph, visualization_id=visualization.id)
    return render(request, 'visualizations/show.html', dict(visualization=visualization))

def edit(request, visualization_id):
    visualization = get_object_or_404(Visualization, pk=visualization_id, account=request.user.account)
    return render(request, 'visualizations/edit.html', dict(visualization=visualization))

def update(request, visualization_id):
    visualization = get_object_or_404(Visualization, pk=visualization_id, account=request.user.account)
    visualization.name = request.POST.get('name')
    visualization.description = request.POST.get('description')
    visualization.save()
    return redirect(show, visualization_id=visualization.id)

def query(request, visualization_id):
    visualization = get_object_or_404(Visualization, pk=visualization_id, account=request.user.account)
    return render(request, 'visualizations/query.html', dict(visualization=visualization))

def query_update(request, visualization_id):
    visualization = get_object_or_404(Visualization, pk=visualization_id, account=request.user.account)
    if visualization.query:
        query = visualization.query
        query.script = request.POST.get('script')
        query.save()
    else:
        query = Query()
        query.script = request.POST.get('script')
        query.save()
        visualization.query = query
        visualization.save()
    if request.is_ajax():
        return redirect(execute, visualization_id=visualization.id)
    return redirect(graph, visualization_id=visualization.id)

def graph(request, visualization_id):
    visualization = get_object_or_404(Visualization, pk=visualization_id, account=request.user.account)
    return render(request, 'visualizations/graph.html', dict(visualization=visualization))

def graph_update(request, visualization_id):
    visualization = get_object_or_404(Visualization, pk=visualization_id, account=request.user.account)
    if visualization.graph:
        graph = visualization.graph
        graph.options = request.POST.get('options')
        graph.chart_type = request.POST.get('chart_type')
        graph.save()
    else:
        graph = Graph()
        graph.options = request.POST.get('options')
        graph.chart_type = request.POST.get('chart_type')
        graph.save()
        visualization.graph = graph
        visualization.save()
    return redirect(show, visualization_id=visualization.id)

def execute(request, visualization_id):
    visualization = get_object_or_404(Visualization, pk=visualization_id, account=request.user.account)
    err, job = visualization.execute()
    if err:
        return HttpResponse(err, 'application/json', status=404)
    return HttpResponse(json.dumps(dict(url=job.get_results_url())), 'application/json')

def remove(request, visualization_id):
    visualization = get_object_or_404(Visualization, pk=visualization_id, account=request.user.account)
    visualization.is_active = False
    visualization.save()
    return redirect(index)
