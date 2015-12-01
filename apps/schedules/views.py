from django.shortcuts import render, get_object_or_404, redirect
from apps.schedules.models import Schedule, ScheduleOption

def index(request):
    schedules = Schedule.objects.filter(created_by=request.user, is_active=True)
    concerned_schedules = Schedule.objects.filter(email=request.user.email, is_active=True).exclude(id__in=[s.id for s in schedules])
    return render(request, 'schedules/index.html', dict(schedules=schedules,
                                                        concerned_schedules=concerned_schedules,))

def remove(request, schedule_id):
    schedule = get_object_or_404(Schedule, created_by=request.user, is_active=True, pk=schedule_id)
    schedule.is_active = False
    schedule.save()
    return redirect(index)