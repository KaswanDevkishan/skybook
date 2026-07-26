from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from reservations.models import Flight


@require_GET
def home(request):
    return render(request, "reservations/home.html")


@require_GET
def flight_list(request):
    flights = Flight.objects.order_by("departure_time")
    return render(request, "reservations/flight_list.html", {"flights": flights})


@require_GET
def flight_detail(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)
    return render(request, "reservations/flight_detail.html", {"flight": flight})


@require_GET
def booking_new(request):
    return render(request, "reservations/booking_form.html")


@require_POST
def booking_submit(request):
    passenger_name = request.POST.get("passenger_name", "")
    passenger_email = request.POST.get("passenger_email", "")
    errors = {}

    if not passenger_name.strip():
        errors["passenger_name"] = "Passenger name is required."
    if not passenger_email.strip():
        errors["passenger_email"] = "Passenger email is required."

    if errors:
        context = {
            "errors": errors,
            "passenger_name": passenger_name,
            "passenger_email": passenger_email,
        }
        return render(request, "reservations/booking_form.html", context, status=400)

    return redirect("reservations:home")


@require_GET
def health(request):
    return HttpResponse("ok", content_type="text/plain")
