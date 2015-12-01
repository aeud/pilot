from django.shortcuts import render, get_object_or_404, redirect
from apps.schedules.models import Schedule, ScheduleOption

def index(request):
    schedules = Schedule.objects.filter(created_by=request.user, is_active=True)
    return render(request, 'schedules/index.html', dict(schedules=schedules))

def remove(request, schedule_id):
    schedule = get_object_or_404(Schedule, created_by=request.user, is_active=True, pk=schedule_id)
    schedule.is_active = False
    schedule.save()
    return redirect(index)