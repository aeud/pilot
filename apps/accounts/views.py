from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth import login as manual_login
from oauth2client import client
from oauth2client.client import OAuth2Credentials as Credentials
from oauth2client.client import verify_id_token
from apiclient.discovery import build
import httplib2, functools, hashlib, uuid, gzip, json, requests
from apps.accounts.models import Account, BigQueryProject, User


def index(request):
    pending_invitations = User.objects.filter(account=request.user.account)
    return render(request, 'accounts/index.html', dict(pending_invitations=pending_invitations))

def invite(request):
    return render(request, 'accounts/invite.html')

def invite_post(request):
    email = request.POST.get('email')
    try:
        user = User.objects.get(email=email)
        if user.account:
            return redirect(index)
        user.account = request.user.account
    except User.DoesNotExist:
        user = User(email=email, account=request.user.account)
    user.save()
    return redirect(index)

def get_flow(request):
    return client.flow_from_clientsecrets(
        settings.GA_JSON_PATH,
        scope='https://www.googleapis.com/auth/bigquery',
        redirect_uri=request.build_absolute_uri(reverse('accounts_bigquery_connect_callback')))

def bq_connect(request):
    account = request.user.account
    if not account.credentials:
        flow = get_flow(request)
        return redirect(flow.step1_get_authorize_url())
    bq_project = account.bq_project
    if not bq_project:
        return redirect(bq_choose_project)
    return redirect(index)

def oauth_callback(request):
    account = request.user.account
    auth_code = request.GET.get('code')
    flow = get_flow(request)
    credentials = flow.step2_exchange(auth_code)
    account.credentials = credentials.to_json()
    account.save()
    return redirect(bq_connect)

def bq_choose_project(request):
    account = request.user.account
    credentials = Credentials.from_json(account.credentials)
    http_auth = credentials.authorize(httplib2.Http())
    bigquery_service = build('bigquery', 'v2', http=http_auth)
    results = bigquery_service.projects().list().execute()
    return render(request, 'accounts/choose-project.html', dict(projects=results.get('projects', [])))

def bq_choose_project_post(request):
    account = request.user.account
    project_id = request.POST.get('project_id')
    bq_project = BigQueryProject(project_id=project_id)
    bq_project.save()
    account.bq_project = bq_project
    account.save()
    return redirect(bq_connect)

def bq_remove_project(request):
    account = request.user.account
    account.bq_project = None
    account.save()
    return redirect(bq_connect)

def login_google(request):
    #print(request.build_absolute_uri(reverse('login_google_callback')))
    url = 'https://accounts.google.com/o/oauth2/auth?client_id='
    url += settings.GA_CLIENT_ID
    url += '&response_type=code&max_auth_age=0&scope=openid email&redirect_uri='
    url += request.build_absolute_uri(reverse('login_google_callback'))
    url += '&state=toto'
    return redirect(url)

def login_google_callback(request):
    url = 'https://www.googleapis.com/oauth2/v3/token?code='
    url += request.GET.get('code')
    url += '&client_id='
    url += settings.GA_CLIENT_ID
    url += '&client_secret='
    url += settings.GA_CLIENT_SECRET
    url += '&redirect_uri='
    url += request.build_absolute_uri(reverse('login_google_callback'))
    url += '&grant_type=authorization_code'
    r = requests.post(url)
    jwt = verify_id_token(r.json().get('id_token'), settings.GA_CLIENT_ID)
    email = jwt.get('email').lower()
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User(email=email)
        user.save()
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    manual_login(request, user)
    return redirect('home')

def aws_connect(request):
    return render(request, 'accounts/aws-credentials.html')

def aws_connect_post(request):
    account = request.user.account
    account.aws_access_key_id = request.POST.get('key')
    account.aws_secret_access_key = request.POST.get('secret')
    account.save()
    return redirect(index)

def aws_remove(request):
    account = request.user.account
    account.aws_access_key_id = None
    account.aws_secret_access_key = None
    account.save()
    return redirect(aws_connect)