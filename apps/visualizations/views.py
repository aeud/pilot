from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.db.models import Count
from apps.visualizations.models import Query, Visualization, Graph
from apps.jobs.models import Job, JobRequest
from apps.dashboards.models import Dashboard, DashboardEntity
import json, pandas as pd, httplib2, hashlib, gzip, json, pytz, uuid
from datetime import datetime, timedelta
from oauth2client.client import OAuth2Credentials as Credentials
from apiclient.errors import HttpError
from oauth2client import client
from apiclient.discovery import build

def index(request):
    visualizations = Visualization.objects.filter(account=request.user.account, is_active=True).annotate(dashboards_count=Count('dashboardentity__id')).order_by('name')
    return render(request, 'visualizations/index.html', dict(visualizations=visualizations))

def new(request):
    return render(request, 'visualizations/new.html')

def create(request):
    visualization = Visualization(name=request.POST.get('name'),
                                  description=request.POST.get('description'),
                                  account=request.user.account)
    if request.POST.get('cache_for'):
        visualization.cache_for = int(request.POST.get('cache_for'))
        visualization.cache_until = None
    elif request.POST.get('cache_until'):
        visualization.cache_for = None
        visualization.cache_until = request.POST.get('cache_until')
    else:
        visualization.cache_for = None
        visualization.cache_until = None
    visualization.save()
    return redirect(query, visualization_id=visualization.id)

def show(request, visualization_id):
    visualization = get_object_or_404(Visualization, pk=visualization_id, account=request.user.account)
    if not visualization.query:
        return redirect(query, visualization_id=visualization.id)
    if not visualization.graph:
        return redirect(graph, visualization_id=visualization.id)
    relative_dashboards = Dashboard.objects.filter(dashboardentity__visualization=visualization)
    all_dashboards = Dashboard.objects.filter(account=request.user.account, is_active=True).order_by('name')
    return render(request, 'visualizations/show.html', dict(visualization=visualization,
                                                            relative_dashboards=relative_dashboards,
                                                            all_dashboards=all_dashboards))

def edit(request, visualization_id):
    visualization = get_object_or_404(Visualization, pk=visualization_id, account=request.user.account)
    if request.GET.get('dashboard'):
        dashboard = get_object_or_404(Dashboard, pk=request.GET.get('dashboard'), account=request.user.account)
        return render(request, 'visualizations/edit.html', dict(visualization=visualization, dashboard=dashboard))
    return render(request, 'visualizations/edit.html', dict(visualization=visualization))

def update(request, visualization_id):
    visualization = get_object_or_404(Visualization, pk=visualization_id, account=request.user.account)
    visualization.name = request.POST.get('name')
    visualization.description = request.POST.get('description')
    if request.POST.get('cache_for'):
        visualization.cache_for = int(request.POST.get('cache_for'))
        visualization.cache_until = None
    elif request.POST.get('cache_until'):
        visualization.cache_for = None
        visualization.cache_until = request.POST.get('cache_until')
    else:
        visualization.cache_for = None
        visualization.cache_until = None
    visualization.save()
    if request.POST.get('dashboard'):
        dashboard = get_object_or_404(Dashboard, pk=request.POST.get('dashboard'), account=request.user.account)
        return redirect('dashboards_play', dashboard_slug=dashboard.slug)
    return redirect(show, visualization_id=visualization.id)

def query(request, visualization_id):
    visualization = get_object_or_404(Visualization, pk=visualization_id, account=request.user.account)
    if request.GET.get('dashboard'):
        dashboard = get_object_or_404(Dashboard, pk=request.GET.get('dashboard'), account=request.user.account)
        return render(request, 'visualizations/query.html', dict(visualization=visualization, dashboard=dashboard))
    return render(request, 'visualizations/query.html', dict(visualization=visualization))

def query_update(request, visualization_id):
    visualization = get_object_or_404(Visualization, pk=visualization_id, account=request.user.account)
    if visualization.query:
        query = visualization.query
        query.script = request.POST.get('script')
        query.unstack = int(request.POST.get('unstack', '0')) == 1
        query.save()
    else:
        query = Query()
        query.script = request.POST.get('script')
        query.unstack = int(request.POST.get('unstack', '0')) == 1
        query.save()
        visualization.query = query
        visualization.save()
    if request.POST.get('dashboard'):
        dashboard = get_object_or_404(Dashboard, pk=request.POST.get('dashboard'), account=request.user.account)
        return redirect('dashboards_play', dashboard_slug=dashboard.slug)
    return redirect(graph, visualization_id=visualization.id)

def graph(request, visualization_id):
    visualization = get_object_or_404(Visualization, pk=visualization_id, account=request.user.account)
    if request.GET.get('dashboard'):
        dashboard = get_object_or_404(Dashboard, pk=request.GET.get('dashboard'), account=request.user.account)
        return render(request, 'visualizations/graph.html', dict(visualization=visualization, dashboard=dashboard))
    return render(request, 'visualizations/graph.html', dict(visualization=visualization))

def graph_update(request, visualization_id):
    visualization = get_object_or_404(Visualization, pk=visualization_id, account=request.user.account)
    if visualization.graph:
        graph = visualization.graph
        graph.options = request.POST.get('options')
        graph.chart_type = request.POST.get('chart_type')
        graph.map_script = request.POST.get('map_script')
        graph.options_is_stacked = request.POST.get('options_is_stacked')
        graph.save()
    else:
        graph = Graph()
        graph.options = request.POST.get('options')
        graph.chart_type = request.POST.get('chart_type')
        graph.map_script = request.POST.get('map_script')
        graph.options_is_stacked = request.POST.get('options_is_stacked')
        graph.save()
        visualization.graph = graph
        visualization.save()
    if request.POST.get('dashboard'):
        dashboard = get_object_or_404(Dashboard, pk=request.POST.get('dashboard'), account=request.user.account)
        return redirect('dashboards_play', dashboard_slug=dashboard.slug)
    return redirect(show, visualization_id=visualization.id)

def execute_query(request, visualization):
    if visualization.query:
        job = Job(query=visualization.query, start_at=timezone.now(), query_checksum=visualization.query.checksum, created_by=request.user)
        if visualization.account.credentials:
            credentials = Credentials.from_json(visualization.account.credentials)
            http_auth = credentials.authorize(httplib2.Http())
            bigquery_service = build('bigquery', 'v2', http=http_auth)
            try:
                response = bigquery_service.jobs().query(projectId=visualization.account.bq_project.project_id,
                                                         body=dict(query=visualization.query.script)).execute()
            except HttpError as err:
                return [err.content, None]
            
            job.job_id = response.get('jobReference').get('jobId')
            job.total_rows = response.get('totalRows')
            job.completed_at = timezone.now()
            def replace_name(col):
                col['name'] = col.get('name').replace('_', ' ')
                return col
            schema = [replace_name(col) for col in response.get('schema').get('fields')]
            def cast_value(index, value, p=1):
                column = schema[index]
                column_type = column.get('type')
                if column_type == 'INTEGER':
                    return int((value if value else '0'))
                elif column_type == 'FLOAT':
                    return float(value if value else '0')
                elif column_type == 'TIMESTAMP' and (not visualization.query.unstack or p > 1):
                    return datetime.fromtimestamp(int(float(value))).isoformat() if value else None
                return value
            def change_type(t):
                if t == 'INTEGER' or t == 'FLOAT':
                    return 'number'
                elif t == 'STRING':
                    return 'string'
                elif t == 'BOOLEAN':
                    return 'boolean'
                elif t == 'DATE':
                    return 'date'
                elif t == 'TIMESTAMP':
                    return 'date'
                else:
                    return 'string'
            rows = [[cast_value(index, value.get('v')) for index, value in enumerate(row.get('f'))] for row in response.get('rows')]
            if visualization.query.unstack:
                p = pd.DataFrame(rows).set_index([0,1]).unstack(-1).fillna(0)
                matrix = p.as_matrix().tolist()
                rows_index = p.index.values
                columns_index = [v[1] for v in p.columns.values]
                s = schema[0]
                columns_index.insert(0, dict(id=s.get('name'), label=s.get('name'), type=change_type(s.get('type'))))
                new_matrix = [columns_index]
                for index, row in enumerate(matrix):
                    row = [cast_value(2, c, 2) for c in row]
                    row.insert(0, cast_value(0, rows_index[index], 2))
                    new_matrix.append(row)
                rows = new_matrix
            else:
                rows.insert(0, [dict(id=s.get('name'), label=s.get('name'), type=change_type(s.get('type'))) for s in schema])
            now = timezone.now()
            job.cache_key = 'jobs/' + str(now.year) + '/' + str(now.month) + '/' + str(now.day) + '/' + str(uuid.uuid4())
            job.save_results(rows, schema)
            if visualization.cache_for:
                job.cache_url = job.get_results_url(visualization.cache_for)
                job.cached_until = timezone.now() + timedelta(seconds=visualization.cache_for)
            elif visualization.cache_until:
                now = timezone.now()
                new_date = pytz.timezone('Asia/Singapore').localize(datetime(now.year, now.month, now.day, visualization.cache_until.hour, visualization.cache_until.minute))
                if new_date < now:
                    new_date = new_date + timedelta(days=1)
                job.cache_url = job.get_results_url((new_date-now).total_seconds())
                job.cached_until = pytz.timezone('Asia/Singapore').localize(new_date)
            job.save()
            return [None, job]
    return ['No query', None]

def execute(request, visualization_id):
    visualization = get_object_or_404(Visualization, pk=visualization_id, account=request.user.account)
    err = None
    try:
        job = Job.objects.filter(completed_at__isnull=False, query__visualization=visualization, cached_until__gte=datetime.now()).order_by('-start_at')[:1].get()
        if job.query_checksum != job.query.checksum:
            err, job = execute_query(request, visualization)
    except Job.DoesNotExist:
        err, job = execute_query(request, visualization)
    if err:
        return HttpResponse(err, 'application/json', status=404)
    job_request = JobRequest(created_by=request.user, job=job)
    job_request.save()
    return HttpResponse(json.dumps(dict(url=job.cache_url, export_url=request.build_absolute_uri(reverse('jobs_export', kwargs=dict(job_id=job.id))))), 'application/json')

def remove(request, visualization_id):
    visualization = get_object_or_404(Visualization, pk=visualization_id, account=request.user.account)
    visualization.is_active = False
    visualization.save()
    return redirect(index)

def duplicate(request, visualization_id):
    visualization = get_object_or_404(Visualization, pk=visualization_id, account=request.user.account)
    new_visualization = Visualization.duplicate(visualization)
    return redirect(edit, visualization_id=new_visualization.id)

def v_export(request, visualization_id):
    visualization = get_object_or_404(Visualization, pk=visualization_id, account=request.user.account)
    response = HttpResponse(json.dumps([visualization.to_dict()], sort_keys=True, indent=4), 'application/json')
    response['Content-Disposition'] = 'attachment; filename="visualization_' + str(visualization.id) + '.json"'
    return response

def v_export_all(request):
    visualizations = Visualization.objects.filter(account=request.user.account, is_active=True)
    response = HttpResponse(json.dumps([visualization.to_dict() for visualization in visualizations]), 'application/json')
    response['Content-Disposition'] = 'attachment; filename="visualization_all.json"'
    return response

def v_import(request):
    return render(request, 'visualizations/import.html')

def v_import_post(request):
    array = json.loads(request.POST.get('file'))
    for v in array:
        visualization = Visualization.new_from_dict(request, v)
    if len(array) == 1:
        return redirect(show, visualization_id=visualization.id)
    return redirect(index)

def quick_add_to_dashboard(request, visualization_id, dashboard_id):
    visualization = get_object_or_404(Visualization, pk=visualization_id, account=request.user.account)
    dashboard = get_object_or_404(Dashboard, pk=dashboard_id, account=request.user.account)
    try:
        entity = DashboardEntity.objects.filter(dashboard=dashboard, visualization=visualization)[:1].get()
    except DashboardEntity.DoesNotExist:
        next_value = DashboardEntity.objects.filter(dashboard=dashboard).count() + 1
        entity = DashboardEntity(dashboard=dashboard, visualization=visualization, position=next_value, size='col-md-6 col-lg-6')
        entity.save()
    return redirect('dashboards_visualizations_edit', dashboard_id=dashboard.id, dashboard_entity_id=entity.id)
    

