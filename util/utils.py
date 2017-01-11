from django.http import HttpResponse, Http404
from social.apps.django_app.default.models import UserSocialAuth
from social.apps.django_app.utils import load_strategy
import requests
import json

MAX_TRIES = 5

def auth_headers(social_user):
    access_token = social_user.access_token
    headers = {
            'Authorization': 'Bearer %s' % access_token,
    }
    return headers

def api_call(request, url, request_type='GET',
        headers=None, raw=False, data=None,
        user=None):
    if not user:
        social_user = UserSocialAuth.objects.get(user=request.user)
    else:
        social_user = UserSocialAuth.objects.get(user=user)
    headers = auth_headers(social_user)
    if request_type == 'GET':
        response = requests.get(url, headers=headers)
    elif request_type == 'POST':
        if not data:
            data = {}
        response = requests.post(url, headers=headers, data=data)
    else:
        raise Exception, "Invalid request type specified: {}".format(request_type)
    if response.status_code > 200:
        strategy = load_strategy(request)
        social_user.refresh_token(strategy)
        headers = auth_headers(social_user)
        response = requests.get(url, headers=headers)
    if raw:
        return response
    return response.json()

def drchrono_get(request, url, headers=None, raw=False, user=None):
    return api_call(request, url, headers=headers, raw=raw, user=user)

def drchrono_post(request, url, data, headers=None, raw=False, user=None):
    return api_call(request, url, headers=headers, raw=False, data=data, user=user)

