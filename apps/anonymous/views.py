from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from apps.anonymous.models import SharedDashboard, SharedVisualization
from datetime import timedelta

def index(request):
    shared_dashboards = SharedDashboard.objects.filter(is_active=True, created_by=request.user)
    for s in shared_dashboards:
        s.url = s.generate_url(request)
    shared_visualizations = SharedVisualization.objects.filter(is_active=True, created_by=request.user)
    for s in shared_visualizations:
        s.url = s.generate_url(request)
    return render(request, 'anonymous/index.html', dict(shared_dashboards=shared_dashboards,
                                                        shared_visualizations=shared_visualizations,))

@csrf_exempt
def update_shared_dashboard(request):
    shared_dashboard = get_object_or_404(SharedDashboard, pk=request.POST.get('id'), created_by=request.user)
    shared_dashboard.label = request.POST.get('label')
    shared_dashboard.valid_until = ((timezone.now() + timedelta(days=int(request.POST.get('days')))) if request.POST.get('days') else None)
    shared_dashboard.save()
    return HttpResponse(True, 'application/json')

def remove_dashboard(request, shared_dashboard_id):
    shared_dashboard = get_object_or_404(SharedDashboard, pk=shared_dashboard_id, created_by=request.user)
    shared_dashboard.is_active = False
    shared_dashboard.save()
    return redirect(index)