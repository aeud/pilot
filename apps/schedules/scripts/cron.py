from apps.schedules.models import Schedule
from apps.visualizations.models import Visualization
from apps.jobs.models import Job
from apps.visualizations.views import execute_query
from collections import namedtuple
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.conf import settings
from django.db import connection
from django.db.models import Q

from premailer import transform

def run(*args):
    time = args[0] if len(args) > 0 else 'morning'
    query = """
select distinct
    s.id
from
    pilot.schedules_schedule s
    left join pilot.schedules_scheduleoption o on (s.id = o.schedule_id)
where
    s.is_active
    and s.time = %s
    and (
        (s.frequency = 'monthly' and o.option = extract(day from current_timestamp + interval '8 hours'))
        or (s.frequency = 'weekly' and o.option = extract(dow from current_timestamp + interval '8 hours'))
        or s.frequency = 'daily'
    )
;
        """
    cursor = connection.cursor()
    cursor.execute(query, [time])
    schedules = cursor.fetchall()
    for schedule_id in schedules:
        schedule = Schedule.objects.get(pk=schedule_id[0])
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
                                                                                       absolute_url=settings.MAIN_HOST + reverse('visualizations_show', kwargs=dict(visualization_id=visualization.id)),
                                                                                       schema=schema,
                                                                                       num_indexes=num_indexes)))
            email_message = EmailMultiAlternatives(subject, body, visualization.name + ' <colors+' + str(visualization.id) + '@luxola.com>', [schedule.email], reply_to=['colors@luxola.com'])
            html_email = body
            email_message.attach_alternative(html_email, 'text/html')
            email_message.send()



