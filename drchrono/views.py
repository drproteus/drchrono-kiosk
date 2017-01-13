from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from social.apps.django_app.default.models import UserSocialAuth
from django.contrib.auth.decorators import login_required
import requests
import json
from util.utils import doc_get, doc_post, redirect_if_kiosk

@redirect_if_kiosk
def index(request):
    if not request.user.is_authenticated():
        return redirect(reverse('login'))
    return render(request, 'index.html', {})

@redirect_if_kiosk
def login_view(request):
    if request.user.is_authenticated():
        return redirect(reverse('index'))
    return render(request, 'login.html', {})

@redirect_if_kiosk
def logout_view(request):
    logout(request)
    return redirect(reverse('login'))

@login_required
@redirect_if_kiosk
def enable_kiosk(request):
    request.session['kioskMode'] = True
    return redirect(reverse('kiosk:home'))
