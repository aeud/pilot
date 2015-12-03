from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.conf import settings
from apps.schedules.models import Schedule, ScheduleOption
from apps.visualizations.models import Visualization
from apps.jobs.models import Job
from apps.visualizations.views import execute_query
from premailer import transform


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
        num_indexes = [i for i, v in enumerate(schema) if v.get('type') in ['FLOAT', 'INTEGER']]
        body = transform(loader.render_to_string('emails/visualization.html', dict(visualization=visualization,
                                                                                   job=job,
                                                                                   rows=rows,
                                                                                   absolute_url=settings.MAIN_HOST + reverse('visualizations_show', kwargs=dict(visualization_id=visualization.id)),
                                                                                   schema=schema,
                                                                                   num_indexes=num_indexes)))
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