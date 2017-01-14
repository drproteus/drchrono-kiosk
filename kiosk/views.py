from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from kiosk.forms import SearchForm, ConfigurationForm, CheckinForm, DisableForm, InfoForm
from kiosk.models import *
from drchrono.utils import *
from django.contrib import messages

@login_required
def home(request):
    searchForm = SearchForm()
    disableForm = DisableForm()
    kioskMode = request.session.get('kioskMode', False)
    config = Configuration.get_config_for_user(request.user)
    contextDict = {'form': searchForm, 'kioskMode': kioskMode,
            'disable': disableForm, 'config': config}
    return render(request, 'kiosk-index.html', contextDict)

@login_required
def search(request):
    if request.method == 'POST':
        searchForm = SearchForm(request.POST)
        if searchForm.is_valid():
            results = search_appointments(request,
                    first_name=searchForm.cleaned_data['first_name'],
                    last_name=searchForm.cleaned_data['last_name'])
            results = filter(lambda patient: bool(patient['appointments']), results)
            if not results:
                messages.error(request, 'No appointments found for today.')
                return redirect(reverse('kiosk:home'))
            return render(request, 'kiosk-search-results.html',
                    {'results': results})
    return redirect(reverse('kiosk:home'))

@login_required
def checkin(request, appointment_id):
    if request.method == 'POST':
        form = CheckinForm(request.POST)
        if form.is_valid():
            # Confirm SSN match?
            patient_photo = form.cleaned_data['patient_photo']
            if patient_photo == 'None':
                patient_photo = None
            arrival = Arrival(
                doctor=request.user,
                appointment_id=appointment_id,
                patient_id=form.cleaned_data['patient_id'],
                scheduled_time=form.cleaned_data['scheduled_time'],
                duration=form.cleaned_data['duration'],
                patient_name=form.cleaned_data['patient_name']
            )
            if patient_photo:
                arrival.patient_photo = patient_photo
            arrival.save()
            set_appointment_status(request, appointment_id, "Arrived")
            messages.success(request, "You've successfully checked-in, {}. The doctor will be with you shortly. Thank you.".format(arrival.patient_name))
            return redirect(reverse('kiosk:home'))
    return redirect(reverse('kiosk:home'))

     
