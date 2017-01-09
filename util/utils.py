from django.http import HttpResponse, Http404
from social.apps.django_app.default.models import UserSocialAuth
from social.apps.django_app.utils import load_strategy
import requests
import json

MAX_TRIES = 5

def api_call(request, url, headers=None, raw=False):
    the_doctor = UserSocialAuth.objects.get(user=request.user)
    access_token = the_doctor.access_token
    headers = {
            'Authorization': 'Bearer %s' % access_token,
    }
    response = requests.get(url, headers=headers)
    if response.status_code > 200:
        strategy = load_strategy(request)
        the_doctor.refresh_token(strategy) 
        response = requests.get(url, headers=headers)
    if raw:
        return response
    return response.json()

