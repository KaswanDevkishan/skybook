from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.utils import timezone

from reservations.models import Booking, City, Seat


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if get_user_model().objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email address already exists.")
        return email


class SignInForm(AuthenticationForm):
    error_messages = {
        **AuthenticationForm.error_messages,
        "invalid_login": (
            "We couldn’t sign you in. Check your username and password and try again."
        ),
    }

    def full_clean(self):
        super().full_clean()
        for field_name in self.errors:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs["aria-describedby"] = (
                    f"{self[field_name].id_for_label}-errors"
                )


class FlightSearchForm(forms.Form):
    SAME_ROUTE_ERROR = (
        "Your origin and destination cannot be the same. Please select a different airport."
    )

    origin = forms.ModelChoiceField(queryset=City.objects.all())
    destination = forms.ModelChoiceField(queryset=City.objects.all())
    departure_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ("origin", "destination"):
            self.fields[field_name].widget.attrs["aria-describedby"] = "same-route-error"
        departure_date = self.fields["departure_date"]
        departure_date.widget.attrs.update(
            {
                "aria-describedby": "id_departure_date-errors",
                "min": timezone.localdate().isoformat(),
            }
        )

    def clean_departure_date(self):
        departure_date = self.cleaned_data["departure_date"]
        if departure_date < timezone.localdate():
            raise ValidationError("Departure date cannot be in the past.")
        return departure_date

    def clean(self):
        cleaned_data = super().clean()
        origin = cleaned_data.get("origin")
        destination = cleaned_data.get("destination")

        if origin is not None and origin == destination:
            for field_name in ("origin", "destination"):
                self.fields[field_name].widget.attrs["aria-invalid"] = "true"
            raise ValidationError(self.SAME_ROUTE_ERROR, code="same_route")

        return cleaned_data

    @property
    def has_same_route_error(self):
        return any(error.code == "same_route" for error in self.errors.as_data().get("__all__", ()))


class BookingForm(forms.Form):
    seat = forms.ModelChoiceField(
        queryset=Seat.objects.none(),
        widget=forms.RadioSelect,
        error_messages={"invalid_choice": "Select an available seat for this flight."},
    )
    passenger_name = forms.CharField(max_length=100)
    passenger_email = forms.EmailField()

    def __init__(self, *args, flight, **kwargs):
        super().__init__(*args, **kwargs)
        self.flight = flight
        self.fields["seat"].queryset = (
            Seat.objects.filter(
                flight=flight,
            )
            .exclude(
                bookings__status=Booking.Status.CONFIRMED,
            )
            .order_by("cabin_class", "seat_number")
        )

    def clean_passenger_name(self):
        passenger_name = self.cleaned_data["passenger_name"].strip()
        if not passenger_name:
            raise ValidationError("Enter the passenger's name.")
        return passenger_name
