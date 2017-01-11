from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from util.utils import drchrono_get, drchrono_post

TODO = 200
class Patient(models.Model):
    doctor = models.ForeignKey(User, related_name="patient")
    drchrono_id = models.IntegerField()
    first_name = models.CharField(max_length=TODO, blank=True, null=True)
    middle_name = models.CharField(max_length=TODO, blank=True, null=True)
    last_name = models.CharField(max_length=TODO, null=True)
    birthday = models.DateField(blank=True, null=True)
    email = models.CharField(max_length=TODO, blank=True, null=True)
    gender = models.CharField(max_length=TODO, default="")
    zip_code = models.CharField(max_length=TODO, blank=True, null=True)
    cell_phone = models.CharField(max_length=TODO, blank=True, null=True)
    photo = models.CharField(max_length=TODO, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def create_patient(klass, user, data):
        patient = Patient(doctor=user)
        patient.drchrono_id = data.get('id')
        patient.first_name = data.get('first_name')
        patient.middle_name = data.get('middle_name')
        patient.last_name = data.get('last_name')
        patient.birthday = data.get('date_of_birth')
        patient.email = data.get('email')
        patient.gender = data.get('gender')
        patient.photo = data.get('patient_photo')
        patient.zip_code = data.get('zip_code')
        patient.cell_phone = data.get('cell_phone')
        patient.save()
        return patient

    @classmethod
    def last_updated_date(klass, user=None):
        last_updated = Patient.objects.order_by('-updated_at')
        if user:
            last_updated = last_updated.filter(doctor=user)
        if not last_updated:
            return None
        return last_updated.first().updated_at

class BirthdayAlert(models.Model):
    send_text = models.BooleanField(default=False)
    send_email = models.BooleanField(default=False)
    custom_email_body = models.TextField()
    custom_text_body = models.CharField(max_length=160)
    birthday = models.DateField()
    doctor = models.ForeignKey(User, related_name="patient_alert")
    patient = models.ForeignKey(Patient, related_name="alert")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

def synchronize_patients(sender, user, request, **kwargs):
    patients = []
    patients_url = 'https://drchrono.com/api/patients'
    last_updated_date = Patient.last_updated_date(user=user)
    if last_updated_date:
        patients_url += '?since={}'.format(last_updated_date)
    while patients_url:
        data = drchrono_get(request, patients_url, user=user)
        patients.extend(data['results'])
        patients_url = data['next']
    for patient in patients:
        Patient.create_patient(user, patient)

user_logged_in.connect(synchronize_patients)
