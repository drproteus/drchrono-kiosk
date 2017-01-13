from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from bcrypt import hashpw, gensalt

class Arrival(models.Model):
    appointment_id = models.IntegerField()
    patient_id = models.IntegerField()
    doctor = models.ForeignKey(User, related_name="arrival")
    created_at = models.DateTimeField(auto_now_add=True)
    seen_at = models.DateTimeField(blank=True, null=True)

    @property
    def time_spent_waiting(self):
        # returns microsecond difference between created_at and
        # either seen_at if seen, or datetime.now() if still waiting.
        if self.seen_at:
            return (self.seen_at - self.created_at).seconds
        else:
            return (datetime.now() - self.created_at).seconds

    @classmethod
    def average_wait_time(klass):
        if klass.objects.count() < 1:
            return -1
        return sum([arrival.time_spent_waiting for arrival in
            klass.objects.all()]) / float(klass.objects.count())

class Configuration(models.Model):
    doctor = models.ForeignKey(User, related_name="config")
    office_name = models.CharField(max_length=200)
    exit_kiosk_key = models.CharField(max_length=200)

    def set_kiosk_key(self, key):
        self.exit_kiosk_key = hashpw(key, gensalt())
    
    def is_kiosk_key(self, key):
        if hashpw(key, self.exit_kiosk_key) == self.exit_kiosk_key:
            return True
        return False

