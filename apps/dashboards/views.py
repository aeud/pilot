from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max, Count
from apps.dashboards.models import Dashboard, DashboardRedirection, DashboardEntity, DashboardRequest
from apps.visualizations.models import Visualization, Query, Graph
from apps.anonymous.models import SharedDashboard
import json, uuid

def index(request):
    dashboards = Dashboard.objects.filter(account=request.user.account, is_active=True).annotate(entities_count=Count('dashboardentity__id', distinct=True)).order_by('name')
    return render(request, 'dashboards/index.html', dict(dashboards=dashboards))

def my(request):
    stars = Dashboard.objects.filter(is_active=True, star_users=request.user).annotate(entities_count=Count('dashboardentity__id', distinct=True)).order_by('name')
    best_dashboards = Dashboard.objects.values('name', 'id', 'slug').filter(is_active=True, dashboardrequest__created_by=request.user).annotate(requests_count=Count('dashboardrequest__id', distinct=True), entities_count=Count('dashboardentity__id', distinct=True), last_visited_at=Max('dashboardrequest__created_at')).order_by('-requests_count')[:5]
    last_dashboards = Dashboard.objects.values('name', 'id', 'slug').filter(is_active=True, dashboardrequest__created_by=request.user).annotate(entities_count=Count('dashboardentity__id', distinct=True), last_visited_at=Max('dashboardrequest__created_at')).order_by('-last_visited_at').distinct()[:5]
    return render(request, 'dashboards/stars.html', dict(last_dashboards=last_dashboards, stars=stars, best_dashboards=best_dashboards))

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
    DashboardRequest(dashboard=dashboard, created_by=request.user).save()
    return render(request, 'dashboards/play.html', dict(dashboard=dashboard,
                                                        dashboard_entities=dashboard_entities))

def play_anonymous(request, dashboard_id, token):
    shared_dashboard = get_object_or_404(SharedDashboard, dashboard__id=dashboard_id, token=token)
    dashboard = shared_dashboard.dashboard
    if request.user.id and dashboard.account == request.user.account:
        return redirect(play, dashboard_slug=dashboard.slug)
    if not shared_dashboard.is_active or (shared_dashboard.valid_until and shared_dashboard.valid_until < timezone.now()):
        return render(request, 'errors/403.html', status=403)
    dashboard_entities = DashboardEntity.objects.filter(dashboard=dashboard, visualization__is_active=True).order_by('position')
    DashboardRequest(dashboard=dashboard, created_by=shared_dashboard.created_by).save()
    return render(request, 'dashboards/play_anonymous.html', dict(anonymous_token=token,
                                                                  dashboard=dashboard,
                                                                  dashboard_entities=dashboard_entities,))

def new(request):
    return render(request, 'dashboards/new.html')

def create(request):
    dashboard = Dashboard(name=request.POST.get('name'), account=request.user.account, slug=request.POST.get('slug'), created_by=request.user)
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

def hard_remove(request, dashboard_id):
    dashboard = get_object_or_404(Dashboard, pk=dashboard_id, account=request.user.account)
    dashboard_entities = DashboardEntity.objects.filter(dashboard=dashboard, visualization__is_active=True).order_by('position')
    dashboard.is_active = False
    dashboard.save()
    for entity in dashboard_entities:
        v = entity.visualization
        v.is_active = False
        v.save()
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
    next_value = DashboardEntity.objects.filter(dashboard=dashboard).count() + 1
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

def d_export(request, dashboard_id):
    dashboard = get_object_or_404(Dashboard, id=dashboard_id, account=request.user.account)
    response = HttpResponse(json.dumps(dict(dashboard=dashboard.to_dict()), sort_keys=True, indent=4), 'application/json')
    response['Content-Disposition'] = 'attachment; filename="dashboard_' + str(dashboard.id) + '.json"'
    return response

def d_import(request):
    return render(request, 'dashboards/import.html')

def d_import_post(request):
    account = request.user.account
    d = json.loads(request.POST.get('file')).get('dashboard')
    dashboard = Dashboard.new_from_dict(request, d)
    return redirect(play, dashboard_slug=dashboard.slug)

def share(request, dashboard_id):
    dashboard = get_object_or_404(Dashboard, id=dashboard_id, account=request.user.account)
    shared_dashboard = SharedDashboard(dashboard=dashboard,
                                       created_by=request.user,)
    shared_url = shared_dashboard.generate_url(request)
    shared_dashboard.save()
    return HttpResponse(shared_url, 'application/json')

