from django.db import models
from datetime import datetime

class Arrival(models.Model):
    appointment_id = models.IntegerField()
    patient_id = models.IntegerField()
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
        return sum([arrival.time_spent_waiting for arrival in
            klass.objects.all()]) / float(klass.objects.count())
