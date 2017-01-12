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
