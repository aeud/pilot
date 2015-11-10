from oauth2client import client
from apiclient.discovery import build
import httplib2
import sys

from oauth2client.client import OAuth2Credentials as Credentials
from apps.accounts.models import Account, BigQueryProject

def run():
    account = Account.objects.all()[:1].get()

    if not account.credentials:
        flow = client.flow_from_clientsecrets(
            '/Users/adrien/Downloads/client_secret_315463305042-l4e6vp0ds763snsgbi6rvu80r02cjufs.apps.googleusercontent.com.json',
            scope='https://www.googleapis.com/auth/bigquery',
            redirect_uri='http://localhost/oauth2callback')
        auth_uri = flow.step1_get_authorize_url()
        print(auth_uri)
        auth_code = line = input('CODE> ')
        credentials = flow.step2_exchange(auth_code)
        account.credentials = credentials.to_json()
        account.save()
    else:
        credentials = Credentials.from_json(account.credentials)

    http_auth = credentials.authorize(httplib2.Http())

    bigquery_service = build('bigquery', 'v2', http=http_auth)

    bq_project = account.bq_project

    if not bq_project:
        results = bigquery_service.projects().list().execute()
        for project in results.get('projects', []):
            print(project)
        index = line = input('INDEX> ')
        bq_project = BigQueryProject(project_id=results.get('projects')[int(index)].get('id'))
        bq_project.save()
        account.bq_project = bq_project
        account.save()

    query_request = bigquery_service.jobs()
    query_data = dict(query='''SELECT o.orderId order_id, o.totals.grossRevenue gross_revenue FROM dwh.orders o LIMIT 10''')

    query_response = query_request.query(projectId=bq_project.project_id,
                                         body=query_data).execute()
    print(query_response)