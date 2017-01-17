from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from bcrypt import hashpw, gensalt

class ArrivalQueryset(models.query.QuerySet):
    def unseen(self):
        return self.filter(seen_at=None)

class ArrivalManager(models.Manager):
    def get_queryset(self):
        return ArrivalQueryset(self.model, using=self.db)

    def unseen(self):
        return self.get_queryset().unseen()

class Arrival(models.Model):
    appointment_id = models.IntegerField()
    patient_id = models.IntegerField()
    doctor = models.ForeignKey(User, related_name="arrivals")
    reason = models.CharField(max_length=500, blank=True)
    scheduled_time = models.DateTimeField()
    duration = models.IntegerField()
    patient_photo = models.CharField(max_length=500,
            default="http://placekitten.com/g/200/200")
    patient_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    seen_at = models.DateTimeField(blank=True, null=True)

    objects = ArrivalManager()

    @property
    def time_spent_waiting(self):
        # returns second difference between created_at and
        # either seen_at if seen, or timezone.now() if still waiting.
        if self.seen_at:
            return (self.seen_at - self.created_at).seconds
        else:
            return (timezone.now() - self.created_at).seconds

    @classmethod
    def average_wait_time(klass):
        arrivals = klass.objects.all()
        if arrivals.count() < 1:
            return -1
        return sum([arrival.time_spent_waiting for arrival in
            arrivals]) / float(arrivals.count())

class Configuration(models.Model):
    doctor = models.OneToOneField(User, related_name="configuration")
    office_name = models.CharField(max_length=200)
    exit_kiosk_key = models.CharField(max_length=200)

    # Unicode troubles with hashing putting the following on the back-burner
    # Not as concerned with this security as a much as a password. Bummer.
    # def set_kiosk_key(self, key):
    #     self.exit_kiosk_key = hashpw(key, gensalt())
    # 
    # def is_kiosk_key(self, key):
    #     if hashpw(key, self.exit_kiosk_key) == self.exit_kiosk_key:
    #         return True
    #     return False

    @classmethod
    def get_config_for_user(klass, user):
        configs = klass.objects.filter(doctor=user)
        if configs.count() < 1:
            return None
        return configs.first()

