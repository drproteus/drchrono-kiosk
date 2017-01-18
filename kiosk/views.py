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
    config = Configuration.get_config_for_user(request.user)
    if request.method == 'POST':
        searchForm = SearchForm(request.POST)
        if searchForm.is_valid():
            results = search_appointments(request,
                    first_name=searchForm.cleaned_data['first_name'],
                    last_name=searchForm.cleaned_data['last_name'])
            ssn_tail = searchForm.cleaned_data['ssn_tail']
            import pdb; pdb.set_trace()
            if ssn_tail:
                matches = filter(lambda patient: patient.get('social_security_number', "")[-4:] == ssn_tail,
                        results)
                if matches:
                    results = matches
            else:
                results = filter(lambda patient: not bool(patient.get('social_security_number', None)), results)
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
                    {'results': results, 'kioskMode': kioskMode,
                        'config': config})
        else:
            if 'This field is required.' in searchForm.errors.get('last_name', ''):
                messages.error(request, "Need to specify at least a last name to search on.")
    return redirect(reverse('kiosk:home'))

@login_required
def verify(request, appointment_id):
    kioskMode = request.session.get('kioskMode', False)
    config = Configuration.get_config_for_user(request.user)
    if request.method == 'POST':
        try:
            arrival = Arrival.objects.get(appointment_id=appointment_id)
            messages.error(request, "You've already checked in for this appointment")
            return redirect(reverse('kiosk:home'))
        except Arrival.DoesNotExist, e:
            # haven't checked in
            pass
        form = InfoForm(request.POST)
        return render(request, 'kiosk-verify.html', {'form': form, 'kioskMode': kioskMode,
            'appointment_id': appointment_id, 'config': config})
    return redirect(reverse('kiosk:home'))

@login_required
def checkin(request, appointment_id):
    DEMO_FIELDS = ['first_name', 'middle_name', 'last_name',
            'address', 'zip_code', 'state', 'home_phone',
            'cell_phone', 'email', 'emergency_contact_name',
            'emergency_contact_phone', 'ethnicity', 'race', 'city']
    if request.method == 'POST':
        try:
            arrival = Arrival.objects.get(appointment_id=appointment_id)
            messages.error(request, "You've already checked in for this appointment")
            return redirect(reverse('kiosk:home'))
        except Arrival.DoesNotExist, e:
            # haven't checked in
            pass
        form = InfoForm(request.POST)
        if form.is_valid():
            updated_info = {k: v for k, v in form.cleaned_data.items() if k in DEMO_FIELDS}
            patient_id = form.cleaned_data['patient_id']
            update_patient(request, patient_id, updated_info)
            # Confirm SSN match?
            patient_photo = form.cleaned_data['patient_photo']
            if patient_photo == 'None':
                patient_photo = None
            patient_name = " ".join(filter(lambda name: bool(name), [form.cleaned_data['first_name'], form.cleaned_data['middle_name'], form.cleaned_data['last_name']]))
            arrival = Arrival(
                doctor=request.user,
                appointment_id=appointment_id,
                patient_id=form.cleaned_data['patient_id'],
                scheduled_time=form.cleaned_data['scheduled_time'],
                duration=form.cleaned_data['duration'],
                reason=form.cleaned_data['reason'],
                patient_name=patient_name
            )
            if patient_photo:
                arrival.patient_photo = patient_photo
            arrival.save()
            update_appointment_data = {
                    "status": "Arrived",
                    "reason": form.cleaned_data['reason'],
            }
            update_appointment(request, appointment_id, update_appointment_data)
            messages.success(request, "You've successfully checked-in, {}. The doctor will be with you shortly. Thank you.".format(arrival.patient_name))
            return redirect(reverse('kiosk:home'))
    return redirect(reverse('kiosk:home'))
