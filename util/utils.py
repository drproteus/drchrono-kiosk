from django.http import HttpResponse, Http404
from social.apps.django_app.default.models import UserSocialAuth
from social.apps.django_app.utils import load_strategy
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
import requests
import json
from datetime import datetime

#-------------------------------------------------------------------------------
# DRCHRONO API HELPERS
#-------------------------------------------------------------------------------
MAX_TRIES = 5
API_ROOT = 'https://drchrono.com/api/'

def auth_headers(social_user):
    access_token = social_user.access_token
    headers = {
            'Authorization': 'Bearer %s' % access_token,
    }
    return headers

def api_call(request, url, request_type='GET',
        headers=None, raw=False, data=None,
        user=None, params=None):
    if not user:
        social_user = UserSocialAuth.objects.get(user=request.user)
    else:
        social_user = UserSocialAuth.objects.get(user=user)
    headers = auth_headers(social_user)
    if request_type == 'GET':
        response = requests.get(url, headers=headers, params=params)
    elif request_type == 'POST':
        if not data:
            data = {}
        response = requests.post(url, headers=headers, data=data)
    elif request_type == 'PATCH':
        if not data:
            data = {}
        response = requests.patch(url, headers=headers, data=data)
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

def doc_get(request, url, headers=None, raw=False, user=None, params=None):
    return api_call(request, url, headers=headers, raw=raw, user=user, params=params, request_type='GET')

def doc_post(request, url, data, headers=None, raw=False, user=None):
    return api_call(request, url, headers=headers, raw=raw, data=data, user=user, request_type='POST')

def doc_patch(request, url, data, headers=None, raw=False, user=None):
    return api_call(request, url, data=data, headers=headers, raw=raw, user=user, request_type='PATCH')

#-------------------------------------------------------------------------------
# SPECIFIC HELPERS
#-------------------------------------------------------------------------------
def get_todays_appointments(request, for_patient=None, user=None):
    url = "{}/appointments".format(API_ROOT)
    params = {"date": datetime.now().date().isoformat()}
    if for_patient:
        params["patient"] = for_patient
    return doc_get(request, url, params=params, user=user)

def set_appointment_status(request, appointment_id, new_status, user=None):
    if new_status not in ["Arrived", "In Session", "Complete"]:
        raise Exception, "Updated status must be one of 'Arrived', 'In Session', or 'Complete'."
    url = "{}/appointments/{}".format(API_ROOT, appointment_id)
    data = {"status": new_status}
    return doc_patch(request, url, data=data, user=user)

def get_patient(request, patient_id, user=None, params=None):
    url = "{}/patients/{}".format(API_ROOT, patient_id)
    return doc_get(request, url, user=user, params=params)

def update_patient(request, patient_id, data, user=None):
    url = "{}/patients/{}".format(API_ROOT, patient_id)
    return doc_patch(request, url, data, user=user)

#-------------------------------------------------------------------------------
# FUNCTION DECORATORS
#-------------------------------------------------------------------------------
def redirect_if_kiosk(func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('kioskMode', False):
            return redirect(reverse('kiosk:home'))
        return func(request, *args, **kwargs)
    return wrapper
