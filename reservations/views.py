import re

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from reservations.forms import BookingForm, FlightSearchForm
from reservations.models import Booking, Flight, Seat
from reservations.pricing import calculate_booking_price
from reservations.queries import flights_with_availability
from reservations.services import BookingReferenceError, SeatUnavailableError, create_guest_booking

SEAT_NUMBER_PATTERN = re.compile(r"^(?P<row>\d+)(?P<letter>[A-Z]+)$")


def _seat_position(seat_number):
    match = SEAT_NUMBER_PATTERN.fullmatch(seat_number.strip().upper())
    if match is None:
        return seat_number, seat_number
    return match.group("row"), match.group("letter")


def _seat_groups(seats):
    groups = []
    for cabin_value, cabin_label in (
        (Seat.CabinClass.BUSINESS, Seat.CabinClass.BUSINESS.label),
        (Seat.CabinClass.ECONOMY, Seat.CabinClass.ECONOMY.label),
    ):
        rows = {}
        letters = set()
        for seat in seats:
            if seat.cabin_class != cabin_value:
                continue
            seat.is_available = not bool(seat.bookings.all())
            seat.row_number, seat.seat_letter = _seat_position(seat.seat_number)
            seat.estimated_price = calculate_booking_price(seat.price)
            rows.setdefault(seat.row_number, {})[seat.seat_letter] = seat
            letters.add(seat.seat_letter)
        if rows:
            ordered_letters = sorted(letters)
            cabin_rows = []
            for number, row_seats in sorted(
                rows.items(),
                key=lambda item: (int(item[0]) if item[0].isdigit() else float("inf"), item[0]),
            ):
                cells = []
                previous_seat = None
                for letter in ordered_letters:
                    seat = row_seats.get(letter)
                    aisle_before = bool(
                        previous_seat
                        and seat
                        and previous_seat.seat_type == Seat.SeatType.AISLE
                        and seat.seat_type == Seat.SeatType.AISLE
                    )
                    cells.append(
                        {
                            "letter": letter,
                            "seat": seat,
                            "aisle_before": aisle_before,
                        }
                    )
                    if seat:
                        previous_seat = seat
                cabin_rows.append({"number": number, "cells": cells})
            groups.append(
                {
                    "value": cabin_value,
                    "label": cabin_label,
                    "letters": ordered_letters,
                    "rows": cabin_rows,
                }
            )
    return groups


@require_GET
def home(request):
    return render(request, "reservations/home.html")


@require_GET
def flight_list(request):
    form = FlightSearchForm(request.GET or None)
    flights = flights_with_availability()

    if form.is_bound:
        if form.is_valid():
            flights = flights.filter(
                origin=form.cleaned_data["origin"],
                destination=form.cleaned_data["destination"],
                departure_time__date=form.cleaned_data["departure_date"],
            )
        else:
            flights = flights_with_availability(Flight.objects.none())

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


@require_http_methods(["GET", "POST"])
def flight_booking(request, flight_id):
    flight = get_object_or_404(
        Flight.objects.select_related("airline", "origin", "destination"),
        pk=flight_id,
    )
    form = BookingForm(request.POST or None, flight=flight)
    all_seats = list(
        flight.seats.order_by("cabin_class", "seat_number").prefetch_related("bookings")
    )
    context = {"flight": flight, "form": form, "seat_groups": _seat_groups(all_seats)}

    if request.method == "POST" and form.is_valid():
        seat = form.cleaned_data["seat"]
        price = calculate_booking_price(seat.price)
        context.update({"selected_seat": seat, "price": price})

        if request.POST.get("action") == "confirm":
            try:
                booking = create_guest_booking(
                    flight=flight,
                    seat=seat,
                    passenger_name=form.cleaned_data["passenger_name"],
                    passenger_email=form.cleaned_data["passenger_email"],
                )
            except SeatUnavailableError as error:
                form.add_error("seat", str(error))
            except BookingReferenceError as error:
                form.add_error(None, str(error))
            else:
                return redirect(
                    "reservations:booking_confirmation",
                    booking_reference=booking.booking_reference,
                )
        else:
            return render(request, "reservations/booking_review.html", context)

    return render(request, "reservations/booking_form.html", context)


@require_GET
def booking_confirmation(request, booking_reference):
    booking = get_object_or_404(
        Booking.objects.select_related(
            "seat__flight__airline",
            "seat__flight__origin",
            "seat__flight__destination",
        ),
        booking_reference=booking_reference,
    )
    return render(
        request,
        "reservations/booking_confirmation.html",
        {"booking": booking, "flight": booking.seat.flight},
    )


@require_GET
def health(request):
    return HttpResponse("ok", content_type="text/plain")
