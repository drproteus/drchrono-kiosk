from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.http import HttpResponse, Http404
from social.apps.django_app.default.models import UserSocialAuth
from django.contrib.auth.decorators import login_required
import requests
import json
from util.utils import drchrono_get, drchrono_post
from drchrono.models import Patient, BirthdayAlert


def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def patients(request, filters=None):
    patients = []
    patients_url = 'https://drchrono.com/api/patients'
    if filters:
        for filter in filter:
            patients_url += '?{}={}'.format(filter[0], filter[1])
    while patients_url:
        data = drchrono_get(request, patients_url)
        patients.extend(data['results'])
        patients_url = data['next']
    return HttpResponse(json.dumps(patients), content_type='json')
