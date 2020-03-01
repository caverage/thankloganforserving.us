import datetime
import os

import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone

from .models import Thank


def _thanked_today():
    try:
        most_recent_thank = Thank.objects.all().order_by("-id")[0]
        # breaks if someone waits a year to thank him
        thanked_today = (
            timezone.localtime(timezone.now()).date()
            == most_recent_thank.timestamp.date()
        )
    except IndexError:
        # this means no thanks on record :(
        thanked_today = False

    return thanked_today


def index(request):
    tomorrow = timezone.localtime(timezone.now()) + timezone.timedelta(days=1)
    most_recent_thanker = Thank.objects.all().order_by("-id")[0].thanker
    print(most_recent_thanker)
    context = {
        "thanked": _thanked_today(),
        "tomorrow": tomorrow.date(),
        "most_recent_thanker": most_recent_thanker,
    }

    return render(request, "thank_logan/index.html", context)


def give_thanks(request):
    if not _thanked_today():
        thanker = request.POST.get("name", None)
        thank = Thank(timestamp=timezone.now(), thanker=thanker)
        thank.save()

        endpoint = "http://smsgw.sip.us/api/v1/18775902283/send"
        key = os.environ["SMS_KEY"]
        destination = os.environ["LOGAN_CELL"]
        message = f"{thanker} thanks you for your service!"
        data = {"key": key, "destination": destination, "message": message}

        thank_message = requests.post(url=endpoint, data=data)

        print(thank_message.text)

    return HttpResponseRedirect(reverse("thank_logan:index"))
