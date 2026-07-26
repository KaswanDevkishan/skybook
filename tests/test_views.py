from datetime import timedelta

import pytest
from django.test import Client
from django.urls import reverse
from django.utils import timezone
from reservations.models import Airline, Booking, City, Flight


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


def test_booking_form_renders_fields_and_csrf_token(client):
    response = client.get(reverse("reservations:booking_new"))
    content = response.content.decode()

    assert response.status_code == 200
    assert_template_used(response, "reservations/booking_form.html")
    assert 'name="passenger_name"' in content
    assert 'name="passenger_email"' in content
    assert 'name="csrfmiddlewaretoken"' in content


def test_booking_submission_without_csrf_token_is_forbidden():
    client = Client(enforce_csrf_checks=True)

    response = client.post(
        reverse("reservations:booking_submit"),
        {"passenger_name": "Aiko Tanaka", "passenger_email": "aiko@example.com"},
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_valid_booking_submission_redirects_without_persisting(client):
    response = client.post(
        reverse("reservations:booking_submit"),
        {"passenger_name": "Aiko Tanaka", "passenger_email": "aiko@example.com"},
    )

    assert response.status_code == 302
    assert response.url == reverse("reservations:home")
    assert Booking.objects.count() == 0


@pytest.mark.parametrize(
    ("data", "error_field"),
    [
        ({"passenger_email": "aiko@example.com"}, "passenger_name"),
        ({"passenger_name": "Aiko Tanaka"}, "passenger_email"),
        (
            {"passenger_name": "", "passenger_email": "aiko@example.com"},
            "passenger_name",
        ),
        (
            {"passenger_name": "Aiko Tanaka", "passenger_email": "   "},
            "passenger_email",
        ),
    ],
)
def test_invalid_booking_submission_returns_form_with_errors(client, data, error_field):
    response = client.post(reverse("reservations:booking_submit"), data)

    assert response.status_code == 400
    assert_template_used(response, "reservations/booking_form.html")
    assert error_field in response.context["errors"]
    assert response.context["passenger_name"] == data.get("passenger_name", "")
    assert response.context["passenger_email"] == data.get("passenger_email", "")


def test_booking_submission_rejects_unsupported_methods(client):
    response = client.get(reverse("reservations:booking_submit"))

    assert response.status_code == 405
