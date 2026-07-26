from django import forms
from django.core.exceptions import ValidationError

from reservations.models import City, Seat


class FlightSearchForm(forms.Form):
    origin = forms.ModelChoiceField(queryset=City.objects.all())
    destination = forms.ModelChoiceField(queryset=City.objects.all())
    departure_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    def clean(self):
        cleaned_data = super().clean()
        origin = cleaned_data.get("origin")
        destination = cleaned_data.get("destination")

        if origin is not None and origin == destination:
            raise ValidationError("Origin and destination must be different.")

        return cleaned_data


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
        self.fields["seat"].queryset = Seat.objects.filter(
            flight=flight,
            bookings__isnull=True,
        ).order_by("cabin_class", "seat_number")

    def clean_passenger_name(self):
        passenger_name = self.cleaned_data["passenger_name"].strip()
        if not passenger_name:
            raise ValidationError("Enter the passenger's name.")
        return passenger_name
