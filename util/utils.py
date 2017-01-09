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

def api_call(request, url, headers=None, raw=False):
    social_user = UserSocialAuth.objects.get(user=request.user)
    headers = auth_headers(social_user)
    response = requests.get(url, headers=headers)
    if response.status_code > 200:
        strategy = load_strategy(request)
        social_user.refresh_token(strategy)
        headers = auth_headers(social_user)
        response = requests.get(url, headers=headers)
    if raw:
        return response
    return response.json()

