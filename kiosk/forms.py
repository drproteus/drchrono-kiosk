from django import forms
from kiosk.models import Configuration

class SearchForm(forms.Form):
    first_name = forms.CharField(max_length=160, required=False)
    last_name = forms.CharField(max_length=160)
    ssn_tail = forms.CharField(max_length=4)

class DemographicsForm(forms.Form):
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
    first_name = models.CharField(max_length=160, required=False)
    middle_name = models.CharField(max_length=160, required=False)
    last_name = models.CharField(max_length=160, required=False)
    address = models.TextField(max_length=400, required=False)
    zip_code = models.CharField(max_length=20, required=False)
    state = models.CharField(max_length=20, required=False)
    home_phone = models.CharField(max_length=30, required=False)
    cell_phone = models.CharField(max_length=30, required=False)
    email = models.CharField(max_length=160, required=False)
    emergency_contact_name = models.CharField(max_length=200, required=False)
    emergency_contact_phone = models.CharField(max_length=30, required=False)
    ethnicity = models.ChoiceField(choices=ETHNICITY_CHOICES, required=False)
    race = models.ChoiceField(choices=RACE_CHOICES, required=False)

class ConfigurationForm(forms.Form):
    office_name = models.CharField(max_length=200)
    exit_kiosk_key = models.CharField(max_length=300)
