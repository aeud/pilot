from django.db import models
from django.utils import timezone
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from apps.visualizations.models import Query
from apps.accounts.models import Account, User
from apps.dashboards.models import Dashboard
import gzip, json

class Job(models.Model):
    query          = models.ForeignKey(Query)
    start_at       = models.DateTimeField()
    completed_at   = models.DateTimeField()
    job_id         = models.CharField(max_length=255)
    total_rows     = models.IntegerField()
    created_by     = models.ForeignKey(User)
    query_checksum = models.CharField(max_length=32)
    cached_until   = models.DateTimeField(null=True)
    cache_url      = models.CharField(max_length=255, null=True)
    cache_key      = models.CharField(max_length=255, null=True)

    def schema_key(self):
        return 'jobs/' + str(self.id) + '/schema.json'

    def results_key(self):
        return self.cache_key

    def save_schema(self, schema):
        account = Account.objects.get(visualization__query=self.query)
        conn = S3Connection(aws_access_key_id=account.aws_access_key_id, aws_secret_access_key=account.aws_secret_access_key)
        bucket = conn.get_bucket('lx-pilot')
        key = Key(bucket)
        key.key = self.schema_key()
        key.set_metadata('Content-Type', 'application/json')
        key.set_metadata('Content-Encoding', 'gzip')
        key.set_contents_from_string(gzip.compress(bytes(json.dumps(schema), 'utf-8')))

    def save_results(self, rows, schema):
        account = Account.objects.get(visualization__query=self.query)
        conn = S3Connection(aws_access_key_id=account.aws_access_key_id, aws_secret_access_key=account.aws_secret_access_key)
        bucket = conn.get_bucket('lx-pilot')
        key = Key(bucket)
        key.key = self.results_key()
        key.set_metadata('Content-Type', 'application/json')
        key.set_metadata('Content-Encoding', 'gzip')
        key.set_contents_from_string(gzip.compress(bytes(json.dumps(dict(schema=schema, rows=rows, cached_at=timezone.now().isoformat())), 'utf-8')))

    def get_schema_url(self):
        account = Account.objects.get(visualization__query=self.query)
        conn = S3Connection(aws_access_key_id=account.aws_access_key_id, aws_secret_access_key=account.aws_secret_access_key)
        bucket = conn.get_bucket('lx-pilot')
        key = Key(bucket)
        key.key = self.schema_key()
        simple_url = key.generate_url(expires_in=3600)
        return simple_url

    def get_results_url(self, seconds=3600):
        account = Account.objects.get(visualization__query=self.query)
        conn = S3Connection(aws_access_key_id=account.aws_access_key_id, aws_secret_access_key=account.aws_secret_access_key)
        bucket = conn.get_bucket('lx-pilot')
        key = Key(bucket)
        key.key = self.results_key()
        simple_url = key.generate_url(expires_in=seconds)
        return simple_url

    def export(self):
        export = JobExport(job=self, key='toto', url='http://adrien.eudes.co/')
        return export

class JobExport(models.Model):
    job        = models.OneToOneField(Job)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)
    key        = models.CharField(max_length=255)

    def generate_url(self, seconds=3600):
        account = Account.objects.get(visualization__query__job=self.job)
        conn = S3Connection(aws_access_key_id=account.aws_access_key_id, aws_secret_access_key=account.aws_secret_access_key)
        bucket = conn.get_bucket('lx-pilot')
        key = Key(bucket)
        key.key = self.key
        return key.generate_url(expires_in=seconds, response_headers={
            'response-content-disposition': 'attachment; filename=export.csv'
        })

class JobRequest(models.Model):
    job        = models.ForeignKey(Job)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)
    dashboard  = models.ForeignKey(Dashboard, null=True)

class JobExportRequest(models.Model):
    export     = models.ForeignKey(JobExport)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)

