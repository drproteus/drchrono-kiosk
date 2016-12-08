from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpResponse
from social.apps.django_app.default.models import UserSocialAuth
from django.contrib.auth.decorators import login_required
import requests
import json


def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def user_view(request):
    access_token = UserSocialAuth.objects.get(user=request.user).access_token
    response = requests.get('https://drchrono.com/api/users/current', headers={
        'Authorization' : 'Bearer %s' % access_token,
    })
    response.raise_for_status()

    return HttpResponse(response, content_type="json")

@login_required
def patients_view(request):
    access_token = UserSocialAuth.objects.get(user=request.user).access_token
    headers = {
            'Authorization': 'Bearer %s' % access_token,
    }
    patients = []
    patients_url = 'https://drchrono.com/api/patients'
    while patients_url:
        data = requests.get(patients_url, headers=headers).json()
        patients.extend(data['results'])
        patients_url = data['next']
    html = "<pre>"
    for patient in patients:
        html += (json.dumps(patient)+'\n')
    html += "</pre>"
    return HttpResponse(html)
