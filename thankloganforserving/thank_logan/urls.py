from django.urls import path

from . import views

app_name = "thank_logan"
urlpatterns = [
    path("", views.index, name="index"),
    path("thank/", views.give_thanks, name="thank"),
]
