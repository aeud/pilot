from apps.schedules.models import Schedule
from apps.visualizations.models import Visualization
from apps.jobs.models import Job
from apps.visualizations.views import execute_query
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.conf import settings

from premailer import transform

def run():
    schedules = Schedule.objects.filter(is_active=True)
    for schedule in schedules:
        visualization = schedule.visualization
        err = None
        try:
            job = Job.objects.filter(completed_at__isnull=False, query__visualization=visualization, cached_until__gte=timezone.now()).order_by('-start_at')[:1].get()
            if job.query_checksum != job.query.checksum:
                err, job = execute_query(schedule.created_by, visualization)
        except Job.DoesNotExist:
            err, job = execute_query(schedule.created_by, visualization)
        if not err:
            subject = 'Colors: Your report ' + visualization.name + ' is ready. [' + timezone.now().isoformat() + ']'
            rows, schema = job.get_rows()
            num_indexes = [i for i, v in enumerate(schema) if v.get('type') in ['FLOAT', 'INTEGER']]
            body = transform(loader.render_to_string('emails/visualization.html', dict(visualization=visualization,
                                                                                       job=job,
                                                                                       rows=rows,
                                                                                       absolute_url=settings.MAIN_HOST + reverse('jobs_show', kwargs=dict(job_id=job.id)),
                                                                                       schema=schema,
                                                                                       num_indexes=num_indexes)))
            email_message = EmailMultiAlternatives(subject, body, visualization.name + ' <colors+' + str(visualization.id) + '@luxola.com>', [schedule.email], reply_to=['colors@luxola.com'])
            html_email = body
            email_message.attach_alternative(html_email, 'text/html')
            email_message.send()
            #visualization.absolute_url(request),