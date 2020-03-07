import datetime
import os

import requests
from django.db.models import Count
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
    except Thank.DoesNotExist:
        # this means no thanks on record :(
        thanked_today = False

    return thanked_today


def _current_streak():
    return None


def _longest_streak():
    return None


def _leader_board():
    most_thanks = (
        Thank.objects.values("thanker")
        .annotate(count=Count("thanker"))
        .order_by("-count")
    )[0:5]

    position = 1
    previous_count = None
    for thanker in most_thanks:
        if previous_count is None:
            thanker["position"] = position
        elif thanker["count"] == previous_count:
            thanker["position"] = position
        else:
            position += 1
            thanker["position"] = position

        previous_count = thanker["count"]

    return filter(lambda thanker: thanker["count"] > 1, most_thanks)


def index(request):
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
        "leader_board": _leader_board(),
    }

    return render(request, "thank_logan/index.html", context)


def give_thanks(request):
    if not _thanked_today():
        thanker = request.POST.get("name", None)
        thank = Thank(timestamp=_now(), thanker=thanker)
        thank.save()

        SMSQueue(thank=thank).save()

    return HttpResponseRedirect(reverse("thank_logan:index"))
