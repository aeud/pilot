from oauth2client import client
from apiclient.discovery import build
import httplib2
import sys


flow = client.flow_from_clientsecrets(
    '/Users/adrien/Downloads/client_secret_315463305042-l4e6vp0ds763snsgbi6rvu80r02cjufs.apps.googleusercontent.com.json',
    scope='https://www.googleapis.com/auth/bigquery',
    redirect_uri='http://localhost/oauth2callback')
auth_uri = flow.step1_get_authorize_url()
print(auth_uri)

auth_code = line = input('CODE> ')
credentials = flow.step2_exchange(auth_code)

print(credentials)

http_auth = credentials.authorize(httplib2.Http())

bigquery_service = build('bigquery', 'v2', http=http_auth)

query_request = bigquery_service.jobs()
query_data = dict(query='SELECT COUNT(*) FROM dwh.orders')

query_response = query_request.query(projectId='luxola.com:luxola-analytics',
                                     body=query_data).execute()
print(query_response)