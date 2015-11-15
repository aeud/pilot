from django.db import models
from apps.accounts.models import Account
import hashlib

class Query(models.Model):
    script        = models.TextField()
    checksum      = models.CharField(max_length=32)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)
    unstack       = models.BooleanField(default=False)

    def to_dict(self):
        return dict(script=self.script,
                    unstack=self.unstack,)

    def save(self, *args, **kwargs):
        m = hashlib.md5()
        m.update(self.script.encode('utf-8'))
        if self.unstack:
            m.update('unstack'.encode('utf-8'))
        self.checksum = m.hexdigest()
        return super(Query, self).save(*args, **kwargs)

class Graph(models.Model):
    options       = models.TextField()
    chart_type    = models.CharField(max_length=255)
    map_script    = models.TextField(null=True)

    def to_dict(self):
        return dict(options=self.options,
                    chart_type=self.chart_type,
                    map_script=self.map_script,)

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

    def to_dict(self):
        return dict(name=self.name,
                    description=self.description,
                    cache_for=self.cache_for,
                    cache_until=self.cache_until.isoformat() if self.cache_until else None,
                    query=self.query.to_dict(),
                    graph=self.graph.to_dict(),)

#    def execute(self):
#        err = None
#        try:
#            job = Job.objects.filter(completed_at__isnull=False, query__visualization=self, cached_until__gte=datetime.now()).order_by('-start_at')[:1].get()
#            if job.query_checksum != job.query.checksum:
#                err, job = self.execute_query()
#        except Job.DoesNotExist:
#            err, job = self.execute_query()
#        return [err, job]

#    def execute_query(self):
#        if self.query:
#            job = Job(query=self.query, start_at=timezone.now(), query_checksum=self.query.checksum)
#            if self.account.credentials:
#                credentials = Credentials.from_json(self.account.credentials)
#                http_auth = credentials.authorize(httplib2.Http())
#                bigquery_service = build('bigquery', 'v2', http=http_auth)
#                try:
#                    response = bigquery_service.jobs().query(projectId=self.account.bq_project.project_id,
#                                                             body=dict(query=self.query.script)).execute()
#                except HttpError as err:
#                    return [err.content, None]
#                
#                job.job_id = response.get('jobReference').get('jobId')
#                job.total_rows = response.get('totalRows')
#                job.completed_at = timezone.now()
#                def replace_name(col):
#                    col['name'] = col.get('name').replace('_', ' ')
#                    return col
#                schema = [replace_name(col) for col in response.get('schema').get('fields')]
#                def cast_value(index, value, p=1):
#                    column = schema[index]
#                    column_type = column.get('type')
#                    if column_type == 'INTEGER':
#                        return int((value if value else '0'))
#                    elif column_type == 'FLOAT':
#                        return float(value if value else '0')
#                    elif column_type == 'TIMESTAMP' and p > 1:
#                        return datetime.fromtimestamp(int(float(value))).isoformat() if value else None
#                    return value
#                def change_type(t):
#                    if t == 'INTEGER' or t == 'FLOAT':
#                        return 'number'
#                    elif t == 'STRING':
#                        return 'string'
#                    elif t == 'BOOLEAN':
#                        return 'boolean'
#                    elif t == 'DATE':
#                        return 'date'
#                    elif t == 'TIMESTAMP':
#                        return 'date'
#                    else:
#                        return 'string'
#                rows = [[cast_value(index, value.get('v')) for index, value in enumerate(row.get('f'))] for row in response.get('rows')]
#                if self.query.unstack:
#                    p = pd.DataFrame(rows).set_index([0,1]).unstack(-1).fillna(0)
#                    matrix = p.as_matrix().tolist()
#                    rows_index = p.index.values
#                    columns_index = [v[1] for v in p.columns.values]
#                    s = schema[0]
#                    columns_index.insert(0, dict(id=s.get('name'), label=s.get('name'), type=change_type(s.get('type'))))
#                    new_matrix = [columns_index]
#                    for index, row in enumerate(matrix):
#                        row = [cast_value(2, c, 2) for c in row]
#                        row.insert(0, cast_value(0, rows_index[index], 2))
#                        new_matrix.append(row)
#                    rows = new_matrix
#                else:
#                    rows.insert(0, [dict(id=s.get('name'), label=s.get('name'), type=change_type(s.get('type'))) for s in schema])
#                now = timezone.now()
#                job.cache_key = 'jobs/' + str(now.year) + '/' + str(now.month) + '/' + str(now.day) + '/' + str(uuid.uuid4())
#                job.save_results(rows, schema)
#                if self.cache_for:
#                    job.cache_url = job.get_results_url(self.cache_for)
#                    job.cached_until = timezone.now() + timedelta(seconds=self.cache_for)
#                elif self.cache_until:
#                    now = timezone.now()
#                    new_date = pytz.timezone('Asia/Singapore').localize(datetime(now.year, now.month, now.day, self.cache_until.hour, self.cache_until.minute))
#                    if new_date < now:
#                        new_date = new_date + timedelta(days=1)
#                    job.cache_url = job.get_results_url((new_date-now).total_seconds())
#                    job.cached_until = new_date
#                job.save()
#                return [None, job]
#        return ['No query', None]

#class Job(models.Model):
#    query          = models.ForeignKey(Query)
#    start_at       = models.DateTimeField()
#    completed_at   = models.DateTimeField()
#    job_id         = models.CharField(max_length=255)
#    total_rows     = models.IntegerField()
#    query_checksum = models.CharField(max_length=32)
#    cached_until   = models.DateTimeField(null=True)
#    cache_url      = models.CharField(max_length=255, null=True)
#    cache_key      = models.CharField(max_length=255, null=True)#

#    def schema_key(self):
#        return 'jobs/' + str(self.id) + '/schema.json'#

#    def results_key(self):
#        return self.cache_key#

#    def save_schema(self, schema):
#        account = Account.objects.get(visualization__query=self.query)
#        conn = S3Connection(aws_access_key_id=account.aws_access_key_id, aws_secret_access_key=account.aws_secret_access_key)
#        bucket = conn.get_bucket('lx-pilot')
#        key = Key(bucket)
#        key.key = self.schema_key()
#        key.set_metadata('Content-Type', 'application/json')
#        key.set_metadata('Content-Encoding', 'gzip')
#        key.set_contents_from_string(gzip.compress(bytes(json.dumps(schema), 'utf-8')))#

#    def save_results(self, rows, schema):
#        account = Account.objects.get(visualization__query=self.query)
#        conn = S3Connection(aws_access_key_id=account.aws_access_key_id, aws_secret_access_key=account.aws_secret_access_key)
#        bucket = conn.get_bucket('lx-pilot')
#        key = Key(bucket)
#        key.key = self.results_key()
#        key.set_metadata('Content-Type', 'application/json')
#        key.set_metadata('Content-Encoding', 'gzip')
#        key.set_contents_from_string(gzip.compress(bytes(json.dumps(dict(schema=schema, rows=rows, cached_at=datetime.now().isoformat())), 'utf-8')))#

#    def get_schema_url(self):
#        account = Account.objects.get(visualization__query=self.query)
#        conn = S3Connection(aws_access_key_id=account.aws_access_key_id, aws_secret_access_key=account.aws_secret_access_key)
#        bucket = conn.get_bucket('lx-pilot')
#        key = Key(bucket)
#        key.key = self.schema_key()
#        simple_url = key.generate_url(expires_in=3600)
#        return simple_url#

#    def get_results_url(self, seconds=3600):
#        account = Account.objects.get(visualization__query=self.query)
#        conn = S3Connection(aws_access_key_id=account.aws_access_key_id, aws_secret_access_key=account.aws_secret_access_key)
#        bucket = conn.get_bucket('lx-pilot')
#        key = Key(bucket)
#        key.key = self.results_key()
#        simple_url = key.generate_url(expires_in=seconds)
#        return simple_url#

#    def export(self):
#        export = JobExport(job=self, key='toto', url='http://adrien.eudes.co/')
#        return export#

#class JobExport(models.Model):
#    job        = models.ForeignKey(Job)
#    created_at = models.DateTimeField(auto_now_add=True)
#    key        = models.CharField(max_length=255)
#    url        = models.CharField(max_length=255)


