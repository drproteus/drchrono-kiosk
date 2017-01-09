from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.http import HttpResponse, Http404
from social.apps.django_app.default.models import UserSocialAuth
from django.contrib.auth.decorators import login_required
import requests
import json
from util.utils import api_call


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
def integrate(request):
    access_token = UserSocialAuth.objects.get(user=request.user).access_token
    headers = {
            'Authorization': 'Bearer %s' % access_token,
    }
    requests.post('https://drchrono.com/api/iframe_integration', headers=headers)
    return redirect('/')


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
    return render(request, 'patients.html', {'patients': patients})

@login_required
def patients(request):
    patients = []
    patients_url = 'https://drchrono.com/api/patients'
    while patients_url:
        data = api_call(request, patients_url)
        patients.extend(data['results'])
        patients_url = data['next']
    return HttpResponse(patients, content_type='json')


def ensure_from_drchrono(func):
    def wrapper(request):
        if not 'drchrono.com' in request.META['HTTP_REFERER']:
            raise Http404
        return func(request)
    return wrapper

@ensure_from_drchrono
def patient_frame(request):
    response = HttpResponse("hello, world")
    response['X-Frame-Options'] = 'ALLOW-FROM http://jakes-mac-mini.home/'
    return response
