from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection
from django.db.models import Count
from apps.jobs.models import Job, JobRequest
from apps.accounts.models import User

def index(request):
    query = """
select
    i::date date,
    count(distinct j.id) jobs,
    count(distinct r.id) job_requests,
    count(distinct e.id) exports,
    count(distinct er.id) export_requests
from
    generate_series(
        CURRENT_DATE - '1 month'::interval + '1 day'::interval, CURRENT_DATE, '1 day'::interval
    ) i
    left join pilot.jobs_job j on (date(i) = date(j.completed_at))
    left join pilot.jobs_jobrequest r on (j.id = r.job_id)
    left join pilot.jobs_jobexport e on (j.id = e.job_id)
    left join pilot.jobs_jobexportrequest er on (e.id = er.export_id)
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

def users(request):
    users = User.objects.all().annotate(requests_count=Count('jobrequest__id', distinct=True)).order_by('email')
    return render(request, 'admin/users/index.html', dict(users=users))

def user_change_password(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'admin/users/change-password.html', dict(user=user))

def user_change_password_post(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.set_password(request.POST.get('password'))
    user.save()
    return redirect(users)

def last_jobs(request):
    last_jobs = Job.objects.values('id', 'created_by__email', 'completed_at', 'query__visualization__name').all().order_by('-completed_at')[:20]
    last_job_requests = JobRequest.objects.values('id', 'created_by__email', 'created_at', 'job__query__visualization__name').all().order_by('-created_at')[:20]
    return render(request, 'admin/last-jobs.html', dict(last_jobs=last_jobs,
                                                        last_job_requests=last_job_requests,))