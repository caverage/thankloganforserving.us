import datetime
import os

import requests
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from thank_logan.models import SMSQueue


class Command(BaseCommand):
    help = "Checks queued thanks against time to text Logan his thanks."

    def handle(self, *args, **options):
        queue = SMSQueue.objects.all()
        for sms in queue:
            self.text_logan(sms)
        print("no more queued thanks")

    def text_logan(self, sms):
        try:
            if (
                datetime.time(21, 00)
                > timezone.localtime(timezone.now()).time()
                > datetime.time(9, 00)
            ):
                thanker = sms.thank.thanker
                endpoint = "http://smsgw.sip.us/api/v1/18775902283/send"
                key = os.environ["SMS_KEY"]
                destination = os.environ["LOGAN_CELL"]
                message = f"{thanker} thanks you for your service!"
                data = {"key": key, "destination": destination, "message": message}

                thank_message = requests.post(url=endpoint, data=data)

                sms.delete()
                print(thank_message.text)
                print(f"Thank sent on behalf of - {thanker}")
            else:
                print("it's past Logan's bedtime, try again later")
        except:
            raise CommandError("SMS could not send")
