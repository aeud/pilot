from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import Http404, HttpResponse
from apps.jobs.models import Job, JobExport, JobExportRequest
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import gzip, json, csv, uuid
from io import StringIO, BytesIO

#import numpy as np
#import pandas as pd
#from matplotlib.backends.backend_agg import FigureCanvasAgg
#import matplotlib
#import matplotlib.pyplot as plt
#matplotlib.style.use('ggplot')

def rm_dict_value (value):
    if type(value) is dict:
        if 'v' in value:
            return value.get('v')
        elif 'label' in value:
            return value.get('label')
    return value

def rm_dict_row(row):
    return [rm_dict_value(value) for value in row]

def export_job(request, job):
    account = request.user.account
    conn = S3Connection(aws_access_key_id=account.aws_access_key_id, aws_secret_access_key=account.aws_secret_access_key)
    bucket = conn.get_bucket('lx-pilot')
    key = Key(bucket)
    key.key = job.cache_key
    string = gzip.decompress(key.get_contents_as_string())
    result = json.loads(string.decode('utf-8'))
    rows = result.get('rows')
    rows = [rm_dict_row(row) for row in rows]
    output = StringIO()
    writer = csv.writer(output)
    writer.writerows(rows)
    now = timezone.now()
    key_string = 'exports/' + str(now.year) + '/' + str(now.month) + '/' + str(now.day) + '/' + str(uuid.uuid4())
    export = JobExport(job=job, created_by=request.user, key=key_string)
    key = Key(bucket)
    key.key = export.key
    key.set_metadata('Content-Type', 'text/csv')
    key.set_metadata('Content-Encoding', 'gzip')
    key.set_contents_from_string(gzip.compress(bytes(output.getvalue(), 'utf-8')))
    key.close()
    key = Key(bucket)
    key.key = export.key
    export.save()
    return export

def export(request, job_id):
    job = get_object_or_404(Job, pk=job_id, query__visualization__account=request.user.account, cache_key__isnull=False)
    try:
        export = JobExport.objects.get(job=job)
    except JobExport.DoesNotExist:
        export = export_job(request, job)
    export_request = JobExportRequest(export=export, created_by=request.user)
    export_request.save()
    return redirect(export.generate_url())

#def plot(request, job_id):
#    job = get_object_or_404(Job, pk=job_id, query__visualization__account=request.user.account, cache_key__isnull=False)
##    try:
##        export = JobExport.objects.get(job=job)
##    except JobExport.DoesNotExist:
##        export = export_job(request, job)
##    export_request = JobExportRequest(export=export, created_by=request.user)
##    export_request.save()
#    account = request.user.account
#    conn = S3Connection(aws_access_key_id=account.aws_access_key_id, aws_secret_access_key=account.aws_secret_access_key)
#    bucket = conn.get_bucket('lx-pilot')
#    key = Key(bucket)
#    key.key = job.cache_key
#    string = gzip.decompress(key.get_contents_as_string())
#    result = json.loads(string.decode('utf-8'))
#    rows = result.get('rows')
#    rows = [rm_dict_row(row) for row in rows]
#    rows.pop(0)
#    df = pd.DataFrame(rows).set_index([0])
#    print(df)
#    df.plot(kind='bar', stacked=True)
#    buf = BytesIO()
#    plt.savefig(buf, format='png')
#    return HttpResponse(buf.getvalue(), content_type='image/png')
#export LC_ALL=en_US.UTF-8
#export LANG=en_US.UTF-8
