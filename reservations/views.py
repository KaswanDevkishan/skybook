from django.db import IntegrityError, transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from reservations.forms import BookingForm, FlightSearchForm
from reservations.models import Booking, Flight


@require_GET
def home(request):
    return render(request, "reservations/home.html")


@require_GET
def flight_list(request):
    form = FlightSearchForm(request.GET or None)
    flights = Flight.objects.order_by("departure_time")

    if form.is_bound:
        if form.is_valid():
            flights = flights.filter(
                origin=form.cleaned_data["origin"],
                destination=form.cleaned_data["destination"],
                departure_time__date=form.cleaned_data["departure_date"],
            )
        else:
            flights = Flight.objects.none()

    context = {"form": form, "flights": flights}
    template_name = (
        "reservations/partials/flight_results.html"
        if request.headers.get("HX-Request") == "true"
        else "reservations/flight_list.html"
    )
    return render(request, template_name, context)


@require_GET
def flight_detail(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)
    return render(request, "reservations/flight_detail.html", {"flight": flight})


@require_GET
def booking_new(request):
    return render(request, "reservations/booking_form.html", {"form": BookingForm()})


@require_POST
def booking_submit(request):
    form = BookingForm(request.POST)

    if form.is_valid():
        try:
            with transaction.atomic():
                form.save()
        except IntegrityError:
            seat = form.cleaned_data["seat"]
            if not Booking.objects.filter(seat=seat).exists():
                raise
            form.add_error("seat", "This seat was booked before your request completed.")
        else:
            return redirect("reservations:home")

    return render(request, "reservations/booking_form.html", {"form": form})


@require_GET
def health(request):
    return HttpResponse("ok", content_type="text/plain")
