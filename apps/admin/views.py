from django.shortcuts import render
from apps.jobs.models import Job
from django.db import connection

def index(request):
    query = """
select
    i::date date,
    sum(case when j is not null then 1 else 0 end) jobs,
    sum(case when e is not null then 1 else 0 end) exports
from
    generate_series(
        CURRENT_DATE - '1 month'::interval + '1 day'::interval, CURRENT_DATE, '1 day'::interval
    ) i left join pilot.jobs_job j on (date(i) = date(j.completed_at)) left join pilot.jobs_jobexport e on (j.id = e.job_id)
group by i
order by i asc;
        """
    cursor = connection.cursor()
    cursor.execute(query)
    jobs = cursor.fetchall()
    query = """
select
    i::date date,
    sum(case when v.is_active is not null then 1 else 0 end) new_visualizations
from
    generate_series(
        CURRENT_DATE - '1 month'::interval + '1 day'::interval, CURRENT_DATE, '1 day'::interval
    ) i left join pilot.visualizations_visualization v on (date(i) = date(v.created_at))
group by i
order by i asc;
        """
    cursor = connection.cursor()
    cursor.execute(query)
    visualizations = cursor.fetchall()
    return render(request, 'admin/index.html', dict(jobs=jobs, visualizations=visualizations))
