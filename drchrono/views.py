from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.http import HttpResponse, Http404
from social.apps.django_app.default.models import UserSocialAuth
from django.contrib.auth.decorators import login_required
import requests
import json
from util.utils import doc_get, doc_post


def index(request):
    if not request.user.is_authenticated():
        return redirect('login')
    return render(request, 'index.html', {})

def login_view(request):
    if request.user.is_authenticated():
        return redirect('home')
    return render(request, 'login.html', {})

def logout_view(request):
    logout(request)
    return redirect('/')
