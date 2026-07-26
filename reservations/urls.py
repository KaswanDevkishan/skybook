from django.urls import path

from reservations import views

app_name = "reservations"

urlpatterns = [
    path("", views.home, name="home"),
    path("flights/", views.flight_list, name="flight_list"),
    path("flights/<int:flight_id>/", views.flight_detail, name="flight_detail"),
    path("flights/<int:flight_id>/book/", views.flight_booking, name="flight_booking"),
    path(
        "bookings/<str:booking_reference>/confirmation/",
        views.booking_confirmation,
        name="booking_confirmation",
    ),
    path("health/", views.health, name="health"),
]
