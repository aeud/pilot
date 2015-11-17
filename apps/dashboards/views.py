from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max, Count
from apps.dashboards.models import Dashboard, DashboardRedirection, DashboardEntity
from apps.visualizations.models import Visualization
import json

def index(request):
    dashboards = Dashboard.objects.filter(account=request.user.account, is_active=True).annotate(entities_count=Count('dashboardentity__id', distinct=True)).order_by('name')
    return render(request, 'dashboards/index.html', dict(dashboards=dashboards))

def stars(request):
    print(request.COOKIES)
    last_dashboards = Dashboard.objects.filter(dashboardentity__visualization__query__job__jobrequest__created_by=request.user).annotate(request_created_at=Max('dashboardentity__visualization__query__job__jobrequest__created_at'), entities_count=Count('dashboardentity__id', distinct=True)).order_by('-request_created_at')[:8]
    stars = Dashboard.objects.filter(star_users=request.user).annotate(entities_count=Count('dashboardentity__id', distinct=True)).order_by('name')
    return render(request, 'dashboards/stars.html', dict(last_dashboards=last_dashboards, stars=stars))

def show(request, dashboard_id):
    dashboard = get_object_or_404(Dashboard, pk=dashboard_id, account=request.user.account)
    dashboard_entities = DashboardEntity.objects.filter(dashboard=dashboard, visualization__is_active=True).order_by('position')
    return render(request, 'dashboards/show.html', dict(dashboard=dashboard, dashboard_entities=dashboard_entities))

def play(request, dashboard_slug):
    try:
        dashboard = Dashboard.objects.get(slug=dashboard_slug, account=request.user.account)
    except Dashboard.DoesNotExist:
        try:
            dashboard_redirection = DashboardRedirection.objects.filter(slug=dashboard_slug, account=request.user.account)[:1].get()
            return redirect(play, dashboard_slug=dashboard_redirection.dashboard.slug)
        except dashboard_redirection.DoesNotExist:
            return Http404('Not found')
    dashboard_entities = DashboardEntity.objects.filter(dashboard=dashboard, visualization__is_active=True).order_by('position')
    return render(request, 'dashboards/play.html', dict(dashboard=dashboard,
                                                        dashboard_entities=dashboard_entities))

def new(request):
    return render(request, 'dashboards/new.html')

def create(request):
    dashboard = Dashboard(name=request.POST.get('name'), account=request.user.account, slug=request.POST.get('slug'))
    dashboard.save()
    return redirect(play, dashboard_slug=dashboard.slug)

def edit(request, dashboard_id):
    dashboard = get_object_or_404(Dashboard, pk=dashboard_id, account=request.user.account)
    return render(request, 'dashboards/edit.html', dict(dashboard=dashboard))

def update(request, dashboard_id):
    dashboard = get_object_or_404(Dashboard, pk=dashboard_id, account=request.user.account)
    dashboard.name = request.POST.get('name')
    if dashboard.slug != request.POST.get('slug'):
        dashboard_redirection = DashboardRedirection(dashboard=dashboard, slug=dashboard.slug, account=request.user.account)
        dashboard_redirection.save()
        dashboard.slug = request.POST.get('slug')
    dashboard.save()
    return redirect(play, dashboard_slug=dashboard.slug)

def remove(request, dashboard_id):
    dashboard = get_object_or_404(Dashboard, pk=dashboard_id, account=request.user.account)
    dashboard.is_active = False
    dashboard.save()
    return redirect(index)

def star(request, dashboard_id):
    dashboard = get_object_or_404(Dashboard, pk=dashboard_id, account=request.user.account)
    dashboard.star_users.add(request.user)
    dashboard.save()
    return redirect(play, dashboard_slug=dashboard.slug)

def unstar(request, dashboard_id):
    dashboard = get_object_or_404(Dashboard, pk=dashboard_id, account=request.user.account)
    dashboard.star_users.remove(request.user)
    dashboard.save()
    return redirect(play, dashboard_slug=dashboard.slug)

def visualization_new(request, dashboard_id):
    dashboard = get_object_or_404(Dashboard, pk=dashboard_id, account=request.user.account)
    if request.GET.get('visualization'):
        visualizations = Visualization.objects.filter(pk=request.GET.get('visualization'), account=request.user.account)
    else:
        visualizations = Visualization.objects.filter(account=request.user.account, is_active=True).order_by('name')
    next_value = DashboardEntity.objects.filter(dashboard=dashboard).count()
    return render(request, 'dashboards/add-visualization.html', dict(dashboard=dashboard,
                                                                     visualizations=visualizations,
                                                                     next_value=next_value,))

def visualization_create(request, dashboard_id):
    dashboard = get_object_or_404(Dashboard, pk=dashboard_id, account=request.user.account)
    visualization = get_object_or_404(Visualization, pk=request.POST.get('visualization'), account=request.user.account)
    dashboard_entity = DashboardEntity(dashboard=dashboard, visualization=visualization, size=request.POST.get('size'), position=request.POST.get('position'))
    dashboard_entity.save()
    return redirect(play, dashboard_slug=dashboard.slug)

def visualization_edit(request, dashboard_id, dashboard_entity_id):
    dashboard = get_object_or_404(Dashboard, pk=dashboard_id, account=request.user.account)
    dashboard_entity = get_object_or_404(DashboardEntity, pk=dashboard_entity_id, dashboard=dashboard)
    return render(request, 'dashboards/edit-visualization.html', dict(dashboard=dashboard,
                                                                      dashboard_entity=dashboard_entity))

def visualization_update(request, dashboard_id, dashboard_entity_id):
    dashboard = get_object_or_404(Dashboard, pk=dashboard_id, account=request.user.account)
    dashboard_entity = get_object_or_404(DashboardEntity, pk=dashboard_entity_id, dashboard=dashboard)
    dashboard_entity.size = request.POST.get('size')
    dashboard_entity.position=request.POST.get('position')
    dashboard_entity.save()
    return redirect(play, dashboard_slug=dashboard.slug)

def visualization_remove(request, dashboard_id, dashboard_entity_id):
    dashboard = get_object_or_404(Dashboard, pk=dashboard_id, account=request.user.account)
    dashboard_entity = get_object_or_404(DashboardEntity, pk=dashboard_entity_id, dashboard=dashboard)
    dashboard_entity.delete()
    return redirect(play, dashboard_slug=dashboard.slug)

def sort(request, dashboard_id):
    dashboard = get_object_or_404(Dashboard, pk=dashboard_id, account=request.user.account)
    dashboard_entities = DashboardEntity.objects.filter(dashboard=dashboard, visualization__is_active=True).order_by('position')
    return render(request, 'dashboards/sort.html', dict(dashboard=dashboard, dashboard_entities=dashboard_entities))

@csrf_exempt
def positions(request, dashboard_id):
    dashboard = get_object_or_404(Dashboard, pk=dashboard_id, account=request.user.account)
    positions = json.loads(request.body.decode('utf-8'))
    for row in positions:
        entity = get_object_or_404(DashboardEntity, pk=row[1], dashboard=dashboard)
        if entity.position != row[0]:
            entity.position = row[0]
            entity.save()
    return HttpResponse(json.dumps('coucou'), 'application/json')


