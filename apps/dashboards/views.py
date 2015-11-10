from django.shortcuts import render, redirect, get_object_or_404
from apps.dashboards.models import Dashboard
from apps.visualizations.models import Visualization

def index(request):
    all_visualizations = Visualization.objects.filter(is_active=True)
    return render(request, 'dashboards/index.html', dict(all_visualizations=all_visualizations))

def show(request, dashboard_id):
    dashboard = get_object_or_404(Dashboard, pk=dashboard_id)
    return render(request, 'dashboards/show.html', dict(dashboard=dashboard))

def new(request):
    return render(request, 'dashboards/new.html')

def create(request):
    dashboard = Dashboard()
    dashboard.save()
    return redirect(show, dashboard_id=dashboard.id)

def edit(request, dashboard_id):
    dashboard = get_object_or_404(Dashboard, pk=dashboard_id)
    return render(request, 'dashboards/edit.html', dict(dashboard=dashboard))

def update(request, dashboard_id):
    dashboard = get_object_or_404(Dashboard, pk=dashboard_id)
    dashboard.save()
    return redirect(show, dashboard_id=dashboard.id)

def remove(request, dashboard_id):
    dashboard = get_object_or_404(Dashboard, pk=dashboard_id)
    dashboard.is_active = False
    dashboard.save()
    return redirect(show, dashboard_id=dashboard.id)
