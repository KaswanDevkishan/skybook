from django import forms
from django.core.exceptions import ValidationError

from reservations.models import Booking, City, Seat


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
    seat = forms.ModelChoiceField(queryset=Seat.objects.all())
    passenger_name = forms.CharField(max_length=100)
    passenger_email = forms.EmailField()

    def clean_seat(self):
        seat = self.cleaned_data["seat"]
        if Booking.objects.filter(seat=seat).exists():
            raise ValidationError("This seat is already booked.")
        return seat

    def save(self):
        if not self.is_valid():
            raise ValueError("Cannot save an invalid booking form.")

        return Booking.objects.create(
            seat=self.cleaned_data["seat"],
            guest_name=self.cleaned_data["passenger_name"],
            guest_email=self.cleaned_data["passenger_email"],
        )
