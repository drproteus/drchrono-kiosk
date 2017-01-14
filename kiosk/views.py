from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from kiosk.forms import SearchForm, ConfigurationForm, CheckinForm, DisableForm, InfoForm, HiddenInfoForm
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
    kioskMode = request.session.get('kioskMode', False)
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
            for result in results:
                for appointment in result['appointments']:
                    formData = {k: v for k, v in result.items() if k != 'appointments'}
                    formData.update(appointment)
                    formData.update({'appointment_id': appointment['id'],
                        'patient_id': result['id']})
                    form = HiddenInfoForm(formData)
                    appointment['form'] = form
            return render(request, 'kiosk-search-results.html',
                    {'results': results, 'kioskMode': kioskMode})
    return redirect(reverse('kiosk:home'))

@login_required
def verify(request, appointment_id):
    kioskMode = request.session.get('kioskMode', False)
    if request.method == 'POST':
        form = InfoForm(request.POST)
        return render(request, 'kiosk-verify.html', {'form': form, 'kioskMode': kioskMode,
            'appointment_id': appointment_id})
    return redirect(reverse('kiosk:home'))

@login_required
def checkin(request, appointment_id):
    if request.method == 'POST':
        try:
            arrival = Arrival.objects.get(appointment_id=appointment_id)
            messages.error(request, "You've already checked in for this appointment")
            return redirect(reverse('kiosk:home'))
        except Arrival.DoesNotExist, e:
            # haven't checked in
            pass
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

@login_required
def verify_info(request):
    pass
