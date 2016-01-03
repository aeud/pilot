from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.conf import settings
from datetime import timedelta
from apps.schedules.models import Schedule, ScheduleOption, GlobaleSchedule, GlobaleScheduleOption, GlobaleScheduleVisualization
from apps.visualizations.models import Visualization
from apps.dashboards.models import Dashboard
from apps.anonymous.models import SharedDashboard
from apps.jobs.models import Job
from apps.visualizations.views import execute_query
from premailer import transform
from functools import reduce


def index(request):
    schedules = Schedule.objects.filter(created_by=request.user, is_active=True).order_by('visualization__name')
    concerned_schedules = Schedule.objects.filter(email=request.user.email, is_active=True).exclude(id__in=[s.id for s in schedules])
    globale_schedules = GlobaleSchedule.objects.filter(created_by=request.user, is_active=True, account__isnull=False).order_by('subject')
    return render(request, 'schedules/index.html', dict(schedules=schedules,
                                                        concerned_schedules=concerned_schedules,
                                                        globale_schedules=globale_schedules,))

def remove(request, schedule_id):
    schedule = get_object_or_404(Schedule, created_by=request.user, is_active=True, pk=schedule_id)
    schedule.is_active = False
    schedule.save()
    return redirect(index)

def globale_remove(request, schedule_id):
    schedule = get_object_or_404(GlobaleSchedule, created_by=request.user, is_active=True, pk=schedule_id)
    schedule.is_active = False
    schedule.save()
    return redirect(index)

def prepare_email(schedule):
    visualization = schedule.visualization
    err = None
    try:
        job = Job.objects.filter(completed_at__isnull=False, query__visualization=visualization, cached_until__gte=timezone.now()).order_by('-start_at')[:1].get()
        if job.query_checksum != job.query.checksum:
            err, job = execute_query(schedule.created_by, visualization)
    except Job.DoesNotExist:
        err, job = execute_query(schedule.created_by, visualization)
    if not err:
        rows, schema = job.get_rows()
        header = rows.pop(0)
        num_indexes = [i for i, v in enumerate(schema) if v.get('type') in ['FLOAT', 'INTEGER']]
        integer_indexes = [i for i, v in enumerate(schema) if v.get('type') in ['INTEGER']]
        totals = None
        if schedule.show_sum:
            totals = [reduce(lambda x,y: x + y, list(map(lambda x: x[i], rows)), 0) if v.get('type') in ['FLOAT', 'INTEGER'] else None for i, v in enumerate(schema)]
        body = transform(loader.render_to_string('emails/visualization.html', dict(visualization=visualization,
                                                                                   job=job,
                                                                                   rows=rows,
                                                                                   absolute_url=settings.MAIN_HOST + reverse('visualizations_show', kwargs=dict(visualization_id=visualization.id)),
                                                                                   schema=schema,
                                                                                   num_indexes=num_indexes,
                                                                                   integer_indexes=integer_indexes,
                                                                                   header=header,
                                                                                   schedule=schedule,
                                                                                   totals=totals,)))
    return body

def prepare_email_globale(schedule):
    schedule_visualizations = GlobaleScheduleVisualization.objects.filter(schedule=schedule).order_by('position')
    jobs = []
    for schedule_visualization in schedule_visualizations:
        visualization = schedule_visualization.visualization
        err = None
        try:
            job = Job.objects.filter(completed_at__isnull=False, query__visualization=visualization, cached_until__gte=timezone.now()).order_by('-start_at')[:1].get()
            if job.query_checksum != job.query.checksum:
                err, job = execute_query(schedule.created_by, visualization)
        except Job.DoesNotExist:
            err, job = execute_query(schedule.created_by, visualization)
        if not err:
            rows, schema = job.get_rows()
            header = rows.pop(0)
            num_indexes = [i for i, v in enumerate(schema) if v.get('type') in ['FLOAT', 'INTEGER']]
            integer_indexes = [i for i, v in enumerate(schema) if v.get('type') in ['INTEGER']]
            totals = None
            if schedule_visualization.show_sum:
                totals = [reduce(lambda x,y: x + y, list(map(lambda x: x[i], rows)), 0) if v.get('type') in ['FLOAT', 'INTEGER'] else None for i, v in enumerate(schema)]
            jobs.append(dict(visualization=visualization,
                             job=job,
                             rows=rows,
                             absolute_url=settings.MAIN_HOST + reverse('visualizations_show', kwargs=dict(visualization_id=visualization.id)),
                             schema=schema,
                             num_indexes=num_indexes,
                             integer_indexes=integer_indexes,
                             header=header,
                             schedule=schedule_visualization,
                             totals=totals,))
    if schedule.linked_dashboard:
        if schedule.anonymous_link:
            shared_dashboard = SharedDashboard(dashboard=schedule.linked_dashboard,
                                               created_by=schedule.created_by,
                                               valid_until=timezone.now() + timedelta(days=2))
            shared_dashboard.save()
            dashbaord_url = settings.MAIN_HOST + shared_dashboard.generate_path()
        else:
            dashbaord_url = settings.MAIN_HOST + reverse('dashboards_play', kwargs=dict(dashboard_slug=schedule.linked_dashboard.slug))
    else:
        dashbaord_url = None 
    body = transform(loader.render_to_string('emails/visualization_globale.html', dict(jobs=jobs,
                                                                                       schedule=schedule,
                                                                                       absolute_url=settings.MAIN_HOST + reverse('visualizations_show', kwargs=dict(visualization_id=visualization.id)),
                                                                                       dashbaord_url=dashbaord_url,)))
    return body

def send_all(request, schedule_id):
    schedule = get_object_or_404(Schedule, created_by=request.user, is_active=True, pk=schedule_id)
    visualization = schedule.visualization
    body = prepare_email(schedule)
    email_message = EmailMultiAlternatives(schedule.generate_subject(), body, visualization.name + ' <colors+' + str(visualization.id) + '@luxola.com>', [schedule.email], reply_to=['colors@luxola.com'], bcc=['adrien.eudes.sf@gmail.com'])
    html_email = body
    email_message.attach_alternative(html_email, 'text/html')
    email_message.send()
    return HttpResponse(True, 'application/json')

def send_one(request, schedule_id):
    schedule = get_object_or_404(Schedule, is_active=True, pk=schedule_id, visualization__account=request.user.account)
    visualization = schedule.visualization
    body = prepare_email(schedule)
    email_message = EmailMultiAlternatives(schedule.generate_subject(), body, visualization.name + ' <colors+' + str(visualization.id) + '@luxola.com>', [request.user.email], reply_to=['colors@luxola.com'], bcc=['adrien.eudes.sf@gmail.com'])
    html_email = body
    email_message.attach_alternative(html_email, 'text/html')
    email_message.send()
    return HttpResponse(True, 'application/json')

def show(request, schedule_id):
    schedule = get_object_or_404(Schedule, is_active=True, pk=schedule_id, visualization__account=request.user.account)
    visualization = schedule.visualization
    return HttpResponse(prepare_email(schedule))

def new(request):
    visualizations = Visualization.objects.filter(is_active=True, account=request.user.account)
    dashboards = Dashboard.objects.filter(is_active=True, account=request.user.account)
    if not request.user.can_schedule:
        return Http404('Not Allowed here')
    return render(request, 'schedules/new.html', dict(visualizations=visualizations, dashboards=dashboards))

def create(request):
    if not request.user.can_schedule:
        return Http404('Not Allowed here')
    schedule = GlobaleSchedule(created_by=request.user,
                               account=request.user.account,
                               email=request.POST.get('email', request.user.email),
                               time=request.POST.get('time', 'morning'),
                               frequency=request.POST.get('frequency', 'daily'),
                               subject=request.POST.get('subject', 'No subject'),
                               message=request.POST.get('message', None),
                               anonymous_link=request.POST.get('anonymous_link', 'no') != 'no',)
    if request.POST.get('dashboard', 'no') != 'no':
        dashboard = get_object_or_404(Dashboard, pk=request.POST.get('dashboard', 'no'), account=request.user.account)
        schedule.linked_dashboard=dashboard
    schedule.save()
    for option in dict(request.POST).get('options[]', []):
        schedule_option = GlobaleScheduleOption(schedule=schedule, option=int(option))
        schedule_option.save()
    for i, visualization_id in enumerate(dict(request.POST).get('visualizations[]', [])):
        visualization = get_object_or_404(Visualization, pk=visualization_id, account=request.user.account)
        schedule_v = GlobaleScheduleVisualization(schedule=schedule, visualization=visualization, position=i, show_sum=dict(request.POST).get('totals[]', [])[i] == 'sum')
        schedule_v.save()
    return redirect(index)

def preview(request, schedule_id):
    schedule = get_object_or_404(GlobaleSchedule, is_active=True, pk=schedule_id, account=request.user.account)
    return HttpResponse(prepare_email_globale(schedule))

def edit(request, schedule_id):
    schedule = get_object_or_404(GlobaleSchedule, is_active=True, pk=schedule_id, account=request.user.account)
    #schedule_visualizations = get_object_or_404(GlobaleScheduleVisualization, is_active=True, pk=schedule_id, account=request.user.account)
    return render(request, 'schedules/edit.html')

def update(request, schedule_id):
    schedule = get_object_or_404(GlobaleSchedule, is_active=True, pk=schedule_id, account=request.user.account)
    return HttpResponse(prepare_email_globale(schedule))






