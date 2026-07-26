import re

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from reservations.forms import BookingForm, FlightSearchForm, RegistrationForm, SignInForm
from reservations.models import Booking, Flight, Seat
from reservations.pending_booking import (
    clear_pending_booking,
    load_pending_booking,
    store_pending_booking,
)
from reservations.pricing import calculate_booking_price
from reservations.queries import flights_with_availability
from reservations.services import BookingReferenceError, SeatUnavailableError, create_booking

SEAT_NUMBER_PATTERN = re.compile(r"^(?P<row>\d+)(?P<letter>[A-Z]+)$")


class SignInView(LoginView):
    authentication_form = SignInForm
    template_name = "reservations/sign_in.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        if load_pending_booking(self.request) is not None:
            return reverse("reservations:resume_booking")
        return super().get_success_url()


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
            seat.is_available = not any(
                booking.status == Booking.Status.CONFIRMED for booking in seat.bookings.all()
            )
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


@require_http_methods(["GET", "POST"])
def register(request):
    if request.user.is_authenticated:
        return redirect("reservations:account")

    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        if load_pending_booking(request) is not None:
            return redirect("reservations:resume_booking")
        return redirect("reservations:account")
    return render(request, "reservations/register.html", {"form": form})


@require_POST
def sign_out(request):
    logout(request)
    return redirect("reservations:flight_list")


@login_required
@require_GET
def account(request):
    now = timezone.now()
    bookings = (
        Booking.objects.filter(
            user=request.user,
            status=Booking.Status.CONFIRMED,
        )
        .select_related(
            "seat__flight__airline",
            "seat__flight__origin",
            "seat__flight__destination",
        )
        .order_by("-created_at")
    )
    for booking in bookings:
        booking.can_cancel = booking.seat.flight.departure_time > now
    return render(request, "reservations/account.html", {"bookings": bookings})


@require_GET
def my_bookings(request):
    if request.user.is_authenticated:
        return redirect("reservations:account")
    return render(request, "reservations/guest_bookings.html")


@require_GET
def flight_list(request):
    form = FlightSearchForm(request.GET or None)
    flights = Flight.objects.none()

    if form.is_bound:
        if form.is_valid():
            flights = flights_with_availability().filter(
                origin=form.cleaned_data["origin"],
                destination=form.cleaned_data["destination"],
                departure_time__date=form.cleaned_data["departure_date"],
            )
    else:
        flights = flights_with_availability()

    is_htmx = request.headers.get("HX-Request") == "true"
    context = {"form": form, "flights": flights, "is_htmx": is_htmx}
    template_name = (
        "reservations/partials/flight_results.html" if is_htmx else "reservations/flight_list.html"
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
    initial = {}
    if request.method == "GET" and request.user.is_authenticated:
        initial = {
            "passenger_name": request.user.get_full_name().strip(),
            "passenger_email": request.user.email,
        }
    form = BookingForm(request.POST or None, flight=flight, initial=initial)
    all_seats = list(
        flight.seats.order_by("cabin_class", "seat_number").prefetch_related("bookings")
    )
    context = {"flight": flight, "form": form, "seat_groups": _seat_groups(all_seats)}

    if request.method == "POST" and form.is_valid():
        seat = form.cleaned_data["seat"]
        if not request.user.is_authenticated:
            store_pending_booking(
                request,
                flight=flight,
                seat=seat,
                passenger_name=form.cleaned_data["passenger_name"],
                passenger_email=form.cleaned_data["passenger_email"],
            )
            authentication_route = (
                "reservations:register"
                if request.POST.get("action") == "register"
                else "reservations:sign_in"
            )
            authentication_url = reverse(authentication_route)
            resume_url = reverse("reservations:resume_booking")
            return redirect(f"{authentication_url}?next={resume_url}")

        price = calculate_booking_price(seat.price)
        context.update({"selected_seat": seat, "price": price})

        if request.POST.get("action") == "confirm":
            try:
                booking = create_booking(
                    flight=flight,
                    seat=seat,
                    passenger_name=form.cleaned_data["passenger_name"],
                    passenger_email=form.cleaned_data["passenger_email"],
                    user=request.user,
                )
            except SeatUnavailableError as error:
                form.add_error("seat", str(error))
            except BookingReferenceError as error:
                form.add_error(None, str(error))
            else:
                clear_pending_booking(request)
                return redirect(
                    "reservations:booking_confirmation",
                    booking_reference=booking.booking_reference,
                )
        else:
            return render(request, "reservations/booking_review.html", context)

    return render(request, "reservations/booking_form.html", context)


@login_required
@require_GET
def resume_booking(request):
    pending = load_pending_booking(request)
    if pending is None:
        messages.error(request, "Your saved booking details are no longer available.")
        return redirect("reservations:flight_list")

    flight = get_object_or_404(
        Flight.objects.select_related("airline", "origin", "destination"),
        pk=pending.flight_id,
    )
    form = BookingForm(pending.as_form_data(), flight=flight)
    all_seats = list(
        flight.seats.order_by("cabin_class", "seat_number").prefetch_related("bookings")
    )
    context = {"flight": flight, "form": form, "seat_groups": _seat_groups(all_seats)}
    if not form.is_valid():
        clear_pending_booking(request)
        form.add_error("seat", "The selected seat is no longer available.")
        return render(request, "reservations/booking_form.html", context)

    seat = form.cleaned_data["seat"]
    context.update(
        {
            "selected_seat": seat,
            "price": calculate_booking_price(seat.price),
        }
    )
    return render(request, "reservations/booking_review.html", context)


@require_GET
def booking_confirmation(request, booking_reference):
    visible_bookings = Booking.objects.filter(user__isnull=True)
    if request.user.is_authenticated:
        visible_bookings = Booking.objects.filter(Q(user__isnull=True) | Q(user=request.user))
    booking = get_object_or_404(
        visible_bookings.select_related(
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


@login_required
@require_http_methods(["GET", "POST"])
def cancel_booking(request, booking_reference):
    booking = get_object_or_404(
        Booking.objects.select_related(
            "seat__flight__airline",
            "seat__flight__origin",
            "seat__flight__destination",
        ),
        booking_reference=booking_reference,
        user=request.user,
    )
    flight = booking.seat.flight
    can_cancel = (
        booking.status == Booking.Status.CONFIRMED and flight.departure_time > timezone.now()
    )

    if request.method == "POST":
        with transaction.atomic():
            booking = get_object_or_404(
                Booking.objects.select_for_update().select_related("seat__flight"),
                pk=booking.pk,
                user=request.user,
            )
            if booking.status == Booking.Status.CANCELLED:
                messages.info(request, f"Booking {booking.booking_reference} is already cancelled.")
                return redirect("reservations:account")
            if booking.seat.flight.departure_time <= timezone.now():
                messages.error(
                    request,
                    "This booking cannot be cancelled because the flight has departed.",
                )
                return redirect(
                    "reservations:cancel_booking",
                    booking_reference=booking.booking_reference,
                )
            booking.status = Booking.Status.CANCELLED
            booking.save(update_fields=["status"])
        messages.success(
            request,
            f"Booking {booking.booking_reference} was cancelled. No real refund was issued.",
        )
        return redirect("reservations:account")

    return render(
        request,
        "reservations/booking_cancellation.html",
        {"booking": booking, "flight": flight, "can_cancel": can_cancel},
    )


@require_GET
def health(request):
    return HttpResponse("ok", content_type="text/plain")
