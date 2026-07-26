from datetime import timedelta
from unittest.mock import patch

import pytest
from django.db import IntegrityError
from django.test import Client
from django.urls import reverse
from django.utils import timezone
from reservations.forms import BookingForm
from reservations.models import Airline, Booking, City, Flight, Seat


def assert_template_used(response, template_name):
    assert template_name in [template.name for template in response.templates]


@pytest.fixture
def flight_factory(db):
    airline = Airline.objects.create(name="SkyBook Air", code="SKY")
    origin = City.objects.create(name="Tokyo", code="TYO")
    destination = City.objects.create(name="Osaka", code="OSA")

    def create_flight(*, flight_number, departure_time):
        return Flight.objects.create(
            airline=airline,
            flight_number=flight_number,
            origin=origin,
            destination=destination,
            departure_time=departure_time,
            arrival_time=departure_time + timedelta(hours=1),
        )

    return create_flight


@pytest.fixture
def seat(db, flight_factory):
    flight = flight_factory(
        flight_number="201",
        departure_time=timezone.now() + timedelta(days=1),
    )
    return Seat.objects.create(flight=flight, seat_number="1A")


@pytest.mark.parametrize(
    ("route_name", "expected_path"),
    [
        ("home", "/"),
        ("flight_list", "/flights/"),
        ("booking_new", "/booking/new/"),
        ("booking_submit", "/booking/submit/"),
        ("health", "/health/"),
    ],
)
def test_static_routes_reverse(route_name, expected_path):
    assert reverse(f"reservations:{route_name}") == expected_path


def test_flight_detail_route_reverses_with_flight_id():
    assert reverse("reservations:flight_detail", kwargs={"flight_id": 42}) == "/flights/42/"


def test_home_renders_navigation_links(client):
    response = client.get(reverse("reservations:home"))

    assert response.status_code == 200
    assert_template_used(response, "reservations/home.html")
    assert reverse("reservations:flight_list") in response.content.decode()
    assert reverse("reservations:booking_new") in response.content.decode()


def test_health_returns_plain_text(client):
    response = client.get(reverse("reservations:health"))

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("text/plain")
    assert response.content


@pytest.mark.django_db
def test_flight_list_renders_empty_context(client):
    response = client.get(reverse("reservations:flight_list"))

    assert response.status_code == 200
    assert_template_used(response, "reservations/flight_list.html")
    assert list(response.context["flights"]) == []


@pytest.mark.django_db
def test_flight_list_orders_flights_by_departure_time(client, flight_factory):
    later_departure = timezone.now() + timedelta(days=2)
    earlier = flight_factory(
        flight_number="102", departure_time=later_departure - timedelta(days=1)
    )
    later = flight_factory(flight_number="101", departure_time=later_departure)

    response = client.get(reverse("reservations:flight_list"))

    assert response.status_code == 200
    assert_template_used(response, "reservations/flight_list.html")
    assert list(response.context["flights"]) == [earlier, later]


@pytest.mark.django_db
def test_flight_list_renders_unbound_search_form(client):
    response = client.get(reverse("reservations:flight_list"))
    content = response.content.decode()

    assert response.status_code == 200
    assert not response.context["form"].is_bound
    assert 'name="origin"' in content
    assert 'name="destination"' in content
    assert 'name="departure_date"' in content
    assert 'method="get"' in content


@pytest.mark.django_db
def test_flight_list_filters_valid_get_query_and_orders_results(client):
    origin = City.objects.create(name="Tokyo", code="TYO")
    destination = City.objects.create(name="Osaka", code="OSA")
    other_destination = City.objects.create(name="Sapporo", code="SPK")
    airline = Airline.objects.create(name="SkyBook Air", code="SKY")
    departure_date = timezone.localdate() + timedelta(days=2)
    start = timezone.make_aware(
        timezone.datetime.combine(departure_date, timezone.datetime.min.time())
    )

    later = Flight.objects.create(
        airline=airline,
        flight_number="102",
        origin=origin,
        destination=destination,
        departure_time=start + timedelta(hours=12),
        arrival_time=start + timedelta(hours=13),
    )
    earlier = Flight.objects.create(
        airline=airline,
        flight_number="101",
        origin=origin,
        destination=destination,
        departure_time=start + timedelta(hours=8),
        arrival_time=start + timedelta(hours=9),
    )
    Flight.objects.create(
        airline=airline,
        flight_number="103",
        origin=origin,
        destination=other_destination,
        departure_time=start + timedelta(hours=7),
        arrival_time=start + timedelta(hours=8),
    )

    response = client.get(
        reverse("reservations:flight_list"),
        {
            "origin": origin.pk,
            "destination": destination.pk,
            "departure_date": departure_date.isoformat(),
        },
    )

    assert response.status_code == 200
    assert response.context["form"].is_valid()
    assert list(response.context["flights"]) == [earlier, later]


@pytest.mark.django_db
def test_flight_list_rejects_same_city_and_retains_values(client):
    city = City.objects.create(name="Tokyo", code="TYO")

    response = client.get(
        reverse("reservations:flight_list"),
        {
            "origin": city.pk,
            "destination": city.pk,
            "departure_date": "2026-08-01",
        },
    )
    content = response.content.decode()

    assert response.status_code == 200
    assert list(response.context["flights"]) == []
    assert "Origin and destination must be different." in content
    assert f'<option value="{city.pk}" selected>' in content
    assert 'value="2026-08-01"' in content


@pytest.mark.django_db
@pytest.mark.parametrize(
    "query",
    [
        {"origin": "", "destination": "", "departure_date": ""},
        {"origin": "999", "destination": "998", "departure_date": "not-a-date"},
    ],
)
def test_flight_list_invalid_input_shows_errors_and_no_results(client, query):
    response = client.get(reverse("reservations:flight_list"), query)
    content = response.content.decode()

    assert response.status_code == 200
    assert response.context["form"].errors
    assert list(response.context["flights"]) == []
    assert "errorlist" in content


@pytest.mark.django_db
def test_flight_list_retains_invalid_date_value(client):
    origin = City.objects.create(name="Tokyo", code="TYO")
    destination = City.objects.create(name="Osaka", code="OSA")

    response = client.get(
        reverse("reservations:flight_list"),
        {
            "origin": origin.pk,
            "destination": destination.pk,
            "departure_date": "not-a-date",
        },
    )

    assert "not-a-date" in response.content.decode()
    assert "departure_date" in response.context["form"].errors


@pytest.mark.django_db
def test_flight_detail_renders_flight_fields(client, flight_factory):
    flight = flight_factory(flight_number="101", departure_time=timezone.now())

    response = client.get(reverse("reservations:flight_detail", args=[flight.id]))
    content = response.content.decode()

    assert response.status_code == 200
    assert_template_used(response, "reservations/flight_detail.html")
    assert response.context["flight"] == flight
    assert str(flight.airline) in content
    assert str(flight.origin) in content
    assert str(flight.destination) in content
    assert str(flight.departure_time.year) in content
    assert str(flight.arrival_time.year) in content


@pytest.mark.django_db
def test_flight_detail_returns_404_for_missing_flight(client):
    response = client.get(reverse("reservations:flight_detail", args=[999]))

    assert response.status_code == 404


@pytest.mark.django_db
def test_booking_form_renders_unbound_fields_and_csrf_token(client):
    response = client.get(reverse("reservations:booking_new"))
    content = response.content.decode()

    assert response.status_code == 200
    assert_template_used(response, "reservations/booking_form.html")
    assert not response.context["form"].is_bound
    assert 'name="seat"' in content
    assert 'name="passenger_name"' in content
    assert 'name="passenger_email"' in content
    assert 'name="csrfmiddlewaretoken"' in content


@pytest.mark.django_db
def test_booking_submission_without_csrf_token_is_forbidden():
    client = Client(enforce_csrf_checks=True)

    response = client.post(
        reverse("reservations:booking_submit"),
        {"seat": "1", "passenger_name": "Aiko Tanaka", "passenger_email": "aiko@example.com"},
    )

    assert response.status_code == 403
    assert Booking.objects.count() == 0


@pytest.mark.django_db
def test_valid_booking_submission_creates_guest_booking_and_redirects(client, seat):
    response = client.post(
        reverse("reservations:booking_submit"),
        {
            "seat": seat.pk,
            "passenger_name": "Aiko Tanaka",
            "passenger_email": "aiko@example.com",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("reservations:home")
    booking = Booking.objects.get()
    assert booking.seat == seat
    assert booking.user is None
    assert booking.guest_name == "Aiko Tanaka"
    assert booking.guest_email == "aiko@example.com"


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("data_factory", "error_field"),
    [
        (
            lambda seat: {
                "seat": seat.pk,
                "passenger_email": "aiko@example.com",
            },
            "passenger_name",
        ),
        (
            lambda seat: {
                "seat": seat.pk,
                "passenger_name": "Aiko Tanaka",
                "passenger_email": "not-an-email",
            },
            "passenger_email",
        ),
        (
            lambda seat: {
                "seat": 999999,
                "passenger_name": "Aiko Tanaka",
                "passenger_email": "aiko@example.com",
            },
            "seat",
        ),
    ],
)
def test_invalid_booking_submission_retains_values_and_creates_nothing(
    client, seat, data_factory, error_field
):
    data = data_factory(seat)
    response = client.post(reverse("reservations:booking_submit"), data)
    content = response.content.decode()

    assert response.status_code == 200
    assert_template_used(response, "reservations/booking_form.html")
    assert error_field in response.context["form"].errors
    assert data.get("passenger_name", "") in content
    assert data.get("passenger_email", "") in content
    assert Booking.objects.count() == 0


@pytest.mark.django_db
def test_booking_submission_rejects_already_booked_seat(client, seat):
    Booking.objects.create(
        seat=seat,
        guest_name="Existing Passenger",
        guest_email="existing@example.com",
    )

    response = client.post(
        reverse("reservations:booking_submit"),
        {
            "seat": seat.pk,
            "passenger_name": "Aiko Tanaka",
            "passenger_email": "aiko@example.com",
        },
    )

    assert response.status_code == 200
    assert "This seat is already booked." in response.content.decode()
    assert Booking.objects.count() == 1


@pytest.mark.django_db
def test_booking_submission_handles_stale_duplicate_conflict(client, seat):
    existing = Booking.objects.create(
        seat=seat,
        guest_name="Existing Passenger",
        guest_email="existing@example.com",
    )

    with (
        patch.object(BookingForm, "clean_seat", lambda form: form.cleaned_data["seat"]),
        patch.object(BookingForm, "save", side_effect=IntegrityError("duplicate seat")),
    ):
        response = client.post(
            reverse("reservations:booking_submit"),
            {
                "seat": seat.pk,
                "passenger_name": "Aiko Tanaka",
                "passenger_email": "aiko@example.com",
            },
        )

    assert response.status_code == 200
    assert "booked before your request completed" in response.content.decode()
    assert list(Booking.objects.all()) == [existing]


def test_booking_submission_rejects_unsupported_methods(client):
    response = client.get(reverse("reservations:booking_submit"))

    assert response.status_code == 405
