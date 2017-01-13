from django import forms
from kiosk.models import Configuration

class SearchForm(forms.Form):
    first_name = forms.CharField(max_length=160, required=False)
    last_name = forms.CharField(max_length=160)
    ssn_tail = forms.CharField(max_length=4)

class CheckinForm(forms.Form):
    ETHNICITY_CHOICES = (
        ('blank', ''),
        ('hispanic', 'Hispanic'),
        ('not_hispanic', 'Not Hispanic'),
        ('declined', 'Decline to self-identify'),
    )
    RACE_CHOICES = (
        ('blank', ''),
        ('indian', 'Indian'),
        ('asian', 'Asian'),
        ('black', 'Black'),
        ('hawaiian', 'Hawaiian'),
        ('white', 'White'),
        ('declined', 'Decline to self-identify'),
    )
    # Demographic Fields
    first_name = forms.CharField(max_length=160, required=False)
    middle_name = forms.CharField(max_length=160, required=False)
    last_name = forms.CharField(max_length=160, required=False)
    address = forms.CharField(widget=forms.Textarea, max_length=400, required=False)
    zip_code = forms.CharField(max_length=20, required=False)
    state = forms.CharField(max_length=20, required=False)
    home_phone = forms.CharField(max_length=30, required=False)
    cell_phone = forms.CharField(max_length=30, required=False)
    email = forms.CharField(max_length=160, required=False)
    emergency_contact_name = forms.CharField(max_length=200, required=False)
    emergency_contact_phone = forms.CharField(max_length=30, required=False)
    ethnicity = forms.ChoiceField(choices=ETHNICITY_CHOICES, required=False)
    race = forms.ChoiceField(choices=RACE_CHOICES, required=False)
    # Appointment Fields
    appointment_id = forms.CharField(max_length=160, widget=forms.HiddenInput())
    scheduled_time = forms.DateTimeField(widget=forms.HiddenInput())
    duration = forms.IntegerField(widget=forms.HiddenInput())

class ConfigurationForm(forms.Form):
    office_name = forms.CharField(max_length=200)
    exit_kiosk_key = forms.CharField(max_length=300, required=False)

class DisableForm(forms.Form):
    exit_kiosk_key = forms.CharField(max_length=300, required=False)
