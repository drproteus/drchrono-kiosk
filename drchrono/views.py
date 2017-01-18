from django.contrib.auth import logout
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from social.apps.django_app.default.models import UserSocialAuth
from django.contrib.auth.decorators import login_required
import requests
import json
from .utils import *
from kiosk.models import Configuration, Arrival
from kiosk.forms import ConfigurationForm, DisableForm
from django.contrib import messages
from django.utils import timezone

@redirect_if_kiosk
def index(request):
    if not request.user.is_authenticated():
        return redirect(reverse('login'))
    config = Configuration.get_config_for_user(request.user)
    if not config:
        messages.warning(request, "Please Create a Configuration for the Kiosk")
        return redirect(reverse('config'))
    hideNav = True
    return render(request, 'index.html', {'config': config, 'hideNav': hideNav})

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
        return render(request, 'config.html', {'form': form, 'config': configs.first()})
    form = ConfigurationForm()
    config = None
    if configs.count() > 0:
        config = configs.first()
        form.fields['office_name'].initial = config.office_name
        form.fields['exit_kiosk_key'].initial = config.exit_kiosk_key
    return render(request, 'config.html', {'form': form, 'config': config})

@login_required
@redirect_if_kiosk
def dashboard(request):
    config = Configuration.get_config_for_user(request.user)
    average_wait_time = Arrival.average_wait_time(request.user)
    arrivals = request.user.arrivals.incomplete().order_by('-seen_at')
    arrivals.update(new=False)
    return render(request, 'dashboard.html',
            {'arrivals': arrivals,
                'average_wait_time': average_wait_time,
                'config': config})

@login_required
@redirect_if_kiosk
def archive(request):
    config = Configuration.get_config_for_user(request.user)
    average_wait_time = Arrival.average_wait_time(request.user)
    arrivals = request.user.arrivals.completed()
    return render(request, 'archive.html', 
            {'arrivals': arrivals,
                'average_wait_time': average_wait_time,
                'config': config})

@login_required
@redirect_if_kiosk
def see_patient(request, arrival_id):
    arrival = get_object_or_404(Arrival, id=arrival_id)
    appointment_id = arrival.appointment_id
    set_appointment_status(request, appointment_id, "In Session")
    arrival.seen_at = timezone.now()
    arrival.save()
    messages.info(request, "You will now see {}.".format(arrival.patient_name))
    return redirect(reverse('dashboard'))

@login_required
@redirect_if_kiosk
def complete_appointment(request, arrival_id):
    arrival = get_object_or_404(Arrival, id=arrival_id, doctor=request.user)
    appointment_id = arrival.appointment_id
    set_appointment_status(request, appointment_id, "Complete")
    arrival.completed = True
    arrival.save()
    messages.info(request,
            "You have completed your appointment with {}".format(arrival.patient_name))
    return redirect(reverse('dashboard'))

@login_required
@redirect_if_kiosk
def reset_to_arrived(request, arrival_id):
    arrival = get_object_or_404(Arrival, id=arrival_id, doctor=request.user)
    appointment_id = arrival.appointment_id
    set_appointment_status(request, appointment_id, "Arrived")
    arrival.completed = False
    arrival.seen_at = None
    arrival.new = True
    arrival.save()
    messages.info(request,
            "Reset Appointment #{}".format(arrival.appointment_id))
    return redirect(reverse('dashboard'))

@login_required
@redirect_if_kiosk
def get_time_info(request):
    average_wait_time = Arrival.average_wait_time(request.user)
    return render(request, 'get-time-info.html', {'average_wait_time': average_wait_time})

@login_required
@redirect_if_kiosk
def get_arrivals(request):
    arrivals = request.user.arrivals.incomplete().order_by('-seen_at')
    return render(request, 'arrivals.html', {'arrivals': arrivals})

@login_required
@redirect_if_kiosk
def check_if_new_arrivals(request, mark_as_read=True):
    arrivals = request.user.arrivals.new()
    response = {'new_arrival_count': arrivals.count(), 'new_arrivals': None}
    for arrival in arrivals:
        if not response.get('new_arrivals'):
            response['new_arrivals'] = []
        response['new_arrivals'].append({'patient_name': arrival.patient_name,
            'scheduled_time': arrival.scheduled_time, 
            'checked_in': arrival.created_at})
    arrivals.update(new=False)
    return HttpResponse(json.dumps(response), content_type="application/json")
