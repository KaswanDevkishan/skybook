from datetime import timedelta
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

import pytest
from django.template import Context, Template
from django.test import Client
from django.urls import NoReverseMatch, reverse
from django.utils import timezone
from reservations.models import Airline, Booking, City, Flight, Seat
from reservations.services import SeatUnavailableError


def assert_template_used(response, template_name):
    assert template_name in [template.name for template in response.templates]


@pytest.fixture
def flight_factory(db):
    airline = Airline.objects.create(name="SkyBook Air", code="SKY")
    origin = City.objects.create(name="Tokyo", code="TYO")
    destination = City.objects.create(name="Osaka", code="OSA")

    def create_flight(*, flight_number="201", departure_time=None):
        departure_time = departure_time or timezone.now() + timedelta(days=1)
        return Flight.objects.create(
            airline=airline,
            flight_number=flight_number,
            origin=origin,
            destination=destination,
            departure_time=departure_time,
            arrival_time=departure_time + timedelta(hours=1, minutes=25),
        )

    return create_flight


@pytest.fixture
def flight(flight_factory):
    return flight_factory()


@pytest.fixture
def seats(flight):
    return [
        Seat.objects.create(
            flight=flight,
            seat_number="1A",
            cabin_class=Seat.CabinClass.BUSINESS,
            seat_type=Seat.SeatType.WINDOW,
            price=Decimal("50000"),
        ),
        Seat.objects.create(
            flight=flight,
            seat_number="2B",
            cabin_class=Seat.CabinClass.ECONOMY,
            seat_type=Seat.SeatType.MIDDLE,
            price=Decimal("15005"),
        ),
        Seat.objects.create(
            flight=flight,
            seat_number="2C",
            cabin_class=Seat.CabinClass.ECONOMY,
            seat_type=Seat.SeatType.AISLE,
            price=Decimal("18000"),
        ),
    ]


@pytest.mark.parametrize(
    ("route_name", "expected_path"),
    [("home", "/"), ("flight_list", "/flights/"), ("health", "/health/")],
)
def test_static_routes_reverse(route_name, expected_path):
    assert reverse(f"reservations:{route_name}") == expected_path


def test_flight_specific_routes_reverse():
    assert reverse("reservations:flight_detail", args=[42]) == "/flights/42/"
    assert reverse("reservations:flight_booking", args=[42]) == "/flights/42/book/"
    assert (
        reverse("reservations:booking_confirmation", args=["SKY-ABCDEFGH"])
        == "/bookings/SKY-ABCDEFGH/confirmation/"
    )


def test_generic_booking_routes_are_removed(client):
    with pytest.raises(NoReverseMatch):
        reverse("reservations:booking_new")
    with pytest.raises(NoReverseMatch):
        reverse("reservations:booking_submit")
    assert client.get("/booking/new/").status_code == 404
    assert client.post("/booking/submit/").status_code == 404


def test_home_and_navigation_only_link_to_connected_entry(client):
    response = client.get(reverse("reservations:home"))
    content = response.content.decode()
    primary_navigation = content.split('<nav aria-label="Primary navigation">', 1)[1].split(
        "</nav>", 1
    )[0]

    assert response.status_code == 200
    assert "Japan is closer than you think" in content
    assert "Where will Japan take you next?" in content
    assert (
        "Search domestic routes, compare fares, and choose your perfect seat—all in one "
        "smooth journey."
    ) in content
    assert reverse("reservations:flight_list") in content
    assert "Booking form" not in content
    assert "Book a Flight" not in content
    assert '<nav aria-label="Primary navigation">' in content
    assert 'class="skip-link" href="#main-content"' in content
    assert f'class="site-name" href="{reverse("reservations:home")}"' in content
    assert primary_navigation.count("<li>") == 1
    assert primary_navigation.count("<a ") == 1
    assert "Home" not in primary_navigation
    assert "Flights" in primary_navigation
    assert reverse("reservations:flight_list") in primary_navigation
    assert "aria-current" not in primary_navigation
    assert "Sign In" not in content
    assert "Sign in" not in content
    assert "Create Account" not in content
    assert "site-name__mark" not in content
    assert "S SkyBook" not in content
    assert "<footer" not in content
    assert "site-footer" not in content
    assert "SkyBook Web Engineering Project" not in content


def test_health_returns_plain_text(client):
    response = client.get(reverse("reservations:health"))

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("text/plain")
    assert response.content


@pytest.mark.django_db
def test_empty_flight_list_has_complete_page_and_search_form(client):
    response = client.get(reverse("reservations:flight_list"))
    content = response.content.decode()

    assert response.status_code == 200
    assert_template_used(response, "reservations/flight_list.html")
    assert list(response.context["flights"]) == []
    assert 'method="get"' in content
    assert 'hx-get="/flights/"' in content
    assert 'aria-live="polite"' in content
    assert 'class="flight-search-hero"' in content
    assert "Flights without the friction" in content
    assert "Where are you flying next?" in content
    assert 'class="search-card"' in content
    assert 'class="container container--wide main-content"' in content
    assert "How it works" not in content
    assert "how-it-works" not in content
    assert "No flights are currently scheduled." in content


@pytest.mark.django_db
def test_flight_results_show_schedule_price_count_cabins_and_book_link(client, flight, seats):
    Booking.objects.create(
        seat=seats[2],
        guest_name="Booked Guest",
        guest_email="booked@example.com",
    )

    response = client.get(reverse("reservations:flight_list"))
    content = response.content.decode()
    result = response.context["flights"][0]

    assert result.available_seat_count == 2
    assert result.lowest_available_price == Decimal("15005")
    assert result.business_available
    assert result.economy_available
    for expected in (
        flight.airline.name,
        flight.flight_number,
        flight.origin.code,
        flight.destination.code,
        "Nonstop",
        "Seats remaining",
        "¥15,005",
        "Business",
        "Economy",
        "1h 25m",
        "View seats",
    ):
        assert expected in content
    assert "1:25:00" not in content
    assert "Book this flight" not in content
    assert 'class="flight-list flight-list--responsive"' in content
    assert 'class="flight-card__journey"' in content
    assert 'class="flight-card__route-line"' in content
    assert 'class="button flight-card__cta"' in content
    assert reverse("reservations:flight_booking", args=[flight.pk]) in content


@pytest.mark.django_db
def test_sold_out_flight_has_no_book_link(client, flight, seats):
    for index, seat in enumerate(seats):
        Booking.objects.create(
            seat=seat,
            guest_name=f"Guest {index}",
            guest_email=f"guest{index}@example.com",
        )

    response = client.get(reverse("reservations:flight_list"))
    content = response.content.decode()

    assert response.context["flights"][0].available_seat_count == 0
    assert "Sold out — no seats available" in content
    assert "View seats" not in content
    assert reverse("reservations:flight_booking", args=[flight.pk]) not in content


@pytest.mark.django_db
def test_flight_results_order_filter_and_htmx_partial_are_preserved(client, flight_factory):
    first = flight_factory(
        flight_number="100",
        departure_time=timezone.now() + timedelta(days=1),
    )
    second = flight_factory(
        flight_number="200",
        departure_time=timezone.now() + timedelta(days=2),
    )

    full_response = client.get(reverse("reservations:flight_list"))
    assert list(full_response.context["flights"]) == [first, second]

    search_response = client.get(
        reverse("reservations:flight_list"),
        {
            "origin": second.origin_id,
            "destination": second.destination_id,
            "departure_date": timezone.localtime(second.departure_time).date().isoformat(),
        },
    )
    assert list(search_response.context["flights"]) == [second]

    htmx_response = client.get(
        reverse("reservations:flight_list"),
        headers={"HX-Request": "true"},
    )
    assert_template_used(htmx_response, "reservations/partials/flight_results.html")
    htmx_content = htmx_response.content.decode()
    assert "<!DOCTYPE html>" not in htmx_content
    assert 'class="flight-list flight-list--responsive"' in htmx_content
    assert "Where are you flying next?" not in htmx_content
    assert "How it works" not in htmx_content


@pytest.mark.django_db
def test_flights_navigation_marks_search_and_booking_as_current(client, flight):
    for url in (
        reverse("reservations:flight_list"),
        reverse("reservations:flight_detail", args=[flight.pk]),
        reverse("reservations:flight_booking", args=[flight.pk]),
    ):
        content = client.get(url).content.decode()
        primary_navigation = content.split('<nav aria-label="Primary navigation">', 1)[1].split(
            "</nav>", 1
        )[0]
        assert primary_navigation.count("<li>") == 1
        assert primary_navigation.count("<a ") == 1
        assert f'href="{reverse("reservations:flight_list")}"' in primary_navigation
        assert content.count('aria-current="page"') == 1


@pytest.mark.django_db
@pytest.mark.parametrize("header_value", [None, "false", "True", "1"])
def test_only_exact_lowercase_true_header_returns_htmx_partial(client, header_value):
    headers = {} if header_value is None else {"HX-Request": header_value}
    response = client.get(reverse("reservations:flight_list"), headers=headers)
    assert_template_used(response, "reservations/flight_list.html")


@pytest.mark.django_db
def test_invalid_search_retains_values_and_returns_accessible_errors(client):
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
    content = response.content.decode()

    assert list(response.context["flights"]) == []
    assert "not-a-date" in content
    assert 'class="error-summary" role="alert"' in content


@pytest.mark.django_db
def test_flight_booking_get_is_scoped_and_accessible(client, flight, seats, flight_factory):
    other_flight = flight_factory(flight_number="999")
    other_seat = Seat.objects.create(flight=other_flight, seat_number="9F")
    Booking.objects.create(
        seat=seats[2],
        guest_name="Booked Guest",
        guest_email="booked@example.com",
    )

    response = client.get(reverse("reservations:flight_booking", args=[flight.pk]))
    content = response.content.decode()

    assert response.status_code == 200
    assert_template_used(response, "reservations/booking_form.html")
    assert_template_used(response, "reservations/base.html")
    assert other_seat not in response.context["form"].fields["seat"].queryset
    assert f'value="{other_seat.pk}"' not in content
    assert "Business" in content
    assert "Economy" in content
    assert response.context["seat_groups"][0]["rows"][0]["number"] == "1"
    assert response.context["seat_groups"][0]["letters"] == ["A"]
    assert response.context["seat_groups"][1]["rows"][0]["number"] == "2"
    assert response.context["seat_groups"][1]["letters"] == ["B", "C"]
    assert "Window" in content
    assert "Middle" in content
    assert "Aisle" in content
    assert "Available" in content
    assert "Unavailable" in content
    assert 'type="radio"' in content
    assert "¥50,000" in content
    assert "JPY 50000" not in content
    assert 'class="site-header"' in content
    assert '<nav aria-label="Primary navigation">' in content
    assert 'class="booking-layout booking-layout--seat-map"' in content
    assert 'class="booking-sidebar"' in content
    assert 'class="seat-map-scroll"' in content
    assert 'class="aircraft-map"' in content
    assert 'class="aircraft-map__nose"' in content
    assert 'class="aircraft-map__cabin"' in content
    assert 'class="cabin-map cabin-map--business"' in content
    assert 'class="seat-control seat-control--unavailable"' in content
    assert 'aria-label="Seat 1A, Business, Window, ¥50,000, available"' in content
    assert 'aria-label="Seat 2C, Economy, Aisle, ¥18,000, unavailable"' in content
    assert 'role="tooltip"' in content
    assert "✓ Selected" in content
    assert "Seat summary" in content
    assert "Estimated fee" in content
    assert "Estimated total" in content
    assert "Final pricing is recalculated on the server." in content
    assert "Available</span>" in content
    assert "Selected</span>" in content
    assert "Unavailable</span>" in content
    assert "disabled" in content
    assert 'aria-disabled="true"' in content
    assert 'name="csrfmiddlewaretoken"' in content
    assert 'src="/static/reservations/seat-map.js"' in content


@pytest.mark.django_db
def test_selected_seat_retains_native_checked_state_and_summary_estimates(client, flight, seats):
    response = client.post(
        reverse("reservations:flight_booking", args=[flight.pk]),
        {
            "action": "review",
            "seat": seats[1].pk,
            "passenger_name": "",
            "passenger_email": "aiko@example.com",
        },
    )
    content = response.content.decode()

    assert response.status_code == 200
    assert f'id="seat-{seats[1].pk}"' in content
    assert "checked" in content
    assert 'data-seat-number="2B"' in content
    assert 'data-base-fare="¥15,005"' in content
    assert 'data-estimated-fee="¥1,501"' in content
    assert 'data-estimated-total="¥16,506"' in content


@pytest.mark.django_db
def test_invalid_flight_booking_returns_404(client):
    assert client.get(reverse("reservations:flight_booking", args=[999999])).status_code == 404


@pytest.mark.django_db
def test_review_calculates_server_price_without_creating_booking(client, flight, seats):
    response = client.post(
        reverse("reservations:flight_booking", args=[flight.pk]),
        {
            "action": "review",
            "seat": seats[1].pk,
            "passenger_name": "Aiko Tanaka",
            "passenger_email": "aiko@example.com",
            "base_fare": "1",
            "total_price": "1",
        },
    )
    content = response.content.decode()

    assert response.status_code == 200
    assert_template_used(response, "reservations/booking_review.html")
    assert Booking.objects.count() == 0
    for expected in (
        "Aiko Tanaka",
        "aiko@example.com",
        "Seat",
        "2B",
        "Economy",
        "Middle",
        "¥15,005",
        "¥1,501",
        "¥16,506",
        "Taxes and fees (10%)",
    ):
        assert expected in content


@pytest.mark.django_db
def test_confirm_creates_guest_booking_and_redirects_to_detailed_receipt(client, flight, seats):
    response = client.post(
        reverse("reservations:flight_booking", args=[flight.pk]),
        {
            "action": "confirm",
            "seat": seats[1].pk,
            "passenger_name": "Aiko Tanaka",
            "passenger_email": "aiko@example.com",
            "total_price": "1",
        },
    )

    booking = Booking.objects.get()
    assert response.status_code == 302
    assert response.url == reverse(
        "reservations:booking_confirmation",
        args=[booking.booking_reference],
    )
    assert booking.user is None
    assert booking.base_fare == Decimal("15005")
    assert booking.taxes_and_fees == Decimal("1501")
    assert booking.total_price == Decimal("16506")

    receipt = client.get(response.url)
    content = receipt.content.decode()
    for expected in (
        booking.booking_reference,
        "Aiko Tanaka",
        "aiko@example.com",
        flight.airline.name,
        flight.flight_number,
        flight.origin.name,
        flight.destination.name,
        seats[1].seat_number,
        "Economy",
        "Middle",
        "¥15,005",
        "¥1,501",
        "¥16,506",
        "Return to flight search",
    ):
        assert expected in content


@pytest.mark.django_db
def test_direct_confirm_rejects_cross_flight_seat(client, flight, flight_factory):
    other_flight = flight_factory(flight_number="999")
    other_seat = Seat.objects.create(flight=other_flight, seat_number="9A")

    response = client.post(
        reverse("reservations:flight_booking", args=[flight.pk]),
        {
            "action": "confirm",
            "seat": other_seat.pk,
            "passenger_name": "Aiko Tanaka",
            "passenger_email": "aiko@example.com",
        },
    )

    assert response.status_code == 200
    assert "Select an available seat for this flight." in response.content.decode()
    assert Booking.objects.count() == 0


@pytest.mark.django_db
def test_booked_seat_and_stale_confirmation_are_rejected(client, flight, seats):
    existing = Booking.objects.create(
        seat=seats[0],
        guest_name="Existing Guest",
        guest_email="existing@example.com",
    )
    response = client.post(
        reverse("reservations:flight_booking", args=[flight.pk]),
        {
            "action": "confirm",
            "seat": seats[0].pk,
            "passenger_name": "Aiko Tanaka",
            "passenger_email": "aiko@example.com",
        },
    )

    assert response.status_code == 200
    assert "Select an available seat for this flight." in response.content.decode()
    assert list(Booking.objects.all()) == [existing]


@pytest.mark.django_db
def test_transaction_conflict_returns_visible_error(client, flight, seats):
    with patch(
        "reservations.views.create_guest_booking",
        side_effect=SeatUnavailableError("This seat was booked before confirmation."),
    ):
        response = client.post(
            reverse("reservations:flight_booking", args=[flight.pk]),
            {
                "action": "confirm",
                "seat": seats[0].pk,
                "passenger_name": "Aiko Tanaka",
                "passenger_email": "aiko@example.com",
            },
        )

    assert response.status_code == 200
    assert "This seat was booked before confirmation." in response.content.decode()
    assert 'role="alert"' in response.content.decode()


@pytest.mark.django_db
def test_booking_posts_require_csrf(flight, seats):
    client = Client(enforce_csrf_checks=True)
    response = client.post(
        reverse("reservations:flight_booking", args=[flight.pk]),
        {
            "action": "confirm",
            "seat": seats[0].pk,
            "passenger_name": "Aiko",
            "passenger_email": "aiko@example.com",
        },
    )
    assert response.status_code == 403
    assert Booking.objects.count() == 0


@pytest.mark.django_db
def test_confirmation_404_and_method_rules(client, flight):
    assert (
        client.get(reverse("reservations:booking_confirmation", args=["SKY-NOTFOUND"])).status_code
        == 404
    )
    assert client.put(reverse("reservations:flight_booking", args=[flight.pk])).status_code == 405
    assert (
        client.post(reverse("reservations:booking_confirmation", args=["SKY-NOTFOUND"])).status_code
        == 405
    )


def test_booking_styles_include_responsive_focus_and_state_rules():
    stylesheet = Path("reservations/static/reservations/styles.css")
    content = stylesheet.read_text()
    for expected in (
        ":focus-visible",
        ".seat-map-scroll",
        ".aircraft-map__nose",
        ".aircraft-map__wing",
        ".aircraft-map__cabin",
        ".aircraft-seat-row",
        ".seat-control input:checked + label",
        ".seat-control input:focus-visible + label",
        ".seat-control--unavailable",
        ".cabin-map--business",
        ".booking-layout--seat-map",
        ".booking-sidebar__sticky",
        ".booking-mobile-action",
        "overflow-x: auto",
        "position: sticky",
        "@media (max-width: 64rem)",
        ".review-card",
        "@media (max-width: 40rem)",
    ):
        assert expected in content


def test_seat_map_script_only_enhances_the_native_selection_summary():
    script = Path("reservations/static/reservations/seat-map.js").read_text()

    assert 'input[name="seat"]' in script
    assert "data-seat-summary" in script
    assert "dataset.estimatedTotal" in script
    assert "fetch(" not in script


def test_flight_search_styles_use_readable_wide_layout_without_scaling():
    stylesheet = Path("reservations/static/reservations/styles.css")
    content = stylesheet.read_text()

    assert ".container--wide {" in content
    assert "width: min(100% - 3rem, 72rem);" in content
    assert "calc((100vw - 72rem) / 2)" in content
    assert "transform: scale" not in content
    assert "zoom:" not in content
    assert ".how-it-works" not in content


def test_navigation_styles_preserve_keyboard_and_responsive_behavior():
    stylesheet = Path("reservations/static/reservations/styles.css").read_text()

    assert ":focus-visible" in stylesheet
    assert ".site-name {" in stylesheet
    assert ".nav-list a {" in stylesheet
    assert '.nav-list a[aria-current="page"]' in stylesheet
    assert "@media (max-width: 40rem)" in stylesheet
    assert ".header-layout {" in stylesheet
    assert ".nav-list {" in stylesheet
    assert ".site-footer" not in stylesheet


def test_jpy_template_filter_groups_whole_yen_without_decimals():
    rendered = Template("{% load reservation_format %}{{ first|jpy }} / {{ second|jpy }}").render(
        Context({"first": Decimal("52000"), "second": Decimal("16500")})
    )

    assert rendered == "¥52,000 / ¥16,500"
