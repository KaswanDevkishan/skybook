from datetime import timedelta
from decimal import Decimal
from pathlib import Path

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from django.utils import timezone
from reservations.models import Airline, Booking, City, Flight, Seat
from reservations.pending_booking import PENDING_BOOKING_SESSION_KEY
from reservations.services import create_booking

pytestmark = pytest.mark.django_db

PASSWORD = "SkyBook!4729Unique"


@pytest.fixture
def user():
    return get_user_model().objects.create_user(
        username="aiko",
        email="aiko@example.com",
        first_name="Aiko",
        last_name="Tanaka",
        password=PASSWORD,
    )


@pytest.fixture
def flight_and_seats():
    origin = City.objects.create(name="Tokyo", code="TYO")
    destination = City.objects.create(name="Sapporo", code="SPK")
    airline = Airline.objects.create(name="SkyBook Air", code="SKY")
    departure = timezone.now() + timedelta(days=2)
    flight = Flight.objects.create(
        airline=airline,
        flight_number="401",
        origin=origin,
        destination=destination,
        departure_time=departure,
        arrival_time=departure + timedelta(hours=1, minutes=40),
    )
    seats = [
        Seat.objects.create(flight=flight, seat_number=number, price=Decimal(price))
        for number, price in (("1A", "20000"), ("1B", "22000"), ("1C", "24000"))
    ]
    return flight, seats


def registration_data(**overrides):
    data = {
        "username": "newtraveler",
        "email": "new@example.com",
        "first_name": "New",
        "last_name": "Traveler",
        "password1": PASSWORD,
        "password2": PASSWORD,
    }
    data.update(overrides)
    return data


def test_account_routes_reverse():
    assert reverse("reservations:register") == "/accounts/register/"
    assert reverse("reservations:sign_in") == "/accounts/sign-in/"
    assert reverse("reservations:sign_out") == "/accounts/sign-out/"
    assert reverse("reservations:account") == "/account/"
    assert reverse("reservations:my_bookings") == "/bookings/"


def test_successful_registration_hashes_password_and_logs_user_in(client):
    response = client.post(reverse("reservations:register"), registration_data())

    created = get_user_model().objects.get(username="newtraveler")
    assert response.status_code == 302
    assert response.url == reverse("reservations:account")
    assert created.email == "new@example.com"
    assert created.first_name == "New"
    assert created.last_name == "Traveler"
    assert created.password != PASSWORD
    assert created.check_password(PASSWORD)
    assert client.get(reverse("reservations:account")).context["user"] == created


@pytest.mark.parametrize(
    ("overrides", "field_name"),
    [
        ({"password2": "Different!5830Pass"}, "password2"),
        ({"password1": "password", "password2": "password"}, "password2"),
        ({"email": "not-an-email"}, "email"),
    ],
)
def test_registration_rejects_invalid_password_or_email(client, overrides, field_name):
    response = client.post(reverse("reservations:register"), registration_data(**overrides))

    assert response.status_code == 200
    assert field_name in response.context["form"].errors
    assert get_user_model().objects.count() == 0


def test_registration_rejects_duplicate_username_and_email(client, user):
    username_response = client.post(
        reverse("reservations:register"),
        registration_data(username=user.username),
    )
    email_response = client.post(
        reverse("reservations:register"),
        registration_data(username="different", email="AIKO@EXAMPLE.COM"),
    )

    assert "username" in username_response.context["form"].errors
    assert "email" in email_response.context["form"].errors
    assert get_user_model().objects.count() == 1


def test_invalid_registration_retains_safe_values_but_not_passwords(client):
    response = client.post(
        reverse("reservations:register"),
        registration_data(password2="Different!5830Pass"),
    )
    content = response.content.decode()

    assert 'value="newtraveler"' in content
    assert 'value="new@example.com"' in content
    assert PASSWORD not in content
    assert "Different!5830Pass" not in content
    assert 'role="alert"' in content


def test_failed_sign_in_shows_one_friendly_accessible_alert(client, user):
    failed = client.post(
        reverse("reservations:sign_in"),
        {"username": user.username, "password": "wrong"},
    )
    content = failed.content.decode()
    friendly_message = "We couldn’t sign you in. Check your username and password and try again."

    assert failed.status_code == 200
    assert content.count(friendly_message) == 1
    assert "Please enter a correct username and password." not in content
    assert 'class="error-summary auth-form__error" role="alert"' in content
    assert "_auth_user_id" not in client.session


def test_required_sign_in_field_errors_stay_associated_with_inputs(client):
    response = client.post(reverse("reservations:sign_in"), {})
    content = response.content.decode()

    assert response.status_code == 200
    assert "We couldn’t sign you in." not in content
    for field_name in ("username", "password"):
        field = response.context["form"][field_name]
        assert field.errors
        assert f'id="{field.id_for_label}-errors"' in content
        assert f'aria-describedby="{field.id_for_label}-errors"' in content


def test_successful_sign_in_and_safe_redirects_are_unchanged(client, user):
    success = client.post(
        reverse("reservations:sign_in"),
        {"username": user.username, "password": PASSWORD},
    )
    assert success.url == reverse("reservations:account")
    assert client.session["_auth_user_id"] == str(user.pk)

    for next_url, expected in (
        (reverse("reservations:flight_list"), reverse("reservations:flight_list")),
        ("https://attacker.example/steal", reverse("reservations:account")),
        ("//attacker.example/steal", reverse("reservations:account")),
    ):
        client.logout()
        response = client.post(
            reverse("reservations:sign_in"),
            {
                "username": user.username,
                "password": PASSWORD,
                "next": next_url,
            },
        )
        assert response.url == expected


def test_logout_is_post_only_and_csrf_protected(user):
    client = Client(enforce_csrf_checks=True)
    client.force_login(user)

    assert client.get(reverse("reservations:sign_out")).status_code == 405
    assert "_auth_user_id" in client.session
    assert client.post(reverse("reservations:sign_out")).status_code == 403
    assert "_auth_user_id" in client.session

    flights = client.get(reverse("reservations:flight_list"))
    csrf_token = flights.cookies["csrftoken"].value
    response = client.post(
        reverse("reservations:sign_out"),
        {"csrfmiddlewaretoken": csrf_token},
    )
    assert response.status_code == 302
    assert response.url == reverse("reservations:flight_list")
    assert "_auth_user_id" not in client.session


def test_account_requires_login_and_renders_profile(client, user):
    anonymous = client.get(reverse("reservations:account"))
    assert anonymous.url == (
        f"{reverse('reservations:sign_in')}?next={reverse('reservations:account')}"
    )

    client.force_login(user)
    response = client.get(reverse("reservations:account"))
    content = response.content.decode()
    assert "Aiko Tanaka" in content
    assert user.email in content
    assert user.username in content
    assert "You have no active bookings." in content


def test_navigation_and_my_bookings_follow_authentication_state(client, user):
    anonymous = client.get(reverse("reservations:my_bookings"))
    anonymous_content = anonymous.content.decode()
    assert "Guest lookup is coming later" in anonymous_content
    assert "Sign In" in anonymous_content
    assert "Create Account" in anonymous_content
    assert "Log Out" not in anonymous_content
    assert 'aria-current="page"' in anonymous_content

    client.force_login(user)
    member_content = client.get(reverse("reservations:flight_list")).content.decode()
    assert "My Bookings" in member_content
    assert "Account" in member_content
    assert "Log Out" in member_content
    assert "Sign In" not in member_content
    assert "Create Account" not in member_content
    assert 'class="nav-form"' in member_content
    assert 'name="csrfmiddlewaretoken"' in member_content

    member_bookings = client.get(reverse("reservations:my_bookings"))
    assert member_bookings.status_code == 302
    assert member_bookings.url == reverse("reservations:account")


def test_account_history_only_displays_owned_bookings(client, user, flight_and_seats):
    flight, seats = flight_and_seats
    other = get_user_model().objects.create_user(username="other", password=PASSWORD)
    owned = Booking.objects.create(
        seat=seats[0],
        user=user,
        guest_name="Owned Passenger",
        guest_email="owned@example.com",
    )
    other_booking = Booking.objects.create(
        seat=seats[1],
        user=other,
        guest_name="Other Passenger",
        guest_email="other@example.com",
    )
    guest = Booking.objects.create(
        seat=seats[2],
        guest_name="Aiko Email Match",
        guest_email=user.email,
    )
    cancelled_seat = Seat.objects.create(
        flight=flight,
        seat_number="2A",
        price=Decimal("24000"),
    )
    cancelled = Booking.objects.create(
        seat=cancelled_seat,
        user=user,
        guest_name="Cancelled Passenger",
        guest_email="cancelled@example.com",
        status=Booking.Status.CANCELLED,
    )

    client.force_login(user)
    response = client.get(reverse("reservations:account"))
    content = response.content.decode()

    assert list(response.context["bookings"]) == [owned]
    assert owned.booking_reference in content
    assert flight.origin.code in content
    assert flight.destination.code in content
    assert "¥22,000" in content
    assert cancelled.booking_reference not in content
    assert other_booking.booking_reference not in content
    assert guest.booking_reference not in content


def test_booking_receipts_enforce_owner_and_preserve_guest_access(client, user, flight_and_seats):
    _, seats = flight_and_seats
    owned = Booking.objects.create(
        seat=seats[0],
        user=user,
        guest_name="Owned Passenger",
        guest_email="owned@example.com",
    )
    guest = Booking.objects.create(
        seat=seats[1],
        guest_name="Guest Passenger",
        guest_email="guest@example.com",
    )
    owned_url = reverse("reservations:booking_confirmation", args=[owned.booking_reference])
    guest_url = reverse("reservations:booking_confirmation", args=[guest.booking_reference])

    assert client.get(owned_url).status_code == 404
    assert client.get(guest_url).status_code == 200

    other = get_user_model().objects.create_user(username="other", password=PASSWORD)
    client.force_login(other)
    assert client.get(owned_url).status_code == 404
    assert client.get(guest_url).status_code == 200

    client.force_login(user)
    assert client.get(owned_url).status_code == 200


def test_authenticated_booking_prefills_and_preserves_edits(client, user, flight_and_seats):
    flight, seats = flight_and_seats
    client.force_login(user)

    initial = client.get(reverse("reservations:flight_booking", args=[flight.pk]))
    assert 'value="Aiko Tanaka"' in initial.content.decode()
    assert 'value="aiko@example.com"' in initial.content.decode()

    invalid = client.post(
        reverse("reservations:flight_booking", args=[flight.pk]),
        {
            "action": "review",
            "seat": "",
            "passenger_name": "Mina Sato",
            "passenger_email": "mina@example.com",
        },
    )
    invalid_content = invalid.content.decode()
    assert 'value="Mina Sato"' in invalid_content
    assert 'value="mina@example.com"' in invalid_content
    assert 'value="Aiko Tanaka"' not in invalid_content

    data = {
        "action": "review",
        "seat": seats[0].pk,
        "passenger_name": "Mina Sato",
        "passenger_email": "mina@example.com",
    }
    review = client.post(reverse("reservations:flight_booking", args=[flight.pk]), data)
    assert "Mina Sato" in review.content.decode()
    assert "mina@example.com" in review.content.decode()

    confirmed = client.post(
        reverse("reservations:flight_booking", args=[flight.pk]),
        {**data, "action": "confirm"},
    )
    booking = Booking.objects.get()
    assert confirmed.status_code == 302
    assert booking.user == user
    assert booking.guest_name == "Mina Sato"
    assert booking.guest_email == "mina@example.com"
    assert booking.total_price == Decimal("22000")


def test_logged_out_booking_preserves_pending_details_without_creating_booking(
    client,
    flight_and_seats,
):
    flight, seats = flight_and_seats
    initial_content = client.get(
        reverse("reservations:flight_booking", args=[flight.pk])
    ).content.decode()
    assert 'name="passenger_name"' in initial_content
    assert 'name="passenger_email"' in initial_content
    assert 'value="Aiko Tanaka"' not in initial_content

    response = client.post(
        reverse("reservations:flight_booking", args=[flight.pk]),
        {
            "action": "confirm",
            "seat": seats[0].pk,
            "passenger_name": "Guest Traveler",
            "passenger_email": "guest@example.com",
        },
    )
    assert response.status_code == 302
    assert response.url == (
        f"{reverse('reservations:sign_in')}?next={reverse('reservations:resume_booking')}"
    )
    assert Booking.objects.count() == 0
    assert client.session[PENDING_BOOKING_SESSION_KEY] == {
        "version": 1,
        "flight_id": flight.pk,
        "seat_id": seats[0].pk,
        "passenger_name": "Guest Traveler",
        "passenger_email": "guest@example.com",
    }


def test_service_assigns_optional_owner(user, flight_and_seats):
    flight, seats = flight_and_seats
    booking = create_booking(
        flight=flight,
        seat=seats[0],
        passenger_name="Different Passenger",
        passenger_email="passenger@example.com",
        user=user,
    )

    assert booking.user == user
    assert booking.guest_name == "Different Passenger"
    assert booking.guest_email == "passenger@example.com"


def test_seat_selection_actions_follow_authentication_state(
    client,
    user,
    flight_and_seats,
):
    flight, _ = flight_and_seats
    anonymous_content = client.get(
        reverse("reservations:flight_booking", args=[flight.pk])
    ).content.decode()
    assert "Sign in or create an account to continue your booking." in anonymous_content
    assert "Sign in to continue" in anonymous_content
    assert "New to SkyBook? Create an account" in anonymous_content
    assert "Review price" not in anonymous_content

    client.force_login(user)
    authenticated_content = client.get(
        reverse("reservations:flight_booking", args=[flight.pk])
    ).content.decode()
    assert "Review price" in authenticated_content
    assert "Sign in to continue" not in authenticated_content


def _store_pending_booking(client, flight, seat, *, action="sign_in"):
    return client.post(
        reverse("reservations:flight_booking", args=[flight.pk]),
        {
            "action": action,
            "seat": seat.pk,
            "passenger_name": "Mina Sato",
            "passenger_email": "unregistered-passenger@example.com",
            "base_fare": "1",
            "total_price": "1",
        },
    )


def test_sign_in_resumes_pending_booking_with_current_database_price(
    client,
    user,
    flight_and_seats,
):
    flight, seats = flight_and_seats
    response = _store_pending_booking(client, flight, seats[0])
    assert response.url.endswith(f"?next={reverse('reservations:resume_booking')}")
    assert Booking.objects.count() == 0

    seats[0].price = Decimal("33333")
    seats[0].save(update_fields=["price"])
    signed_in = client.post(
        reverse("reservations:sign_in"),
        {
            "username": user.username,
            "password": PASSWORD,
            "next": "https://attacker.example/steal",
        },
        follow=True,
    )
    content = signed_in.content.decode()

    assert signed_in.redirect_chain == [(reverse("reservations:resume_booking"), 302)]
    assert "Mina Sato" in content
    assert "unregistered-passenger@example.com" in content
    assert "¥33,333" in content
    assert "¥3,333" in content
    assert "¥36,666" in content
    assert Booking.objects.count() == 0


def test_registration_resumes_pending_booking(client, flight_and_seats):
    flight, seats = flight_and_seats
    response = _store_pending_booking(client, flight, seats[1], action="register")
    assert response.url == (
        f"{reverse('reservations:register')}?next={reverse('reservations:resume_booking')}"
    )

    registered = client.post(
        reverse("reservations:register"),
        registration_data(),
        follow=True,
    )
    assert registered.redirect_chain == [(reverse("reservations:resume_booking"), 302)]
    assert "Mina Sato" in registered.content.decode()
    assert "unregistered-passenger@example.com" in registered.content.decode()
    assert Booking.objects.count() == 0


def test_unregistered_passenger_email_can_be_booked_by_authenticated_user(
    client,
    user,
    flight_and_seats,
):
    flight, seats = flight_and_seats
    client.force_login(user)
    response = client.post(
        reverse("reservations:flight_booking", args=[flight.pk]),
        {
            "action": "confirm",
            "seat": seats[0].pk,
            "passenger_name": "Someone Else",
            "passenger_email": "nobody-has-this-account@example.com",
        },
    )

    booking = Booking.objects.get()
    assert response.status_code == 302
    assert booking.user == user
    assert booking.guest_name == "Someone Else"
    assert booking.guest_email == "nobody-has-this-account@example.com"


def test_passenger_email_never_discloses_account_existence(
    client,
    user,
    flight_and_seats,
):
    flight, seats = flight_and_seats
    other = get_user_model().objects.create_user(
        username="passenger-account",
        email="registered-passenger@example.com",
    )
    client.force_login(user)

    for seat, passenger_email in (
        (seats[0], other.email),
        (seats[1], "not-registered@example.com"),
    ):
        response = client.post(
            reverse("reservations:flight_booking", args=[flight.pk]),
            {
                "action": "review",
                "seat": seat.pk,
                "passenger_name": "Passenger",
                "passenger_email": passenger_email,
            },
        )
        content = response.content.decode()
        assert response.status_code == 200
        assert passenger_email in content
        assert "Email not registered" not in content


def test_direct_logged_out_review_and_confirmation_are_blocked(client, flight_and_seats):
    flight, seats = flight_and_seats
    for action in ("review", "confirm"):
        response = client.post(
            reverse("reservations:flight_booking", args=[flight.pk]),
            {
                "action": action,
                "seat": seats[0].pk,
                "passenger_name": "Pending Passenger",
                "passenger_email": "pending@example.com",
            },
        )
        assert response.status_code == 302
        assert response.url.startswith(reverse("reservations:sign_in"))
        assert Booking.objects.count() == 0


def test_successful_confirmation_clears_pending_session(
    client,
    user,
    flight_and_seats,
):
    flight, seats = flight_and_seats
    _store_pending_booking(client, flight, seats[0])
    client.force_login(user)
    assert client.get(reverse("reservations:resume_booking")).status_code == 200

    response = client.post(
        reverse("reservations:flight_booking", args=[flight.pk]),
        {
            "action": "confirm",
            "seat": seats[0].pk,
            "passenger_name": "Mina Sato",
            "passenger_email": "unregistered-passenger@example.com",
        },
    )

    assert response.status_code == 302
    assert Booking.objects.get().user == user
    assert PENDING_BOOKING_SESSION_KEY not in client.session


def test_missing_or_unavailable_pending_seat_is_cleared(
    client,
    user,
    flight_and_seats,
):
    flight, seats = flight_and_seats
    _store_pending_booking(client, flight, seats[0])
    seats[0].delete()
    signed_in = client.post(
        reverse("reservations:sign_in"),
        {"username": user.username, "password": PASSWORD},
    )
    assert signed_in.url == reverse("reservations:account")
    assert PENDING_BOOKING_SESSION_KEY not in client.session

    client.logout()
    _store_pending_booking(client, flight, seats[1])
    Booking.objects.create(
        seat=seats[1],
        guest_name="Historical Guest",
        guest_email="historical@example.com",
    )
    client.force_login(user)
    unavailable = client.get(reverse("reservations:resume_booking"))
    assert unavailable.status_code == 200
    assert "no longer available" in unavailable.content.decode()
    assert PENDING_BOOKING_SESSION_KEY not in client.session


def test_malformed_pending_session_is_cleared(client, user):
    session = client.session
    session[PENDING_BOOKING_SESSION_KEY] = {
        "version": 1,
        "flight_id": "not-an-integer",
        "seat_id": 3,
        "passenger_name": "Passenger",
        "passenger_email": "passenger@example.com",
        "total_price": "1",
    }
    session.save()
    client.force_login(user)

    response = client.get(reverse("reservations:resume_booking"))
    assert response.status_code == 302
    assert response.url == reverse("reservations:flight_list")
    assert PENDING_BOOKING_SESSION_KEY not in client.session


def test_authentication_templates_use_accessible_responsive_styles(client):
    for route_name in ("register", "sign_in"):
        content = client.get(reverse(f"reservations:{route_name}")).content.decode()
        assert 'class="skip-link" href="#main-content"' in content
        assert '<nav aria-label="Primary navigation">' in content
        assert '<main id="main-content"' in content
        assert "<footer" not in content
        assert 'class="auth-' in content
        assert "<label " in content
        assert 'name="csrfmiddlewaretoken"' in content

    stylesheet = Path("reservations/static/reservations/styles.css").read_text()
    for selector in (
        ".auth-card",
        ".account-booking-card",
        ".nav-action",
        ":focus-visible",
        "@media (max-width: 40rem)",
    ):
        assert selector in stylesheet
