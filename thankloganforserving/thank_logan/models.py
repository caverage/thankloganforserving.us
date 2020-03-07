from django.db import models
from django.utils import timezone


class Thank(models.Model):
    timestamp = models.DateTimeField("time of thanks")
    thanker = models.CharField(max_length=100)

    def __str__(self):
        return f"{timezone.localtime(self.timestamp)} - {self.thanker}"


class SMSQueue(models.Model):
    thank = models.ForeignKey(Thank, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.thank.timestamp} - {self.thank.thanker}"
