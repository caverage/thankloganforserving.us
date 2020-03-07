import datetime
import os

import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone

from .models import SMSQueue, Thank


def _now():
    return timezone.localtime(timezone.now())


def _most_recent_thank():
    return Thank.objects.all().latest("timestamp")


def _thanked_today():
    try:
        most_recent_thank = _most_recent_thank()
        thanked_today = (
            _now().date() == timezone.localtime(most_recent_thank.timestamp).date()
        )
        print(_now().date())
        print(most_recent_thank.timestamp.date())
    except Thank.DoesNotExist:
        # this means no thanks on record :(
        thanked_today = False

    return thanked_today


def _current_streak():
    return None


def _longest_streak():
    return None


def index(request):
    print(_now().date())
    tomorrow = _now() + timezone.timedelta(days=1)
    try:
        most_recent_thanker = _most_recent_thank().thanker
    except Thank.DoesNotExist:
        # this means no thanks on record :(
        most_recent_thanker = None
    context = {
        "thanked": _thanked_today(),
        "tomorrow": tomorrow.date(),
        "most_recent_thanker": most_recent_thanker,
        "current_streak": _current_streak(),
        "longest_streak": _longest_streak(),
    }

    return render(request, "thank_logan/index.html", context)


def give_thanks(request):
    if not _thanked_today():
        thanker = request.POST.get("name", None)
        print(_now)
        thank = Thank(timestamp=_now(), thanker=thanker)
        thank.save()

        SMSQueue(thank=thank).save()

    return HttpResponseRedirect(reverse("thank_logan:index"))
