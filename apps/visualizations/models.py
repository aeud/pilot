from django.db import models
from django.utils import timezone
from apps.accounts.models import Account
from oauth2client import client
from apiclient.discovery import build
from apiclient.errors import HttpError
import httplib2, hashlib, gzip, json, pytz, uuid
from oauth2client.client import OAuth2Credentials as Credentials
from datetime import datetime, timedelta
from boto.s3.connection import S3Connection
from boto.s3.key import Key

class Query(models.Model):
    script        = models.TextField()
    checksum      = models.CharField(max_length=32)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        m = hashlib.md5()
        m.update(self.script.encode('utf-8'))
        self.checksum = m.hexdigest()
        return super(Query, self).save(*args, **kwargs)

class Graph(models.Model):
    options       = models.TextField()
    chart_type    = models.CharField(max_length=255)

class Visualization(models.Model):
    is_active    = models.BooleanField(default=True)
    query        = models.OneToOneField(Query, null=True)
    graph        = models.OneToOneField(Graph, null=True)
    name         = models.CharField(max_length=255)
    description  = models.TextField(null=True)
    account      = models.ForeignKey(Account)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    cache_for    = models.IntegerField(null=True)
    cache_until  = models.TimeField(null=True)

    def execute(self):
        err = None
        try:
            job = Job.objects.filter(completed_at__isnull=False, query__visualization=self, cached_until__gte=datetime.now()).order_by('-start_at')[:1].get()
            if job.query_checksum != job.query.checksum:
                err, job = self.execute_query()
        except Job.DoesNotExist:
            err, job = self.execute_query()
        return [err, job]

    def execute_query(self):
        if self.query:
            job = Job(query=self.query, start_at=timezone.now(), query_checksum=self.query.checksum)
            if self.account.credentials:
                credentials = Credentials.from_json(self.account.credentials)
                http_auth = credentials.authorize(httplib2.Http())
                bigquery_service = build('bigquery', 'v2', http=http_auth)
                try:
                    response = bigquery_service.jobs().query(projectId=self.account.bq_project.project_id,
                                                             body=dict(query=self.query.script)).execute()
                except HttpError as err:
                    return [err.content, None]
                
                job.job_id = response.get('jobReference').get('jobId')
                job.total_rows = response.get('totalRows')
                job.completed_at = timezone.now()
                def replace_name(col):
                    col['name'] = col.get('name').replace('_', ' ')
                    return col
                schema = [replace_name(col) for col in response.get('schema').get('fields')]
                def cast_value(index, value):
                    column = schema[index]
                    column_type = column.get('type')
                    if column_type == 'INTEGER':
                        return dict(v=int(value))
                    elif column_type == 'FLOAT':
                        return dict(v=float(value))
                    return dict(v=value)
                rows = [[cast_value(index, value.get('v')) for index, value in enumerate(row.get('f'))] for row in response.get('rows')]
                now = timezone.now()
                job.cache_key = 'jobs/' + str(now.year) + '/' + str(now.month) + '/' + str(now.day) + '/' + str(uuid.uuid4())
                #job.save()
                #job.save_schema(schema)
                job.save_results(rows, schema)
                if self.cache_for:
                    job.cache_url = job.get_results_url(self.cache_for)
                    job.cached_until = timezone.now() + timedelta(seconds=self.cache_for)
                    job.save()
                elif self.cache_until:
                    now = timezone.now()
                    new_date = pytz.timezone('Asia/Singapore').localize(datetime(now.year, now.month, now.day, self.cache_until.hour, self.cache_until.minute))
                    if new_date < now:
                        new_date = new_date + timedelta(days=1)
                    job.cache_url = job.get_results_url((new_date-now).total_seconds())
                    job.cached_until = new_date
                    job.save()
                job.save()
                return [None, job]
        return ['No query', None]

class Job(models.Model):
    query          = models.ForeignKey(Query)
    start_at       = models.DateTimeField()
    completed_at   = models.DateTimeField()
    job_id         = models.CharField(max_length=255)
    total_rows     = models.IntegerField()
    query_checksum = models.CharField(max_length=32)
    cached_until   = models.DateTimeField(null=True)
    cache_url      = models.CharField(max_length=255, null=True)
    cache_key      = models.CharField(max_length=255, null=True)

    def schema_key(self):
        return 'jobs/' + str(self.id) + '/schema.json'

    def results_key(self):
        return self.cache_key

    def save_schema(self, schema):
        conn = S3Connection()
        bucket = conn.get_bucket('lx-pilot')
        key = Key(bucket)
        key.key = self.schema_key()
        key.set_metadata('Content-Type', 'application/json')
        key.set_metadata('Content-Encoding', 'gzip')
        key.set_contents_from_string(gzip.compress(bytes(json.dumps(schema), 'utf-8')))

    def save_results(self, rows, schema):
        conn = S3Connection()
        bucket = conn.get_bucket('lx-pilot')
        key = Key(bucket)
        key.key = self.results_key()
        key.set_metadata('Content-Type', 'application/json')
        key.set_metadata('Content-Encoding', 'gzip')
        key.set_contents_from_string(gzip.compress(bytes(json.dumps(dict(schema=schema, rows=rows, cached_at=datetime.now().isoformat())), 'utf-8')))

    def get_schema_url(self):
        conn = S3Connection()
        bucket = conn.get_bucket('lx-pilot')
        key = Key(bucket)
        key.key = self.schema_key()
        simple_url = key.generate_url(expires_in=3600)
        return simple_url

    def get_results_url(self, seconds=3600):
        conn = S3Connection()
        bucket = conn.get_bucket('lx-pilot')
        key = Key(bucket)
        key.key = self.results_key()
        simple_url = key.generate_url(expires_in=seconds)
        return simple_url




