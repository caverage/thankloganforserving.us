from django.db import models


class Thank(models.Model):
    timestamp = models.DateTimeField("time of thanks")
    thanker = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.timestamp} - {self.thanker}"
