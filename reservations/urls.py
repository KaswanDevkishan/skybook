from django.urls import path

from reservations import views

app_name = "reservations"

urlpatterns = [
    path("", views.home, name="home"),
    path("flights/", views.flight_list, name="flight_list"),
    path("flights/<int:flight_id>/", views.flight_detail, name="flight_detail"),
    path("booking/new/", views.booking_new, name="booking_new"),
    path("booking/submit/", views.booking_submit, name="booking_submit"),
    path("health/", views.health, name="health"),
]
