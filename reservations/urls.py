from django.urls import path
from django.views.generic import RedirectView

from reservations import views

app_name = "reservations"

urlpatterns = [
    path(
        "",
        RedirectView.as_view(pattern_name="reservations:flight_list", permanent=False),
        name="home",
    ),
    path("accounts/register/", views.register, name="register"),
    path("accounts/sign-in/", views.SignInView.as_view(), name="sign_in"),
    path("accounts/sign-out/", views.sign_out, name="sign_out"),
    path("account/", views.account, name="account"),
    path("bookings/", views.my_bookings, name="my_bookings"),
    path("flights/", views.flight_list, name="flight_list"),
    path("flights/<int:flight_id>/", views.flight_detail, name="flight_detail"),
    path("flights/<int:flight_id>/book/", views.flight_booking, name="flight_booking"),
    path("bookings/resume/", views.resume_booking, name="resume_booking"),
    path(
        "bookings/<str:booking_reference>/confirmation/",
        views.booking_confirmation,
        name="booking_confirmation",
    ),
    path(
        "bookings/<str:booking_reference>/cancel/",
        views.cancel_booking,
        name="cancel_booking",
    ),
    path("health/", views.health, name="health"),
]
