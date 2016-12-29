from django.db import models
from django.contrib.auth.models import User

class BirthdayAlert(models.Model):
    patient_id = models.IntegerField()
    send_text = models.BooleanField(default=False)
    send_email = models.BooleanField(default=False)
    custom_body = models.TextField()
    birthday = models.DateTimeField()
    doctor = models.ForeignKey(User, related_name="alerts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
