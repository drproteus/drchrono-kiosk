from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from social.apps.django_app.default.models import UserSocialAuth
from django.contrib.auth.decorators import login_required
import requests
import json
from .utils import doc_get, doc_post, redirect_if_kiosk
from kiosk.models import Configuration
from kiosk.forms import ConfigurationForm, DisableForm
from django.contrib import messages

@redirect_if_kiosk
def index(request):
    if not request.user.is_authenticated():
        return redirect(reverse('login'))
    config = Configuration.get_config_for_user(request.user)
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
    config = Configuration.get_config_for_user(request.user)
    if not config:
        messages.error(request, "Must set Kiosk Configuration before enabling Kiosk Mode")
        return redirect(reverse('config'))
    request.session['kioskMode'] = True
    return redirect(reverse('kiosk:home'))

@login_required
def disable_kiosk(request):
    if request.method == 'POST':
        form = DisableForm(request.POST)
        if form.is_valid():
            key = form.cleaned_data['exit_kiosk_key']
            config = Configuration.get_config_for_user(request.user)
            if key == config.exit_kiosk_key:
                del request.session['kioskMode']
                return redirect(reverse('index'))
    return redirect(reverse('kiosk:home'))

@login_required
@redirect_if_kiosk
def config(request):
    configs = Configuration.objects.filter(doctor=request.user)
    if request.method == 'POST':
        form = ConfigurationForm(request.POST)
        if form.is_valid():
            config = None
            if configs.count() > 0:
                config = configs.first()
            else:
                config = Configuration(doctor=request.user)
            config.office_name = form.cleaned_data['office_name']
            config.exit_kiosk_key = form.cleaned_data['exit_kiosk_key']
            config.save()
            return redirect(reverse('index'))
        return render(request, 'config.html', {'form': form})
    form = ConfigurationForm()
    config = None
    if configs.count() > 0:
        config = configs.first()
        form.fields['office_name'].initial = config.office_name
        form.fields['exit_kiosk_key'].initial = config.exit_kiosk_key
    return render(request, 'config.html', {'form': form})

@login_required
@redirect_if_kiosk
def dashboard(request):
    arrivals = request.user.arrivals.unseen()
    return render(request, 'dashboard.html', {'arrivals': arrivals})
