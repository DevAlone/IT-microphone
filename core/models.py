import datetime

from django.db import models
from django.utils import timezone


class Event(models.Model):
    lector = models.CharField(max_length=50)
    theme = models.CharField(max_length=150)
    description = models.CharField(max_length=1500)
    location = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now=True)
    event_start_time = models.DateTimeField()
    event_end_time = models.DateTimeField()
    need_subscribers = models.IntegerField()

    def __str__(self):
        return self.theme

    def wasPublishedRecently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def expired(self):
        return self.event_end_time < timezone.now()

    def duration(self):
        return self.event_end_time - self.event_start_time
